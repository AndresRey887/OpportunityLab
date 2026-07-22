# OpportunityLab AI Handover

## Current Phase

Phase 2 — Discovery Expansion  
Version: 0.20.0  
Codename: Trailblazer

## Current Package

Package-020A-20

### Purpose

Persist filter and source selections between application sessions.

### New files

- `src/filters/filter_settings_store.py`
- `scripts/test_phase2_filter_persistence.py`

### Replaced files

- `src/filters/filter_engine.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

### Behaviour

- Blocked domains, blocked keywords, and allowed sources save automatically.
- Settings load from `data/filter_settings.json` at startup.
- Missing or invalid settings files safely use defaults.
- Startup version display properties are retained.

### Test

`python scripts\test_phase2_filter_persistence.py`

Expected: `Phase 2 filter persistence test passed.`
