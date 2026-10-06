"""Compare actual SVG marks with the pinned World Bank snapshot; no render verdict."""

import argparse
import hashlib
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


NUMBER = r'[-+]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][-+]?[0-9]+)?'
SPACE = r'[ \t\r\n]'
SEPARATOR = rf'(?:{SPACE}+,?{SPACE}*|,{SPACE}*)'
PAIR = rf'{NUMBER}(?:{SEPARATOR}{NUMBER}|(?=-){NUMBER})'
POINTS = re.compile(rf'{SPACE}*(?:{PAIR}(?:{SEPARATOR}{PAIR})*)?{SPACE}*')
NUMBERS = re.compile(rf'{SPACE}*{NUMBER}(?:{SEPARATOR}{NUMBER})*{SPACE}*')
IDENTITY = (1, 0, 0, 1, 0, 0)


def numbers(text, *, points=False):
    if not (POINTS if points else NUMBERS).fullmatch(text):
        raise ValueError('invalid points syntax' if points else 'invalid transform numbers')
    values = [float(match.group()) for match in re.finditer(NUMBER, text)]
    if not all(math.isfinite(value) for value in values):
        raise ValueError('nonfinite coordinates or transform')
    return values


def multiply(left, right):
    a, b, c, d, e, f = left
    g, h, i, j, k, l = right
    return (a*g+c*h, b*g+d*h, a*i+c*j, b*i+d*j, a*k+c*l+e, b*k+d*l+f)


def point(matrix, x, y):
    a, b, c, d, e, f = matrix
    result = (a*x+c*y+e, b*x+d*y+f)
    if not all(math.isfinite(value) for value in result):
        raise ValueError('nonfinite transformed coordinates')
    return result


def inverse(matrix):
    a, b, c, d, e, f = matrix
    determinant = a*d-b*c
    if not math.isfinite(determinant) or determinant == 0:
        raise ValueError('singular chart coordinate frame')
    return (d/determinant, -b/determinant, -c/determinant, a/determinant,
            (c*f-d*e)/determinant, (b*e-a*f)/determinant)


def transform(text):
    result, position = IDENTITY, 0
    while position < len(text):
        match = re.match(r'[ \t\r\n]*([A-Za-z]+)[ \t\r\n]*\(([^()]*)\)', text[position:])
        if not match:
            raise ValueError('unsupported or invalid affine transform')
        name, arguments = match.group(1), numbers(match.group(2))
        if name == 'matrix' and len(arguments) == 6:
            current = tuple(arguments)
        elif name == 'translate' and len(arguments) in {1, 2}:
            current = (1, 0, 0, 1, arguments[0], arguments[1] if len(arguments) == 2 else 0)
        elif name == 'scale' and len(arguments) in {1, 2}:
            current = (arguments[0], 0, 0, arguments[1] if len(arguments) == 2 else arguments[0], 0, 0)
        elif name == 'rotate' and len(arguments) in {1, 3}:
            angle = math.radians(arguments[0])
            current = (math.cos(angle), math.sin(angle), -math.sin(angle), math.cos(angle), 0, 0)
            if len(arguments) == 3:
                x, y = arguments[1:]
                current = multiply(multiply((1, 0, 0, 1, x, y), current), (1, 0, 0, 1, -x, -y))
        elif name in {'skewX', 'skewY'} and len(arguments) == 1:
            tangent = math.tan(math.radians(arguments[0]))
            current = (1, 0, tangent, 1, 0, 0) if name == 'skewX' else (1, tangent, 0, 1, 0, 0)
        else:
            raise ValueError('unsupported or invalid affine transform: ' + name)
        result = multiply(result, current)
        if not all(math.isfinite(value) for value in result):
            raise ValueError('nonfinite affine transform')
        position += match.end()
        separator = re.match(SEPARATOR, text[position:])
        if separator:
            position += separator.end()
            if position == len(text) and ',' in separator.group():
                raise ValueError('invalid trailing transform separator')
        elif position < len(text):
            raise ValueError('invalid transform separator')
    return result


