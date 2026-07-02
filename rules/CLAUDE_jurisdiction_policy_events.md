# CLAUDE.md — Constitution for Jurisdiction-Level Legal and Policy Event Scraping

## 0. Purpose of This Constitution

This file is the governing instruction set for Claude Code/Codex-style agents that scrape, normalize, classify, and export jurisdiction-level legal and policy events relevant to adolescent use of AI chatbots for mental health needs.

This constitution covers **jurisdiction-level legal and policy events only**: federal, state, county, municipal, school-district, agency, regulatory, professional-board, and enforcement actions. It does **not** cover company/platform governance events such as OpenAI, Anthropic, Google, Meta, Snapchat, xAI, Replika, Wysa, or Youper product changes. Platform governance will be governed by a separate constitution.

Claude must read this file at the beginning of every run and treat it as the source of truth for scope, fields, taxonomy, workflow, classification rules, and output requirements.

---

## 1. Overarching Objective

The objective is to build a reproducible, periodically updated inventory of legal and policy events that may directly or indirectly affect:

1. adolescent use of AI chatbots for mental health support;
2. adolescent exposure to unsafe, misleading, privacy-invasive, or crisis-related AI chatbot interactions;
3. adolescent help-seeking after AI chatbot interactions, including disclosure to caregivers/clinicians, contacting 988, scheduling care, or seeking formal mental health services;
4. provider engagement with adolescent AI chatbot use, including screening, documentation, counseling, referral, and risk management;
5. payer, facility, school, or public-sector adoption of AI tools that may alter adolescent mental health care or AI-related counseling.

The final product is an analyzable, versioned dataset suitable for longitudinal and quasi-experimental analyses, including state-year, county-year, and event-time analyses where treatment timing and geographic variation permit.

The central analytic principle is: **capture law/policy events with enough structure to link them to survey waves, jurisdictions, populations, mechanisms, and outcomes, without creating an impossible scraping burden.**

---

## 2. Operational Workflow

Claude must follow this workflow exactly unless the human operator explicitly changes it.

### Step 1. Read this constitution

At the beginning of each run, Claude must read `CLAUDE.md` or this constitution file and confirm internally that the task is limited to jurisdiction-level legal and policy events.

### Step 2. Read the input source workbook

Claude must look for an Excel workbook named:

```text
input_sources.xlsx
```

The workbook should contain a sheet named `sources`. If no sheet name is specified or detectable, Claude should use the first worksheet.

The workbook must contain at least these two columns:

| Required column | Meaning |
|---|---|
| `source_name` | Human-readable name of the source, e.g., `NCSL AI Legislation Database`, `Manatt Health AI Policy Tracker`, `California Legislature`, `Municode` |
| `source_url` | URL to scrape, query, download, or use as the starting point for source discovery |

The workbook may also contain these optional columns. Claude should use them when present but must not require them:

| Optional column | Meaning |
|---|---|
| `enabled` | If present and equal to `FALSE`, `0`, or `no`, skip this source |
| `source_tier` | `official`, `tracker`, `local_code`, `agency`, `professional_board`, `enforcement`, `other` |
| `jurisdiction_level_hint` | `federal`, `state`, `county`, `municipal`, `school_district`, `agency`, `professional_board`, `other` |
| `jurisdiction_hint` | Name of state, county, municipality, agency, or board when known |
| `source_type_hint` | `api`, `html`, `pdf`, `spreadsheet`, `legislative_tracker`, `code_library`, `agenda_system`, `unknown` |
| `notes` | Free-text instructions from the human operator |

If only `source_name` and `source_url` are present, Claude must still proceed.

### Step 3. Scrape or query each listed source

For every enabled row in `input_sources.xlsx`, Claude must attempt to retrieve candidate legal/policy records.

Claude should prefer, in order:

1. official API endpoint, if available;
2. official structured HTML;
3. official downloadable CSV/XLSX/JSON;
4. official PDF or document text;
5. reputable tracker page;
6. local code or agenda platform;
7. manually parsable HTML.

Claude must not bypass paywalls, authentication, robots restrictions, or anti-scraping mechanisms. If a source cannot be scraped reliably, Claude must log the failure in the output workbook and continue with the next source.

### Step 4. Extract candidate records

A candidate record may be any of the following:

- bill;
- enacted law;
- statute;
- ordinance;
- regulation;
- proposed rule;
- final rule;
- executive order;
- agency guidance;
- professional board guidance;
- attorney general advisory;
- enforcement action;
- consent decree;
- school board policy;
- county or municipal AI governance policy;
- public-sector procurement rule.

Claude must extract both metadata and text when possible. If full text is not available, Claude must extract the best available summary and source URL, then mark `human_review_needed = TRUE`.

### Step 5. Normalize, deduplicate, and classify

Claude must normalize records into the data model in Section 4 and classify them using the taxonomy in Section 5.

Claude must deduplicate records across sources. For example, the same state bill may appear in NCSL, Manatt, Beeck, LegiScan, and an official legislature site. The canonical record should prefer official bill/law text, while retaining secondary source URLs in `supporting_source_urls`.

### Step 6. Export the output workbook

Claude must generate an Excel workbook named:

```text
jurisdiction_policy_events_output_YYYYMMDD.xlsx
```

where `YYYYMMDD` is the run date.

The workbook must include the required sheets described in Section 8.

### Step 7. Generate a run report

Claude must generate a short markdown run report named:

```text
jurisdiction_policy_events_run_report_YYYYMMDD.md
```

The report must summarize sources attempted, sources failed, records extracted, records included, records excluded, high-priority records, and human-review issues.

---

## 3. Scope Rules

### 3.1 Include records when they plausibly affect adolescent AI chatbot mental health use or provider response

Include a record if it concerns at least one of the following:

