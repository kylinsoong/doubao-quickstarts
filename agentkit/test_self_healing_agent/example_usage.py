#!/usr/bin/env python3
"""
Example usage of the content design loop agent

This script demonstrates how to use the content design loop agent
which includes a write agent and an evaluation agent.
"""

import asyncio

from veadk import Runner
from veadk.memory.short_term_memory import ShortTermMemory
from veadk.utils.logger import get_logger

from agent import root_agent

logger = get_logger(__name__)


async def main():
    """Main function to demonstrate the content design loop agent."""
    logger.info("=== Starting Content Design Loop Agent Demo ===")
    
    # Configuration
    app_name = "content_design_app"
    user_id = "content_design_user"
    session_id = "content_design_session"
    
    # Create short-term memory
    short_term_memory = ShortTermMemory()
    
    # Create runner
    runner = Runner(
        agent=root_agent,
        short_term_memory=short_term_memory,
        app_name=app_name,
        user_id=user_id,
    )
    
    # Run the agent with a sample query
    logger.info("Running content design loop agent...")
    try:
        response = await runner.run(
            messages="请撰写一篇关于人工智能在文案设计中的应用的文档",
            session_id=session_id,
        )
        
        logger.info(f"\n=== Final Result ===")
        logger.info(f"{response}")
    except Exception as e:
        logger.error(f"Error during agent execution: {e}")
    
    logger.info("=== Content Design Loop Agent Demo Completed ===")


if __name__ == "__main__":
    asyncio.run(main())
