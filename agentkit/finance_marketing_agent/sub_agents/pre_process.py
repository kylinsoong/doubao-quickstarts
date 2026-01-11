from veadk import Agent
from prompts import PRE_PROCESS_AGENT_PROMPT

pre_process_agent = Agent(
    name="pre_process_agent",
    description="消费金融营销助手，负责从用户问题中提取查询知识库的Query信息，以及获取生成营销素材的相关的要求",
    instruction=PRE_PROCESS_AGENT_PROMPT,
) 
