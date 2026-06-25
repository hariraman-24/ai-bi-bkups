from llm_engine import LLMEngine
llm = LLMEngine()
question = "show sales data"
result = llm.ask_llm(question)

print("LLM Response:", result)