def build_prompt(question, context):

    return f"""
You are a helpful assistant.

Answer the question using only the provided context.

Context:
{context}

Question:
{question}

Provide a clear and accurate answer.
"""