- AI chatbots, AI companions, generative AI, automated decision systems, or digital agents;
- AI in mental health, behavioral health, therapy, counseling, psychotherapy, diagnosis, treatment, screening, triage, or crisis support;
- minors, youth, adolescents, children, students, or age-appropriate AI/data design;
- privacy or health data rules plausibly affecting AI chatbot conversations, mental health data, sensitive data, or minors’ data;
- AI transparency, disclosure, labeling, auditing, risk management, incident reporting, or human review;
- reimbursement, Medicaid, payer coverage, utilization management, or clinical workflow involving AI in behavioral health or health care;
- deceptive, unsafe, or unsupported AI health claims;
- school, county, or municipal policies governing youth-facing AI tools, AI access, or AI procurement;
- 988, suicide prevention, crisis routing, mobile crisis, or digital crisis infrastructure relevant to AI referral pathways.

### 3.2 Exclude records with no plausible pathway

Exclude records if they are about AI but have no meaningful youth, health, behavioral-health, privacy, safety, consumer-protection, crisis, public-sector, school, or provider pathway.

Examples likely to exclude:

- AI tax credits unrelated to health, minors, privacy, safety, or consumer protection;
- AI workforce training programs with no health, youth, education, or public-sector service link;
- AI procurement rules limited to transportation, agriculture, energy, or defense with no health/youth relevance;
- general technology modernization bills with no AI, automated decision, privacy, or youth relevance.

Excluded records should be placed in the `excluded_records` sheet, not silently discarded, if they were retrieved as candidate records.

### 3.3 Do not invent missing facts

If a date, status, citation, jurisdiction, or applicability flag is not available, Claude must use `unknown`, not guess. If a date is inferred from context, Claude must set `date_confidence = low` and explain the inference in `human_review_reason`.

---

## 4. Parsimonious Analyzable Data Model

Claude should capture a **parsimonious core set of fields**. Do not create dozens of speculative variables. The goal is to support analysis, deduplication, and human review.

### 4.1 Required sheet: `policy_events`

One row per distinct legal/policy record after deduplication.

| Field | Required? | Description |
|---|---:|---|
| `record_id` | Yes | Stable unique ID generated from jurisdiction + instrument ID + session/year + normalized title or text hash |
| `run_id` | Yes | Run date/time or UUID |
| `retrieved_at` | Yes | Timestamp when Claude retrieved the source |
| `source_name` | Yes | Primary source name from `input_sources.xlsx` |
| `source_url` | Yes | Primary source URL from `input_sources.xlsx` or official record URL if reached from source |
| `supporting_source_urls` | No | Pipe-delimited list of additional URLs that mention the same record |
| `jurisdiction_level` | Yes | `federal`, `state`, `county`, `municipal`, `school_district`, `agency`, `professional_board`, `other`, `unknown` |
| `jurisdiction_name` | Yes | U.S., state name, county, city, agency, board, or district |
| `state` | No | Two-letter state abbreviation when applicable |
| `policy_instrument_type` | Yes | `bill`, `law`, `statute`, `ordinance`, `regulation`, `proposed_rule`, `final_rule`, `executive_order`, `guidance`, `board_policy`, `enforcement_action`, `consent_decree`, `procurement_policy`, `school_policy`, `other`, `unknown` |
| `bill_or_policy_id` | No | Bill number, act number, chapter number, ordinance number, docket number, rule ID, case number, or policy ID |
| `session_year` | No | Legislative or policy year/session, if available |
| `title` | Yes | Official or best available title |
| `short_summary` | Yes | 1–3 sentence neutral summary of the relevant provisions |
| `current_status` | Yes | `introduced`, `pending`, `passed_one_chamber`, `enacted_signed`, `enacted_unsigned`, `vetoed`, `failed`, `withdrawn`, `repealed`, `active_rule`, `proposed_rule`, `guidance`, `enforcement_action`, `unknown` |
| `latest_action` | No | Most recent official action text, if available |
| `latest_action_date` | No | Date of most recent action, ISO format `YYYY-MM-DD` |
| `enacted_date` | No | Date enacted/signed/adopted, if applicable |
| `effective_date` | No | Date provisions take effect, if available |
| `date_basis` | Yes | `effective_date`, `enacted_date`, `signed_date`, `latest_action_date`, `introduced_date`, `unknown` |
| `date_confidence` | Yes | `high`, `medium`, `low`, `unknown` |
| `primary_category_code` | Yes | One code from taxonomy in Section 5 |
| `primary_subcategory_code` | Yes | One subcategory code from taxonomy in Section 5 |
| `all_category_codes` | Yes | Pipe-delimited category codes; include primary and all secondary categories |
| `all_subcategory_codes` | Yes | Pipe-delimited subcategory codes |
| `directness_score` | Yes | `3`, `2`, `1`, or `0`; see Section 6 |
| `empirical_priority` | Yes | `high_confirmatory`, `medium_secondary`, `covariate_context`, `low_descriptive`, `exclude` |
| `applies_to_minors` | Yes | `TRUE`, `FALSE`, or `UNKNOWN` |
| `applies_to_healthcare` | Yes | `TRUE`, `FALSE`, or `UNKNOWN` |
| `applies_to_behavioral_health` | Yes | `TRUE`, `FALSE`, or `UNKNOWN` |
| `applies_to_consumer_chatbots` | Yes | `TRUE`, `FALSE`, or `UNKNOWN` |
| `applies_to_provider_behavior` | Yes | `TRUE`, `FALSE`, or `UNKNOWN` |
| `mechanism_summary` | Yes | Short statement of the hypothesized pathway to adolescent AI use, safety, help-seeking, privacy, or provider response |
| `relevant_quote` | Yes | Short excerpt from source text supporting classification; keep under 500 characters |
| `quote_location` | No | Section, page, line, bill section, or URL fragment if available |
| `text_hash` | No | Hash of retrieved text for change detection |
| `classification_confidence` | Yes | `high`, `medium`, `low` |
| `human_review_needed` | Yes | `TRUE` or `FALSE` |
| `human_review_reason` | No | Required when `human_review_needed = TRUE` |

