"""Diagnostic fixtures using actual source bytes; these are not native SVG evidence."""

import contextlib
import hashlib
import importlib.util
import io
import json
import shutil
import sys
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('worldbank_svg_checker', HERE / 'check-worldbank-svg.py')
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)
SOURCE_PATH = HERE / 'source-acquisition/derived/worldbank-series.jsonl'
SOURCE_BYTES = SOURCE_PATH.read_bytes()
SOURCE = json.loads(SOURCE_BYTES)
OBSERVATIONS = sorted(SOURCE['data'], key=lambda row: int(row['date']))


def chart(*, group='', circles='', polyline='', points_prefix='', equal_values=False):
    first, last = OBSERVATIONS[0]['value'], OBSERVATIONS[-1]['value']
    marks, points = [], []
    for row in OBSERVATIONS:
        year, value = int(row['date']), row['value']
        x = 100 + (year - 2000) * 20
        y = 600 - (value - first) * 400 / (last - first)
        point = f'{x:.6f},{y:.6f}'
        points.append(point)
        marks.append(f'<circle id="year-{year}" data-year="{year}" '
                     f'data-value="{first if equal_values else value}" '
                     f'cx="{x:.6f}" cy="{y:.6f}" r="3" {circles}/>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="900">'
            '<title>Diagnostic source chart</title><desc>Year order</desc>'
            '<text>Population, total SP.POP.TOTL raw unit field blank</text>'
            f'<g {group}>' + ''.join(marks) +
            f'<polyline points="{points_prefix}{" ".join(points)}" {polyline}/></g></svg>')


