# TODO

> Project direction: keep **Daily Paper Reader** as a general-purpose, fork-and-run research paper discovery, recommendation, reading, and digest platform. Domain specialization should be expressed through editable user profiles, templates, filters, and ranking weights—not hardcoded into the core pipeline.

## Guiding Principles

- [ ] Preserve the project as a general research-intelligence system, not a single-domain tool
- [ ] Keep topic specialization configurable through UI/config profiles
- [ ] Reuse the existing pipeline whenever possible: crawl → recall → fusion/rerank → LLM refine → select → docs/frontend
- [ ] Prefer source adapters and schema extensions over one-off integrations
- [ ] Support graceful degradation when metadata, PDF, code, or citations are missing
- [ ] Avoid paywall bypassing and unauthorized PDF downloading
- [ ] Keep the fork-and-run experience simple for individual researchers and labs
- [ ] Ensure every major new feature has tests, docs, and a rollback path

---

## 0. Skills Encapsulation and Agent Workflow

### Goals

- [ ] Add a repository-maintenance skill within the project: `.codex/skills/maintain-daily-paper-reader/SKILL.md`
- [ ] Define the maintenance workflow for crawling, recall, reranking, LLM refinement, document generation, and frontend workflow panels
- [ ] Define boundaries for the skill:
  - read-only checks
  - pipeline modifications
  - workflow modifications
  - docs generation modifications
  - frontend panel modifications
  - test and regression checks
- [ ] Decide whether to add `agents/openai.yaml` based on stability and maintenance needs
- [ ] Keep the skill general-purpose and avoid encoding a specific research domain

### Acceptance Criteria

- [ ] The skill can orient an AI coding assistant to the repository structure
- [ ] The skill explains the correct order of pipeline steps
- [ ] The skill warns against breaking the fork-and-run workflow
- [ ] The skill documents safe modification boundaries
- [ ] The skill includes a checklist for validating changes before commit

---

## 1. Internationalization and English-First Documentation

### Goals

- [ ] Provide an English-first user experience for international researchers
- [ ] Preserve Chinese support if useful, but avoid mixing languages in the default UI
- [ ] Move toward a maintainable i18n structure instead of scattered hardcoded strings

### UI Localization

- [ ] Translate user-facing Chinese UI text into clear academic English
- [ ] Translate backend-management panel labels
- [ ] Translate topic/subscription management labels
- [ ] Translate workflow trigger panel labels
- [ ] Translate loading, empty-state, success, warning, and error messages
- [ ] Translate model/API configuration labels
- [ ] Translate GitHub PAT setup labels
- [ ] Translate Zotero integration labels
- [ ] Translate tooltip text and button text
- [ ] Keep internal comments in Chinese only if they are not user-facing and are still useful to maintainers

### Documentation

- [ ] Translate `README.md`
- [ ] Translate quick-start guide
- [ ] Translate tutorial pages
- [ ] Translate backend-management usage guide
- [ ] Translate GitHub Actions setup guide
- [ ] Translate local development guide
- [ ] Translate LLM provider configuration guide
- [ ] Translate Zotero integration guide
- [ ] Add screenshots for the English workflow if the UI changes significantly

### i18n Structure

- [ ] Decide whether to implement lightweight i18n files such as:
  - `app/i18n/en.json`
  - `app/i18n/zh.json`
- [ ] Add a language config option such as `ui.language: en`
- [ ] Add fallback behavior when a translation key is missing
- [ ] Add developer guidance for adding new user-facing strings

### Testing and Acceptance

- [ ] Add a script to detect remaining CJK characters in user-facing files
- [ ] Exclude known non-user-facing files from the localization check
- [ ] Add CI or manual checklist for untranslated strings
- [ ] Verify that localization does not alter pipeline logic
- [ ] Verify that GitHub Actions, GitHub Pages deployment, and paper-fetch workflows still work after localization

---

## 2. General Topic Profile System

### Goals

