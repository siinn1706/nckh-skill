# Writer action and output locale

Both writers and the compatibility router normalize the same request.
Polish/translate route to `nckh-humanwrite`; outline/section/argument/reporting/
revision-response route to `nckh-paperwrite`. The word "paper" alone never selects
authoring. Retain `nckh-write` for legacy prose requests and bilingual output.

`--en` chooses English and `--vi` Vietnamese. Both flags conflict before creating
or editing an artifact. With no flag use the explicit target language, then the
brief, then the draft's dominant language; mixed/unknown inputs require one
clarification and no mutation. A bilingual request without a flag remains
bilingual; an explicit flag overrides its output target. Carry normalized locale
and the original flags through the compatibility handoff.

Load VI and EN style separately and share preservation/evidence. Output locale
never changes a resource record's locale, license or domain. These arguments are
interpreted by the skill; generated frontmatter is not native invocation evidence.
