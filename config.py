"""LLM, embedding model, and OpenAI client configuration."""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()


def get_llm() -> ChatOpenAI:
    return ChatOpenAI(model="gpt-4o")


def get_embedding() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(model="text-embedding-3-small")
