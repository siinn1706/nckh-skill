# Scientific Writing Fidelity Brief: Gender Disparities in Methodological Research

## 1. Source receipt and license

- **Source Identifier (`source_id`)**: `pmc-PMC13623154`
- **PubMed Central Identifier (PMCID)**: `PMC13623154`
- **Digital Object Identifier (DOI)**: `10.1371/journal.pone.0359403`
- **Upstream Article Locator**: `https://www.ncbi.nlm.nih.gov/pmc/articles/PMC13623154/`
- **Full-Text XML Locator**: `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13623154/fullTextXML`
- **Raw XML File (`raw_file`)**: `raw/pmc-PMC13623154.xml`
- **Raw XML SHA-256 Checksum (`raw_sha256`)**: `135e35ecbac31f8a2429ce25426d2564c3a87aa66f4f2ebaf3fd1bd15114c69c`
- **Raw XML Size**: `128,666 bytes`
- **Derived Excerpt Hash (`record_sha256`)**: `546888bb164ac36cd719f432ccacb7ed3dba076704b8191c47c88f5efe2f0223`
- **Reader Receipt Path**: `plans/evaluation/personal-use/native/agy-gemini-r24-repair-02/reader-receipts/nckh-write__R-pmc-scientific__pmc-PMC13623154.json`
- **Article-Level License**: `CC BY 4.0` (Creative Commons Attribution 4.0 International License, as verified in `raw/pmc-PMC13623154.xml`).
- **Derived Projection Scope**: Bounded title, abstract, and introductory body paragraphs capped at `9,000 characters` (field-preserving projection, separate from the full unedited JATS/XML article).

---

## 2. Five-row claim ledger

| # | Source Anchor | Faithful Paraphrase | Numbers & Units | Certainty / Association Wording | Forbidden Overclaim |
|---|---|---|---|---|---|
| **1** | *"Of the 1,375 included studies, the genders of 1,332 first authors and 1,334 last authors were determined."* | From the total evaluated dataset of 1,375 methodological studies, binary gender categorization was established for 1,332 primary authors and 1,334 senior authors. | `1,375` studies; `1,332` first authors; `1,334` last authors (counts) | Descriptive sample counts based on $\ge 60\%$ probability threshold | Claiming that all authors' genders were verified with 100% biological certainty across all studies. |
| **2** | *"Among first authors, 675 (50.7%) were women, and 657 (49.3%) were men, indicating no gender difference."* | First authorship positions showed roughly equal distribution between women and men, demonstrating no statistically significant gender difference at the primary author position in this sample. | `675` women (`50.7%`); `657` men (`49.3%`) | *"indicating no gender difference"* (descriptive parity in sample) | Inferring that first authorship directly measures early-career stage or that women face zero systemic career obstacles. |
| **3** | *"Among last authors, 486 (36.4%) were women, and 848 (63.6%) were men, with a statistically significant difference (χ² = 98.23, p < 0.001)."* | In senior leadership positions operationalized by last authorship, women represented approximately one-third while men accounted for nearly two-thirds, a difference that reached statistical significance. | `486` women (`36.4%`); `848` men (`63.6%`); `$\chi^2 = 98.23$`; `$p < 0.001$` | *"statistically significant difference"* via chi-square test | Asserting that men produce superior methodological research or that malicious discrimination directly caused this disparity. |
| **4** | *"Studies with women last authors had fewer listed co-authors than those with men (t = −3.63, p < 0.001; risk difference = −27.14%, 95% CI −32.50% to −21.77%). In adjusted models, women’s last authorship was negatively associated with number of authors (adjusted odds ratio [aOR]=0.93, 95% CI 0.90–0.97)."* | Methodological publications with female senior authors were associated with smaller collaboration teams, showing a negative association with the total count of co-authors in multivariable models. *(Note: $t = -3.63$ and $\text{RD} = -27.14\%$ are anchored in the Abstract; the Results section in the full XML reports $t = -3.77$ with mean difference $-1$, representing an unresolved internal source discrepancy).* | `$t = -3.63$`, `$p < 0.001$`; risk difference = `$-27.14\%$` (`95% CI -32.50% to -21.77%`); `$\text{aOR} = 0.93$` (`95% CI 0.90–0.97`) | *"negatively associated"*, *"may reflect differences in collaborative structure"* | Claiming that smaller team sizes actively prevent women from achieving senior authorship or cause lower research output. |
| **5** | *"Publication year was associated with both women first (aOR=1.03, 95% CI 1.01–1.05) and last (aOR=1.05, 95% CI 1.02–1.07) authorship."* | More recent calendar years of publication exhibited a modest positive association with female representation in both lead and senior author positions. | Lead author `$\text{aOR} = 1.03$` (`95% CI 1.01–1.05`); Senior author `$\text{aOR} = 1.05$` (`95% CI 1.02–1.07`) | *"associated with"* (temporal statistical trend) | Declaring that gender disparities are rapidly self-resolving or that time automatically causes gender equity. |

