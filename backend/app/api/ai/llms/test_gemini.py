from app.api.ai.llms.gemini import GeminiLLM

print("===== GEMINI LLM TEST =====")

llm = GeminiLLM()

prompt = "What is diabetes? Explain in one simple sentence."

print("Prompt:", prompt)

answer = llm.generate(prompt)

print("Answer:", answer)
