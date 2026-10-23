# Northstar Commerce Inc.

## Chargeback Resolution and Dispute Authority Policy

**Policy ID:** NCR-CB-001

**Version:** 2.0

**Effective Date:** 2026-10-16

**Owner:** Payments & Risk Operations

**Applies To:** Chargeback Operations, Payment Operations, Risk Operations, Customer Support, and authorized automated agents used in formal dispute handling

---

## 1. Purpose

This policy governs how Northstar Commerce Inc. receives, prioritizes, investigates, evaluates, responds to, and closes formal card-payment disputes and chargebacks.

The objective is not to contest every dispute. The objective is to reach a commercially reasonable, evidence-based, auditable resolution while balancing:

- response deadlines;
- financial exposure;
- strength and availability of evidence;
- investigation effort and cost;
- customer experience;
- merchant responsibility;
- operational risk; and
- applicable Stripe, card-network, and Northstar requirements.

Activities governed by this policy may be performed by authorized personnel or approved automated agents, subject to the same substantive requirements and to applicable authority, control, audit, and review requirements.

This policy establishes decision principles and control requirements. It does not prescribe a fixed decision tree where case-specific judgment is required.

---

## 2. Scope

This policy applies after a formal payment dispute has been created through Stripe.

It does not govern ordinary customer-service refunds or upstream pre-dispute prevention workflows.

A customer-service refund and a formal card-network dispute are separate processes. The existence of one must not be assumed to cancel or resolve the other.

Relevant information may be obtained from:

- Stripe dispute, Charge, and PaymentIntent records;
- Northstar's Order Management System;
- shipping and tracking providers;
- customer communications;
- internal refund, shipping, fulfillment, and customer-service policies;
- Stripe dispute guidance;
- card-network and reason-code guidance; and
- historical resolved cases when used as supporting operational context.

Live case facts must come from current operational systems or persisted case state rather than being inferred from static policy documents.

---

## 3. Operating Principles

### 3.1 Case-Specific Assessment

Each dispute must be evaluated on its own facts.

A dispute reason or network reason code is an important starting point, but it does not by itself determine the appropriate outcome.

Each Case assessment should consider, as applicable:

- the customer's stated basis for the dispute;
- Northstar's records of the transaction, fulfillment, refund, replacement, and related activity;
- evidence supporting or contradicting material assertions;
- material facts that remain unknown;
- information gaps most likely to change the recommended resolution;
- the expected value of further investigation;
- the remaining response period;
- the commercial reasonableness of accepting or contesting the dispute; and
- whether the proposed action falls within delegated authority.

### 3.2 Evidence Before Assertion

No inference may be recorded, submitted, or represented as a verified fact unless supported by sufficient evidence.

Case records should distinguish, where relevant:

- verified facts;
- third-party records;
- customer statements;
- internal assumptions or hypotheses;
- unresolved questions; and
- contradictions between sources.

### 3.3 Continuous Investigation

A formal dispute is handled through one continuous investigation process.

The investigation should repeatedly:

1. assess what is currently known;
2. identify the most valuable missing information;
3. obtain information from an appropriate authorized source;
4. incorporate newly obtained facts; and
5. reassess the Case.

At any reassessment point, a Case may:

- remain under investigation;
- proceed to a recommendation to accept;
- proceed to a recommendation to contest;
- be determined ready for submission preparation; or
- be escalated for human review.

A recommendation to contest does not, by itself, establish that the evidence package is complete.

If the evidence package remains incomplete, investigation should continue until sufficient evidence has been obtained or a stopping condition under this policy has been reached.

### 3.4 Proportional Effort

Investigation effort should be proportionate to:

- disputed value;
- urgency;
- evidence availability;
- complexity;
- expected probability that further work will materially improve the outcome;
- cost of further investigation; and
- operational risk.

A low-value dispute with clear merchant responsibility should not consume the same resources as a complex or high-risk dispute in which additional evidence is reasonably likely to affect the result.

### 3.5 Selective Human Involvement

Human review is not required for every routine action.

Automated agents may perform routine actions where:

- the applicable policy is sufficiently clear;
- the available evidence is sufficiently strong;
- delegated authority permits the action; and
- no exceptional risk condition applies.

Human review is required where a Case exceeds delegated authority, contains material ambiguity, or presents legal, privacy, regulatory, financial, customer, or reputational risk outside normal operating policy.

