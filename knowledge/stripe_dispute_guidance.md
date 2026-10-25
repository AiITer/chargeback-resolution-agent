# Stripe Dispute Guidance

**Purpose:** External operational guidance for Northstar dispute handling.  
**Authority:** Stripe documentation and Stripe Help & Support.  
**Last reviewed:** 2026-10-23

This document contains long-lived Stripe dispute mechanics and evidence guidance. It is not a source of live case facts. Current dispute status, payment state, refund state, deadlines, and other transaction-specific facts must be retrieved from Stripe or other operational systems.

---

## 1. Formal Dispute Lifecycle and Financial Effect

A formal card dispute is initiated by the cardholder through the card issuer.

When a formal dispute is opened, Stripe can debit the merchant's Stripe balance for the disputed amount and applicable dispute fees. The disputed funds remain subject to the dispute outcome.

The merchant may respond by submitting evidence before the applicable deadline. The card issuer, not Stripe, determines the final outcome.

A dispute can ultimately be resolved as won or lost. If the merchant wins, the disputed amount is returned according to the applicable Stripe dispute process.

A dispute that has already been opened is not erased merely because the customer and merchant later resolve the underlying issue.

**Primary Stripe sources:**
- Stripe Documentation — How disputes work
- Stripe Help & Support — Dispute fees FAQ

---

## 2. Accepting Versus Countering a Dispute

Accepting a dispute and countering a dispute are different actions.

Accepting or closing a dispute indicates that the merchant does not intend to submit evidence to overturn it. Closing a dispute is treated as acknowledging the dispute as lost and is irreversible.

Countering a dispute means submitting evidence for review in an attempt to overturn the dispute. Evidence may be staged and later submitted, or submitted through the Dashboard or API depending on the workflow.

Choosing to counter a dispute does not guarantee a win. The issuer evaluates the evidence and determines the outcome.

**Primary Stripe sources:**
- Stripe API Reference — Disputes
- Stripe API Reference — Close a dispute

---

## 2.1 Financial Effects of Accepting and Countering a Dispute

When a formal dispute is created, Stripe reverses the disputed payment and debits the merchant's Stripe balance for the disputed amount. A dispute received fee also applies.

The dispute received fee is incurred when the dispute is received. Accepting the dispute does not cancel or refund this fee.

Accepting a dispute means the merchant will not submit evidence to overturn it. The dispute is closed as lost and the acceptance is irreversible. The merchant should therefore not treat acceptance as a way to avoid the financial consequences of an already-created dispute.

Countering a dispute means submitting evidence for issuer review. A separate dispute countered fee may apply depending on the merchant's region and pricing. If the merchant wins, Stripe generally returns the disputed amount and the dispute countered fee, subject to regional rules.

Accordingly, the financial comparison between accepting and countering should distinguish:

- financial loss that has already occurred when the dispute was created;
- fees that are unavoidable once the dispute exists;
- additional costs associated specifically with countering;
- the disputed amount that may be recovered if the merchant wins; and
- the risk of duplicate merchant loss when a transaction was already refunded before the formal dispute.

A dispute that follows a prior refund requires particular care. The merchant should not assume that accepting the dispute avoids financial loss merely because the customer was already refunded. The prior refund and the formal dispute are separate financial events, and refund evidence may be relevant when attempting to recover the disputed amount.

---

## 3. Disputes After a Full Refund

A transaction can still be disputed after the merchant has already issued a full refund.

This can happen when the refund and dispute occur close together or when the issuing bank does not recognize the refund before creating the dispute.

When a dispute is opened after a full refund, the merchant may counter the dispute using the prior refund as material evidence. Relevant refund evidence can include the refund amount, refund date, refund identifier, and other Stripe refund details available for the transaction.

A completed refund is material to the formal dispute response because Stripe permits refund details to be submitted as evidence when a fully refunded transaction is later disputed.

Refund status, amount, timing, and available refund identifiers should therefore be considered when preparing the response.

**Primary Stripe source:**
- Stripe Help & Support — Disputes on a Refunded Transaction FAQ

---

## 4. Partial Refunds and Disputed Amounts

If a customer disputes the full charge after the merchant has already issued a partial refund, Stripe guidance states that evidence of the partial refund should be included in the dispute response.

Relevant evidence includes the refund amount and refund date.

Even if the merchant expects to accept the unrefunded portion, the prior partial refund should still be included so that the dispute can be assessed against the amount that remains economically unresolved.

The disputed amount and the amount that remains legitimately at issue are not always identical.

**Primary Stripe source:**
- Stripe Help & Support — Dispute for full charge amount after a partial refund was issued

---

## 5. Product Not Received Evidence

For a `product_not_received` dispute involving a physical product, delivery and shipment evidence is relevant when it addresses whether the customer received the product.

Potentially relevant evidence includes:

- carrier;
- tracking number;
- shipment date;
- delivery date;
- delivery status;
- delivery location;
- delivery notifications;
- proof of delivery;
- signature verification; and
- other relevant tracking history.

Evidence should be selected because it addresses the dispute claim, not merely because it exists.

Shipping evidence should be interpreted together with other material transaction evidence. Stripe's guidance for `product_not_received` focuses on evidence relevant to shipment and delivery, while separate refund evidence may also be relevant when the transaction has already been refunded.

**Primary Stripe source:**
- Stripe Documentation — Dispute sample evidence packets

---

## 6. Evidence and Outcome Boundaries

Stripe facilitates the dispute process but does not decide the issuer's final ruling.

Evidence should be relevant to the dispute reason and should accurately represent the underlying transaction history.

No response should imply that contesting guarantees a win.

No live dispute fact should be inferred from this document. Live facts must be retrieved from Stripe, Northstar systems, shipping providers, customer communications, or persisted Case state as appropriate.

---

## Source URLs

- https://docs.stripe.com/disputes/how-disputes-work
- https://docs.stripe.com/api/disputes
- https://docs.stripe.com/api/disputes/close
- https://docs.stripe.com/disputes/visual-evidence
- https://support.stripe.com/questions/disputes-on-a-refunded-transaction-faq
- https://support.stripe.com/questions/dispute-for-full-charge-amount-after-a-partial-refund-was-issued
- https://support.stripe.com/questions/dispute-fees-faq
