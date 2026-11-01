from utcp.utcp_client import UtcpClient
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_utcp_adapters import load_utcp_tools
from dotenv import load_dotenv

from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

import os

print("Google API KEY : "+os.getenv("GOOGLE_API_KEY")[:4]+10*"*")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

from langchain_core.tools import StructuredTool

def normalize_tools(tools):
    normalized = []

    for original in tools:
        alias = original.name.replace(".", "_")

        async def execute(_tool=original, **kwargs):
            return await _tool.ainvoke(kwargs)

        normalized.append(
            StructuredTool.from_function(
                coroutine=execute,
                name=alias,
                description=original.description,
                args_schema=original.args_schema,
            )
        )

    return normalized


async def build_agent():
    client = await UtcpClient.create(config={
        "manual_call_templates": [
            {
                "name": "commerce",
                "call_template_type": "http",
                "url": "http://localhost:8000/openapi.json",
                "http_method": "GET"
            }
        ]
    })

    # Discover tools
    # tools = await client.search_tools(
    #     "get order status",
    #     limit=1
    # )

    # for tool in tools:
    #     print("Discovered:", tool.name)

    # Direct native HTTP execution through UTCP
    result = await client.call_tool(
        tool_name="commerce.get_order_status",
        tool_args={"order_id": 101}
    )

    print("Result:", result)

    tools = await load_utcp_tools(client)

    for tool in tools:
        print("Before Normalization")
        print(tool.name)
        print(tool.args)

    tools = normalize_tools(tools)

    for tool in tools:
            print("After normalization")
            print(tool.name)
            print(tool.args)


    tool_agent = create_agent(
        model=llm,
        tools=tools,
        checkpointer=InMemorySaver()
    )

    return tool_agent


