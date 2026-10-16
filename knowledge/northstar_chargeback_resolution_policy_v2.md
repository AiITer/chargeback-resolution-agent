# Northstar Commerce Inc.
## Chargeback Resolution and Dispute Authority Policy

**Policy ID:** NCR-CB-001  
**Version:** 2.0  
**Effective Date:** 2026-10-16  
**Owner:** Payments & Risk Operations  
**Applies To:** Chargeback Operations, Payment Operations, Risk Operations, Customer Support, and authorized automated agents

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

Authorized automated agents may perform work under this policy. They are expected to reason over the facts of each case, consult relevant company and external guidance, and document the basis for material decisions.

This policy should not be interpreted as a fixed decision tree where contextual judgment is required.

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

### 3.1 Case-specific reasoning

Each dispute must be evaluated on its own facts.

A dispute reason or network reason code is an important starting point, but it does not by itself determine the appropriate outcome.

The reviewer or authorized agent should continually consider:

- What does the customer claim happened?
- What do Northstar's records show happened?
- What evidence supports or contradicts each account?
- Which facts remain unknown?
- Which missing information would most materially change the decision?
- Is additional investigation likely to be valuable?
- Does sufficient time remain?
- Is accepting or contesting commercially reasonable?
- Does the proposed action fall within delegated authority?

### 3.2 Evidence before assertion

No reviewer or automated agent may present an inference as a verified fact.

Case records should distinguish, where relevant:

- verified facts;
- third-party records;
- customer statements;
- internal assumptions or hypotheses;
- unresolved questions; and
- contradictions between sources.

### 3.3 Continuous investigation

A formal dispute is handled through one continuous investigation process.

The investigation should repeatedly follow this pattern:

1. assess what is currently known;
2. identify the most valuable missing information;
3. obtain information from an appropriate source;
4. incorporate the new facts;
5. reassess the case.

At any reassessment point, the reviewer or agent may:

- continue investigating;
- recommend acceptance;
- recommend contesting;
- determine that sufficient evidence exists for submission preparation; or
- escalate for human review.

A recommendation that a case is worth contesting does not necessarily end the investigation.

If the evidence package is incomplete, investigation should continue until sufficient evidence has been obtained or a stopping condition is reached.

### 3.4 Proportional effort

Investigation effort should be proportional to:

- disputed value;
- urgency;
- evidence availability;
- complexity;
- expected probability of improving the outcome;
- cost of further investigation; and
- operational risk.

A low-value dispute with clear merchant responsibility should not consume the same resources as a complex or high-risk dispute where additional evidence is likely to materially affect the result.

### 3.5 Selective human involvement

Human review is not required for every routine action.

Automation should be permitted where:

- policy is sufficiently clear;
- evidence is sufficiently strong;
- delegated authority permits the action; and
- no exceptional risk condition applies.

Human review is required when the case exceeds delegated authority, contains material ambiguity, or presents legal, privacy, regulatory, financial, customer, or reputational risk outside normal operating policy.

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

Case creation is a deterministic system responsibility.

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

Cases waiting for customers, employees, Stripe, carriers, approval, or other external events should be suspended and should not consume active reasoning capacity.

Prioritization and capacity management must remain separate from the reasoning performed inside one individual Case workflow.

---

## 6. Investigation and Evidence Gathering

Investigation is adaptive rather than a fixed sequence of mandatory checks.

The reviewer or agent should identify the factual questions that matter for the current dispute and select the most appropriate evidence source.

Evidence should not be gathered merely because it is available.

The investigation should focus on evidence that can:

- confirm or reject a material fact;
- resolve a contradiction;
- clarify responsibility;
- satisfy Stripe or card-network evidence expectations;
- determine whether accepting or contesting is commercially reasonable; or
- complete an evidence package after a contest recommendation.

The reviewer or agent should avoid redundant tool calls when the required fact is already available in durable case state.

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

The reviewer or agent should also consider whether:

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

Live operational facts must not be substituted with static RAG knowledge.

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

An automated agent may draft or send routine case-related email when permitted by communication authority.

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

At every significant point in the investigation, the reviewer or agent should reassess whether available evidence is:

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

Routine actions may be executed automatically only when permitted by explicit company authority policy.

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

A reviewer or automated agent must not divide, reclassify, manipulate, or otherwise alter a Case to bypass an authority requirement.

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

These safeguards must not depend solely on model judgment.

---

## 14. Submission and Waiting for Stripe

Once an authorized evidence response has been successfully submitted to Stripe, the Case should enter a waiting state.

The workflow should not continue consuming active reasoning capacity while waiting for Stripe.

Stripe webhook events or other authoritative status changes should resume the appropriate durable Case workflow.

Submission must be protected against duplicate execution through deterministic idempotency controls.

---

## 15. Customer Withdrawal and Merchant Resolution

A customer may state that they have withdrawn a dispute with their issuer or resolved the matter with Northstar.

Such a statement may be relevant evidence but must not be treated as proof that the formal dispute no longer exists.

Northstar must continue to follow the formal Stripe dispute lifecycle until an authoritative status update confirms the outcome.

A merchant refund does not automatically terminate a formal dispute.

If a refund has already been issued, the reviewer or agent should assess the possibility of duplicate compensation.

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

Historical outcomes may inform future reasoning but must not be treated as unquestionable ground truth.

Automated agents may identify or recommend potential policy improvements.

They may not independently change company policy, delegated authority, or hard system controls.

---

## 18. Auditability

Material automated and human actions should be attributable to a Case and recorded with sufficient context for later review.

Records may include:

- Case ID;
- timestamp;
- workflow state;
- source consulted;
- tool or external system used;
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

## 19. Automated-Agent Operating Boundary

Northstar's Chargeback Agent is an operational decision-making system, not a fixed rule engine.

The Agent may reason about:

- which evidence matters;
- what information is missing;
- which source should be consulted next;
- whether customer contact is useful;
- whether further investigation is worthwhile;
- whether evidence is sufficient;
- whether evidence conflicts;
- whether accepting or contesting is appropriate;
- whether an evidence package is ready; and
- whether uncertainty requires escalation.

The Agent must use tools to retrieve current external facts or perform external actions.

It must not invent live facts that have not been retrieved or persisted.

Deterministic system controls should govern:

- authentication and authorization;
- credential protection;
- deadline enforcement;
- approval gates;
- execution permissions;
- concurrency limits;
- claim and lease behavior;
- retries;
- idempotency;
- duplicate submission prevention;
- data-integrity validation; and
- non-negotiable authority boundaries.

The system should preserve the strengths of agent reasoning without allowing probabilistic judgment to bypass hard operational safeguards.

---

**End of Policy**