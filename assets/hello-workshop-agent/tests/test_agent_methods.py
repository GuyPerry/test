"""Additional tests for agent methods to improve coverage."""
import sys
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from litellm.exceptions import APIConnectionError

APP_PATH = str(Path(__file__).parent.parent / "app")
if APP_PATH not in sys.path:
    sys.path.insert(0, APP_PATH)

import types
for mod_name in [
    "sap_cloud_sdk.agent_memory",
    "sap_cloud_sdk.agent_memory.factory",
    "sap_cloud_sdk.agent_memory.factory.langgraph_checkpoint",
]:
    if mod_name not in sys.modules:
        sys.modules[mod_name] = types.ModuleType(mod_name)

mock_checkpointer = MagicMock()
sys.modules["sap_cloud_sdk.agent_memory.factory.langgraph_checkpoint"].create_checkpointer = (
    lambda ttl_seconds=None: mock_checkpointer
)


@pytest.mark.asyncio
async def test_agent_stream_exception_handling():
    """Test that stream handles exceptions gracefully."""
    from agent import SampleAgent

    agent = SampleAgent()

    with patch.object(agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.side_effect = Exception("Unexpected error")
        chunks = []
        async for chunk in agent.stream("test query", "test-context-error"):
            chunks.append(chunk)

    final = chunks[-1]
    assert final["is_task_complete"] is True
    assert "error" in final["content"].lower()


@pytest.mark.asyncio
async def test_agent_invoke_error_state():
    """Test that invoke returns completed status even when agent encounters an error internally."""
    from agent import SampleAgent

    agent = SampleAgent()

    with patch.object(agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.side_effect = Exception("LLM unavailable")
        response = await agent.invoke("test query", "test-context-err")

    # Agent catches exceptions and returns a friendly error message with completed status
    assert response.status in ("completed", "error")
    assert len(response.message) > 0


@pytest.mark.asyncio
async def test_agent_invoke_with_fallback_success():
    """Test _invoke_with_fallback succeeds with primary model."""
    from agent import SampleAgent

    agent = SampleAgent()
    mock_graph = AsyncMock()
    mock_graph.ainvoke.return_value = {
        "messages": [MagicMock(content="Hello from primary model")]
    }

    with patch.object(agent, "_create_graph", return_value=mock_graph):
        result = await agent._invoke_with_fallback(
            tools=[],
            system_prompt="test prompt",
            query="hello",
            context_id="ctx-1",
        )

    assert "messages" in result


@pytest.mark.asyncio
async def test_agent_invoke_with_fallback_uses_fallback_on_connection_error():
    """Test _invoke_with_fallback uses fallback when primary fails with APIConnectionError."""
    from agent import SampleAgent

    agent = SampleAgent()
    agent._fallback_llm = MagicMock()  # Enable fallback
    agent._fallback_model = "fallback-model"

    mock_primary_graph = AsyncMock()
    mock_primary_graph.ainvoke.side_effect = APIConnectionError(
        message="Connection refused", llm_provider="openai", model="gpt-4"
    )

    mock_fallback_graph = AsyncMock()
    mock_fallback_graph.ainvoke.return_value = {
        "messages": [MagicMock(content="Hello from fallback")]
    }

    call_count = {"count": 0}

    def create_graph_side_effect(llm, tools, system_prompt):
        call_count["count"] += 1
        if call_count["count"] == 1:
            return mock_primary_graph
        return mock_fallback_graph

    with patch.object(agent, "_create_graph", side_effect=create_graph_side_effect):
        result = await agent._invoke_with_fallback(
            tools=[],
            system_prompt="test prompt",
            query="hello",
            context_id="ctx-fallback",
        )

    assert "messages" in result
