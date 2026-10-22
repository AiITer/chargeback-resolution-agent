from haystack.components.query import QueryExpander
from haystack_integrations.components.generators.ollama import OllamaChatGenerator

from app.config import settings

from app.rag.retrieval import search_knowledge

from haystack import Document
from haystack_integrations.components.rankers.sentence_transformers import (
    SentenceTransformersSimilarityRanker,
)


generator = OllamaChatGenerator(
    model=settings.ollama_model,
    url=settings.ollama_base_url,
    generation_kwargs={"temperature": 0.0},
    response_format="json",
    think=False,
)

QUERY_EXPANSION_PROMPT = """
You are preparing search queries for a retrieval system.

Given the original query:
"{{ query }}"

Generate {{ n_expansions }} alternative search queries.

Requirements:
- Preserve the user's exact information need.
- Remove organization names, knowledge-base names, and generic framing
  when they are only context rather than the search target.
- Do not broaden the topic.
- Do not introduce related but different concepts.
- Each query should be independently useful for semantic retrieval.

Return JSON only:
{"queries": ["query1", "query2", "query3"]}
"""

expander = QueryExpander(
    chat_generator=generator,
    prompt_template=QUERY_EXPANSION_PROMPT,
    n_expansions=3,
    include_original_query=True,
)

ranker = SentenceTransformersSimilarityRanker()
ranker.warm_up()

queries = [
    "product_not_received dispute handling policy and evidence submission requirements",
    # "product_not_received dispute evidence requirements and handling procedures",
    # "Northstar Commerce Inc. chargeback policy: product_not_received dispute evidence requirements",
]

for query in queries:
    print("\n" + "=" * 80)
    print("ORIGINAL:")
    print(query)

    expansion_result = expander.run(query=query)

    candidates_by_chunk_id = {}

    for expanded_query in expansion_result["queries"]:
        print("\nEXPANDED QUERY:")
        print(expanded_query)

        retrieval_results = search_knowledge(
            expanded_query,
            top_k=5,
        )

        for result in retrieval_results:
            candidates_by_chunk_id[result.chunk_id] = result

    candidate_documents = [
        Document(
            id=str(result.chunk_id),
            content=result.content,
            meta={
                "section": result.section,
                "source": result.source,
                "chunk_id": result.chunk_id,
            },
        )
        for result in candidates_by_chunk_id.values()
    ]

    reranked = ranker.run(
        query=query,
        documents=candidate_documents,
        top_k=5,
    )

    print("\nRERANKED TOP 5:")

    for rank, document in enumerate(
        reranked["documents"],
        start=1,
    ):
        print(
            f"{rank}. "
            f"{document.meta['section']} | "
            f"{document.score:.4f}"
        )