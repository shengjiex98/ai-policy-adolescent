# CLAUDE.md — Constitution for AI Platform Governance Event Scraping

## 0. Purpose of This Constitution

This file is the governing instruction set for Claude Code/Codex-style agents that scrape, normalize, classify, and export **AI platform governance events** relevant to adolescent use of AI chatbots for mental health needs.

This constitution covers **platform- and company-level governance events only**: public changes, disclosures, policies, safety features, privacy settings, age controls, crisis protocols, model/system cards, release notes, transparency reports, app-store metadata, and other public documentation from companies that operate general-purpose AI chatbots, companion chatbots, mental-health chatbots, or AI systems plausibly used by adolescents for emotional support or mental health advice.

This constitution does **not** cover jurisdiction-level legal or policy events such as federal/state laws, county ordinances, agency rules, school board policies, or enforcement actions unless those events are referenced only as context for a platform's own product, policy, or governance change. Jurisdiction-level legal and policy events are governed by a separate constitution.

Claude must read this file at the beginning of every run and treat it as the source of truth for scope, fields, taxonomy, workflow, classification rules, output requirements, and human-review standards.

---

## 1. Overarching Objective

The objective is to build a reproducible, periodically updated inventory of **time-dated AI platform governance events** that may directly or indirectly affect:

1. adolescent use of AI chatbots for emotional support, mental health advice, companionship, crisis support, or help-seeking;
2. adolescent exposure to unsafe, harmful, misleading, overly therapeutic, privacy-invasive, or dependency-promoting AI chatbot interactions;
3. adolescent actions after AI chatbot interactions, including contacting 988, disclosing use to caregivers/clinicians, seeking formal care, or delaying care;
4. provider perceptions of AI chatbot safety, appropriateness, and clinical relevance;
5. platform-specific safety exposure measures for survey respondents, especially by primary platform, any platform use, and frequency-weighted platform use.

The final product is an analyzable, versioned dataset suitable for longitudinal survey linkage and platform-event analyses. The dataset should support event-time, interrupted-time-series-style descriptive analyses, and stacked difference-in-differences analyses using differential exposure by platform where the study design permits.

The central analytic principle is: **capture platform governance events with enough structure to identify what changed, when it changed, which platform/product/users were affected, and the plausible safety or behavioral pathway—without asking the scraper to infer private product behavior or undocumented internal policies.**

---

## 2. Operational Workflow

Claude must follow this workflow exactly unless the human operator explicitly changes it.

### Step 1. Read this constitution

At the beginning of each run, Claude must read `CLAUDE.md` or this constitution file and confirm internally that the task is limited to **AI platform governance events**, not jurisdiction-level laws or policies.

### Step 2. Read the input source workbook

Claude must look for an Excel workbook named:

```text
input_sources.xlsx
```

The workbook should contain a sheet named `sources` if available. If no sheet name is specified or detectable, Claude should use the first worksheet.

The workbook should contain at least these two columns:

| Required column | Meaning |
|---|---|
| `source_name` | Human-readable source name, e.g., `OpenAI Release Notes`, `Anthropic System Cards`, `Google Gemini Privacy Notice`, `Snapchat My AI Help Center`, `Character.AI Safety Center`, `Replika Privacy Policy`, `Wysa Safety Page` |
| `source_url` | URL to scrape, query, download, or use as the starting point for source discovery |

The workbook may also contain these optional columns. Claude should use them when present but must not require them:

| Optional column | Meaning |
|---|---|
| `enabled` | If present and equal to `FALSE`, `0`, or `no`, skip this source |
| `company_hint` | Company name, e.g., `OpenAI`, `Anthropic`, `Google`, `Meta`, `Snap`, `xAI`, `Luka`, `Wysa`, `Youper` |
| `platform_hint` | Platform/product name, e.g., `ChatGPT`, `Claude`, `Gemini`, `Meta AI`, `Grok`, `My AI`, `Character.AI`, `Replika`, `Wysa`, `Youper` |
| `source_tier` | `official`, `app_store`, `archive`, `third_party_tracker`, `news_context`, `other` |
| `source_type_hint` | `release_notes`, `changelog`, `safety_policy`, `usage_policy`, `privacy_policy`, `terms`, `model_card`, `system_card`, `transparency_report`, `help_center`, `blog_post`, `developer_policy`, `app_store_metadata`, `web_archive`, `unknown` |
| `date_filter_start` | Earliest date to include, if specified, ISO `YYYY-MM-DD` |
| `date_filter_end` | Latest date to include, if specified, ISO `YYYY-MM-DD` |
| `scrape_depth` | `single_page`, `follow_same_domain_links`, `api`, `download_only`, or `unknown` |
| `notes` | Free-text instructions from the human operator |

If only `source_name` and `source_url` are present, Claude must still proceed.

### Step 3. Scrape or query each listed source

For every enabled row in `input_sources.xlsx`, Claude must attempt to retrieve candidate platform-governance records.

Claude should prefer, in order:

1. official API endpoint or structured changelog, if available;
2. official release notes, safety page, help-center page, model card, system card, transparency report, privacy policy, terms of service, or usage policy;
3. official downloadable PDF, HTML, JSON, CSV, or text file;
4. official app-store metadata page;
5. official web archive or archived version supplied by the human operator;
6. reputable third-party source only as context or discovery, not as canonical evidence unless no official source exists.

Claude must not bypass paywalls, authentication, robots restrictions, app login requirements, rate limits, anti-scraping mechanisms, CAPTCHAs, or private APIs. If a source cannot be scraped reliably, Claude must log the failure in the output workbook and continue with the next source.

### Step 4. Extract candidate platform-governance records

A candidate platform-governance record may be any public event, announcement, documentation change, policy change, or product-safety feature related to:

- age eligibility, age assurance, teen mode, youth safety defaults, or supervised access;
- parental controls or family oversight;
- self-harm, suicide, crisis, emergency, 988, or trusted-contact handling;
- harmful-content refusals or safety filters;
- boundaries around therapy, diagnosis, clinical advice, medication advice, or crisis support;
- privacy policy, data retention, chat history, memory, model-training data, deletion, or third-party sharing;
- transparency reporting, system cards, model cards, red-teaming, independent audits, or safety evaluations;
- product or model releases that materially change user interaction, safety behavior, memory, modality, or access;
- API/developer policies governing youth-facing, mental-health, companion, or self-harm-related uses;
- app-store age ratings, platform availability, account eligibility, or regional restrictions when they affect minors or mental-health-related use.

Claude must extract both metadata and text when possible. If full text is not available, Claude must extract the best available summary and source URL, then mark `human_review_needed = TRUE`.

### Step 5. Normalize, deduplicate, classify, and decide whether the record is a major event

Claude must normalize records into the data model in Section 4 and classify them using the taxonomy in Section 5.

Claude must deduplicate records across sources. For example, the same ChatGPT teen-safety change may appear in a company blog post, a release note, a help-center page, and a privacy-policy update. The canonical record should prefer the most direct official source describing the change, while retaining secondary source URLs in `supporting_source_urls`.

Claude must classify each event as one of:

| Event importance | Meaning |
|---|---|
| `major_safety_relevant_event` | A documented change plausibly affecting adolescent safety, crisis response, harmful-content exposure, privacy, youth access, mental-health advice boundaries, or platform-specific study outcomes |
| `minor_contextual_update` | A routine release, documentation update, UI change, or model update with plausible but weak relevance; retain descriptively |
| `baseline_policy_snapshot` | Current policy or setting captured on first run when no prior version is available; useful for baseline governance inventory but not necessarily an event-time exposure |
| `exclude` | No meaningful pathway to adolescent AI mental health use, safety, privacy, help-seeking, or provider response |

