# OpportunityLab AI Handover

## Current build

- Version: 1.2.1
- Package: Package-110A-07A
- Build: 10
- Codename: Gold Rush
- Status: Production
- Phase: 6 — complete

## Package 100A-01

Phase 6 begins with a safe System Health diagnostic centre. It checks the
Python runtime, required project folders, writable data storage, required
dependencies, JSON validity, and SQLite integrity. Open it from Data Tools.

Diagnostics are read-only except for a temporary write test in the data
directory. They do not expose credentials or alter saved application data.
Package 100A-01A closes SQLite diagnostic connections explicitly so temporary
databases and application files are released correctly on Windows.
Package 100A-01B also closes the test database setup connection explicitly.

Package 100A-02 adds release-file and regression-suite readiness checks. The
System Health window can export a safe JSON diagnostic report containing check
results and basic runtime information, without saved data or credentials.

Package 100A-03 installs a Tkinter callback error boundary. Unexpected UI
callback failures are logged normally, saved as timestamped local crash reports
under `logs`, and shown to the user with the report location.

Package 100A-04 prepares reproducible Windows application builds with a
PyInstaller spec, separate build dependency file, dependency-complete runtime
requirements, and a guarded Windows build command.

Package 100A-05 adds a controlled regression runner with per-test isolation,
timeouts, captured failure details, execution timing, and a one-command Phase 6
release-check summary.

Package 100A-06 records monotonic application startup timings at service
initialisation, interface construction, and ready state. The summary is written
to the normal application log for performance comparison without user data.

Package 100A-07 coordinates shutdown actions independently. The scheduled
search monitor, background task manager, and main window are all given a chance
to close even if another shutdown action fails; failures are logged.

Package 100A-08 completes Phase 6 and marks OpportunityLab 1.0.0 as Production.
Release manifests provide deterministic SHA-256 checksums for distributable
source, scripts, documentation, requirements, and build configuration while
excluding private application data.

## Next work

Phase 6 production-readiness work is complete.

## Package 100B-01

Adds persistent manual selection between primary and alternate Gemini API
keys. The selector is available from Data Tools. Key values remain only in
gitignored `config/secrets.py`; the saved selection contains only the words
Primary or Alternate. Legacy `GEMINI_API_KEY` remains supported as Primary.

## Package 100B-02

Adds persistent Personal and organisation sender profiles. Each profile can
store the sender, role, organisation, email, website, organisation description,
charity information, custom signature, and writing tone. Response templates
append the active profile signature. Profiles are managed from Response Draft.

Package 100B-02A prefers Gemini's parsed structured response, accepts fenced
JSON, increases the output allowance to prevent truncation, and converts
malformed responses into a safe retry message instead of a UI failure.

## Package 100B-03

Connects the existing local Ollama email-writing capability to Response Draft.
Generate with Ollama runs in the background and uses the selected opportunity,
active sender profile, organisation and charity details, custom signature, and
profile tone. The generated subject and body remain editable and are saved.

## Package 100B-04

Adds persistent Normal, Large, and Extra Large interface sizes. The setting is
available from Data Tools and is applied before the main interface is built on
future startups. It scales text and controls throughout OpportunityLab.


## Package 110A-01

Adds profile-aware discovery and opportunity scoring. Personal profiles keep
the existing search behaviour. Nonprofit profiles expand searches using their
mission, beneficiaries, service area, support needs, and opportunity types.
Results are rescored and labelled Open Opportunity, Funding Prospect,
Relationship Lead, or Weak Lead. The labels are evidence-led and do not make
tax-deductibility claims or imply that a company is accepting requests.

## Package 110A-02

Activates the persistent Australia Only filter. When enabled it adds Australia
to discovery queries and only displays results with Australian country,
location, text, or `.au` domain evidence.

## Package 110A-03

Adds evidence-based score explanations to Opportunity Details. Each scoring
rule records the signal it matched. Nonprofit results show their classification,
active profile, profile-term matches, service-area match, funding or relationship
signals, available action signals, and closed-opportunity warnings.

## Package 110A-04

Adds a separate Evidence Quality score. Official opportunity pages, eligibility,
funding amounts, closing dates, and clear application or contact actions receive
positive weight. Low-value videos, general-information pages, missing actions,
and closed opportunities receive penalties. Result cards and Opportunity
Details display the evidence tier and supporting reasons.

## Package 110A-05

Adds supporter and donor prospect discovery for nonprofit profiles. Public
charity-support language, past-support reports, partnership contact paths,
cash or in-kind support, and mission relevance receive separate scoring.
Results are labelled Possible Supporter, Relevant Supporter, Support History,
or Contactable Supporter. These labels never assume current availability.

## Package 110A-06

Adds a persistent Hide Weak Evidence option to Search Filters. Adds Quick,
Standard, and Deep search depth to the main search bar, requesting approximately
10, 20, or 30 results per enabled Serper-backed source. Standard is the default.

Package 110A-06A changes Standard and Deep to genuine page-by-page retrieval.
Later-page failures retain results already received instead of failing the
entire source. Company Websites uses a shorter nonprofit-friendly query to
reduce query failures.

Package 110A-06B strengthens Australia Only with geographic eligibility
checks. A foreign-targeted opportunity is rejected even when its title or
Australian government domain also mentions Australia, unless the result
explicitly says Australian organisations are eligible.

## Package 110A-07

Adds webpage evidence verification for the highest-ranked search results. The
active nonprofit profile now has an address field. OpportunityLab reads
eligible-location text from result pages, compares it with the profile address
and service area, removes only clear location exclusions, and keeps unclear
cases as Eligibility Unverified. Verified matches receive a small score bonus.
Gemini receives the extracted webpage evidence and profile-location comparison.

Package 110A-07A adds permanent visible labels above every sender-profile field
and clearer entry placeholders, including the new address field.