- [ ] Keep topic specialization fully configurable through the UI
- [ ] Make topic profiles the core abstraction for personalization
- [ ] Support researchers from different fields without code changes

### Profile Schema

- [ ] Extend each topic profile to support:
  - `tag`
  - `description`
  - `keywords`
  - `intent_queries`
  - `preferred_sources`
  - `preferred_venues`
  - `excluded_terms`
  - `language_preference`
  - `minimum_score_threshold`
  - `digest_frequency`
  - `ranking_mode`
  - `enabled`
  - `paused`
- [ ] Keep backward compatibility with existing `subscriptions.intent_profiles`
- [ ] Add validation for profile fields
- [ ] Add migration logic for old profile structures

### Profile Templates

- [ ] Add optional editable templates for common research areas:
  - Machine Learning
  - Computer Vision
  - NLP
  - AI Agents
  - Robotics
  - Data Science
  - Bioinformatics
  - Medicine
  - Neuroscience
  - Chemistry
  - Materials Science
  - Social Science
  - Economics
- [ ] Ensure templates are optional presets, not hardcoded pipeline logic
- [ ] Allow users to create, duplicate, edit, pause, export, and import profiles
- [ ] Allow per-profile source selection
- [ ] Allow per-profile schedule/digest frequency

### UI

- [ ] Improve profile creation flow:
  - free-text research need
  - generated candidate keywords
  - generated candidate intent queries
  - user selection and editing
  - preview of expected matches
- [ ] Add profile health indicators:
  - too broad
  - too narrow
  - duplicate profile
  - weak keywords
  - missing intent queries
- [ ] Add “test this profile” dry-run search
- [ ] Add “explain this profile” view showing how keywords and intent queries are used

### Testing and Acceptance

- [ ] Add tests for profile parsing
- [ ] Add tests for profile migration
- [ ] Add tests for profile validation
- [ ] Add tests to ensure domain templates do not affect users unless explicitly selected

---

## 3. Multi-Source Paper Recommendation Integration

### Goals

- [ ] Expand recommendation candidates beyond a single `arXiv / OpenReview` path into multi-source aggregation
- [ ] Maintain reusability of existing BM25, embedding, RRF fusion, reranking, LLM refine, selection, and docs generation steps
- [ ] Keep source integration modular and safe

### Unified Paper Data Model

- [ ] Define a common `PaperRecord` schema
- [ ] Add unified fields:
  - `id`
  - `source`
  - `source_id`
  - `title`
  - `authors`
  - `abstract`
  - `published`
  - `updated`
  - `venue`
  - `doi`
  - `canonical_url`
  - `pdf_url`
  - `landing_page_url`
  - `license`
  - `categories`
  - `keywords`
  - `source_metadata`
- [ ] Add cross-source external ID fields:
  - `arxiv_id`
  - `openreview_id`
  - `openalex_id`
  - `semantic_scholar_id`
  - `pubmed_id`
  - `pmid`
  - `pmcid`
  - `dblp_id`
  - `crossref_doi`
- [ ] Add general research-workflow fields:
  - `code_url`
  - `project_page_url`
  - `dataset_url`
  - `benchmark_name`
  - `contribution_type`
  - `evaluation_type`
  - `reproducibility_signals`
  - `source_reliability`
  - `pdf_access_type`
- [ ] Allow non-arXiv papers to safely enter recall, rerank, LLM refine, selection, and docs generation

### Cross-Source Deduplication

- [ ] Prioritize exact identifiers:
  - DOI
  - arXiv ID
  - PMID
  - PMCID
  - OpenReview ID
- [ ] Add approximate matching using normalized title + year
- [ ] Add author-aware matching for ambiguous titles
- [ ] Merge arXiv preprint and conference/journal versions when appropriate
- [ ] Preserve all known source links after merging
- [ ] Record canonical source selection rationale
- [ ] Add warning for uncertain duplicates
- [ ] Allow manual override for duplicate decisions

### Source Adapter Framework

