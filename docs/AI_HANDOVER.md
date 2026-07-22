# OpportunityLab AI Handover

## Current Phase

Phase 2 — Discovery Expansion  
Version: 0.20.0  
Codename: Trailblazer

## Current Package

Package-020A-35

### Purpose

Add the foundation for grouping opportunities by source or website.

### New files

- `src/grouping/__init__.py`
- `src/grouping/opportunity_group.py`
- `src/grouping/opportunity_grouper.py`
- `scripts/test_phase2_opportunity_grouping.py`

### Replaced files

- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Behaviour

- Opportunities can be grouped by discovery source.
- Opportunities can be grouped by normalized website domain.
- Groups expose their label, contents, and result count.
- Groups are ordered by count and then label.
- No UI changes in this package.

### Test

`python scripts\test_phase2_opportunity_grouping.py`

Expected: `Phase 2 opportunity grouping test passed.`