### Step 6. Export the output workbook

Claude must generate an Excel workbook named:

```text
platform_governance_events_output_YYYYMMDD.xlsx
```

where `YYYYMMDD` is the run date.

The workbook must include the required sheets described in Section 8.

### Step 7. Generate a run report

Claude must generate a short markdown run report named:

```text
platform_governance_events_run_report_YYYYMMDD.md
```

The report must summarize sources attempted, sources failed, records extracted, records included, records excluded, major safety-relevant events, changed source hashes, and human-review issues.

---

## 3. Scope Rules

### 3.1 Include records when they plausibly affect adolescent AI chatbot mental health use or provider response

Include a record if it concerns at least one of the following:

- general-purpose AI chatbot platforms that adolescents may use for emotional support or mental health advice;
- AI companion, social chatbot, character chatbot, or relational AI platforms;
- mental-health-specific chatbots or digital mental health tools using AI;
- youth, teens, minors, children, students, families, parental controls, or supervised accounts;
- self-harm, suicide, crisis, abuse, eating disorder, substance use, emergency escalation, 988, or other safety-critical interaction handling;
- AI advice boundaries related to therapy, diagnosis, treatment, medication, clinical care, crisis care, or professional help-seeking;
- privacy, retention, memory, model training, human review, deletion, or third-party sharing of chatbot conversations;
- model/system cards, safety reports, transparency reports, red-team reports, independent evaluations, safety announcements, or audit documentation;
- product changes likely to affect adolescent exposure, such as teen mode, voice mode, memory, companion mode, roleplay, API access, or social-media integration;
- developer policies that restrict or permit youth-facing, mental-health, companion, or crisis-related uses of the platform.

### 3.2 Exclude records with no plausible pathway

Exclude records if they are about AI or software but have no meaningful youth, mental-health, safety, privacy, crisis, companion, chatbot, provider, or survey-exposure pathway.

Examples likely to exclude:

- infrastructure uptime changes with no safety, privacy, youth, or chatbot behavior relevance;
- enterprise pricing changes unrelated to youth, health, privacy, safety, or access;
- model benchmark announcements with no user-facing safety or governance content;
- developer feature releases unrelated to conversational AI, safety, privacy, youth, health, or mental health;
- broad corporate news with no documented product, policy, safety, privacy, or governance change.

Excluded records should be placed in the `excluded_records` sheet, not silently discarded, if they were retrieved as candidate records.

### 3.3 Do not invent undocumented platform behavior

Claude must not infer internal model behavior from speculation, news commentary, social media anecdotes, or isolated user reports. Claude may record public allegations or incidents only when they are linked to an official platform response, policy update, safety report, product change, app-store metadata change, or documented source that the human operator has asked to track.

If a date, rollout status, affected product, affected age group, or safety implication is not available, Claude must use `unknown`, not guess. If a date is inferred from context, Claude must set `date_confidence = low` and explain the inference in `human_review_reason`.

---

## 4. Parsimonious Analyzable Data Model

Claude should capture a **parsimonious core set of fields**. Do not create dozens of speculative variables. The goal is to support analysis, deduplication, survey linkage, and human review.

### 4.1 Required sheet: `platform_events`

One row per distinct platform-governance event or baseline policy snapshot after deduplication.

| Field | Required? | Description |
|---|---:|---|
| `event_id` | Yes | Stable unique ID generated from company + platform + event date/date basis + normalized event title or text hash |
| `run_id` | Yes | Run date/time or UUID |
| `retrieved_at` | Yes | Timestamp when Claude retrieved the source |
| `source_name` | Yes | Primary source name from `input_sources.xlsx` |
| `source_url` | Yes | Primary source URL from `input_sources.xlsx` or official page reached from source |
| `supporting_source_urls` | No | Pipe-delimited list of additional URLs describing the same event |
| `company` | Yes | Company/operator, e.g., `OpenAI`, `Anthropic`, `Google`, `Meta`, `Snap`, `xAI`, `Luka`, `Character.AI`, `Wysa`, `Youper`, `unknown` |
| `platform` | Yes | Platform/product, e.g., `ChatGPT`, `Claude`, `Gemini`, `Meta AI`, `Grok`, `My AI`, `Replika`, `Wysa`, `Youper`, `unknown` |
| `product_or_surface` | No | Specific app, API, model, feature, account type, or surface affected, e.g., `web app`, `mobile app`, `API`, `teen accounts`, `education accounts`, `voice mode`, `memory`, `companion mode` |
| `model_or_version` | No | Model version, app version, policy version, system card version, or release version, if available |
| `event_title` | Yes | Short neutral title for the event |
| `event_summary` | Yes | 1–3 sentence neutral summary of what changed and why it matters |
| `event_importance` | Yes | `major_safety_relevant_event`, `minor_contextual_update`, `baseline_policy_snapshot`, or `exclude` |
| `event_type` | Yes | `policy_change`, `product_feature_change`, `model_release`, `safety_announcement`, `privacy_change`, `terms_change`, `model_card`, `system_card`, `transparency_report`, `app_store_change`, `developer_policy_change`, `baseline_snapshot`, `other`, `unknown` |
| `announcement_date` | No | Date publicly announced, ISO `YYYY-MM-DD` |
| `rollout_start_date` | No | Date rollout began, if available |
| `rollout_end_date` | No | Date rollout completed, if available |
| `effective_date` | No | Best date for analytic exposure, if available |
| `date_basis` | Yes | `effective_date`, `rollout_start_date`, `rollout_end_date`, `announcement_date`, `policy_effective_date`, `document_date`, `retrieval_date`, `unknown` |
| `date_confidence` | Yes | `high`, `medium`, `low`, `unknown` |
| `primary_category_code` | Yes | One category code from taxonomy in Section 5 |
| `primary_subcategory_code` | Yes | One subcategory code from taxonomy in Section 5 |
| `all_category_codes` | Yes | Pipe-delimited category codes; include primary and secondary categories |
| `all_subcategory_codes` | Yes | Pipe-delimited subcategory codes |
| `affected_user_group` | Yes | `all_users`, `minors`, `teens`, `children_under_13`, `parents_guardians`, `providers`, `developers`, `enterprise_education`, `unknown` |
| `affected_region` | Yes | `global`, `US`, state/country if known, or `unknown` |
| `default_setting_changed` | Yes | `TRUE`, `FALSE`, or `UNKNOWN`; whether default behavior/settings changed rather than optional guidance only |
| `user_control_changed` | Yes | `TRUE`, `FALSE`, or `UNKNOWN`; whether users/parents gained/lost a control, setting, opt-out, deletion option, or supervision option |
| `safety_relevance_score` | Yes | `3`, `2`, `1`, or `0`; see Section 6 |
| `analytic_priority` | Yes | `high_confirmatory`, `medium_secondary`, `covariate_context`, `low_descriptive`, `exclude` |
| `expected_direction` | Yes | `safer`, `riskier`, `mixed_or_ambiguous`, `access_increasing`, `access_restricting`, `unknown` |
| `mechanism_summary` | Yes | Short statement of the hypothesized pathway to adolescent AI use, safety, help-seeking, privacy, or provider response |
| `survey_exposure_mapping` | Yes | How this can map to survey data, e.g., `primary_platform_users`, `any_platform_users`, `frequency_weighted_platform_users`, `all_users_national`, `not_mappable`, `unknown` |
| `relevant_quote` | Yes | Short excerpt from source text supporting event classification; keep under 500 characters |
| `quote_location` | No | Section, page, heading, release note anchor, policy section, or URL fragment if available |
| `text_hash` | No | Hash of retrieved text for change detection |
| `classification_confidence` | Yes | `high`, `medium`, `low` |
| `human_review_needed` | Yes | `TRUE` or `FALSE` |
| `human_review_reason` | No | Required when `human_review_needed = TRUE` |

