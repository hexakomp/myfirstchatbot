# mcpclient.py
import json
import asyncio
import sys
from openai import OpenAI

from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


def to_openai_tools(mcp_tools):
    return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.inputSchema,
            },
        }
        for tool in mcp_tools
    ]


def extract_tool_text(result):
    if hasattr(result, "content") and result.content:
        parts = []
        for item in result.content:
            if hasattr(item, "text"):
                parts.append(item.text)
            else:
                parts.append(str(item))
        return "\n".join(parts)
    return str(result)


async def run():
    params = StdioServerParameters(
        command=sys.executable,
        args=["mcpserver.py"],
    )

    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools_result = await session.list_tools()
            print("Available tools:", [tool.name for tool in tools_result.tools])
            openai_tools = to_openai_tools(tools_result.tools)

            messages = [
                {"role": "user", "content": "what is the capital of India ?"}
            ]

            while True:
                response = client.chat.completions.create(
                    model="functiongemma:latest",
                    messages=messages,
                    tools=openai_tools,
                    tool_choice="auto",
                )

                msg = response.choices[0].message

                if msg.tool_calls:
                    messages.append(
                        {
                            "role": "assistant",
                            "content": msg.content or "",
                            "tool_calls": [
                                {
                                    "id": tc.id,
                                    "type": "function",
                                    "function": {
                                        "name": tc.function.name,
                                        "arguments": tc.function.arguments,
                                    },
                                }
                                for tc in msg.tool_calls
                            ],
                        }
                    )

                    for call in msg.tool_calls:
                        args = json.loads(call.function.arguments)

                        result = await session.call_tool(
                            call.function.name,
                            args
                        )

                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": call.id,
                                "content": extract_tool_text(result),
                            }
                        )
                    continue

                print(msg.content)
                break


if __name__ == "__main__":
    asyncio.run(run())