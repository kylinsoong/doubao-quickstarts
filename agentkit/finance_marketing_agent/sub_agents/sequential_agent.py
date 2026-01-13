import asyncio
import logging
from typing import List, Dict, Any

from prompts import SEQUENTIAL_SERVICE_AGENT_PROMPT
from sub_agents.search_kb import search_kb_agent
from sub_agents.edit_image import edit_image_agent
from sub_agents.pre_process import pre_process_agent
from veadk import Runner
from veadk.agents.sequential_agent import SequentialAgent

# 导入质量控制模块
from quality_control import (
    evaluate_marketing_material_quality,
    filter_high_quality_materials,
    QualityScore
)

# 设置日志
logger = logging.getLogger(__name__)


class EnhancedSequentialAgent(SequentialAgent):
    """增强版串行智能体，添加了质量控制功能"""
    
    async def run(self, messages: Any, **kwargs) -> Any:
        """
        重写run方法，添加质量控制步骤
        """
        try:
            logger.info(f"{self.name} 开始处理请求")
            
            # 调用父类的run方法执行原始工作流
            result = await super().run(messages, **kwargs)
            
            # 添加质量控制步骤
            logger.info(f"{self.name} 执行质量控制")
            
            # 检查结果类型并进行质量评估
            if isinstance(result, dict) and "generated_images" in result:
                # 构造素材数据用于质量评估
                material_data = {
                    "id": f"material_{hash(str(result))}",
                    "content": result,
                    "generation_request": messages
                }
                
                # 评估质量
                quality_score = evaluate_marketing_material_quality(material_data)
                result["quality_score"] = quality_score.__dict__
                
                # 记录质量评分
                logger.info(f"素材质量评分: {quality_score.overall_score}")
                
                # 如果质量评分低于阈值，可以考虑重新生成或过滤
                if quality_score.overall_score < 70.0:
                    logger.warning(f"素材质量评分较低 ({quality_score.overall_score}), 建议优化")
            
            logger.info(f"{self.name} 请求处理完成")
            return result
            
        except Exception as e:
            logger.error(f"{self.name} 处理请求时发生错误: {str(e)}", exc_info=True)
            raise


# 创建增强版串行智能体
sequential_service_agent = EnhancedSequentialAgent(
    name="sequential_service_agent",
    description="消费金融营销助手串行总控，负责按顺序协调子智能体工作，并进行质量控制",
    instruction=SEQUENTIAL_SERVICE_AGENT_PROMPT,
    sub_agents=[pre_process_agent, search_kb_agent, edit_image_agent],
    version="1.0.0",
)

logger.info("增强版串行智能体初始化成功")