---

## 4. Intake and Case Creation

When Stripe reports a new formal dispute, Northstar should create a persistent internal Case without requiring manual employee entry.

The Case record should preserve, where available:

- Northstar Case ID;
- Stripe dispute ID;
- associated Charge ID;
- associated PaymentIntent ID;
- disputed amount and currency;
- Stripe dispute reason;
- card-network reason code;
- Stripe dispute status;
- evidence response deadline;
- dispute creation time; and
- Northstar workflow state.

Case creation must be performed through deterministic system controls and must not depend on discretionary assessment.

---

## 5. Portfolio Prioritization and Capacity

Northstar may receive more disputes than can be investigated simultaneously.

Cases should therefore not be handled strictly first-in, first-out.

Prioritization may consider:

- evidence deadline;
- disputed amount and financial exposure;
- likelihood that timely work can materially improve the outcome;
- evidence availability;
- dispute type and reason code;
- expected investigation effort;
- current workflow state;
- whether the Case is waiting on an external dependency;
- unusual customer or account sensitivity;
- legal, privacy, regulatory, or reputational risk; and
- applicable internal service-level expectations.

Northstar maintains bounded active investigation capacity.

Cases waiting for customers, employees, Stripe, carriers, approval, or other external events should be suspended and should not consume active investigation capacity.

Prioritization and capacity management must remain separate from the substantive assessment of an individual Case.

---

## 6. Investigation and Evidence Gathering

Investigation is adaptive rather than a fixed sequence of mandatory checks.

Investigation should identify the factual questions material to the current dispute and use the most appropriate authorized evidence source for each question.

Evidence should not be gathered merely because it is available.

The investigation should focus on evidence that can:

- confirm or reject a material fact;
- resolve a contradiction;
- clarify responsibility;
- satisfy Stripe or card-network evidence expectations;
- determine whether accepting or contesting is commercially reasonable; or
- complete an evidence package after a contest recommendation.

Evidence already available in durable Case state should not be retrieved redundantly unless re-verification is materially justified.

---

## 7. Authorized Evidence Sources

### 7.1 Stripe

Stripe may be used to obtain or verify:

- dispute details;
- dispute status;
- payment and charge information;
- refund information;
- receipt information;
- statement descriptors;
- applicable evidence requirements;
- response deadline information; and
- submission status.

### 7.2 Order Management System

The Order Management System may be used to obtain or verify:

- order identity;
- products and quantities;
- order value;
- order timestamps;
- fulfillment status;
- cancellation status;
- refund status;
- replacement orders or shipments; and
- relevant internal order notes.

### 7.3 Shipping and Tracking Systems

Shipping providers may be used to obtain or verify:

- carrier;
- tracking number;
- shipment date;
- tracking events;
- delivery date and time;
- delivery location;
- signature or proof of delivery when available;
- return-to-sender events;
- failed delivery events; and
- other delivery exceptions.

A `returned_to_sender` event is relevant evidence but must not automatically determine acceptance.

Assessment of a return, failed delivery, or other shipping exception should also consider whether:

- a refund was already issued;
- a replacement was sent;
- a replacement was later delivered;
- the customer refused delivery;
- an address issue caused the return; or
- subsequent evidence materially changes the interpretation.

### 7.4 Customer Communications

Customer communications may be used to determine:

- whether the customer reported a problem before filing the dispute;
- what the customer claimed;
- what Northstar communicated;
- whether a refund or replacement was offered;
- whether the customer acknowledged receipt or resolution;
- whether statements changed over time; and
- whether communication resolves or creates a material contradiction.

### 7.5 Policies and Guidance

Internal policy and authoritative external guidance may be used to determine:

- company obligations;
- evidence requirements;
- approval requirements;
- customer-contact rules;
- dispute deadlines;
- card-network expectations; and
- Stripe submission requirements.

Long-lived policies and guidance may be maintained in Northstar's approved knowledge system.

Live operational facts must not be substituted with static policy or knowledge-repository content.

---

## 8. Customer Contact

Customer contact is an optional investigation action.

It should be used when clarification is reasonably likely to change the Case assessment, resolve an important information gap, or provide material evidence.

Possible purposes include:

- confirming whether an order ultimately arrived;
- clarifying whether a delivery photo matches the customer's location;
- confirming whether a refund or replacement was received;
- resolving an identity or order mismatch; or
- clarifying a contradiction between customer and operational records.

