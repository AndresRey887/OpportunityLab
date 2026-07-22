# OpportunityLab Build Guide

## Phase 2

Version: 0.20.0  
Codename: Trailblazer  
Focus: Expand discovery sources without destabilising Phase 1.

## Completed Packages

- Package-020A-01 through Package-020A-12 — Discovery pipeline foundation.
- Package-020A-13 — Reddit discovery source.
- Package-020A-14 — YouTube discovery source.

## Package-020A-15

### Goal

Add company-website discovery using the existing Serper connection.

### New files

- `src/discovery/company_website_search_source.py`
- `scripts/test_phase2_company_website_source.py`

### Complete replacements

- `src/core/search_service.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Test command

```text
python scripts\test_phase2_company_website_source.py
```

### Expected result

```text
Phase 2 company-website source test passed.
```

Stop after this test and report `passed` or paste the error.