### 4.2 Date priority rule

For analysis, the preferred treatment date is the first clearly applicable date in this order:

1. `effective_date`;
2. compliance or enforcement start date, if different and clearly specified;
3. enacted/signed/adopted date;
4. chapter law/public act date;
5. latest action date for pending bills;
6. introduced date if no other date exists.

Claude must record which date was used in `date_basis`. Do not use introduced dates as treatment dates for enacted-policy analyses unless no better date exists and the row is clearly marked for review.

---

## 5. Policy Taxonomy

Claude must classify every included record into at least one primary category and one primary subcategory. Multiple secondary categories/subcategories are allowed and should be recorded in `all_category_codes` and `all_subcategory_codes`.

When a record spans multiple categories, choose the primary category based on the **most direct mechanism** linking the record to adolescent AI chatbot mental health use, safety, help-seeking, privacy, or provider engagement.

### Category A. `A_DIRECT_AI_MH_SCOPE` — Direct AI Mental Health / Behavioral Health Scope-of-Use Laws

Use this category for laws or policies that directly regulate AI use in mental health, behavioral health, therapy, counseling, diagnosis, treatment, or clinical mental health decision-making.

#### A1. `A1_AI_THERAPY_PSYCHOTHERAPY_PROHIBITION`

Classify here if the record prohibits or limits AI from acting as a therapist, psychotherapist, counselor, or mental health provider.

Specific examples:

- bans AI from providing therapy, psychotherapy, counseling, or therapeutic communication;
- prohibits AI from directly interacting with patients or clients in a therapeutic capacity;
- prohibits AI from generating therapeutic recommendations or treatment plans without licensed clinician review;
- restricts AI from simulating or impersonating a licensed mental health professional;
- states that AI cannot replace a licensed mental health professional.

#### A2. `A2_DIAGNOSIS_TREATMENT_CLINICAL_DECISION_RESTRICTION`

Classify here if the record restricts AI diagnosis, treatment decisions, clinical recommendations, or clinical decision support.

Specific examples:

- AI cannot independently diagnose a mental health or behavioral health condition;
- AI cannot independently recommend medication, therapy, hospitalization, or discharge;
- AI cannot be the sole basis for treatment modification, denial, discharge, or escalation;
- a licensed clinician must make the final clinical decision;
- AI-generated clinical recommendations require human review, approval, or documentation.

#### A3. `A3_MENTAL_HEALTH_CHATBOT_DEFINITION`

Classify here if the record creates or uses a legal definition directly relevant to AI mental health tools.

Specific examples:

- defines `mental health chatbot`, `behavioral health chatbot`, `AI therapist`, `AI counselor`, `synthetic therapist`, `digital therapeutic`, `automated mental health tool`, or similar term;
- defines AI systems used for mental health screening, diagnosis, treatment, counseling, or crisis support;
- distinguishes AI companions from clinical AI or digital therapeutics.

#### A4. `A4_HUMAN_OVERSIGHT_FOR_AI_MH`

Classify here if the record requires human oversight specifically for AI used in mental or behavioral health.

Specific examples:

- licensed clinician review before AI advice is delivered or acted upon;
- named accountable provider for AI-supported mental health services;
- human-in-the-loop review for AI-generated screening, triage, risk scoring, or treatment recommendations;
- required supervision of AI tools by licensed behavioral health staff;
- documentation that AI output was reviewed by a human clinician.

#### A5. `A5_AI_MH_CRISIS_HANDLING_REQUIREMENT`

Classify here if the record requires crisis, self-harm, suicide, abuse, or emergency protocols for AI mental health systems.

Specific examples:

- requires suicide-risk detection or escalation protocols;
- requires referral to 988, 911, mobile crisis, emergency services, or a licensed professional;
- requires AI tools to display crisis resources when self-harm or suicide is detected;
- requires disclaimers that the AI tool is not a crisis service;
- mandates safety testing for self-harm, suicide, eating disorder, abuse, or violence prompts.

#### A6. `A6_UNAUTHORIZED_PRACTICE_OR_LICENSURE`

Classify here if the record treats AI use as potentially implicating professional licensure or unauthorized practice.

Specific examples:

- states that AI cannot practice psychology, psychiatry, social work, counseling, marriage/family therapy, or behavioral health care;
- prohibits licensees from delegating professional judgment to AI;
- creates disciplinary consequences for improper AI use in patient care;
- board guidance on clinician responsibility when using AI in mental health care.

---

### Category B. `B_YOUTH_COMPANION_CHATBOT_SAFETY` — Youth-Specific AI Companion / Chatbot Safety Laws

Use this category for laws or policies that regulate AI companions, AI chatbots, social chatbots, or generative AI systems used by minors, especially when emotional support, dependency, self-harm, sexual content, or youth safety is addressed.

#### B1. `B1_COMPANION_CHATBOT_SAFETY_PROTOCOLS`

Specific examples:

- requires companion chatbot operators to implement self-harm or suicide-prevention protocols;
- requires safety-by-design protections for minors using AI companions;
- requires mitigation of emotional dependency, manipulation, or overattachment;
- requires crisis-resource presentation during high-risk interactions;
- requires the platform to detect or respond to discussions of self-harm, suicide, abuse, or exploitation.

#### B2. `B2_REQUIRED_AI_CHATBOT_DISCLOSURES_TO_MINORS`

Specific examples:

- requires disclosure that the user is interacting with AI rather than a human;
- requires disclosure that the chatbot is not a licensed therapist or clinician;
- requires disclosure that chatbot advice is not medical, mental health, or emergency advice;
- requires age-appropriate disclosures for minors;
- requires recurring or prominent disclosures, not merely buried terms of service.

#### B3. `B3_MINOR_DESIGN_RESTRICTIONS`

Specific examples:

- prohibits sexualized, romantic, coercive, or exploitative AI interactions with minors;
- restricts deceptive anthropomorphism or simulated intimacy with minors;
- prohibits AI from encouraging minors to conceal use from parents, caregivers, clinicians, or authorities;
- restricts persuasive design, dark patterns, addictive engagement loops, or manipulative nudges targeting minors;
- limits personalized emotional dependency features for minor users.

#### B4. `B4_USE_INTENSITY_DEPENDENCY_CONTROLS`

Specific examples:

- requires time-spent notifications;
- requires break reminders;
- restricts nighttime use by minors;
- requires alerts for prolonged, intense, or emotionally dependent engagement;
- creates safeguards for repeated or compulsive use.

#### B5. `B5_PARENTAL_CONTROLS_AND_MINOR_OVERSIGHT`

Specific examples:

- requires parental controls for AI chatbot or companion use;
- requires parent dashboards or account-level oversight;
- allows parents to disable or restrict AI chatbot features;
- provides caregiver visibility into AI use metadata;
- requires minor-user protections linked to family accounts or supervised accounts.

#### B6. `B6_YOUTH_AI_SAFETY_REPORTING`

Specific examples:

- requires annual public reports on AI companion or youth chatbot safety;
- requires disclosure of self-harm incidents, crisis interventions, or child-safety failures;
- requires reports to attorneys general, health departments, education departments, or consumer protection agencies;
- requires publication of safety protocols or risk assessments for youth-facing AI.

---

### Category C. `C_PRIVACY_HEALTH_YOUTH_DATA` — Privacy, Health Data, and Youth Data Protection

Use this category for privacy or data-protection laws that may affect AI chatbot use, especially when mental health, sensitive data, minors, model training, retention, or third-party sharing are implicated.

#### C1. `C1_COMPREHENSIVE_STATE_PRIVACY`

Specific examples:

- creates access, deletion, correction, portability, or opt-out rights;
- restricts processing of sensitive personal data;
- requires consent for sensitive data processing;
- establishes data minimization or purpose limitation;
- applies to profiling, automated decision-making, or targeted advertising.

#### C2. `C2_CONSUMER_HEALTH_DATA_PRIVACY`

Specific examples:

- regulates consumer-generated health data outside HIPAA;
- treats mental health information, therapy information, emotional state, crisis information, or health inferences as sensitive data;
- restricts sale or sharing of consumer health data;
- regulates health-data geofencing;
- requires consent before collecting or sharing health-related chatbot data.

#### C3. `C3_CHILDREN_MINOR_DATA_PRIVACY`

Specific examples:

- creates special privacy protections for children, teens, minors, students, or users under 13, 16, or 18;
- restricts profiling or targeted advertising to minors;
- requires age-appropriate privacy design;
- requires parental consent or youth-specific notices;
- limits collection, retention, or sharing of minors’ data.

#### C4. `C4_AI_MODEL_TRAINING_DATA_RESTRICTIONS`

Specific examples:

- requires opt-out from AI model training;
- restricts use of minors’ data for AI training;
- restricts use of mental health or sensitive conversation data for model improvement;
- requires deletion or exclusion of user data from training corpora;
- requires clear disclosure of whether chat logs are used for model training.

#### C5. `C5_DATA_RETENTION_MEMORY_CONTROLS`

Specific examples:

- limits retention of chatbot logs or sensitive data;
- requires auto-delete defaults;
- requires memory controls or ability to delete memory;
- creates retention limits for minors’ data;
- requires special treatment of mental health, crisis, or sensitive conversations.

#### C6. `C6_THIRD_PARTY_SHARING_AND_DATA_BROKERS`

Specific examples:

- restricts sharing of sensitive, health, or minor data with third parties;
- requires vendor/subprocessor disclosure;
- restricts data broker sale of health or youth data;
- requires user consent for analytics, advertising, or cross-context behavioral advertising;
- creates opt-out rights from sale or sharing of personal data.

---

### Category D. `D_TRANSPARENCY_DISCLOSURE_LABELING` — Transparency, Disclosure, and Labeling

Use this category for laws requiring AI disclosure, labeling, explanation, notices, or public transparency, especially when related to health, youth, consumer interactions, or provider workflows.

#### D1. `D1_AI_IDENTITY_DISCLOSURE`

Specific examples:

- requires disclosure when a user is interacting with AI rather than a human;
- requires chatbot or automated-agent labeling;
- requires disclosure of synthetic or AI-generated communication;
- applies to consumer-facing chatbots, digital assistants, or virtual agents.

#### D2. `D2_HEALTH_AI_DISCLOSURE`

Specific examples:

- requires disclosure when AI is used in healthcare, behavioral health, diagnosis, treatment, triage, utilization management, or clinical documentation;
- requires clinicians or facilities to notify patients of AI involvement;
- requires explanation of AI’s role in a health-related decision;
- requires AI use to be documented in a medical or clinical record.

#### D3. `D3_CONSUMER_MENTAL_HEALTH_DISCLAIMER`

Specific examples:

- requires disclosure that chatbot content is not therapy, medical advice, diagnosis, treatment, or crisis support;
- requires instruction to seek professional help or emergency services for urgent concerns;
- requires limitation-of-use statements for mental health advice;
- requires age-appropriate warnings for youth users.

#### D4. `D4_PUBLIC_TRANSPARENCY_REPORTING`

Specific examples:

- requires public AI safety reports;
- requires publication of risk assessments, model cards, system cards, or impact assessments;
- requires reporting of child-safety measures, crisis-response metrics, or complaint data;
- requires disclosure of AI limitations, intended uses, prohibited uses, or known risks.

---

### Category E. `E_RISK_AUDIT_INCIDENT_REPORTING` — Risk Management, Safety Evaluation, Audits, and Incident Reporting

Use this category for legal or policy requirements involving AI risk assessments, audits, red-teaming, incident reporting, post-market monitoring, or high-risk AI governance.