Customer contact must be factual and non-coercive.

The customer must not be asked to provide:

- passwords;
- full payment-card numbers;
- authentication secrets; or
- unrelated personal information.

### 8.1 Email

Email is the supported customer-contact channel for the initial system.

Routine case-related email may be drafted or sent by an automated agent only where permitted by the applicable communication authority.

Communication authority may be classified as:

- `AUTONOMOUS`;
- `REVIEW_REQUIRED`; or
- `HUMAN_ONLY`.

Sensitive, strategic, VIP, legal, privacy, or reputationally unusual communications may require human review.

Outbound communication must be associated with the Case.

### 8.2 Asynchronous waiting

Customer contact must not be modeled as an immediate request-response interaction.

After email is sent, the Case may enter a waiting state.

While waiting:

- active workflow capacity should be released;
- a customer reply may resume the Case;
- expiration of the response window may also resume the Case; and
- the investigation may proceed without customer input when waiting is no longer commercially or operationally justified.

A customer reply does not automatically mean that the information gap has been resolved.

---

## 9. Evidence Assessment

At every significant point in the investigation, available evidence should be reassessed for whether it is:

- sufficient;
- relevant;
- internally consistent;
- associated with the correct transaction and customer; and
- capable of addressing the customer's dispute claim.

Assessment should consider:

- whether payment, order, shipment, and customer identities match;
- whether the timeline is coherent;
- whether evidence directly addresses the dispute reason;
- whether refund or replacement activity changes the interpretation;
- whether customer communications support or contradict the proposed position;
- whether evidence is missing;
- whether sources contradict one another; and
- whether the evidence would be understandable to an external reviewer.

Further investigation should continue when an important information gap exists and obtaining additional evidence is reasonably likely to change the decision or strengthen a required evidence package.

Investigation should stop when:

- sufficient evidence has been obtained;
- additional investigation is unlikely to change the recommendation;
- additional work is not commercially reasonable;
- the evidence deadline makes further investigation impractical; or
- the Case requires human judgment outside delegated authority.

---

## 10. Resolution Recommendation

A Case assessment may result in:

- `CONTINUE_INVESTIGATION`;
- `RECOMMEND_ACCEPT`;
- `RECOMMEND_CONTEST`; or
- `NEEDS_HUMAN_REVIEW`.

The assessment should preserve:

- a concise reasoning summary;
- material supporting evidence;
- unresolved evidence gaps;
- material contradictions;
- relevant financial exposure;
- evidence deadline; and
- confidence.

Confidence should reflect uncertainty rather than conceal it.

A recommendation and authority to execute an action are separate.

---

## 11. Delegated Authority and Human Review

Northstar uses bounded delegated autonomy.

Routine actions may be executed by an automated agent only when permitted by explicit company authority policy and applicable system controls.

High-risk, exceptional, sensitive, ambiguous, or otherwise out-of-policy Cases require human involvement.

Authority decisions may consider:

- disputed amount;
- evidence completeness;
- material contradictions;
- customer/account sensitivity;
- legal, regulatory, privacy, or reputational concerns;
- unusual operational conditions;
- confidence;
- fraud or systemic-risk indicators; and
- company-specific approval rules.

Exact monetary thresholds and approval limits are configuration and governance decisions and are not defined by this policy version.

Neither personnel nor automated agents may divide, reclassify, manipulate, or otherwise alter a Case for the purpose of bypassing an authority requirement.

---

## 12. Contest Investigation and Evidence Package

A recommendation to contest establishes the intended resolution direction but does not automatically mean the Case is ready for submission.

If required evidence is still missing, the same investigation continues.

Before submission, the evidence package should:

- directly address the dispute reason;
- present the strongest relevant evidence;
- describe the sequence of events clearly;
- avoid unsupported claims;
- exclude irrelevant evidence;
- use correct customer, order, payment, and shipment identifiers; and
- comply with applicable Stripe and card-network requirements.

The evidence package should be understandable to an external reviewer who has no prior knowledge of the Case.

---

## 13. Submission Validation

Before any response is submitted externally, deterministic validation should verify, where applicable:

- correct Northstar Case ID;
- correct Stripe dispute ID;
- correct order, Charge, and PaymentIntent associations;
- response deadline has not passed;
- required evidence is present;
- evidence belongs to the correct transaction and customer;
- tracking and shipment identifiers match the correct order;
- known material contradictions are not omitted;
- prohibited credentials or sensitive information are not included;
- required approval has been obtained; and
- the dispute has not already been submitted.

