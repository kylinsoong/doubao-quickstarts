import asyncio
import json
import re
import os
from byteLLM import ByteLLM
from mcp_client_demo import MCPClient

api_key = os.environ.get("ARK_API_KEY")
model_id = os.environ.get("ARK_API_ENGPOINT_ID")



def extract_json_from_response_content(content):
    """
    提取 LLM 返回的content内容，解析JSON结构，拿出tool信息
    """
    # 如果已经是 dict，直接返回
    if isinstance(content, dict):
        return content

    # 清除 markdown ```json ``` 包裹
    if isinstance(content, str):
        content = re.sub(r"^```(?:json)?|```$", "", content.strip(), flags=re.IGNORECASE).strip()

    # 最多尝试 3 层 json.loads 解码
    for _ in range(3):
        try:
            parsed = json.loads(content)
            if isinstance(parsed, dict):
                return parsed
            else:
                content = parsed  # 如果解出来还是 str，继续下一层
        except Exception:
            break

    # 如果最终不是 dict，返回原始字符串（表示是普通答复）
    return content


llm = ByteLLM(model=model_id, api_key=api_key)


async def main():
    # === 初始化 MCP 客户端 ===
    client = MCPClient()
    await client.__aenter__()

    tools = await client.list_tools()

    # resources = await client.list_resources()
    tool_names = [t.name for t in tools.tools]

    tool_descriptions = "\n".join(f"- 工具名称：{t.name} \n工具描述：{t.description} \n入参要求：{t.inputSchema}" for t in tools.tools)
    # resource_descriptions = "\n".join(f"- {r.uri}" for r in resources.resources)

    while True:
        # === Step 1. 用户 → MCP host：提出问题 ===
        user_input = input("\n请输入你的问题（输入 exit 退出）：\n> ")
        if user_input.lower() in ("exit", "退出"):
            break

        system_prompt = f'''
你是一个智能助手，拥有以下工具可以调用：

# 工具列表
{tool_descriptions}

# 注意事项
1，请优先判断是否使用【工具列表】中的工具，如使用工具，则返回格式为：
    {{"tool_calls": 
        [
            {{"name": "xxx", "arguments": {{"xxx": "xxx"}}}}
        ]
    }}
    其中arguments格式务必与工具的【入参要求】保持一致
2，不要捏造不存在的工具
3，如无需使用工具，则结合上下文回复用户最终结果
4，如果使用工具，只返回JSON格式，不要解释
'''

        # === 构造 LLM 上下文消息 ===
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        final_reply = ""

        # === 循环处理 tool_calls，直到 LLM 给出最终 content 为止 ===
        while True:
            # === Step 1. MCP host → LLM：转发上下文 ===
            print("******************* new round *****************")
            response = llm.generate(messages)

            if hasattr(response, "reasoning_content"):
                print(f"\n！！！LLM 思考：\n{response.reasoning_content}")


            messages.append({
                "role":"assistant",
                "content": response.content
            })

            # === Step 2. 解析 JSON 格式回复（或普通字符串） ===
            parsed = extract_json_from_response_content(response.content)

            # === 如果是普通自然语言字符串，说明 LLM 已直接答复用户 ===
            if isinstance(parsed, str):
                final_reply = parsed
                print("*********************这里表明模型不再调用工具，准备最终返回结果*************************")
                break

            # === 如果是字典，判断是否包含工具调用 ===
            tool_calls = parsed.get("tool_calls")
            if not tool_calls:
                # LLM 给出普通答复结构（带 content 字段）
                final_reply = parsed
                break

            # === 遍历 LLM 请求的工具调用列表 ===
            for tool_call in tool_calls:
                # === Step 3. LLM → MCP客户端：请求使用工具 ===
                tool_name = tool_call["name"]
                arguments = tool_call["arguments"]

                if tool_name not in tool_names:
                    raise ValueError(f"工具 {tool_name} 未注册")

                # === Step 4. MCP客户端 → MCP服务器：调用工具 ===
                print(f"\n！！！调用工具 {tool_name} 参数: {arguments}")
                result = await client.call_tool(tool_name, arguments)

                # === Step 5. MCP服务器 → MCP客户端：返回结果 ===
                tool_output = result.content[0].text
                print(f"\n！！！工具 {tool_name} 返回：{tool_output}")

                messages.append({
                    "role": "user",
                    "content":  f'调用工具：{tool_name} \n调用结果：{tool_output}'
                })

        # === Step 6. MCP主机 → 用户：最终结果答复 ===
        print(f"\n🎯 最终答复：{final_reply}")

    await client.__aexit__(None, None, None)


if __name__ == "__main__":
    asyncio.run(main())
