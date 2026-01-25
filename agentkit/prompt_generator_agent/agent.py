import asyncio
import threading
import os

from pydantic import BaseModel
from rocketmq.client import ConsumeStatus, ReceivedMessage
from typing_extensions import override
from veadk import Agent, Runner
from veadk.a2a.hub.rocketmq_middleware import (
    RocketMQAgentClient,
    RocketMQClient,
)


class A2AEvent(BaseModel):
    message: str
    description: str


prompt_generator = Agent(
    name="prompt_generator",
    description="Generate prompt for an agent",
    instruction=f"Generate prompt for an agent according to the user's message. Please response with a JSON object: {A2AEvent.model_json_schema()}. The message represents your final response, and the description should be a brief summary of what you did.",
    output_schema=A2AEvent,
)
prompt_generator_runner = Runner(agent=prompt_generator)

prompt_optimizer = Agent(
    name="prompt_optimizer",
    description="Optimize prompt for an agent",
    instruction=f"Optimize prompt for an agent according to the user's message. Please response with a JSON object: {A2AEvent.model_json_schema()}. The message represents your final response, and the description should be a brief summary of what you did.",
    output_schema=A2AEvent,
)
prompt_optimizer_runner = Runner(agent=prompt_optimizer)


rocketmq_client = RocketMQClient(
    name="rocketmq_client",
    producer_group=os.environ.get("ROCKETMQ_PRODUCER_GROUP", "GID_AGENTKIT"), # 在云端创建一个默认的生产者组
    name_server_addr=os.environ.get("ROCKETMQ_NAME_SERVER_ADDR", ""), # 消息队列公网地址
    access_key=os.environ.get("VOLCENGINE_ACCESS_KEY", ""),
    access_secret=os.environ.get("VOLCENGINE_SECRET_KEY", ""),
)


class PromptGeneratorRocketMQClient(RocketMQAgentClient):
    def __init__(
        self,
        agent: Agent,
        rocketmq_client: RocketMQClient,
        subscribe_topic: str,
        group: str,
    ):
        super().__init__(
            agent=agent,
            rocketmq_client=rocketmq_client,
            subscribe_topic=subscribe_topic,
            group=group,
        )

    @override
    def recv_msg_callback(self, msg: ReceivedMessage) -> ConsumeStatus:
        print(f"Receive message {msg.id}: {msg.body}")

        response = asyncio.run(
            prompt_generator_runner.run(msg.body.decode("utf-8"))
        )

        # After response generation, send the response to prompt optimizer's topic
        self.rocketmq_client.send_msg(topic="OptimizerTopic", msg_body=response)

        return ConsumeStatus.CONSUME_SUCCESS


class PromptOptimizerRocketMQClient(RocketMQAgentClient):
    def __init__(
        self,
        agent: Agent,
        rocketmq_client: RocketMQClient,
        subscribe_topic: str,
        group: str,
    ):
        super().__init__(
            agent=agent,
            rocketmq_client=rocketmq_client,
            subscribe_topic=subscribe_topic,
            group=group,
        )

    @override
    def recv_msg_callback(self, msg: ReceivedMessage) -> ConsumeStatus:
        print(f"Receive message {msg.id}: {msg.body}")

        response = asyncio.run(
            prompt_optimizer_runner.run(msg.body.decode("utf-8"))
        )

        print(f"Optimized prompt: {response}")
        return ConsumeStatus.CONSUME_SUCCESS


clients = [
    PromptGeneratorRocketMQClient(
        agent=prompt_generator,
        rocketmq_client=rocketmq_client,
        subscribe_topic="RequestTopic",
        group="RequestGroup",
    ),
    PromptOptimizerRocketMQClient(
        agent=prompt_optimizer,
        rocketmq_client=rocketmq_client,
        subscribe_topic="OptimizerTopic",
        group="OptimizerGroup",
    ),
]

threads = []

for client in clients:
    t = threading.Thread(
        target=client.listen,
        args=(),
        name=f"worker-{client.subscribe_topic}",
    )
    t.start()
    threads.append(t)

for t in threads:
    t.join()

