import os

from crewai import LLM

llm_chatOpenAi = LLM(
    model="gpt-4",
    temperature=0.5,
    max_tokens=150,
    top_p=0.9,
    frequency_penalty=0.1,
    presence_penalty=0.1,
    stop=["END"],
    seed=42,
)

llm_google_gemini = LLM(model="gemini/gemini-1.5-pro-latest", temperature=0.5)

llm_anthropic = LLM(model="anthropic/claude-3-sonnet-20240229-v1:0", temperature=0.5)

llm_groq_llama_3 = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.5)


# TODO: - Add the following models of huggingface llm

# llm_haggingsface = LLM(
#     model="huggingface/meta-llama/Meta-Llama-3.1-8B-Instruct",
#     base_url="https://api-inference.huggingface.co",
#     api_key=os.getenv("HUGGINGFACE_API_KEY"),
# )
