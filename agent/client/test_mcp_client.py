import os
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_groq import ChatGroq

load_dotenv()

async def main():
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
            "Do not attempt to call other tools."
        )
    )

    print("Tools loaded from MCP server:", tools)

    response = await agent.ainvoke(
        {"messages": [
            {"role": "user", "content": "Restart the docker container incident-app"}
        ]}
    )

    print(response)

if __name__ == "__main__":
    asyncio.run(main())