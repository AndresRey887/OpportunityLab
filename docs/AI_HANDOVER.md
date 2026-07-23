# OpportunityLab AI Handover

## Current build

- Version: 0.22.0
- Package: Package-022A-05
- Build: 5
- Codename: Pathfinder
- Phase 4: In progress

## Package-022A-05

This package adds explainable, history-informed recommendations.

- Selected results now provide **Why This Opportunity?**
- Every recommendation shows Strong Match, Worth Reviewing, Possible Fit, or
  Low Priority.
- A match score combines current quality with learned source, keyword, and
  opportunity-type performance.
- Confidence is calculated separately from the amount of tracked and completed
  evidence available.
- Plain-language reasons show exactly what improved the recommendation.
- Cautions identify limited history, few completed outcomes, weak source
  results, low current quality, or completely new search patterns.
- Recommendations remain useful before much history exists and become more
  confident as outcomes accumulate.
- No irreversible action is taken automatically.

## New files

- `src/recommendations/__init__.py`
- `src/recommendations/opportunity_recommendation.py`
- `src/recommendations/recommendation_service.py`
- `src/ui/recommendation_window.py`
- `scripts/test_phase4_recommendations.py`

## Replaced files

- `src/ui/main_window.py`
- `src/version.py`
- `docs/AI_HANDOVER.md`
- `docs/BUILD_GUIDE.md`

## Next package

Add recommendation feedback so useful and unhelpful suggestions directly
improve future ranking confidence.
