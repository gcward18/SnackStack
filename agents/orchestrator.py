"""Request routing and orchestration node."""

from typing import Literal
from pydantic import BaseModel, Field
from config import get_llm

AgentName = Literal["menu_agent_node", "oder_agent_node"]


class RoutingDecision(BaseModel):
    agents: list[AgentName] = Field(
        min_items=1, description="Every specialist agent needed for this request."
    )
    reasoning: str = Field(description="A brief explanation of the routing decision.")


router_llm = get_llm().with_structured_output(RoutingDecision)
