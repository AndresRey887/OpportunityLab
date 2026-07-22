# OpportunityLab AI Handover

## Current Phase

Phase 2 — Discovery Expansion  
Version: 0.20.0  
Codename: Trailblazer

## Current Package

Package-020A-38

### Purpose

Allow result grouping to switch between source and website.

### Replaced files

- `src/ui/results_panel.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### New files

- `scripts/test_phase2_grouping_selector.py`

### Behaviour

- A selector appears beside the Search Results heading.
- `Source` groups results by discovery source.
- `Website` groups results by normalized domain.
- Switching modes redraws existing results without another search.
- Groups remain collapsible in either mode.

### Test

`python scripts\test_phase2_grouping_selector.py`

Expected: `Phase 2 grouping selector test passed.`