class WorldBankSvgChecks(unittest.TestCase):
    def run_check(self, fixture):
        directory = HERE / ('svg-check-diagnostic-' + uuid.uuid4().hex)
        directory.mkdir()
        try:
            svg, receipt = directory / 'diagnostic.svg', directory / 'receipt.json'
            svg.write_text(fixture, encoding='utf-8')
            with patch.object(sys, 'argv', ['checker', '--svg', str(svg), '--output', str(receipt)]):
                with contextlib.redirect_stdout(io.StringIO()):
                    code = CHECKER.main()
            result = json.loads(receipt.read_text(encoding='utf-8'))
        finally:
            shutil.rmtree(directory)
        self.assertEqual(result['source_sha256'], hashlib.sha256(SOURCE_BYTES).hexdigest())
        return code, result

    def test_direct_chart_uses_all_actual_observations(self):
        code, receipt = self.run_check(chart())
        self.assertEqual((code, receipt['status']), (0, 'pass-for-stated-checks'))
        self.assertEqual([(row['year'], row['value']) for row in receipt['marks']],
                         [(int(row['date']), row['value']) for row in OBSERVATIONS])

    def test_common_translated_group_preserves_connections(self):
        code, receipt = self.run_check(chart(group='transform="translate(40,30)"'))
        self.assertEqual(code, 0)
        self.assertEqual((receipt['marks'][0]['x'], receipt['marks'][0]['y']), (140, 630))

    def test_common_rotation_skew_and_nested_scale_are_supported(self):
        for affine in ['rotate(20,100,600)', 'skewX(15)', 'skewY(10)',
                       'translate(40,30) scale(2,3)', 'matrix(2,0,0,3,40,30)']:
            with self.subTest(transform=affine):
                code, receipt = self.run_check(chart(group=f'transform="{affine}"'))
                self.assertEqual((code, receipt['unsupported']), (0, []))
        fixture = chart(group='transform="translate(40,30)"')
        fixture = fixture.replace('<g ', '<g transform="scale(2,3)"><g ', 1).replace('</g></svg>', '</g></g></svg>')
        code, receipt = self.run_check(fixture)
        self.assertEqual(code, 0)
        self.assertEqual((receipt['marks'][0]['x'], receipt['marks'][0]['y']), (280, 1890))

    def test_matching_element_transforms_share_a_coordinate_frame(self):
        affine = 'transform="translate(40,30) rotate(20)"'
        code, receipt = self.run_check(chart(circles=affine, polyline=affine))
        self.assertEqual((code, receipt['unsupported']), (0, []))

    def test_unequal_circle_polyline_transforms_fail_connection(self):
        code, receipt = self.run_check(chart(circles='transform="translate(40,0)"'))
        self.assertEqual(code, 1)
        self.assertIn('no polyline connects the 26 recorded marks in year order', receipt['errors'])

    def test_malformed_polyline_points_are_rejected(self):
        for prefix in ['garbage ', '1e,', ',']:
            with self.subTest(prefix=prefix):
                code, receipt = self.run_check(chart(points_prefix=prefix))
                self.assertEqual(code, 1)
                self.assertTrue(any('invalid points syntax' in error for error in receipt['errors']))

    def test_equal_invalid_data_values_write_a_fail_receipt(self):
        code, receipt = self.run_check(chart(equal_values=True))
        self.assertEqual((code, receipt['status']), (1, 'fail'))
        self.assertTrue(any('source-mismatched mark' in error for error in receipt['errors']))

    def test_affine_composition_has_known_coordinate_results(self):
        cases = [('translate(10,20) scale(2,3)', (1, 1), (12, 23)),
                 ('rotate(90,10,20)', (11, 20), (10, 21)),
                 ('skewX(45)', (1, 2), (3, 2)),
                 ('skewY(45)', (1, 2), (1, 3)),
                 ('matrix(2,3,4,5,6,7)', (1, 2), (16, 20))]
        for affine, original, expected in cases:
            with self.subTest(transform=affine):
                actual = CHECKER.point(CHECKER.transform(affine), *original)
                self.assertAlmostEqual(actual[0], expected[0])
                self.assertAlmostEqual(actual[1], expected[1])

    def test_points_consume_the_complete_valid_svg_number_grammar(self):
        self.assertEqual(CHECKER.numbers('1.-2. 3e1,4e-1', points=True), [1, -2, 30, 0.4])
        for invalid in ['1,2junk 3,4', '1,2,', '1,2,,3,4', '1,2-3,4', '1e,2', '1e999,2']:
            with self.subTest(points=invalid), self.assertRaises(ValueError):
                CHECKER.numbers(invalid, points=True)

    def test_unsupported_coordinate_construct_is_unverified(self):
        code, receipt = self.run_check(chart(group='style="transform: translateX(40px)"'))
        self.assertEqual((code, receipt['status']), (2, 'unverified-for-stated-checks'))
        self.assertTrue(receipt['unsupported'])

    def test_transform_origin_presentation_attribute_is_unverified(self):
        code, receipt = self.run_check(chart(
            circles='transform="rotate(90)" transform-origin="100px 600px"',
            polyline='transform="rotate(90)"'))
        self.assertEqual((code, receipt['status']), (2, 'unverified-for-stated-checks'))
        self.assertTrue(any('presentation attributes' in issue for issue in receipt['unsupported']))

    def test_coordinate_animations_are_unverified(self):
        animations = ['<animateTransform attributeName="transform" type="translate" from="0" to="40"/>',
                      '<animateMotion path="M 0 0 L 40 0"/>',
                      '<animate attributeName="transform" from="translate(0)" to="translate(40)"/>',
                      '<set attributeName="transform" to="translate(40)"/>']
        for animation in animations:
            with self.subTest(animation=animation):
                fixture = chart().replace('<g >', '<g >' + animation, 1)
                code, receipt = self.run_check(fixture)
                self.assertEqual((code, receipt['status']), (2, 'unverified-for-stated-checks'))
                self.assertTrue(any('animated' in issue for issue in receipt['unsupported']))
        for href in ['href', 'xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href']:
            with self.subTest(href=href):
                fixture = chart().replace('</svg>',
                    f'<animateTransform {href}="#year-2000" attributeName="transform" '
                    'type="translate" from="0" to="40"/></svg>')
                code, receipt = self.run_check(fixture)
                self.assertEqual((code, receipt['status']), (2, 'unverified-for-stated-checks'))
                self.assertTrue(any('animated' in issue for issue in receipt['unsupported']))


if __name__ == '__main__':
    unittest.main()