### 4.2 Date priority rule

For analysis, the preferred event date is the first clearly applicable date in this order:

1. `effective_date` explicitly stated in the source;
2. `rollout_start_date` if the change was rolled out over time and start date is known;
3. `rollout_end_date` if only completion date is known;
4. `policy_effective_date` for privacy policy, terms, usage policy, or developer policy changes;
5. `announcement_date` for public announcements without a separate effective date;
6. `document_date` for dated model cards, system cards, transparency reports, or safety reports;
7. `retrieval_date` only for baseline snapshots where no event date exists.

Claude must record which date was used in `date_basis`. Do not use retrieval date as a substantive event date unless the row is clearly marked `baseline_policy_snapshot` or `human_review_needed = TRUE`.

### 4.3 Baseline snapshot rule

On the first run, Claude may create `baseline_policy_snapshot` rows for important current policies/settings even if no change date is available. Baseline snapshots are useful for inventory and survey-wave mapping, but they should not be treated as event-time exposures unless a historical effective date is later confirmed.

Examples of valid baseline snapshots:

- current minimum age policy for a platform;
- current privacy policy regarding model training opt-out;
- current self-harm or crisis response help-center policy;
- current parental-control feature documentation;
- current mental-health advice disclaimer.

---

## 5. Platform Governance Taxonomy

Claude must classify every included record into at least one primary category and one primary subcategory. Multiple secondary categories/subcategories are allowed and should be recorded in `all_category_codes` and `all_subcategory_codes`.

When a record spans multiple categories, choose the primary category based on the **most direct mechanism** linking the platform change to adolescent AI chatbot mental health use, safety, help-seeking, privacy, or provider engagement.

### Category A. `A_AGE_ELIGIBILITY_ASSURANCE` — Age Eligibility and Age Assurance

Use this category for platform governance events that define, change, enforce, or verify who can access the platform or specific AI features by age.

#### A1. `A1_MINIMUM_AGE_POLICY`

Specific examples:

- sets or changes the minimum age for using the platform;
- distinguishes access rules for users under 13, under 16, under 18, or adults;
- changes terms stating that minors require parental or guardian consent;
- creates separate eligibility rules for consumer, school, enterprise, or family accounts;
- clarifies that a platform is not intended for children or minors.

#### A2. `A2_AGE_PREDICTION_OR_AGE_INFERENCE`

Specific examples:

- announces age prediction, age estimation, age inference, or age-classification systems;
- uses behavioral, account, device, or profile signals to infer whether a user is a minor;
- routes suspected teen users into a different experience;
- flags potentially underage users for additional verification or restrictions;
- changes accuracy, appeals, or enforcement procedures for age-prediction systems.

#### A3. `A3_ID_CHECK_OR_AGE_VERIFICATION`

Specific examples:

- requires ID checks, document verification, selfie checks, third-party age verification, or payment-card checks;
- adds age gates before accessing sensitive features;
- requires age verification for voice, companion, image, memory, roleplay, or adult-oriented features;
- creates procedures for users to contest or appeal an age determination.

#### A4. `A4_DEFAULT_TEEN_EXPERIENCE`

Specific examples:

- creates a default teen experience or teen account mode;
- automatically applies stricter settings for users identified as teens;
- changes default content filters, privacy settings, memory settings, or personalization for teen accounts;
- creates a separate teen version of the app, chatbot, or AI assistant.

#### A5. `A5_UNDER_13_SUPERVISED_ACCESS`

Specific examples:

- creates supervised access for children under 13;
- requires parent, school, or guardian management for under-13 users;
- permits under-13 use only through education, family, or managed accounts;
- restricts under-13 access to specific child-safe features;
- clarifies that under-13 users cannot use the service.

#### A6. `A6_AGE_ENFORCEMENT_AND_ACCOUNT_ACTIONS`

Specific examples:

- suspends, limits, or terminates accounts suspected to be underage;
- requires re-verification after age-policy violations;
- changes enforcement for misreported age;
- creates account restrictions for minors attempting to access disallowed features.

---

### Category B. `B_TEEN_MODE_YOUTH_SAFETY_DEFAULTS` — Teen Mode and Youth Safety Defaults

Use this category for youth-specific product defaults, safety settings, content filtering, personalization limits, or account-level protections.

#### B1. `B1_STRICTER_CONTENT_FILTERS_FOR_MINORS`

Specific examples:

- applies stricter filters to teen or minor accounts;
- blocks sensitive or mature topics for minors;
- reduces exposure to self-harm, sexual, violent, substance-use, or exploitative content;
- creates youth-specific refusal behavior;
- applies more conservative moderation thresholds for younger users.

#### B2. `B2_REDUCED_PERSONALIZATION_OR_MEMORY_FOR_MINORS`

Specific examples:

- turns memory off by default for teen users;
- limits personalization using teen conversations;
- prevents long-term memory from storing sensitive teen information;
- reduces emotional personalization, relational continuity, or identity-based profiling for minors;
- limits use of teen data for recommendations or responses.

#### B3. `B3_SENSITIVE_TOPIC_HANDLING_FOR_TEENS`

Specific examples:

- changes how the chatbot responds to teen questions about depression, anxiety, self-harm, eating disorders, abuse, substance use, sexuality, or crisis;
- adds supportive but non-instructional responses for sensitive teen topics;
- adds guidance to contact a trusted adult, clinician, school counselor, 988, or emergency services;
- refuses unsafe advice while offering safer alternatives.

#### B4. `B4_EDUCATION_OR_SCHOOL_ACCOUNT_PROTECTIONS`

Specific examples:

- creates special protections for school, student, classroom, or education accounts;
- limits data sharing or model training for education accounts;
- restricts sensitive features for students;
- gives schools or districts administrative controls over AI access;
- changes student-facing AI defaults.

#### B5. `B5_YOUTH_DEFAULT_PRIVACY_SETTINGS`

Specific examples:

- makes teen accounts private by default;
- limits profile visibility or discoverability for minors;
- limits ad targeting, profiling, or cross-context personalization for minors;
- defaults minors into stricter data-sharing settings;
- changes consent or notice defaults for youth users.

#### B6. `B6_SAFE_COMPLETION_STYLE_FOR_MINORS`

Specific examples:

- changes response style for minors to be more supportive, bounded, and safety-oriented;
- directs teens to trusted adults or professionals for serious issues;
- avoids overly intimate, dependent, romantic, or therapeutic tone with minors;
- reduces validation of harmful plans or delusional beliefs;
- explicitly adds developmental appropriateness to response policies.

---

### Category C. `C_PARENTAL_FAMILY_CONTROLS` — Parental Controls and Family Oversight

Use this category for platform governance events that give parents, guardians, or family managers visibility, control, alerts, or settings related to minors' AI use.

#### C1. `C1_PARENT_DASHBOARD_OR_FAMILY_CENTER`

