from math import sqrt

from app.integrations.embeddings import create_embedding, create_embeddings


INTENTS = {
    "evidence_requirements": (
        "What evidence and investigation steps are required for a payment dispute?"
    ),
    "human_review": (
        "When is human review required for a payment dispute?"
    ),
    "delegated_authority": (
        "What actions can an automated agent take without human approval?"
    ),
    "submission_requirements": (
        "What requirements must be satisfied before dispute evidence is submitted?"
    ),
    "customer_communication": (
        "What are the rules for customer communication during a dispute investigation?"
    ),
    "refund_dispute_relationship": (
        "How do refunds and formal payment disputes interact?"
    ),
}


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    norm_a = sqrt(sum(a * a for a in vector_a))
    norm_b = sqrt(sum(b * b for b in vector_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


intent_names = list(INTENTS.keys())
intent_texts = list(INTENTS.values())

intent_embeddings = create_embeddings(intent_texts)


QUERIES = [
    "product_not_received dispute evidence requirements",
    "product_not_received dispute policy",
    "what evidence is needed for a product not received dispute",
    "when is human review required",
    "what can the agent decide without human approval",
    "requirements before submitting dispute evidence",
]


for query in QUERIES:
    query_embedding = create_embedding(query)

    scores = []

    for intent_name, intent_text, intent_embedding in zip(
        intent_names,
        intent_texts,
        intent_embeddings,
    ):
        score = cosine_similarity(
            query_embedding,
            intent_embedding,
        )

        scores.append(
            (score, intent_name, intent_text)
        )

    scores.sort(reverse=True)

    print("\nQUERY:")
    print(query)

    print("\nMATCHES:")

    for score, intent_name, intent_text in scores:
        print(
            f"{score:.4f} | "
            f"{intent_name} | "
            f"{intent_text}"
        )