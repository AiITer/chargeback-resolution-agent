from haystack.components.query import QueryExpander
from haystack_integrations.components.generators.ollama import OllamaChatGenerator

from app.config import settings

from app.rag.retrieval import search_knowledge


generator = OllamaChatGenerator(
    model=settings.ollama_model,
    url=settings.ollama_base_url,
    generation_kwargs={"temperature": 0.0},
    response_format="json",
    think=False,
)

expander = QueryExpander(
    chat_generator=generator,
    n_expansions=3,
    include_original_query=True,
)

queries = [
    "product_not_received dispute handling policy and evidence submission requirements",
    "product_not_received dispute evidence requirements and handling procedures",
    "Northstar Commerce Inc. chargeback policy: product_not_received dispute evidence requirements",
]

for query in queries:
    print("\n" + "=" * 80)
    print("ORIGINAL:")
    print(query)

    result = expander.run(query=query)

    for expanded_query in result["queries"]:
        print("\nQUERY:")
        print(expanded_query)

        retrieval_results = search_knowledge(
            expanded_query,
            top_k=5,
        )

        print("TOP 5:")

        for rank, retrieval_result in enumerate(
            retrieval_results,
            start=1,
        ):
            print(
                f"{rank}. "
                f"{retrieval_result.section} | "
                f"{retrieval_result.cosine_distance:.4f}"
            )