Specific examples:

- launches or changes a parent dashboard, family center, or supervision hub;
- allows parents to see that a minor uses AI features;
- shows use metadata such as frequency, duration, enabled features, or safety settings;
- allows family managers to view account status or restrictions;
- provides centralized youth-safety controls.

#### C2. `C2_DISABLE_OR_RESTRICT_AI_FEATURES_FOR_MINOR`

Specific examples:

- lets parents disable AI chatbot access;
- lets parents restrict companion, roleplay, memory, voice, image, or sensitive-topic features;
- creates time-of-day or duration restrictions;
- lets parents approve or deny use of specific AI features;
- creates managed-account AI permissions.

#### C3. `C3_PARENTAL_VISIBILITY_AND_MINOR_PRIVACY_BALANCE`

Specific examples:

- gives parents metadata without full chat transcripts;
- gives parents summaries, alerts, or safety flags;
- changes whether parents can view conversation content;
- explains privacy boundaries between teens and parents;
- changes parental notification defaults.

#### C4. `C4_CRISIS_OR_SELF_HARM_ALERTS_TO_PARENT_TRUSTED_CONTACT`

Specific examples:

- alerts parents, guardians, trusted contacts, or emergency contacts about self-harm risk;
- creates trusted-contact escalation features;
- changes policy for when crisis content is shared outside the chat;
- adds opt-in or default emergency-contact features;
- explains limits of confidentiality for minors in crisis situations.

#### C5. `C5_PARENTAL_EDUCATION_AND_GUIDANCE`

Specific examples:

- publishes parent-facing guidance about teen AI use;
- explains mental-health, privacy, dependency, or safety risks to parents;
- provides recommended family rules or conversation guides;
- adds help-center guidance for parents on AI mental health support.

---

### Category D. `D_SELF_HARM_CRISIS_HANDLING` — Self-Harm, Suicide, Crisis, and Emergency Handling

Use this category for platform changes or policies involving suicide, self-harm, crisis escalation, emergency resources, 988, abuse, imminent danger, or related high-risk situations.

#### D1. `D1_988_OR_CRISIS_RESOURCE_ROUTING`

Specific examples:

- adds or changes routing to 988, crisis text lines, emergency services, local crisis resources, or suicide-prevention resources;
- changes when crisis resources appear;
- adds direct links, buttons, banners, or prompts to contact crisis support;
- localizes crisis resources by geography;
- routes teen users differently than adults.

#### D2. `D2_SELF_HARM_OR_SUICIDE_RESPONSE_PROTOCOL`

Specific examples:

- announces a specific protocol for self-harm or suicide-related interactions;
- changes how the model detects, refuses, or responds to self-harm prompts;
- distinguishes ideation, intent, means, imminent risk, or emergency situations;
- provides supportive language while refusing instructions or methods;
- documents a model behavior change for suicidal ideation.

#### D3. `D3_EMERGENCY_ESCALATION_OR_DUTY_TO_ACT_POLICY`

Specific examples:

- explains whether and when the company contacts emergency services;
- changes law-enforcement or emergency escalation policy;
- adds human review for imminent-harm situations;
- clarifies that the platform does not provide real-time monitoring or emergency dispatch;
- creates escalation pathways for imminent threats.

#### D4. `D4_TRUSTED_ADULT_OR_CLINICIAN_DISCLOSURE_PROMPT`

Specific examples:

- encourages minors to contact a trusted adult, caregiver, clinician, school counselor, or therapist;
- changes language encouraging disclosure to human supports;
- adds prompts to seek formal care or schedule an appointment;
- prompts users to move from chatbot conversation to human support.

#### D5. `D5_EATING_DISORDER_SUBSTANCE_ABUSE_OR_ABUSE_CRISIS_HANDLING`

Specific examples:

- changes response policy for eating disorder behaviors, purging, starvation, body-checking, or weight-loss misuse;
- changes response policy for substance misuse, overdose, intoxication, or hiding intoxication;
- changes response policy for abuse, exploitation, trafficking, coercion, or violence;
- routes users to specialized crisis, medical, or safety resources.

#### D6. `D6_NOT_A_CRISIS_SERVICE_DISCLAIMER`

Specific examples:

- states that the platform is not a crisis service;
- instructs users not to rely on the chatbot in emergencies;
- tells users to call emergency services or crisis lines for urgent risk;
- changes placement, wording, or prominence of crisis disclaimers.

---

### Category E. `E_HARMFUL_CONTENT_REFUSAL_SAFETY_FILTERS` — Harmful-Content Refusals and Safety Filters

Use this category for content-policy or model-behavior changes that prevent, refuse, redirect, or moderate harmful outputs.

#### E1. `E1_SELF_HARM_METHODS_OR_INSTRUCTIONS_REFUSAL`

Specific examples:

- refuses instructions for suicide or self-harm methods;
- refuses lethal means information, concealment, optimization, or planning;
- refuses personalized self-harm advice;
- changes the boundary between supportive content and actionable harmful instructions.

#### E2. `E2_VIOLENCE_ABUSE_EXPLOITATION_REFUSAL`

Specific examples:

- refuses violent instructions, abuse facilitation, exploitation, coercion, stalking, or threats;
- improves handling of abuse disclosures;
- changes policies on violence or safety threats involving minors;
- redirects users toward safety resources.

#### E3. `E3_SEXUAL_CONTENT_INVOLVING_MINORS_REFUSAL`

Specific examples:

- prohibits sexual content involving minors;
- restricts sexualized roleplay with teen users or teen characters;
- changes detection/refusal of grooming, exploitation, or sexual coercion;
- prevents the chatbot from encouraging romantic or sexual intimacy with minors.

#### E4. `E4_ILLICIT_SUBSTANCES_OR_MEDICAL_MISUSE_REFUSAL`

Specific examples:

- refuses instructions for drug misuse, overdose, intoxication concealment, or unsafe medication use;
- refuses dangerous combinations of substances or medications;
- redirects users toward medical or emergency help;
- adds safety policies for adolescent substance-related prompts.

#### E5. `E5_EATING_DISORDER_OR_BODY_HARM_REFUSAL`

Specific examples:

- refuses weight-loss, starvation, purging, laxative misuse, or body-harm instructions;
- changes handling of pro-eating-disorder content;
- provides supportive redirection instead of reinforcement;
- adds teen-specific eating disorder safeguards.

#### E6. `E6_EVASION_JAILBREAK_OR_UNSAFE_COACHING_REFUSAL`

Specific examples:

- improves resistance to jailbreaks seeking harmful mental-health, self-harm, or crisis-related content;
- refuses requests to bypass safety policies;
- refuses coaching to hide symptoms, avoid detection, or deceive caregivers/clinicians;
- changes policy around roleplay that enables unsafe advice.

#### E7. `E7_BULLYING_HARASSMENT_OR_COERCION_REFUSAL`

Specific examples:

- refuses bullying, harassment, humiliation, blackmail, or coercive content;
- adds safeguards for teen social harm;
- changes policy for interpersonal manipulation, coercive control, or abuse;
- redirects users away from harmful peer interactions.

---

### Category F. `F_MENTAL_HEALTH_ADVICE_BOUNDARIES` — Mental Health Advice Boundaries and Therapeutic Role Limits

Use this category for changes defining whether, when, and how the platform provides mental-health advice, therapy-like support, diagnosis, treatment guidance, medication advice, or clinical referrals.