def coordinate_frames(root):
    frames, issues = {}, {}
    css_transform = re.compile(r'(?:^|[;{])\s*(?:transform(?:-origin|-box)?|translate|rotate|scale)\s*:', re.I)
    styles = any(element.tag.rsplit('}', 1)[-1] == 'style'
                 and css_transform.search(''.join(element.itertext())) for element in root.iter())
    parents = {child: parent for parent in root.iter() for child in parent}
    animated, unresolved_animation = set(), False
    for element in root.iter():
        local = element.tag.rsplit('}', 1)[-1]
        if local not in {'animateTransform', 'animateMotion'} and not (
                local in {'animate', 'set'} and element.get('attributeName') == 'transform'):
            continue
        href = element.get('href', element.get('{http://www.w3.org/1999/xlink}href'))
        targets = ([target for target in root.iter() if target.get('id') == href[1:]]
                   if href and href.startswith('#') else [parents.get(element)] if not href else [])
        if not targets or targets == [None]:
            unresolved_animation = True
        else:
            animated.update(targets)

    def visit(element, parent, issue=None):
        local = element.tag.rsplit('}', 1)[-1]
        if styles or css_transform.search(element.get('style', '')):
            issue = 'CSS coordinate transforms are unsupported/unverified'
        if 'transform-origin' in element.attrib or 'transform-box' in element.attrib:
            issue = 'transform origin/box presentation attributes are unsupported/unverified'
        if element is not root and local == 'svg':
            issue = 'nested SVG viewports are unsupported/unverified'
        if element in animated or unresolved_animation:
            issue = 'animated coordinate transforms are unsupported/unverified'
        try:
            matrix = multiply(parent, transform(element.get('transform', '').strip()))
        except ValueError as error:
            matrix, issue = parent, str(error)
        frames[element], issues[element] = matrix, issue
        for child in element:
            visit(child, matrix, issue)

    visit(root, IDENTITY)
    return frames, issues


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--svg', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    project = Path(__file__).resolve().parents[3]
    svg, output = args.svg.resolve(), args.output.resolve()
    if not svg.is_relative_to(project) or not output.is_relative_to(project) or output.exists():
        parser.error('use a project SVG and a fresh project receipt')
    data_path = project / 'plans/evaluation/personal-use/source-acquisition/derived/worldbank-series.jsonl'
    source = json.loads(data_path.read_text(encoding='utf-8'))
    observations = sorted(source['data'], key=lambda row: int(row['date']))
    root = ET.fromstring(svg.read_bytes())
    local = lambda element: element.tag.rsplit('}', 1)[-1]
    errors = []
    unsupported = []
    frames, frame_issues = coordinate_frames(root)
    marks = [element for element in root.iter() if local(element) == 'circle'
             and 'data-year' in element.attrib]
    expected = {int(row['date']): row['value'] for row in observations}
    rows = []
    chart_frame = None
    seen = set()
    for element in marks:
        if frame_issues[element]:
            unsupported.append(frame_issues[element])
            continue
        try:
            year, value = int(element.attrib['data-year']), int(element.attrib['data-value'])
            x, y = float(element.attrib['cx']), float(element.attrib['cy'])
            if not math.isfinite(x) or not math.isfinite(y):
                raise ValueError('nonfinite coordinates')
            x, y = point(frames[element], x, y)
        except (ValueError, KeyError) as error:
            errors.append('invalid mark attributes: ' + str(error))
            continue
        if year in seen or expected.get(year) != value:
            errors.append('duplicate or source-mismatched mark: ' + str(year))
        seen.add(year)
        if chart_frame is None:
            chart_frame = frames[element]
        rows.append({'year': year, 'value': value, 'x': x, 'y': y, 'id': element.get('id')})
    rows.sort(key=lambda row: row['year'])
    if len(marks) != 26 or seen != set(expected) and not unsupported:
        errors.append('exactly 26 source year/value marks are required')
    if len(rows) == 26 and seen == set(expected) and all(expected[row['year']] == row['value'] for row in rows):
        try:
            chart_inverse = inverse(chart_frame)
            chart_rows = [{**row, 'x': point(chart_inverse, row['x'], row['y'])[0],
                           'y': point(chart_inverse, row['x'], row['y'])[1]} for row in rows]
        except ValueError as error:
            unsupported.append(str(error))
            chart_rows = []
        if chart_rows:
            first, last = chart_rows[0], chart_rows[-1]
            if last['x'] <= first['x'] or last['y'] >= first['y']:
                errors.append('chart coordinates reverse the year/value axis direction')
            for row in chart_rows:
                x = first['x'] + (last['x'] - first['x']) * (row['year'] - 2000) / 25
                y = first['y'] + (last['y'] - first['y']) * (expected[row['year']] - expected[2000]) / (expected[2025] - expected[2000])
                if abs(row['x'] - x) > 0.51 or abs(row['y'] - y) > 0.51:
                    errors.append('mark is inconsistent with a linear data scale: ' + str(row['year']))
        paths = [element for element in root.iter() if local(element) == 'polyline']
        matching = False
        for element in paths:
            if frame_issues[element]:
                unsupported.append(frame_issues[element])
                continue
            try:
                values = numbers(element.get('points', ''), points=True)
                points = [point(frames[element], values[index], values[index + 1])
                          for index in range(0, len(values), 2)]
            except ValueError as error:
                errors.append('invalid polyline points: ' + str(error))
                continue
            if len(points) == 26 and all(abs(points[i][0] - row['x']) <= 0.01
                    and abs(points[i][1] - row['y']) <= 0.01 for i, row in enumerate(rows)):
                matching = True
        if not matching and not unsupported:
            errors.append('no polyline connects the 26 recorded marks in year order')
    texts = [''.join(element.itertext()).strip() for element in root.iter() if local(element) == 'text']
    titles = [''.join(element.itertext()).strip() for element in root.iter() if local(element) == 'title']
    descriptions = [''.join(element.itertext()).strip() for element in root.iter() if local(element) == 'desc']
    if not texts:
        errors.append('native text elements are absent')
    if not any(titles) or not any(descriptions):
        errors.append('title/description accessibility text is missing')
    if any(local(element) == 'image' for element in root.iter()):
        errors.append('raster image present in the required vector chart')
    visible = '\n'.join(texts)
    for anchor in ('Population, total', 'SP.POP.TOTL', 'raw unit field blank'):
        if anchor not in visible:
            errors.append('required visible axis wording missing: ' + anchor)
    receipt = {'schema_version': 1, 'check': 'pinned-source-to-svg-mark-comparison',
               'status': 'fail' if errors else 'unverified-for-stated-checks' if unsupported else 'pass-for-stated-checks',
               'source_id': source['source_id'], 'source_path': data_path.relative_to(project).as_posix(),
               'source_sha256': sha(data_path), 'artifact_path': svg.relative_to(project).as_posix(),
               'artifact_sha256': sha(svg), 'marks': rows, 'native_text_count': len(texts),
               'title': titles, 'description': descriptions, 'errors': errors,
               'unsupported': sorted(set(unsupported)),
               'coordinate_frame': 'root SVG user coordinates; scale checked in the first mark affine frame',
               'limits': ['Static source/coordinate/accessibility-presence check only.',
                          'Actual open/render/editability, layout, contrast, rights/semantic review and owner judgment are separate.']}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': receipt['status'], 'marks': len(rows), 'errors': errors,
                      'unsupported': receipt['unsupported']}, ensure_ascii=False))
    return 1 if errors else 2 if unsupported else 0


if __name__ == '__main__':
    sys.exit(main())
