# OpportunityLab AI Handover

## Current Status

Phase 1 is complete.

OpportunityLab is a Python desktop application using CustomTkinter.

Working features:

- Serper search
- SQLite database
- Opportunity model
- Rule engine
- Opportunity scoring
- Domain filters
- Keyword filters
- Filter Manager
- Search history
- Recent-search autocomplete
- Gemini Opportunity Intelligence
- Persistent AI cache
- AI Router
- Ollama provider foundation
- Related Intelligence
- AI Controller and stability foundations

## Current Phase

Phase 2 — Discovery Expansion

Version: 0.20.0  
Codename: Trailblazer

## Current Package

Package-020A-02

### Status

Ready for user test.

### Purpose

Add discovery-source registration and source enable/disable control behind the existing search workflow.

### New files

- src/discovery/source_registry.py
- scripts/test_phase2_source_registry.py
- scripts/test_phase2_discovery_sources.py

### Replaced files

- src/discovery/__init__.py
- src/core/search_service.py
- src/version.py
- docs/AI_HANDOVER.md
- docs/BUILD_GUIDE.md

### Behaviour

- Existing Serper search remains the default live source.
- SearchService now searches only enabled registered sources.
- Sources can be registered, enabled, disabled, or removed without changing the search pipeline.
- Existing injected-source tests remain supported.
- No UI changes.
- No additional live discovery source added.

### Test

```bat
python scripts\test_phase2_source_registry.py
```

Expected result:

```text
Phase 2 source registry test passed.
```

## Next Package

Do not begin until Package-020A-02 passes.

Package-020A-03 will build on the tested discovery registry without adding unrelated features.