These safeguards must be enforced independently of model judgment.

---

## 14. Submission and Waiting for Stripe

Once an authorized evidence response has been successfully submitted to Stripe, the Case should enter a waiting state.

A Case waiting for Stripe should not consume active investigation capacity.

A Stripe webhook event or other authoritative status change should resume the applicable durable Case workflow.

Submission must be protected against duplicate execution through deterministic idempotency controls.

---

## 15. Customer Withdrawal and Merchant Resolution

A customer may state that they have withdrawn a dispute with their issuer or resolved the matter with Northstar.

Such a statement may be relevant evidence but must not be treated as proof that the formal dispute no longer exists.

Northstar must continue to follow the formal Stripe dispute lifecycle until an authoritative status update confirms the outcome.

A merchant refund does not automatically terminate a formal dispute.

If a refund has already been issued, the Case assessment should evaluate the financial relationship between the prior refund and the amount still at issue in the formal dispute.

The validity of the customer's original complaint and the appropriate resolution of the formal dispute are separate questions. A customer may have had a valid complaint while also having already received compensation from Northstar.

Prior merchant compensation should be treated as material evidence when assessing the merchant's remaining liability and financial exposure, including the possibility of duplicate compensation.

---

## 16. Outcome and Closure

When a dispute reaches a final or otherwise actionable outcome, the Case should preserve:

- final Stripe outcome;
- Northstar recommendation;
- executed action;
- material evidence used;
- approval history;
- submission timestamp;
- resolution timestamp;
- amount recovered or lost where available; and
- relevant operational notes.

A Case should not be considered closed until required follow-up work has been completed.

---

## 17. Historical Cases and Learning

Resolved disputes may be analyzed to identify:

- recurring dispute reasons;
- merchant-liability patterns;
- evidence patterns associated with outcomes;
- fulfillment or shipping failures;
- refund-process failures;
- customer-communication failures;
- operational bottlenecks; and
- opportunities to improve policy or workflow.

Historical outcomes may inform future assessments but must not be treated as unquestionable ground truth.

Analysis of resolved disputes may identify or recommend potential policy improvements.

An automated agent may identify or recommend potential policy improvements, but may not independently modify company policy, delegated authority, or mandatory system controls.

---

## 18. Auditability

Material actions by personnel and automated agents should be attributable to a Case and recorded with sufficient context for later review.

Records may include:

- Case ID;
- timestamp;
- workflow state;
- source consulted;
- system or evidence source used;
- relevant result;
- model and model version for material model-based decisions;
- Case assessment;
- confidence;
- approval requirement;
- human approval or rejection;
- external action taken; and
- resulting state transition.

Logs must not contain:

- Stripe secret keys;
- OAuth access or refresh tokens;
- PaymentIntent client secrets;
- full payment-card numbers;
- passwords; or
- other credentials.

---

## 19. Automated Agent Governance and System Controls

Approved automated agents may support or perform dispute-handling activities only within the authority, data-access, audit, and control requirements established by Northstar. Automated agents are subject to the same substantive dispute-resolution, evidentiary, and recordkeeping requirements that apply to human handling of a Case.

Within delegated authority, automated agents may:

- identify material evidence;
- identify information gaps;
- select an authorized source for additional evidence;
- determine whether further investigation is warranted;
- assess evidence sufficiency and consistency;
- recommend acceptance, contest, continued investigation, or escalation;
- determine whether an evidence package is ready for submission preparation; and
- identify circumstances requiring human review.

Automated agents must rely on current operational data or persisted Case state for live facts. An agent must not represent an inference, model-generated statement, or unverified assumption as a retrieved or recorded fact.

Automated-agent execution must remain subject to mandatory system controls governing, as applicable:

- authentication and authorization;
- credential protection;
- deadline enforcement;
- approval gates;
- execution permissions;
- workload allocation and concurrency;
- retries;
- idempotency and duplicate-execution prevention;
- data-integrity validation; and
- non-negotiable authority boundaries.

An automated agent must not exceed delegated authority, bypass a required approval or human-review condition, or use model judgment to override a mandatory operational safeguard. Human review remains required where this policy, delegated authority, or applicable risk controls require it.

---

**End of Policy**