---

## 3. Faithful conclusion

This cross-sectional bibliometric study examined gender representation in first and last authorship across 1,375 health science methodological studies, determining genders for 1,332 first and 1,334 last authors. Among first authors, 675 (50.7%) were women and 657 (49.3%) were men, indicating a roughly balanced gender distribution among first authors in this sample. Conversely, among last authors, 486 (36.4%) were women and 848 (63.6%) were men, showing a statistically significant disparity (χ² = 98.23, p < 0.001). The abstract reported that studies with women last authors had fewer co-authors than those with men (t = −3.63, p < 0.001; risk difference = −27.14%, 95% CI −32.50% to −21.77%). Multivariable models showed women's last authorship was negatively associated with team size (aOR = 0.93, 95% CI 0.90–0.97). Publication year was positively associated with women first (aOR = 1.03, 95% CI 1.01–1.05) and last authorship (aOR = 1.05, 95% CI 1.02–1.07). These observational associations highlight gender differences without measuring career stage or proving causal mechanisms.

*(Conclusion word count: 161 whitespace-separated tokens [verified reproducibly via Python str.split()]; strictly verified within the required 120–180 word count limit).*

---

## 4. Limits and uncertainty

1. **Derived Excerpt Limitation (9,000 Character Boundary)**:
   - The primary text analyzed herein was sourced from a normalized projection restricted to 9,000 characters. While the complete JATS/XML article (`raw/pmc-PMC13623154.xml`, 128,666 bytes) is preserved in the project archive, this brief is bounded by the extracted title, abstract, and introductory sections.
2. **Bibliometric Proxies vs. Career Stages**:
   - First and last author positions serve as pragmatic bibliometric proxies for project leadership. Authorship position is an imperfect metric that does not directly measure early-career or senior-career stages, age, or institutional supervisory roles.
3. **Gender Determination Constraints**:
   - Gender categorization was inferred algorithmically using Genderize.io (threshold $\ge 60\%$), which operates on binary assumptions (women/men) and cannot capture gender identity, non-binary individuals, or unlisted names.
4. **Generalizability Limits**:
   - The sample is derived from a focused subset of health science methodological publications indexed up to June 15, 2020. Findings cannot be generalized to all scientific disciplines, non-health STEM fields, or broader academic publishing ecosystems.
5. **Unresolved Internal Source Discrepancy**:
   - There is an observable internal discrepancy within the published article: the Abstract reports $t = -3.63$ and risk difference $-27.14\%$ for the co-author comparison by last author gender, whereas the full-text Results section reports $t = -3.77$ with a mean difference of $-1$ ($95\%$ CI: $-1, -0.1$). This brief preserves the exact Abstract values in the ledger while formally noting this discrepancy without attempting ungrounded harmonization.
6. **Non-Causal Evidence**:
   - In adherence to `evidence-policy.md` and `nckh-write`, statistical associations and adjusted odds ratios must not be interpreted as demonstrated causal relationships or definitive mechanistic explanations.