#### E1. `E1_PREDEPLOYMENT_RISK_ASSESSMENT`

Specific examples:

- requires risk assessment before deployment of AI systems;
- requires impact assessment for high-risk or consequential AI;
- requires assessment of impacts on minors, patients, consumers, or protected groups;
- requires evaluation of safety, privacy, fairness, bias, explainability, or foreseeable misuse.

#### E2. `E2_INDEPENDENT_AUDIT_OR_REVIEW`

Specific examples:

- requires third-party audit of AI systems;
- requires annual audit or periodic reassessment;
- requires audit submission to a regulator;
- requires independent evaluation of AI accuracy, safety, bias, or performance.

#### E3. `E3_RED_TEAMING_AND_SAFETY_TESTING`

Specific examples:

- requires adversarial testing or red-teaming;
- requires testing for self-harm, suicide, eating disorders, abuse, violence, exploitation, or illegal content;
- requires youth-specific safety testing;
- requires documentation of safety testing methods and results.

#### E4. `E4_POSTMARKET_MONITORING_AND_INCIDENT_LOGS`

Specific examples:

- requires ongoing monitoring after deployment;
- requires incident logs, complaint mechanisms, or user safety-event tracking;
- requires correction of identified harms;
- requires monitoring of AI failures, unsafe outputs, discrimination, or privacy breaches.

#### E5. `E5_REGULATORY_INCIDENT_REPORTING`

Specific examples:

- requires reporting AI incidents to an attorney general, health department, insurance department, education department, professional board, or other regulator;
- requires reporting serious injury, self-harm, privacy breach, discrimination, or safety failure;
- establishes reporting deadlines or penalties for non-reporting.

---

### Category F. `F_HEALTHCARE_WORKFLOW_REIMBURSEMENT` — Healthcare Delivery, EHR, Payer, Reimbursement, and Clinical Workflow

Use this category for laws or policies governing AI in healthcare operations, utilization management, reimbursement, EHRs, clinical decision support, or facility-level governance.

#### F1. `F1_AI_UTILIZATION_MANAGEMENT_PRIOR_AUTHORIZATION`

Specific examples:

- prohibits AI from being the sole basis for denial, delay, or limitation of care;
- requires human review of AI-supported utilization management decisions;
- requires disclosure of AI use in prior authorization or payer decisions;
- creates appeal rights for AI-supported denials;
- applies to mental health parity, behavioral health services, or health insurance more generally.

#### F2. `F2_AI_SCREENING_OR_DIGITAL_THERAPEUTIC_REIMBURSEMENT`

Specific examples:

- creates Medicaid, commercial insurance, or public-program reimbursement for AI-supported screening;
- reimburses digital therapeutics, AI-supported behavioral health tools, or AI-assisted triage;
- funds AI-enabled school-based or primary-care mental health screening;
- creates payment parity or billing codes for AI-supported services.

#### F3. `F3_CLINICAL_DECISION_SUPPORT_TRANSPARENCY`

Specific examples:

- regulates AI-enabled clinical decision support in EHRs or certified health IT;
- requires source-data disclosure, explainability, or performance information;
- requires clinician override, review, or monitoring;
- applies to screening, diagnosis, treatment, triage, risk prediction, or documentation.

#### F4. `F4_FACILITY_AI_GOVERNANCE_TRAINING_SOP`

Specific examples:

- requires healthcare facilities to create AI governance committees;
- requires staff training on AI use, risks, privacy, or documentation;
- requires written SOPs for AI use in patient care;
- requires informed consent, patient notice, or audit trails;
- requires organizational oversight for behavioral health AI tools.

#### F5. `F5_PROFESSIONAL_LIABILITY_STANDARD_OF_CARE`

Specific examples:

- clarifies liability for clinicians, facilities, payers, or vendors using AI;
- states that AI use does not reduce professional responsibility;
- establishes malpractice, negligence, or standard-of-care expectations for AI-supported clinical decisions;
- addresses delegation of judgment to AI.

---

### Category G. `G_CONSUMER_PROTECTION_ENFORCEMENT` — Consumer Protection, Deceptive Claims, and Enforcement

Use this category for enforcement actions or legal requirements related to deceptive, unfair, unsupported, or unsafe AI claims or designs.

#### G1. `G1_DECEPTIVE_AI_MENTAL_HEALTH_CLAIMS`

Specific examples:

- prohibits unsupported claims that AI provides therapy, diagnosis, treatment, symptom reduction, or crisis support;
- targets misleading claims that an AI tool is clinically validated;
- targets claims that AI is equivalent or superior to licensed professional care;
- targets deceptive testimonials, fake reviews, or fabricated evidence for AI health tools.

#### G2. `G2_UNFAIR_OR_DECEPTIVE_AI_DESIGN`

Specific examples:

- addresses dark patterns, manipulative AI engagement, emotional exploitation, or deceptive anthropomorphism;
- addresses concealment of data practices;
- addresses failure to disclose material safety limitations;
- addresses AI systems that induce harmful reliance or delay needed care.

#### G3. `G3_AG_FTC_OR_AGENCY_ENFORCEMENT_ACTION`

Specific examples:

- attorney general investigation, settlement, complaint, or advisory involving AI health, youth, privacy, or chatbot harms;
- FTC or consumer-protection enforcement involving AI claims, AI privacy, or AI safety;
- state agency enforcement concerning AI tools in healthcare, schools, or youth-facing services.

#### G4. `G4_CONSENT_DECREE_OR_REQUIRED_PRODUCT_CHANGE`

Specific examples:

- consent decree requiring changes to AI disclosures, data practices, safety protocols, or marketing claims;
- settlement requiring deletion of data or algorithms;
- required safety, privacy, or monitoring changes after enforcement.

---

### Category H. `H_SCHOOLS_YOUTH_INSTITUTIONS` — Schools, Education Agencies, and Youth-Serving Institutions