#### F1. `F1_DIAGNOSIS_TREATMENT_REFUSAL_OR_LIMITATION`

Specific examples:

- refuses to diagnose mental health conditions;
- refuses to provide treatment plans;
- refuses to decide whether therapy, hospitalization, medication, or emergency care is needed;
- states that users should consult a licensed professional for diagnosis or treatment;
- changes model behavior for clinical decision-making prompts.

#### F2. `F2_NOT_THERAPIST_OR_NOT_MEDICAL_ADVICE_DISCLOSURE`

Specific examples:

- adds or changes disclaimer that the chatbot is not a therapist, doctor, clinician, or substitute for professional care;
- adds or changes disclaimer that responses are not medical or mental health advice;
- changes how often or where these disclaimers are shown;
- makes disclaimers age-appropriate or more prominent for teens.

#### F3. `F3_MEDICATION_OR_CLINICAL_CARE_ADVICE_LIMITS`

Specific examples:

- restricts medication advice, dosage advice, starting/stopping medications, or treatment changes;
- refuses to advise users to discontinue therapy, medication, or clinical care;
- directs users to clinicians, pharmacists, or emergency services for medication questions;
- changes guidance for psychiatric medication, side effects, or interactions.

#### F4. `F4_SUPPORTIVE_NONCLINICAL_FRAMING`

Specific examples:

- frames chatbot support as general emotional support, coaching, journaling, or information rather than therapy;
- limits therapeutic claims;
- encourages coping strategies while avoiding clinical treatment advice;
- changes language to avoid overclaiming clinical benefit.

#### F5. `F5_THERAPIST_ROLEPLAY_OR_SIMULATED_CLINICIAN_RESTRICTION`

Specific examples:

- prevents the chatbot from roleplaying as a therapist, psychiatrist, psychologist, counselor, or crisis worker;
- restricts simulated therapeutic relationships;
- restricts persistent therapy personas;
- changes character/companion roleplay policies involving mental health.

#### F6. `F6_PROFESSIONAL_HELP_SEEKING_PROMPTS`

Specific examples:

- prompts users to speak with a clinician, caregiver, trusted adult, school counselor, or other human support;
- prompts users to schedule care;
- adds language distinguishing chatbot support from formal care;
- changes pathways from AI interaction to human care.

---

### Category G. `G_PRIVACY_MEMORY_RETENTION_TRAINING` — Privacy, Memory, Retention, Model Training, and Data Controls

Use this category for changes to how platforms collect, store, retain, use, share, review, delete, or train on user conversations, especially sensitive or minor-user conversations.

#### G1. `G1_CHAT_HISTORY_RETENTION_POLICY`

Specific examples:

- changes chat history retention period;
- changes whether conversations are stored by default;
- changes temporary chat, incognito mode, or history-off settings;
- creates special retention rules for minors or sensitive conversations;
- changes retention after account deletion.

#### G2. `G2_MEMORY_CONTROLS`

Specific examples:

- launches, removes, or changes memory features;
- turns memory on or off by default for any group;
- creates memory deletion, review, or editing controls;
- restricts memory for teen users or sensitive topics;
- changes how remembered facts are used in responses.

#### G3. `G3_MODEL_TRAINING_OPT_OUT_OR_DATA_USE`

Specific examples:

- changes whether user conversations are used to train or improve models;
- creates or modifies opt-out from model training;
- excludes minors, education accounts, enterprise users, health-related chats, or sensitive conversations from training;
- changes user notice about training data;
- changes data use for safety, research, or product improvement.

#### G4. `G4_HUMAN_REVIEW_OF_CONVERSATIONS`

Specific examples:

- changes whether human reviewers may review chats;
- changes review for safety, abuse, quality, or model improvement;
- creates special human-review rules for minors or crisis content;
- changes user disclosure of human review;
- changes retention or redaction for human-reviewed conversations.

#### G5. `G5_SENSITIVE_CONVERSATION_HANDLING`

Specific examples:

- creates special handling for mental-health, crisis, health, biometric, sexual, or minor-user data;
- changes protections for sensitive conversations;
- creates additional consent or deletion options for sensitive content;
- restricts sharing or training on sensitive conversations.

#### G6. `G6_THIRD_PARTY_SHARING_OR_SUBPROCESSORS`

Specific examples:

- changes sharing of chatbot data with vendors, subprocessors, analytics providers, advertisers, affiliates, or third parties;
- changes disclosure of subprocessors;
- changes cross-context advertising or data broker practices;
- changes API/developer data sharing involving user chats.

#### G7. `G7_DELETION_EXPORT_OR_ACCOUNT_DATA_RIGHTS`

Specific examples:

- changes user ability to delete chats, memories, or account data;
- changes ability to export data;
- changes parental or minor data-deletion rights;
- changes deletion timing or exceptions;
- changes privacy-request procedures.

---

### Category H. `H_TRANSPARENCY_REPORTING_EVALUATION` — Transparency, Safety Reporting, Model/System Cards, and Evaluations

Use this category for platform documents that publicly describe safety performance, risks, evaluations, audits, model capabilities, limitations, prohibited uses, or governance processes.

#### H1. `H1_RELEASE_NOTES_OR_CHANGELOG`

Specific examples:

- release note announcing a safety, youth, privacy, crisis, memory, or mental-health-relevant change;
- changelog entry documenting a new guardrail, filter, or user control;
- product update with clear implications for adolescent AI mental-health use or safety;
- timestamped version history for relevant features.

#### H2. `H2_MODEL_CARD_OR_SYSTEM_CARD`

Specific examples:

- model card or system card describing safety evaluations, limitations, red-team results, or deployment safeguards;
- documents handling of self-harm, medical advice, minors, privacy, or harmful content;
- updates model intended-use or prohibited-use statements;
- reports improvements or regressions in safety behavior.

#### H3. `H3_SAFETY_REPORT_OR_TRANSPARENCY_REPORT`

Specific examples:

- public safety report or transparency report with metrics relevant to minors, self-harm, mental health, harmful content, or enforcement;
- reports content moderation volumes, safety interventions, child-safety actions, crisis referrals, or policy violations;
- describes safety operations, human review, incident response, or escalation procedures.

#### H4. `H4_RED_TEAMING_OR_INDEPENDENT_EVALUATION`

Specific examples:

- reports red-team testing for self-harm, youth safety, mental health, abuse, or dangerous advice;
- describes independent audits or external evaluations;
- reports adversarial testing results or mitigation steps;
- documents safety benchmark performance.

#### H5. `H5_POLICY_VERSIONING_OR_DOCUMENTED_GOVERNANCE_PROCESS`

Specific examples:

- publishes versioned usage policies, safety policies, model behavior specs, or privacy terms;
- documents governance boards, safety review processes, or deployment controls;
- changes the process for evaluating or approving safety-relevant product updates.

---

### Category I. `I_PRODUCT_MODEL_INTEGRATION_EVENTS` — Product, Model, Modality, and Integration Events

Use this category for product/model changes that may affect adolescent exposure, intensity, dependency, realism, or access to AI chatbot support, even if the change is not explicitly framed as safety policy.

#### I1. `I1_NEW_MODEL_RELEASE_OR_MODEL_REPLACEMENT`

Specific examples:

- releases a new default model for a chatbot;
- replaces or rolls back a model used by consumers;
- changes model routing or default model selection;
- changes safety-relevant model behavior, even if described as a model upgrade;
- affects platforms named in the survey exposure list.

