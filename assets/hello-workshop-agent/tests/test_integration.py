"""Integration test for the Hello Workshop Agent end-to-end flow."""
import sys
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

# Add app/ to sys.path so agent module can be imported as peer-level
APP_PATH = str(Path(__file__).parent.parent / "app")
if APP_PATH not in sys.path:
    sys.path.insert(0, APP_PATH)

# Mock sap_cloud_sdk submodules not available in test env
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
async def test_agent_invoke_greeting():
    """Test end-to-end agent invoke for a greeting request."""
    from agent import SampleAgent

    agent = SampleAgent()

    with patch.object(agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = {
            "messages": [MagicMock(content="Welcome to the workshop, Alice!")]
        }
        response = await agent.invoke("Please greet Alice", "test-context-001")

    assert response.status == "completed"
    assert len(response.message) > 0


@pytest.mark.asyncio
async def test_agent_stream_question():
    """Test end-to-end agent stream for a question."""
    from agent import SampleAgent

    agent = SampleAgent()

    with patch.object(agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = {
            "messages": [MagicMock(content="The workshop starts at 9 AM.")]
        }
        chunks = []
        async for chunk in agent.stream("When does the workshop start?", "test-context-002"):
            chunks.append(chunk)

    assert len(chunks) > 0
    final = chunks[-1]
    assert final["is_task_complete"] is True
    assert len(final["content"]) > 0