- [ ] Add a common adapter interface:
  - `search(query, date_range, limit)`
  - `fetch_by_id(source_id)`
  - `normalize(raw_record)`
  - `enrich(record)`
  - `rate_limit_policy`
  - `retry_policy`
- [ ] Add per-source configuration:
  - enabled/disabled
  - timeout
  - retry count
  - rate limit
  - API key requirement
  - date-window support
  - PDF policy
  - metadata-only mode
- [ ] Add source-level failure logs
- [ ] Add source health status

### Sources to Integrate

- [ ] arXiv
- [ ] OpenReview
- [ ] CVF Open Access
- [ ] PMLR
- [ ] Semantic Scholar
- [ ] OpenAlex
- [ ] CrossRef
- [ ] DBLP
- [ ] Papers with Code
- [ ] PubMed
- [ ] Europe PMC
- [ ] bioRxiv
- [ ] medRxiv
- [ ] ChemRxiv
- [ ] IEEE Xplore metadata, if API key is available
- [ ] ACM metadata, if legally/API accessible
- [ ] Publisher RSS/TOC feeds where legally available

### Crawl and Recall

- [ ] Add a multi-source query-driven crawling layer using keywords and intent queries
- [ ] Retain arXiv’s existing global crawling capability
- [ ] Allow external sources as supplementary candidate pools
- [ ] Allow source-specific date-window limits
- [ ] Add source-aware candidate caps
- [ ] Add per-source timeouts, retries, and rate limits
- [ ] Add source-aware dry-run mode
- [ ] Log candidate counts per source

### Downstream Compatibility

- [ ] Enable multi-source mixed output for the Step 1 raw paper pool
- [ ] Ensure BM25 retrieval preserves source information
- [ ] Ensure embedding retrieval preserves source information
- [ ] Ensure RRF fusion preserves source information
- [ ] Ensure reranking and LLM refine recognize multi-source papers instead of defaulting to arXiv
- [ ] Ensure selection logic works for non-arXiv sources
- [ ] Enable docs generation when PDF is missing:
  - abstract-only page
  - external-link-only page
  - metadata-only page
- [ ] Enable sidebar and paper page to display the actual source
- [ ] Add source badges to paper cards/pages
- [ ] Add source filters in the UI

### Testing and Acceptance

- [ ] Add unit tests for multi-source paper parsing
- [ ] Add unit tests for source adapters
- [ ] Add unit tests for cross-source deduplication
- [ ] Add regression tests for non-arXiv papers entering the recommendation path
- [ ] Add tests for no-PDF downgrade paths
- [ ] Add tests for missing DOI, missing abstract, and missing venue
- [ ] Add mixed-source fixture data
- [ ] Add integration test for one full multi-source pipeline run using sample data

---

## 4. Legal PDF Access and Source Reliability

### Goals

- [ ] Ensure the system never bypasses paywalls
- [ ] Clearly distinguish legal open-access PDFs from metadata-only records
- [ ] Provide trustworthy source labeling

### Legal PDF Handling

- [ ] Add Unpaywall integration for legal OA PDF lookup
- [ ] Add `pdf_access_type`:
  - `open_access`
  - `publisher_open`
  - `preprint`
  - `author_accepted_manuscript`
  - `metadata_only`
  - `unknown`
- [ ] Add `pdf_source` and `pdf_license` fields
- [ ] Add warning when only metadata or abstract is available
- [ ] Do not download PDFs from unauthorized mirrors
- [ ] Do not bypass IEEE, Nature, Science, ACM, Springer, Elsevier, or other publisher paywalls
- [ ] Add README section explaining the legal PDF policy
- [ ] Add tests for PDF downgrade behavior

### Source Reliability

- [ ] Add `source_reliability` labels:
  - `official_venue`
  - `publisher`
  - `preprint_server`
  - `metadata_index`
  - `code_repository`
  - `lab_blog`
  - `unknown`
- [ ] Add warning for incomplete metadata
- [ ] Add warning for duplicate preprint/conference versions
- [ ] Add warning when citation count or venue metadata is unavailable
- [ ] Add a source reliability legend in the UI