#### I2. `I2_VOICE_VIDEO_OR_MULTIMODAL_ROLLOUT`

Specific examples:

- launches or changes voice mode, video mode, image understanding, screen sharing, or multimodal interaction;
- changes emotional realism, immediacy, or perceived social presence;
- creates new pathways for sensitive disclosures by minors;
- adds safety constraints for voice/video interactions.

#### I3. `I3_COMPANION_CHARACTER_OR_ROLEPLAY_MODE`

Specific examples:

- launches, removes, or changes companion mode, character mode, romantic mode, or roleplay mode;
- changes emotional intimacy, persistent persona, simulated empathy, or dependency-related features;
- changes safeguards for minors using companion or character interactions;
- changes whether therapy-like or crisis-support personas are allowed.

#### I4. `I4_SOCIAL_MEDIA_OR_MESSAGING_INTEGRATION`

Specific examples:

- embeds AI chatbot into social media, messaging, or youth-heavy platforms;
- changes visibility, sharing, discoverability, or social context of AI interactions;
- adds AI chat into group chats, DMs, feeds, search, or recommendation interfaces;
- changes teen exposure through social apps.

#### I5. `I5_API_OR_DEVELOPER_POLICY_CHANGE`

Specific examples:

- changes API policies for mental health, therapy, minors, companion bots, self-harm, or crisis use cases;
- restricts developers from building AI therapy or companion applications for minors;
- requires developer safety disclosures or crisis handling;
- changes moderation requirements for third-party AI apps.

#### I6. `I6_HEALTHCARE_EDUCATION_OR_ENTERPRISE_INTEGRATION`

Specific examples:

- integrates AI tools into EHRs, clinical workflows, school accounts, education products, or youth-serving enterprise environments;
- adds safeguards for school or healthcare deployments;
- changes access for providers, educators, or institutions;
- creates provider-facing AI tools relevant to adolescent counseling or documentation.

---

### Category J. `J_ACCESS_MARKET_APP_STORE_ACCOUNT` — Access, Market Availability, App-Store Metadata, and Account Rules

Use this category for changes in availability, age ratings, app-store metadata, geographic rollout, account restrictions, or consent rules that affect who can use a platform.

#### J1. `J1_APP_STORE_AGE_RATING_OR_METADATA`

Specific examples:

- changes app-store age rating;
- changes app-store content warnings, privacy labels, or mental-health disclaimers;
- adds/removes chatbot from youth-accessible app categories;
- changes app-store description of AI safety, therapy, companionship, or crisis support.

#### J2. `J2_GEOGRAPHIC_ROLLOUT_OR_RESTRICTION`

Specific examples:

- launches or withdraws a product in the U.S., specific states, or other regions;
- creates region-specific privacy, safety, or age policies;
- restricts access due to law, safety, privacy, or age requirements;
- changes availability relevant to U.S. adolescent respondents.

#### J3. `J3_ACCOUNT_ELIGIBILITY_OR_CONSENT_RULES`

Specific examples:

- changes account creation requirements;
- changes parental consent, school consent, or guardian approval requirements;
- changes rules for shared accounts, family accounts, or managed accounts;
- changes terms for minors or users under certain ages.

#### J4. `J4_FEATURE_ACCESS_RESTRICTION_OR_PERMISSIONING`

Specific examples:

- restricts specific features for minors, free users, paid users, school accounts, or regions;
- changes access to memory, voice, image, companion, roleplay, or sensitive-topic features;
- adds permission gates before sensitive features;
- changes defaults for feature availability.

---

### Category K. `K_INCIDENT_RESPONSE_PRODUCT_CHANGE` — Incident Response, Public Controversy Response, and Required Product Changes

Use this category only when a public incident, investigation, litigation, or controversy is linked to a documented platform response or product/policy change. Do not code allegations alone as platform-governance events.

#### K1. `K1_SAFETY_INCIDENT_RESPONSE`

Specific examples:

- company announces product or policy changes after a self-harm, youth-safety, privacy, or mental-health safety incident;
- company publishes post-incident safety measures;
- company changes crisis, minor, companion, or content policies in response to documented harm.

#### K2. `K2_LITIGATION_SETTLEMENT_OR_REGULATORY_RESPONSE`

Specific examples:

- company changes product, safety, disclosure, privacy, or age policies after settlement, consent order, regulatory inquiry, or litigation;
- company announces compliance changes tied to a jurisdictional requirement;
- company publishes required safety documentation following enforcement.

#### K3. `K3_PUBLIC_CONTROVERSY_GOVERNANCE_CHANGE`

Specific examples:

- company responds to public concern about AI companions, teen safety, self-harm, sexual content, or dependency by changing policies or features;
- company publishes new safety commitments after media reports;
- company changes transparency, reporting, or parental-control commitments after public scrutiny.

---

### Category Z. `Z_NOT_RELEVANT_OR_EXCLUDED`

Use this category only in the `excluded_records` sheet.

Specific examples:

- retrieved record has no youth, mental-health, safety, privacy, crisis, companion, chatbot, provider, or survey-exposure relevance;
- source row is irrelevant to the project;
- duplicate record fully captured elsewhere;
- source cannot be interpreted because no text or summary is available;
- event is a generic performance, pricing, enterprise, or benchmark update with no relevant governance pathway.

---

## 6. Safety Relevance and Analytic Priority

### 6.1 `safety_relevance_score`

Claude must assign one score:

| Score | Meaning |
|---:|---|
| `3` | Directly changes or documents youth access, teen protections, self-harm/crisis handling, harmful-content refusals, mental-health advice boundaries, parental controls, memory/privacy defaults, or safety reporting for a named AI chatbot platform |
| `2` | Changes or documents platform governance likely to affect adolescent use, privacy, safety, help-seeking, or provider perceptions, but not limited to mental health or minors |
| `1` | Broad platform, model, privacy, product, or transparency change with only indirect relevance |
| `0` | Not relevant; place in `excluded_records` unless needed for audit trail |

### 6.2 `analytic_priority`

Claude must assign one analytic priority:

| Priority | Use when |
|---|---|
| `high_confirmatory` | Major safety-relevant event with clear platform, timing, affected user group, and plausible mapping to survey exposure by primary/any/frequency-weighted platform use |
| `medium_secondary` | Relevant privacy, memory, transparency, model, youth, or product-governance event with plausible mechanism but weaker timing, targeting, or exposure mapping |
| `covariate_context` | Broad product, model, market, transparency, app-store, or governance context likely useful for interpretation rather than primary exposure |
| `low_descriptive` | Baseline snapshot, ambiguous update, weakly relevant event, or hard-to-time record useful mainly for descriptive tracking |
| `exclude` | No meaningful pathway to study outcomes |

### 6.3 Major event rule

Classify an event as `major_safety_relevant_event` when all three conditions hold:

1. the event is publicly documented by the platform/operator or a source the human operator asked Claude to track;
2. the event changes, introduces, removes, or materially documents a governance feature in the taxonomy;
3. the event has a plausible pathway to adolescent AI use, safety, privacy, crisis handling, help-seeking, or provider response.

Examples likely to be major:

- new teen mode or teen default safety experience;
- new age verification or age-prediction system;
- new parental controls for AI features;
- change to self-harm/988 routing;
- change to mental-health advice boundaries;
- change to memory defaults or training opt-out for minors;
- publication of a system card documenting self-harm or youth-safety evaluations for a newly deployed model;
- release of a companion/roleplay feature with youth-safety implications.

