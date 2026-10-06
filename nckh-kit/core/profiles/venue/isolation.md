# Venue and ranking isolation

Key rules by venue_id, journal/conference/other, year, track and article type.
Store guideline origin/version/hash, as-of, rights and source evidence. Load one active
venue profile per task; do not union conflicting requirements. A venue change
invalidates affected format/reporting/rights checks while retaining source history.

Ranking is a distinct record: issuer/system, category, metric/data year, quartile,
as-of and evidence. DOI, @article, peer review or public access alone cannot establish
Q1/Q2. Leave missing rank unknown. Do not choose a global default venue for the kit.