---

## 5. General Ranking, Reranking, and Recommendation Explanation

### Goals

- [ ] Improve recommendation quality while keeping ranking general-purpose
- [ ] Make ranking interpretable to users
- [ ] Allow per-profile ranking preferences

### General Scoring Components

- [ ] Add `topical_relevance_score`
- [ ] Add `semantic_similarity_score`
- [ ] Add `keyword_match_score`
- [ ] Add `novelty_score`
- [ ] Add `recency_score`
- [ ] Add `venue_or_source_score`
- [ ] Add `citation_or_attention_score`
- [ ] Add `code_availability_score`
- [ ] Add `data_availability_score`
- [ ] Add `benchmark_or_evaluation_score`
- [ ] Add `reproducibility_score`
- [ ] Add `user_feedback_score`
- [ ] Add `final_recommendation_score`

### Ranking Modes

- [ ] Add configurable ranking modes:
  - relevance-first
  - novelty-first
  - high-impact-first
  - code-first
  - dataset/benchmark-first
  - survey-friendly
  - beginner-friendly
  - SOTA-tracking
- [ ] Allow ranking weights to be configured globally
- [ ] Allow ranking weights to be configured per profile
- [ ] Preserve existing BM25, embedding, RRF, reranker, and LLM refine stages

### Explanation

- [ ] Add “Why recommended?” explanation
- [ ] Add score breakdown in paper cards/pages
- [ ] Add matched keywords and matched intent queries
- [ ] Add source/venue contribution to score
- [ ] Add missing-metadata warning when score confidence is low
- [ ] Add “show more like this” and “hide similar papers” hooks for future feedback-aware ranking

### Testing and Acceptance

- [ ] Add unit tests for score calculation
- [ ] Add tests for ranking-mode weight changes
- [ ] Add regression tests to ensure incomplete metadata does not crash scoring
- [ ] Add tests for recommendation explanations
- [ ] Add evaluation fixtures for false positives and false negatives

---

## 6. Digest System

### Goals

- [ ] Keep daily paper updates
- [ ] Add weekly and monthly digest generation
- [ ] Make digests topic-aware and source-aware
- [ ] Archive digests for long-term trend tracking

### Digest Types

- [ ] Daily paper update
- [ ] Weekly digest
- [ ] Monthly trend report
- [ ] Per-profile digest
- [ ] Cross-profile digest
- [ ] Conference digest
- [ ] Manual custom digest from selected papers

### Weekly Digest Structure

- [ ] Executive Summary
- [ ] Must-Read Top Papers
- [ ] Full Ranked List
- [ ] Emerging Trends
- [ ] New Datasets / Benchmarks / Tools
- [ ] Papers with Code or Project Pages
- [ ] Papers to Compare Against Existing Work
- [ ] Suggested Reading Queue
- [ ] Source Coverage and Failure Warnings
- [ ] BibTeX / RIS / Markdown export

### Per-Paper Digest Fields

- [ ] Title
- [ ] Authors
- [ ] Venue/source
- [ ] Publication date
- [ ] Paper link
- [ ] Legal PDF link if available
- [ ] Code/project page/dataset links if available
- [ ] One-sentence takeaway
- [ ] Core contribution
- [ ] Method/task/domain tags
- [ ] Why it matters
- [ ] Limitations
- [ ] Relevance to selected topic profile
- [ ] Reading priority:
  - read now
  - skim
  - archive
  - ignore

### Automation

- [ ] Add weekly GitHub Actions workflow
- [ ] Add monthly GitHub Actions workflow
- [ ] Add manual workflow dispatch for digest regeneration
- [ ] Store digests in `docs/digests/`
- [ ] Update frontend digest archive
- [ ] Add timezone documentation for scheduled workflows
- [ ] Add dry-run mode for digest generation

### Testing and Acceptance

- [ ] Add tests for digest generation from sample recommendations
- [ ] Add tests for empty-week behavior
- [ ] Add tests for missing metadata in digest items
- [ ] Add tests for digest archive index generation