Examples likely to be minor/contextual:

- UI wording change with no meaningful safety or privacy effect;
- general model performance update with no safety documentation;
- app redesign unrelated to youth, mental health, privacy, crisis, or harmful content;
- enterprise-only feature with no adolescent, provider, school, or health relevance.

---

## 7. Classification Rules Claude Must Follow

### 7.1 Use exact source evidence

Every included record must have `relevant_quote`. The quote should be short but specific enough to justify classification.

Bad quote:

```text
We improved safety.
```

Good quote:

```text
Teen accounts will receive additional safeguards, including stricter content protections and prompts to contact emergency services during self-harm conversations.
```

### 7.2 Multi-label but one primary category

Every included record must have exactly one `primary_category_code` and one `primary_subcategory_code`. Secondary categories may be added in `all_category_codes` and `all_subcategory_codes`.

Example:

A platform announces a teen mode that turns memory off by default and adds stronger self-harm routing to 988. Code as:

```text
primary_category_code = B_TEEN_MODE_YOUTH_SAFETY_DEFAULTS
primary_subcategory_code = B2_REDUCED_PERSONALIZATION_OR_MEMORY_FOR_MINORS
all_category_codes = B_TEEN_MODE_YOUTH_SAFETY_DEFAULTS|D_SELF_HARM_CRISIS_HANDLING|G_PRIVACY_MEMORY_RETENTION_TRAINING
all_subcategory_codes = B2_REDUCED_PERSONALIZATION_OR_MEMORY_FOR_MINORS|D1_988_OR_CRISIS_RESOURCE_ROUTING|G2_MEMORY_CONTROLS
```

### 7.3 Distinguish event records from baseline snapshots

If a source documents a new or changed policy with a date, create an event record.

If a source only documents the current policy and no change date is available, create a `baseline_policy_snapshot` only if the policy is important to the study. Otherwise, exclude or place in `low_descriptive`.

### 7.4 Do not treat every release note as an analytic event

Release notes are candidate sources, not automatically events. A release note should become a platform event only if it changes or documents a taxonomy-relevant governance feature.

### 7.5 Do not use news articles as canonical platform evidence unless instructed

News articles, lawsuits, user anecdotes, Reddit posts, social media threads, and advocacy reports may be useful discovery sources only if the human operator includes them. They should not be treated as canonical platform-governance events unless they point to an official company page or the record is explicitly coded as `human_review_needed = TRUE`.

### 7.6 Mark human review when ambiguity matters

Set `human_review_needed = TRUE` if any of the following are true:

- no official source URL found;
- event date or rollout date missing or ambiguous;
- platform/product affected is unclear;
- source text does not clearly state whether minors, teens, or all users are affected;
- category assignment is uncertain;
- documentation describes a feature but not whether it is default or optional;
- platform announced a change but implementation status is unclear;
- source scraping was incomplete;
- duplicate reconciliation is uncertain;
- event is potentially major but `classification_confidence = low` or `date_confidence = low`.

---

## 8. Required Output Workbook

Claude must write an Excel workbook named:

```text
platform_governance_events_output_YYYYMMDD.xlsx
```

The workbook must contain these sheets.

### 8.1 Sheet: `platform_events`

Contains one row per deduplicated included platform-governance event or baseline policy snapshot using the fields in Section 4.1.

### 8.2 Sheet: `category_assignments`

Long-format category table. One row per event-category-subcategory assignment.

Required columns:

| Column | Description |
|---|---|
| `event_id` | Links to `platform_events.event_id` |
| `category_code` | Category code from Section 5 |
| `subcategory_code` | Subcategory code from Section 5 |
| `is_primary` | `TRUE` or `FALSE` |
| `classification_confidence` | `high`, `medium`, `low` |
| `supporting_quote` | Short quote supporting this category |

### 8.3 Sheet: `raw_document_index`

Index of all raw or intermediate source documents retrieved.

Required columns:

| Column | Description |
|---|---|
| `raw_doc_id` | Unique ID for raw document |
| `event_id` | Link to platform event when known |
| `source_name` | Source name |
| `source_url` | Source URL |
| `company` | Company/operator if known |
| `platform` | Platform/product if known |
| `retrieved_at` | Timestamp |
| `content_type` | `html`, `pdf`, `json`, `csv`, `xlsx`, `text`, `app_store_metadata`, `unknown` |
| `local_path` | Path where raw file/text was saved, if applicable |
| `text_hash` | Hash for change detection |
| `retrieval_status` | `success`, `partial`, `failed` |

### 8.4 Sheet: `current_policy_snapshots`

Contains current baseline governance states observed during the run. This sheet supports later change detection and is especially important on the first run.

Required columns:

| Column | Description |
|---|---|
| `snapshot_id` | Unique ID |
| `company` | Company/operator |
| `platform` | Platform/product |
| `source_name` | Source name |
| `source_url` | Source URL |
| `snapshot_date` | Retrieval date or policy effective date |
| `governance_domain` | Main taxonomy category/subcategory |
| `current_setting_summary` | Short neutral summary of current policy or feature |
| `source_quote` | Short quote supporting the snapshot |
| `text_hash` | Hash for change detection |
| `human_review_needed` | `TRUE` or `FALSE` |

### 8.5 Sheet: `excluded_records`

Records retrieved but excluded as irrelevant, duplicate, or unusable.

Required columns:

| Column | Description |
|---|---|
| `excluded_id` | Unique ID |
| `source_name` | Source name |
| `source_url` | Source URL |
| `company` | Company/operator if known |
| `platform` | Platform/product if known |
| `title` | Title or best available label |
| `reason_excluded` | Short reason |
| `candidate_category` | Best guess category, if any |
| `human_review_needed` | `TRUE` or `FALSE` |

### 8.6 Sheet: `source_run_log`

One row per source attempted.

Required columns:

| Column | Description |
|---|---|
| `run_id` | Run ID |
| `source_name` | Source name |
| `source_url` | Source URL |
| `company_hint` | Company hint from input source workbook, if present |
| `platform_hint` | Platform hint from input source workbook, if present |
| `started_at` | Timestamp |
| `finished_at` | Timestamp |
| `status` | `success`, `partial`, `failed`, `skipped` |
| `records_found` | Number of candidate records found |
| `records_included` | Number included in `platform_events` |
| `records_excluded` | Number placed in `excluded_records` |
| `snapshots_created` | Number placed in `current_policy_snapshots` |
| `error_message` | Error text if failed or partial |

### 8.7 Sheet: `review_queue`

Subset of events needing human review.

Required columns:

| Column | Description |
|---|---|
| `event_id` | Link to platform event |
| `review_reason` | Why human review is needed |
| `suggested_question_for_reviewer` | Specific question, e.g., `Confirm rollout date`, `Confirm whether teens are affected`, `Confirm whether default setting changed`, `Confirm major vs minor event` |
| `priority` | `high`, `medium`, `low` |
| `source_url` | URL reviewer should inspect first |

---

## 9. Recommended Source Types

The operational list of sources comes from `input_sources.xlsx`. Claude must not assume that every source below is available unless listed in the workbook. This section tells Claude what kinds of sources are likely to appear and how to treat them.

### 9.1 Official platform sources

Examples:

- release notes and changelogs;
- company blogs and safety announcements;
- safety centers and help-center pages;
- usage policies, model behavior specs, and developer policies;
- privacy policies, terms of service, data processing pages;
- model cards, system cards, safety reports, transparency reports;
- parent, teen, education, or family-center documentation.

