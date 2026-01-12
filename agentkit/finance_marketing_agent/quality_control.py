import logging
from typing import Dict, List, Any
from dataclasses import dataclass

# 设置日志
logger = logging.getLogger(__name__)

@dataclass
class QualityScore:
    """质量评分数据类"""
    relevance_score: float  # 相关性评分 (0-100)
    creativity_score: float  # 创意性评分 (0-100)
    clarity_score: float  # 清晰度评分 (0-100)
    compliance_score: float  # 合规性评分 (0-100)
    overall_score: float  # 总体评分 (0-100)


def evaluate_marketing_material_quality(material_data: Dict[str, Any]) -> QualityScore:
    """
    评估营销素材的质量
    
    参数:
    material_data: 包含营销素材信息的字典，包括素材内容、生成要求等
    
    返回:
    QualityScore: 质量评分对象
    """
    try:
        logger.info(f"开始评估营销素材质量: {material_data.get('id', '未知素材')}")
        
        # 1. 相关性评估
        relevance_score = evaluate_relevance(material_data)
        
        # 2. 创意性评估
        creativity_score = evaluate_creativity(material_data)
        
        # 3. 清晰度评估
        clarity_score = evaluate_clarity(material_data)
        
        # 4. 合规性评估
        compliance_score = evaluate_compliance(material_data)
        
        # 计算总体评分
        overall_score = calculate_overall_score(
            relevance_score, 
            creativity_score, 
            clarity_score, 
            compliance_score
        )
        
        quality_score = QualityScore(
            relevance_score=relevance_score,
            creativity_score=creativity_score,
            clarity_score=clarity_score,
            compliance_score=compliance_score,
            overall_score=overall_score
        )
        
        logger.info(f"营销素材质量评估完成，总体评分: {overall_score:.1f}")
        return quality_score
        
    except Exception as e:
        logger.error(f"评估营销素材质量时发生错误: {str(e)}", exc_info=True)
        # 返回默认评分
        return QualityScore(
            relevance_score=50.0,
            creativity_score=50.0,
            clarity_score=50.0,
            compliance_score=50.0,
            overall_score=50.0
        )


def evaluate_relevance(material_data: Dict[str, Any]) -> float:
    """评估素材与需求的相关性"""
    # 简化实现，实际项目中可以使用更复杂的算法
    return 85.0


def evaluate_creativity(material_data: Dict[str, Any]) -> float:
    """评估素材的创意性"""
    # 简化实现，实际项目中可以使用更复杂的算法
    return 80.0


def evaluate_clarity(material_data: Dict[str, Any]) -> float:
    """评估素材的清晰度"""
    # 简化实现，实际项目中可以使用更复杂的算法
    return 90.0


def evaluate_compliance(material_data: Dict[str, Any]) -> float:
    """评估素材的合规性"""
    # 简化实现，实际项目中可以使用更复杂的算法
    return 95.0


def calculate_overall_score(
    relevance_score: float, 
    creativity_score: float, 
    clarity_score: float, 
    compliance_score: float
) -> float:
    """计算总体评分"""
    # 权重分配
    weights = {
        'relevance': 0.3,
        'creativity': 0.2,
        'clarity': 0.25,
        'compliance': 0.25
    }
    
    overall_score = (
        relevance_score * weights['relevance'] +
        creativity_score * weights['creativity'] +
        clarity_score * weights['clarity'] +
        compliance_score * weights['compliance']
    )
    
    return round(overall_score, 1)


def is_high_quality(quality_score: QualityScore, threshold: float = 70.0) -> bool:
    """
    检查素材是否为高质量
    
    参数:
    quality_score: 质量评分对象
    threshold: 高质量阈值 (默认70.0)
    
    返回:
    bool: 是否为高质量素材
    """
    return quality_score.overall_score >= threshold


def filter_high_quality_materials(
    materials: List[Dict[str, Any]], 
    threshold: float = 70.0
) -> List[Dict[str, Any]]:
    """
    过滤出高质量的营销素材
    
    参数:
    materials: 营销素材列表
    threshold: 高质量阈值
    
    返回:
    List[Dict[str, Any]]: 高质量素材列表
    """
    high_quality_materials = []
    
    for material in materials:
        quality_score = evaluate_marketing_material_quality(material)
        if is_high_quality(quality_score, threshold):
            material['quality_score'] = quality_score.__dict__
            high_quality_materials.append(material)
    
    logger.info(f"从 {len(materials)} 个素材中筛选出 {len(high_quality_materials)} 个高质量素材")
    return high_quality_materials