---

## 7. Interactive Research Dashboard

### Goals

- [ ] Turn the frontend into a general personal/lab research command center
- [ ] Support exploration, filtering, annotation, trend tracking, and export
- [ ] Keep the UI useful across research domains

### Core Dashboard Features

- [ ] Add global searchable paper table
- [ ] Add paper-card view
- [ ] Add profile filter
- [ ] Add source filter
- [ ] Add venue filter
- [ ] Add date filter
- [ ] Add contribution-type filter:
  - method
  - dataset
  - benchmark
  - survey
  - theory
  - system
  - application
  - position/opinion
- [ ] Add evaluation-type filter:
  - empirical
  - theoretical
  - benchmark
  - case study
  - system demo
  - unknown
- [ ] Add code-available filter
- [ ] Add legal-PDF-available filter
- [ ] Add reading-status filter
- [ ] Add “Must-Read” panel
- [ ] Add “Recently Added” panel
- [ ] Add “Trending Topics” panel
- [ ] Add “Conference Watch” panel
- [ ] Add “Papers with Code/Data” panel

### Visualizations

- [ ] Add relevance-vs-novelty scatter plot
- [ ] Add topic-cluster visualization
- [ ] Add weekly trend timeline
- [ ] Add source distribution chart
- [ ] Add venue distribution chart
- [ ] Add contribution-type distribution chart
- [ ] Add open-access coverage chart
- [ ] Add paper similarity graph if embeddings are available

### Reading Workflow

- [ ] Add reading status:
  - unread
  - skimmed
  - read
  - important
  - cite later
  - irrelevant
- [ ] Add personal note field per paper
- [ ] Add “Why this paper matters” expandable section
- [ ] Add “How this connects to my profile” section
- [ ] Add selected-paper comparison panel
- [ ] Add local or backend persistence for reading status and notes
- [ ] Add bulk actions for selected papers

### Testing and Acceptance

- [ ] Add frontend tests for dashboard filters
- [ ] Add tests for reading-status persistence
- [ ] Add tests for missing-field rendering
- [ ] Add sample dashboard data for visual regression checks

---

## 8. Export and Research-Library Integration

### Goals

- [ ] Make it easy to move useful papers into Zotero, BibTeX, Markdown notes, Obsidian, Notion, or a lab reading log

### Export Features

- [ ] Add BibTeX export for selected papers
- [ ] Add RIS export for Zotero/Mendeley import
- [ ] Add CSV export
- [ ] Add JSON export
- [ ] Add Markdown export
- [ ] Add digest export
- [ ] Add selected-paper export
- [ ] Add “cite later” export collection
- [ ] Add Better BibTeX-compatible citation key generation

### Zotero Integration

- [ ] Preserve existing Zotero save workflow
- [ ] Add optional Zotero API integration
- [ ] Add Zotero collection mapping by topic profile
- [ ] Add configurable Zotero note templates
- [ ] Add default note fields:
  - summary
  - core contribution
  - method
  - strengths
  - limitations
  - relation to selected profile
  - possible follow-up ideas
- [ ] Add tests for generated BibTeX/RIS validity

### Notes and Knowledge Management

- [ ] Add Obsidian export template
- [ ] Add Notion export option
- [ ] Add Markdown reading-log export
- [ ] Add project/lab reading-list export

---

## 9. Notifications and Delivery

### Goals

- [ ] Deliver digests without requiring users to manually open the dashboard
- [ ] Keep notification channels optional and failure-safe

### Notification Channels

- [ ] Add optional email notification
- [ ] Add optional GitHub Issue notification
- [ ] Add optional Slack webhook notification
- [ ] Add optional Discord webhook notification
- [ ] Add optional Telegram notification
- [ ] Add optional Feishu/Lark notification
- [ ] Add optional Notion database export

### Notification Content

- [ ] Include executive summary
- [ ] Include top recommended papers
- [ ] Include source coverage summary
- [ ] Include failed-source warnings
- [ ] Include link to dashboard
- [ ] Include link to full digest
- [ ] Include export links where available

