import pytest
from quality_control import (
    evaluate_marketing_material_quality,
    QualityScore,
    is_high_quality,
    filter_high_quality_materials,
    calculate_overall_score
)


def test_calculate_overall_score():
    """测试总体评分计算"""
    overall_score = calculate_overall_score(80, 70, 90, 85)
    assert overall_score == 82.3
    
    # 测试权重分配
    overall_score = calculate_overall_score(100, 0, 0, 0)
    assert overall_score == 30.0
    
    overall_score = calculate_overall_score(0, 100, 0, 0)
    assert overall_score == 20.0
    
    overall_score = calculate_overall_score(0, 0, 100, 0)
    assert overall_score == 25.0
    
    overall_score = calculate_overall_score(0, 0, 0, 100)
    assert overall_score == 25.0


def test_is_high_quality():
    """测试是否为高质量素材"""
    # 创建高质量评分
    high_score = QualityScore(
        relevance_score=80.0,
        creativity_score=75.0,
        clarity_score=90.0,
        compliance_score=85.0,
        overall_score=82.3
    )
    
    # 创建低质量评分
    low_score = QualityScore(
        relevance_score=50.0,
        creativity_score=45.0,
        clarity_score=60.0,
        compliance_score=55.0,
        overall_score=52.5
    )
    
    assert is_high_quality(high_score) is True
    assert is_high_quality(low_score) is False
    
    # 测试自定义阈值
    assert is_high_quality(high_score, threshold=90.0) is False
    assert is_high_quality(low_score, threshold=50.0) is True


def test_evaluate_marketing_material_quality():
    """测试营销素材质量评估"""
    # 准备测试数据
    material_data = {
        "id": "test_material_001",
        "content": {
            "generated_images": ["https://example.com/image1.jpg"],
            "description": "测试营销素材"
        },
        "generation_request": "生成信用卡营销图片"
    }
    
    # 执行评估
    quality_score = evaluate_marketing_material_quality(material_data)
    
    # 验证结果类型
    assert isinstance(quality_score, QualityScore)
    
    # 验证评分范围
    assert 0 <= quality_score.relevance_score <= 100
    assert 0 <= quality_score.creativity_score <= 100
    assert 0 <= quality_score.clarity_score <= 100
    assert 0 <= quality_score.compliance_score <= 100
    assert 0 <= quality_score.overall_score <= 100


def test_filter_high_quality_materials():
    """测试高质量素材筛选"""
    # 准备测试数据
    materials = [
        {
            "id": "material_001",
            "content": {
                "generated_images": ["https://example.com/image1.jpg"],
                "description": "高质量素材"
            }
        },
        {
            "id": "material_002",
            "content": {
                "generated_images": ["https://example.com/image2.jpg"],
                "description": "低质量素材"
            }
        }
    ]
    
    # 执行筛选
    high_quality_materials = filter_high_quality_materials(materials)
    
    # 验证结果
    assert len(high_quality_materials) >= 0
    assert all("quality_score" in material for material in high_quality_materials)
    assert all(isinstance(material["quality_score"], dict) for material in high_quality_materials)
    
    # 测试不同阈值
    strict_high_quality = filter_high_quality_materials(materials, threshold=90.0)
    lenient_high_quality = filter_high_quality_materials(materials, threshold=50.0)
    
    assert len(strict_high_quality) <= len(lenient_high_quality)


def test_quality_score_dataclass():
    """测试质量评分数据类"""
    # 创建质量评分实例
    score = QualityScore(
        relevance_score=85.5,
        creativity_score=78.2,
        clarity_score=92.0,
        compliance_score=89.5,
        overall_score=86.3
    )
    
    # 验证属性
    assert score.relevance_score == 85.5
    assert score.creativity_score == 78.2
    assert score.clarity_score == 92.0
    assert score.compliance_score == 89.5
    assert score.overall_score == 86.3
    
    # 验证转换为字典
    score_dict = score.__dict__
    assert isinstance(score_dict, dict)
    assert score_dict["relevance_score"] == 85.5
    assert score_dict["overall_score"] == 86.3
