# incident_consumer_agent_async.py
import os, asyncio, json
from dotenv import load_dotenv
import aio_pika
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_groq import ChatGroq

load_dotenv()

async def handle_incident(agent, payload):
    response = await agent.ainvoke(
        {"messages": [
            {
                "role": "user",
                "content": f"Incident payload received: {json.dumps(payload)}. "
                           f"Take appropriate action using available tools."
            }
        ]}
    )
    print("\n🤖 Agent Response:", response)

async def setup_agent():
    client = MultiServerMCPClient(
        {
            "incidentops": {
                "transport": "stdio",
                "command": "python",
                "args": ["C:\\Users\\Aditya\\Desktop\\Incident-AIOPS\\agent\\server\\mcp_server.py"],
            }
        }
    )
    tools = await client.get_tools()
    chat_model = ChatGroq(model=os.getenv("LLM_MODEL", "llama-3.1-8b-instant"))
    agent = create_agent(
        chat_model,
        tools,
        system_prompt=(
            "You are an automation agent. "
            "You ONLY have access to the tool 'restartdockercontainer'. "
            "When an incident payload is received, analyze it and decide "
            "whether to restart the container. Do not attempt to call other tools."
        )
    )
    print("Tools loaded from MCP server:", tools)
    return agent

async def main():
    agent = await setup_agent()

    # Async RabbitMQ connection
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()
    queue = await channel.declare_queue("incidents", durable=True)

    print("🚀 Incident consumer started...")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                payload = json.loads(message.body.decode())
                print("\n🔥 INCIDENT EVENT RECEIVED")
                print("Payload:", payload)
                await handle_incident(agent, payload)

if __name__ == "__main__":
    asyncio.run(main())