### Testing and Acceptance

- [ ] Add dry-run mode for notifications
- [ ] Add failure-safe behavior when notification secrets are missing
- [ ] Ensure notification failures do not break ingestion, ranking, docs generation, or dashboard update
- [ ] Add tests for notification payload formatting

---

## 10. API Keys, Secrets, and Security

### Goals

- [ ] Keep the project safe for public GitHub Pages deployment
- [ ] Avoid leaking private API keys, tokens, local config, and generated secrets

### Secrets Management

- [ ] Document required GitHub PAT scopes
- [ ] Add `.env.example` for optional API keys
- [ ] Add GitHub Actions secrets documentation
- [ ] Add API key validation checks
- [ ] Add warning if user tries to commit local secret files
- [ ] Add `.gitignore` entries for:
  - local secret files
  - local databases
  - local generated config
  - private logs
- [ ] Avoid exposing LLM API keys in frontend code where possible
- [ ] Add security notes for GitHub Pages deployment
- [ ] Add secret-leak scan in CI or as a manual script

### Optional API Keys

- [ ] Semantic Scholar API key
- [ ] OpenAlex email / polite pool configuration
- [ ] CrossRef mailto configuration
- [ ] Unpaywall email configuration
- [ ] IEEE Xplore API key
- [ ] Zotero API key
- [ ] Notification webhook secrets
- [ ] LLM provider keys
- [ ] Reranker provider keys
- [ ] Embedding provider keys

### Testing and Acceptance

- [ ] Add tests for missing optional secrets
- [ ] Add tests for invalid API key handling
- [ ] Add documentation for safe rotation of keys
- [ ] Verify no secrets are committed in generated artifacts

---

## 11. Deployment, Local Development, and Reproducibility

### Goals

- [ ] Preserve the fork-and-run user experience
- [ ] Make the project easy to run locally, debug, and deploy
- [ ] Keep workflows reproducible across forks

### Local Development

- [ ] Add one-command local setup if possible
- [ ] Add local run instructions
- [ ] Add local workflow dry-run command
- [ ] Add sample config
- [ ] Add sample paper database
- [ ] Add sample digest output
- [ ] Add troubleshooting section for common macOS/Linux/Windows setup issues
- [ ] Add local-only mode using sample data
- [ ] Add local-only mode for UI development without API keys

### GitHub Actions

- [ ] Keep daily paper ingestion workflow
- [ ] Add weekly digest workflow
- [ ] Add monthly trend workflow
- [ ] Add manual source refresh workflow
- [ ] Add reset/rebuild workflow
- [ ] Add localization check workflow
- [ ] Add unit-test workflow
- [ ] Add dashboard build/deployment workflow
- [ ] Add workflow status summary in the frontend
- [ ] Add concurrency safeguards to avoid cross-run overwrites

### Acceptance Criteria

- [ ] Fresh fork can run with default config
- [ ] Fresh fork can deploy to GitHub Pages
- [ ] User can add one topic profile and fetch papers successfully
- [ ] User can generate a digest manually
- [ ] Scheduled digest can run automatically
- [ ] Dashboard can display mixed-source papers
- [ ] Missing-PDF papers degrade gracefully
- [ ] No API keys are leaked in public files
- [ ] Existing daily workflow remains backward compatible

---

## 12. Observability, Evaluation, and Quality Control

### Goals

- [ ] Measure whether recommendations are useful
- [ ] Make source failures and ranking issues visible
- [ ] Support iterative improvement without hidden regressions

### Metrics

- [ ] Track number of candidates crawled per source
- [ ] Track number of papers after deduplication
- [ ] Track number of papers after recall
- [ ] Track number of papers after rerank
- [ ] Track number of papers after LLM refine
- [ ] Track source coverage statistics
- [ ] Track percentage of papers with legal PDFs
- [ ] Track percentage of papers with code/project pages
- [ ] Track percentage of papers with datasets/benchmarks
- [ ] Track LLM cost and token usage where available
- [ ] Track workflow runtime per step
- [ ] Track user feedback metrics:
  - read
  - skimmed
  - important
  - cite later
  - irrelevant