Use this category for school, education, or youth-serving policies that govern AI chatbot access, student privacy, digital mental health tools, or school-based mental health AI.

#### H1. `H1_SCHOOL_AI_CHATBOT_ACCESS_POLICY`

Specific examples:

- bans, allows, restricts, or approves student use of AI chatbots;
- blocks or permits AI companions or generative AI tools on school devices or networks;
- creates acceptable-use rules for AI tools;
- restricts AI use by age, grade, account type, or parental consent.

#### H2. `H2_STUDENT_DATA_PRIVACY_AI`

Specific examples:

- regulates AI vendors handling student data;
- restricts sharing of student data with AI platforms;
- requires vendor agreements, privacy protections, or data deletion;
- addresses student mental health data or counseling records used in digital tools.

#### H3. `H3_SCHOOL_MENTAL_HEALTH_AI_TOOLS`

Specific examples:

- authorizes, funds, restricts, or regulates AI tools for school mental health screening, triage, counseling, or crisis detection;
- requires human review of AI-generated student risk alerts;
- regulates AI wellness or suicide-prevention platforms in schools.

#### H4. `H4_NETWORK_FILTERING_OR_MONITORING`

Specific examples:

- requires blocking AI companion platforms or certain chatbot functions;
- requires monitoring for self-harm or crisis terms;
- regulates alerts to school officials, parents, or law enforcement;
- addresses AI access on school-owned devices.

#### H5. `H5_YOUTH_SERVING_ORGANIZATION_AI_POLICY`

Specific examples:

- public library, youth center, juvenile justice, child welfare, or recreation agency policy on AI access;
- youth-service procurement policy for AI tools;
- restrictions on AI interaction with minors in public programs.

---

### Category I. `I_CRISIS_SYSTEM_INFRASTRUCTURE` — Crisis-System and Suicide-Prevention Infrastructure

Use this category mostly as contextual or covariate information unless the record directly requires AI systems to route users to crisis services.

#### I1. `I1_988_FUNDING_OR_GOVERNANCE`

Specific examples:

- creates or modifies 988 fees, appropriations, governance, or call-center funding;
- establishes a state 988 trust fund or oversight body;
- funds crisis line capacity relevant to AI crisis referrals.

#### I2. `I2_988_CAPACITY_PERFORMANCE_REPORTING`

Specific examples:

- requires reporting of 988 answer rates, abandonment, wait times, chat/text volume, or outcomes;
- creates public dashboards or performance standards for crisis lines.

#### I3. `I3_MOBILE_CRISIS_OR_YOUTH_CRISIS_RESPONSE`

Specific examples:

- creates, funds, or expands mobile crisis response;
- creates youth-specific crisis teams;
- expands Medicaid mobile crisis coverage;
- links crisis response to schools, pediatric settings, or behavioral health providers.

#### I4. `I4_DIGITAL_CRISIS_REFERRAL_REQUIREMENT`

Specific examples:

- requires apps, websites, schools, or digital tools to display 988 or crisis resources;
- requires digital platforms to route high-risk users to crisis services;
- creates standards for crisis-resource presentation in digital services.

---

### Category J. `J_LOCAL_PUBLIC_SECTOR_AI_GOVERNANCE` — County/Municipal/Public-Sector AI Governance

Use this category for local government policies, ordinances, procurement rules, public-sector AI inventories, or local youth/behavioral health digital policies.

#### J1. `J1_LOCAL_AI_PROCUREMENT_REQUIREMENT`

Specific examples:

- requires algorithmic impact assessments in public procurement;
- requires vendor disclosure of AI use;
- requires privacy, cybersecurity, audit, or bias terms in AI contracts;
- applies to county/city health departments, schools, public libraries, or youth services.

#### J2. `J2_PUBLIC_SECTOR_AI_INVENTORY_TRANSPARENCY`

Specific examples:

- requires public inventory of AI systems used by local government;
- requires disclosure of automated decision systems;
- requires public reporting on AI used in public benefits, health, education, or youth services.

#### J3. `J3_COUNTY_BEHAVIORAL_HEALTH_DIGITAL_TOOL_POLICY`

Specific examples:

- county procurement or governance of digital behavioral health tools;
- public behavioral health chatbot, referral platform, or triage tool;
- county guidance on AI use in behavioral health services.

#### J4. `J4_LOCAL_SUICIDE_PREVENTION_OR_YOUTH_SAFETY_POLICY`

Specific examples:

- county or municipal youth suicide-prevention plans involving digital tools;
- local crisis referral pathways involving apps, chat, text, or AI tools;
- local public-health campaigns requiring digital crisis-resource display.

#### J5. `J5_PUBLIC_LIBRARY_OR_YOUTH_CENTER_AI_ACCESS`

Specific examples:

- policy on AI chatbot use in public libraries or youth centers;
- filtering, blocking, or supervised access for minors;
- privacy rules for minors using AI tools in public facilities.

---

### Category Z. `Z_NOT_RELEVANT_OR_EXCLUDED`

Use this category only in the `excluded_records` sheet.

Specific examples:

- AI bill has no youth, health, privacy, safety, education, consumer protection, provider, payer, crisis, or public-sector relevance;
- source row is irrelevant to the project;
- duplicate record fully captured elsewhere;
- record cannot be interpreted because no text or summary is available.

---

## 6. Directness and Empirical Priority

### 6.1 `directness_score`

Claude must assign one score:

| Score | Meaning |
|---:|---|
| `3` | Directly regulates AI chatbots, AI companions, AI mental health, AI therapy, AI behavioral health, AI crisis handling, or provider use of AI in mental health care |
| `2` | Regulates AI, automated decision-making, youth safety, health AI, privacy, or healthcare workflow in a way likely to affect adolescent AI mental health use or provider response |
| `1` | Broad privacy, AI, school, crisis, consumer protection, or local governance policy with only indirect relevance |
| `0` | Not relevant; place in `excluded_records` unless needed for audit trail |

