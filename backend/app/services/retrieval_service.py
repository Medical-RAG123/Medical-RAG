def retrieve_top5(question):

    semantic_results = semantic_search(question)

    bm25_results = bm25_search(question)

    rrf_results = rrf(semantic_results, bm25_results)

    reranked_results = reranker(question, rrf_results)

    return reranked_results[:5]
