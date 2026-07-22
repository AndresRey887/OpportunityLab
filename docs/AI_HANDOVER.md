# OpportunityLab AI Handover

## Current Phase

Phase 2 — Discovery Expansion  
Version: 0.20.0  
Codename: Trailblazer

## Current Package

Package-020A-39

### Purpose

Add sorting controls to the grouped main results list.

### Replaced files

- `src/ui/main_window.py`
- `src/ui/results_panel.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### New files

- `scripts/test_phase2_result_sorting.py`

### Behaviour

- Results can sort by highest score, lowest score, or title.
- Sorting redraws current results without running another search.
- Source and website grouping remain available.
- MainWindow now sends the complete result list to ResultsPanel at once.

### Test

`python scripts\test_phase2_result_sorting.py`

Expected: `Phase 2 result sorting test passed.`