### 6.2 `empirical_priority`

Claude must assign one empirical priority:

| Priority | Use when |
|---|---|
| `high_confirmatory` | Direct AI mental health, AI therapy, youth companion safety, or crisis-routing requirement with clear jurisdiction, timing, and treatment variation |
| `medium_secondary` | Privacy, health AI, transparency, risk assessment, audit, human-review, or healthcare workflow policy with plausible mechanism and usable timing |
| `covariate_context` | 988, crisis infrastructure, broad school/local policy, or background regulatory environment likely useful as covariate/moderator rather than primary exposure |
| `low_descriptive` | Pending, ambiguous, local, weakly relevant, or hard-to-time record that may be useful descriptively |
| `exclude` | No meaningful pathway to study outcomes |

---

## 7. Classification Rules Claude Must Follow

### 7.1 Use exact source evidence

Every included record must have `relevant_quote`. The quote should be short but specific enough to justify classification.

Bad quote:

```text
This bill relates to artificial intelligence.
```

Good quote:

```text
An AI system may not provide therapy or generate a treatment plan unless reviewed and approved by a licensed professional.
```

### 7.2 Multi-label but one primary category

Every included record must have exactly one `primary_category_code` and one `primary_subcategory_code`. Secondary categories may be added in `all_category_codes` and `all_subcategory_codes`.

Example:

A bill requiring AI therapy tools to disclose they are not licensed clinicians and to route suicidal users to 988 should be coded:

```text
primary_category_code = A_DIRECT_AI_MH_SCOPE
primary_subcategory_code = A5_AI_MH_CRISIS_HANDLING_REQUIREMENT
all_category_codes = A_DIRECT_AI_MH_SCOPE|D_TRANSPARENCY_DISCLOSURE_LABELING
all_subcategory_codes = A5_AI_MH_CRISIS_HANDLING_REQUIREMENT|D3_CONSUMER_MENTAL_HEALTH_DISCLAIMER
```

### 7.3 Prefer effective laws over pending bills for analytic treatment

Pending bills should be retained but generally assigned `empirical_priority = low_descriptive` unless the research team explicitly wants to study agenda-setting or legislative activity.

Enacted laws, final rules, binding regulations, and active agency guidance should receive higher analytic priority when timing is clear.

### 7.4 Distinguish direct restrictions from general AI governance

A general high-risk AI bill is not automatically direct. It should be direct only if the text or official summary specifically covers mental health, healthcare, minors, crisis, therapy, counseling, or consumer chatbot interaction.

### 7.5 Mark human review when ambiguity matters

Set `human_review_needed = TRUE` if any of the following are true:

- no official source URL found;
- effective date missing or ambiguous;
- status conflicts across sources;
- bill text and tracker summary disagree;
- category assignment is uncertain;
- record is local and title/summary are too vague;
- record is broad but may contain a buried relevant provision;
- classification confidence is `low`;
- source scraping was incomplete;
- duplicate reconciliation is uncertain.

---

## 8. Required Output Workbook

Claude must write an Excel workbook named:

```text
jurisdiction_policy_events_output_YYYYMMDD.xlsx
```

The workbook must contain these sheets.

### 8.1 Sheet: `policy_events`

Contains one row per deduplicated included legal/policy record using the fields in Section 4.1.

### 8.2 Sheet: `category_assignments`

Long-format category table. One row per record-category-subcategory assignment.

Required columns:

| Column | Description |
|---|---|
| `record_id` | Links to `policy_events.record_id` |
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
| `record_id` | Link to policy record when known |
| `source_name` | Source name |
| `source_url` | Source URL |
| `retrieved_at` | Timestamp |
| `content_type` | `html`, `pdf`, `json`, `csv`, `xlsx`, `text`, `unknown` |
| `local_path` | Path where raw file/text was saved, if applicable |
| `text_hash` | Hash for change detection |
| `retrieval_status` | `success`, `partial`, `failed` |

### 8.4 Sheet: `excluded_records`

Records retrieved but excluded as irrelevant, duplicate, or unusable.

Required columns:

| Column | Description |
|---|---|
| `excluded_id` | Unique ID |
| `source_name` | Source name |
| `source_url` | Source URL |
| `title` | Title or best available label |
| `reason_excluded` | Short reason |
| `candidate_category` | Best guess category, if any |
| `human_review_needed` | `TRUE` or `FALSE` |

### 8.5 Sheet: `source_run_log`

One row per source attempted.

Required columns:

| Column | Description |
|---|---|
| `run_id` | Run ID |
| `source_name` | Source name |
| `source_url` | Source URL |
| `started_at` | Timestamp |
| `finished_at` | Timestamp |
| `status` | `success`, `partial`, `failed`, `skipped` |
| `records_found` | Number of candidate records found |
| `records_included` | Number included in `policy_events` |
| `records_excluded` | Number placed in `excluded_records` |
| `error_message` | Error text if failed or partial |

### 8.6 Sheet: `review_queue`

Subset of records needing human/legal review.

Required columns:

| Column | Description |
|---|---|
| `record_id` | Link to policy record |
| `review_reason` | Why human review is needed |
| `suggested_question_for_reviewer` | Specific question, e.g., `Confirm effective date`, `Confirm whether this applies to consumer chatbots`, `Confirm category A vs B` |
| `priority` | `high`, `medium`, `low` |
| `source_url` | URL reviewer should inspect first |

---

## 9. Recommended Source Types

The operational list of sources comes from `input_sources.xlsx`. Claude must not assume that every source below is available unless listed in the workbook. This section tells Claude what kinds of sources are likely to appear and how to treat them.

### 9.1 Discovery and tracker sources

Examples:

- NCSL AI legislation trackers;
- Manatt Health AI Policy Tracker;
- Georgetown/Beeck/Digital Service Network AI legislation scans;
- IAPP state privacy tracker;
- other reputable AI, privacy, youth safety, health AI, or legal trackers.

