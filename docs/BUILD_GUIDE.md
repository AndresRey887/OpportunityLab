# OpportunityLab Build Guide

## Phase 2

Version: 0.20.0  
Codename: Trailblazer

## Completed Packages

- Package-020A-01 through Package-020A-12 — Discovery pipeline foundation.
- Package-020A-13 — Reddit discovery source.
- Package-020A-14 — YouTube discovery source.
- Package-020A-15 — Company-website discovery source.
- Package-020A-16 — Source filter engine.
- Package-020A-17 — Source filter UI.
- Package-020A-18 — Selected-source execution.

## Package-020A-19

### Goal

Display discovery-source names on result cards.

### New files

- `scripts/test_phase2_result_source_labels.py`

### Complete replacements

- `src/ui/results_panel.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Test command

`python scripts\test_phase2_result_source_labels.py`

### Expected result

`Phase 2 result source-label test passed.`

Stop after this test and report `passed` or paste the error.