Use official platform sources as canonical whenever possible.

### 9.2 App-store and distribution sources

Examples:

- Apple App Store pages;
- Google Play pages;
- browser extension stores;
- platform age ratings and privacy labels.

Use app-store sources to track age ratings, availability, app descriptions, privacy labels, and youth access metadata. Mark `human_review_needed = TRUE` if app-store metadata conflicts with official platform pages.

### 9.3 Archived and versioned sources

Examples:

- web archives supplied by the human operator;
- versioned privacy-policy archives;
- GitHub repositories or documentation version histories;
- prior raw document snapshots from this scraper.

Use archived/versioned sources to detect changes over time. Do not rely on a web archive alone if a current official source is available, but retain archives for date and diff evidence.

### 9.4 Third-party discovery or context sources

Examples:

- reputable news articles;
- academic audits;
- civil-society reports;
- legal filings;
- app intelligence databases;
- public incident reports.

Use these only when listed in `input_sources.xlsx`. Treat them as discovery/context unless they contain or link to an official platform change. Mark events from these sources as `human_review_needed = TRUE` unless the source is explicitly approved by the human operator as canonical.

---

## 10. Scraping, Parsing, and Change-Detection Requirements

### 10.1 Raw document preservation

Claude must save or index raw documents whenever possible. At minimum, Claude must retain:

- source URL;
- retrieval timestamp;
- content type;
- text hash;
- local path or retrieval note.

Do not overwrite old raw files. Each run should preserve enough information to reconstruct what was seen during that run.

### 10.2 Text extraction

Claude should extract text from HTML, JSON, CSV/XLSX, PDF, app-store metadata, and plain text when possible. If PDF extraction fails, log the failure and retain the PDF URL. Do not hallucinate PDF content.

### 10.3 Linked documents

If a source page lists multiple relevant documents and links to official detail pages on the same domain or clearly official domains, Claude should follow those links. Do not crawl the open web indiscriminately.

### 10.4 Deduplication

Deduplicate using combinations of:

- company;
- platform;
- product or surface;
- event title;
- event date/date basis;
- official URL;
- document version;
- text hash;
- normalized summary.

When duplicate sources disagree, prefer official platform documentation over third-party summaries. Keep secondary URLs in `supporting_source_urls`.

### 10.5 Change detection

If a previously retrieved source has a changed `text_hash`, Claude must treat this as a potentially meaningful update and flag it in the run report. Claude should then compare old and new text, if available, and create a new event only if the change affects a taxonomy-relevant governance feature.

Do not create a new platform event for trivial changes such as formatting, typo fixes, navigation changes, cookie banners, or unrelated marketing copy.

### 10.6 Baseline versus change events

On a first run, many sources will yield baseline snapshots rather than historical change events. Claude should not pretend that baseline snapshots are dated events. Use `baseline_policy_snapshot`, set `date_basis = retrieval_date` when necessary, and mark `human_review_needed = TRUE` if the baseline is likely important for analysis but lacks a historical effective date.

---

## 11. Quality-Control Rules

Claude must apply the following QC checks before final export:

1. Every row in `platform_events` has `event_id`, `source_name`, `source_url`, `company`, `platform`, `event_title`, `event_summary`, `event_importance`, `event_type`, `date_basis`, `date_confidence`, `primary_category_code`, `primary_subcategory_code`, `safety_relevance_score`, `analytic_priority`, `mechanism_summary`, `survey_exposure_mapping`, `relevant_quote`, `classification_confidence`, and `human_review_needed`.
2. Every `primary_category_code` and `primary_subcategory_code` exactly matches a taxonomy code in Section 5.
3. Every date is either blank/unknown or ISO formatted as `YYYY-MM-DD`.
4. Every included event has at least one source URL.
5. Every row with `classification_confidence = low` has `human_review_needed = TRUE`.
6. Every row with missing or ambiguous event date has `human_review_needed = TRUE` unless it is clearly marked `baseline_policy_snapshot`.
7. Every row with `event_importance = major_safety_relevant_event` has `safety_relevance_score` of `2` or `3`.
8. Every row with `analytic_priority = high_confirmatory` has non-missing `company`, `platform`, `date_basis`, `mechanism_summary`, and `survey_exposure_mapping`.
9. Every row in `review_queue` corresponds to a row in `platform_events`.
10. The output workbook must be created even if no relevant events are found. In that case, `source_run_log` and `excluded_records` must explain what happened.

---

## 12. Human-Review Philosophy

The scraper/classifier is not the authority on platform behavior. It is an evidence-gathering and first-pass classification system.

Claude should be aggressive in retrieving and organizing candidate material, but conservative in final claims. Ambiguity should be surfaced, not hidden.

Human reviewers should be able to answer:

- What platform/product changed?
- What exactly changed: policy, product, model, default setting, user control, disclosure, safety behavior, or transparency documentation?
- When did the change become effective or publicly documented?
- Which users were affected: all users, minors, teens, parents, providers, developers, enterprise/education users, or unknown?
- Why is it relevant to adolescent AI chatbot mental health use, safety, privacy, help-seeking, or provider response?
- Which survey respondents could be treated or exposed: primary platform users, any platform users, frequency-weighted users, all users nationally, or no clear mapping?
- Is it suitable for confirmatory analysis, secondary analysis, covariate/context adjustment, or descriptive tracking only?

---

## 13. Run Report Requirements

The markdown run report must include:

1. run date and run ID;
2. number of sources listed in `input_sources.xlsx`;
3. number of sources attempted, successful, partially successful, failed, and skipped;
4. number of candidate records retrieved;
5. number of events included in `platform_events`;
6. number of baseline snapshots created;
7. number of excluded records;
8. number of records needing human review;
9. list of `major_safety_relevant_event` records;
10. list of `high_confirmatory` records;
11. list of sources that failed and why;
12. notes on duplicate reconciliation and source conflicts;
13. notes on changed text hashes from prior runs, if available;
14. recommended next steps for human review.

---

## 14. Non-Negotiable Rules

Claude must follow these rules:

1. Do not invent platform behavior, internal policies, dates, rollout status, affected users, or safety effects.
2. Do not treat a marketing statement as a verified safety feature unless the source documents the relevant feature or policy.
3. Do not treat baseline snapshots as historical events unless a date is available.
4. Do not classify a general model release as safety-relevant unless the documentation supports that pathway.
5. Do not silently drop candidate records that appear relevant but are incomplete; place them in the review queue.
6. Do not bypass scraping restrictions, authentication, paywalls, CAPTCHAs, private APIs, or anti-bot systems.
7. Do not collect or store personal data from users, adolescents, patients, private chat logs, forums, or social media anecdotes.
8. Do not overwrite previous raw files or outputs without versioning.
9. Do not add uncontrolled new category names. Use the taxonomy codes in this constitution.
10. Do not proceed without generating an output workbook and run report.

---

## 15. Minimal Success Criteria

A run is successful if, at minimum:

1. `input_sources.xlsx` was read;
2. every enabled source was attempted or explicitly skipped with a reason;
3. candidate platform-governance records were extracted where available;
4. included records were classified according to Section 5;
5. baseline current-policy snapshots were created when relevant;
6. `platform_governance_events_output_YYYYMMDD.xlsx` was created with all required sheets;
7. `platform_governance_events_run_report_YYYYMMDD.md` was created;
8. events requiring human judgment were placed in `review_queue`.