Use these sources to discover candidate records and topic labels. Do not treat tracker summaries as final if official law or bill text is available.

### 9.2 Official federal sources

Examples:

- Congress.gov;
- GovInfo;
- Federal Register;
- eCFR;
- agency websites such as HHS, OCR, ONC, CMS, SAMHSA, FTC, FDA, ED, FCC.

Use official federal sources as canonical for federal bills, laws, regulations, rules, guidance, and enforcement actions.

### 9.3 Official state sources

Examples:

- state legislature bill pages;
- enrolled act/chapter law pages;
- state administrative code and register pages;
- attorney general pages;
- health department, insurance department, education department, Medicaid agency, and professional board pages.

Use official state sources as canonical for bill status, enacted text, statutory language, and effective dates.

### 9.4 County, municipal, and local sources

Examples:

- Municode;
- eCode360;
- American Legal Publishing;
- Granicus Legistar;
- county board agendas and minutes;
- city council ordinances;
- school board policy portals.

Local sources are often messy. Extract what is available, mark uncertainty clearly, and use `human_review_needed = TRUE` when title/summary does not reveal exact scope.

---

## 10. Scraping and Parsing Requirements

### 10.1 Raw document preservation

Claude must save or index raw documents whenever possible. At minimum, Claude must retain:

- source URL;
- retrieval timestamp;
- content type;
- text hash;
- local path or retrieval note.

Do not overwrite old raw files. Each run should preserve enough information to reconstruct what was seen during that run.

### 10.2 Text extraction

Claude should extract text from HTML, JSON, CSV/XLSX, PDF, and plain text when possible. If PDF extraction fails, log the failure and retain the PDF URL. Do not hallucinate PDF content.

### 10.3 Pagination and linked documents

If a source page lists multiple records and links to detail pages, Claude should follow detail links on the same domain or clearly official domains. Do not crawl the open web indiscriminately.

### 10.4 Deduplication

Deduplicate using combinations of:

- jurisdiction;
- bill or policy ID;
- session year;
- title;
- official URL;
- text hash;
- normalized citation.

When duplicate sources disagree, prefer official law/bill text over tracker summaries. Keep tracker URLs in `supporting_source_urls`.

### 10.5 Change detection

If a record was previously retrieved and the text hash changes, Claude must treat this as a potentially meaningful update and flag it in the run report.

---

## 11. Quality-Control Rules

Claude must apply the following QC checks before final export:

1. Every row in `policy_events` has `record_id`, `source_name`, `source_url`, `jurisdiction_level`, `jurisdiction_name`, `title`, `current_status`, `primary_category_code`, `primary_subcategory_code`, `directness_score`, `empirical_priority`, `relevant_quote`, `classification_confidence`, and `human_review_needed`.
2. Every `primary_category_code` and `primary_subcategory_code` exactly matches a taxonomy code in Section 5.
3. Every date is either blank/unknown or ISO formatted as `YYYY-MM-DD`.
4. Every included record has at least one source URL.
5. Every row with `classification_confidence = low` has `human_review_needed = TRUE`.
6. Every row with missing or ambiguous effective date has `human_review_needed = TRUE` unless the record is pending and clearly labeled as such.
7. Every row in `review_queue` corresponds to a row in `policy_events`.
8. The output workbook must be created even if no relevant records are found. In that case, `source_run_log` and `excluded_records` must explain what happened.

---

## 12. Human-Review Philosophy

The scraper/classifier is not the legal authority. It is an evidence-gathering and first-pass classification system.

Claude should be aggressive in retrieving and organizing candidate material, but conservative in final claims. Ambiguity should be surfaced, not hidden.

Human reviewers should be able to answer:

- What law/policy is this?
- Where is it in effect?
- When did it become effective?
- What does it require, prohibit, fund, disclose, or enforce?
- Why is it relevant to adolescent AI chatbot mental health use or provider response?
- Which survey outcomes could plausibly change because of it?
- Is it suitable for confirmatory analysis, secondary analysis, covariate/context adjustment, or descriptive tracking only?

---

## 13. Run Report Requirements

The markdown run report must include:

1. run date and run ID;
2. number of sources listed in `input_sources.xlsx`;
3. number of sources attempted, successful, partially successful, failed, and skipped;
4. number of candidate records retrieved;
5. number of records included in `policy_events`;
6. number of excluded records;
7. number of records needing human review;
8. list of `high_confirmatory` records;
9. list of sources that failed and why;
10. notes on duplicate reconciliation and source conflicts;
11. notes on changed text hashes from prior runs, if available;
12. recommended next steps for human/legal review.

---

## 14. Non-Negotiable Rules

Claude must follow these rules:

1. Do not invent legal text, dates, citations, bill status, or applicability.
2. Do not treat a pending bill as enacted.
3. Do not treat introduced date as effective date unless explicitly marked and reviewed.
4. Do not classify a broad AI bill as mental-health-specific unless the text supports that classification.
5. Do not silently drop candidate records that appear relevant but are incomplete; place them in the review queue.
6. Do not bypass scraping restrictions, authentication, paywalls, or anti-bot systems.
7. Do not store personal data about adolescents, patients, or private individuals.
8. Do not overwrite previous raw files or outputs without versioning.
9. Do not add uncontrolled new category names. Use the taxonomy codes in this constitution.
10. Do not proceed without generating an output workbook and run report.

---

## 15. Minimal Success Criteria

A run is successful if, at minimum:

1. `input_sources.xlsx` was read;
2. every enabled source was attempted or explicitly skipped with a reason;
3. candidate records were extracted where available;
4. included records were classified according to Section 5;
5. `jurisdiction_policy_events_output_YYYYMMDD.xlsx` was created with all required sheets;
6. `jurisdiction_policy_events_run_report_YYYYMMDD.md` was created;
7. records requiring human/legal judgment were placed in `review_queue`.

