"""LLM, embedding model, and OpenAI client configuration."""

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pydantic import SecretStr

load_dotenv()

api_key: SecretStr |  () | None  = os.environ.get("OPENAI_API_KEY", "")


def get_llm() -> ChatOpenAI:
    return ChatOpenAI(model="gpt-4o", api_key=api_key)


def get_embedding() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key)