### Quality Reports

- [ ] Add daily quality report
- [ ] Add weekly quality report
- [ ] Track false positives and false negatives
- [ ] Track duplicated papers across sources
- [ ] Track failed API calls
- [ ] Track source timeouts
- [ ] Track LLM refinement failures
- [ ] Track missing metadata fields
- [ ] Track no-PDF downgrade frequency
- [ ] Surface major warnings in the dashboard

### Testing and Acceptance

- [ ] Add test fixtures for common failure modes
- [ ] Add regression tests for known bugs
- [ ] Add snapshot tests for generated docs/digests
- [ ] Add pipeline smoke test using sample data
- [ ] Add CI summary for test coverage and workflow health

---

## 13. Advanced Research Intelligence Features

### Near-Term

- [ ] English-first UI and documentation
- [ ] General topic profile improvements
- [ ] Source visibility and source filters
- [ ] Weekly digest generation
- [ ] Reading status and personal notes
- [ ] BibTeX/RIS/Markdown export
- [ ] Legal PDF status and source reliability labels

### Mid-Term

- [ ] Semantic Scholar enrichment
- [ ] OpenAlex enrichment
- [ ] CrossRef enrichment
- [ ] Papers with Code enrichment
- [ ] CVF/PMLR/OpenReview integration improvements
- [ ] Relevance-vs-novelty visualization
- [ ] Human-feedback-aware reranking
- [ ] Per-profile ranking modes

### Long-Term

- [ ] Personalized embedding-based recommendation using the user’s Zotero library
- [ ] Paper similarity graph
- [ ] Multi-week trend detection
- [ ] Research-gap detection
- [ ] Automatic comparison table for selected papers
- [ ] Automatic related-work draft generation
- [ ] Notion/Obsidian/lab-wiki research-log integration
- [ ] Multi-user/lab mode with shared profiles and reading lists

---

## 14. Non-Goals and Guardrails

- [ ] Do not hardcode one research field into the core pipeline
- [ ] Do not replace user-configurable topic profiles with fixed domain logic
- [ ] Do not bypass publisher paywalls
- [ ] Do not depend on a single paid API provider
- [ ] Do not make optional integrations mandatory for basic fork-and-run use
- [ ] Do not break existing arXiv/OpenReview workflows while adding new sources
- [ ] Do not expose private API keys in public frontend files
- [ ] Do not allow one failed source to break the entire pipeline when graceful degradation is possible

---

## Suggested Implementation Order

### Phase 1: Preserve and Stabilize

- [ ] Add maintenance skill
- [ ] Improve English documentation
- [ ] Add user-facing localization checks
- [ ] Improve setup/troubleshooting docs
- [ ] Add basic source/status visibility
- [ ] Add tests around existing workflow behavior

### Phase 2: Generalize the Data Layer

- [ ] Define `PaperRecord`
- [ ] Add source adapter interface
- [ ] Add cross-source deduplication
- [ ] Add legal PDF status
- [ ] Add source reliability labels
- [ ] Add mixed-source sample fixtures

### Phase 3: Generalize the Recommendation Layer

- [ ] Make source-aware recall and rerank robust
- [ ] Add general scoring components
- [ ] Add ranking modes
- [ ] Add recommendation explanations
- [ ] Add feedback-aware ranking hooks

### Phase 4: Improve User Research Workflow

- [ ] Add dashboard filters
- [ ] Add reading status
- [ ] Add personal notes
- [ ] Add weekly/monthly digests
- [ ] Add export features
- [ ] Add optional notifications

### Phase 5: Advanced Intelligence

- [ ] Add Zotero-based personalization
- [ ] Add paper similarity graph
- [ ] Add trend detection
- [ ] Add research-gap detection
- [ ] Add related-work drafting support
