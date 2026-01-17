# Adaptive Self-Healing Loop Agent

基于 `veadk.agents.loop_agent.LoopAgent` 实现的自适应自我修正、自我优化的智能体。

## 功能特性

### 1. 自适应状态管理
- 增强的状态跟踪（`AdaptiveLoopAgentState`）
- 实时监控执行成功率、执行时间和错误计数
- 动态调整学习率和探索率

### 2. 自我评估机制
- 每次迭代后自动评估性能
- 基于事件内容和执行时间判断成功与否
- 计算近期成功率趋势

### 3. 自我修正功能
- 当检测到低成功率时自动调整参数
- 对失败的子代理进行针对性调整
- 性能下降时自动重置参数

### 4. 自我优化功能
- 基于成功率动态调整执行策略
- 自动优化子代理执行顺序
- 定期引入探索机制以保持多样性

### 5. 子代理性能跟踪
- 实时监控每个子代理的执行情况
- 记录成功率、执行时间等关键指标
- 基于性能数据自动调整子代理优先级

## 核心实现

### 1. AdaptiveLoopAgentState
增强的状态类，用于跟踪智能体的自适应参数和性能指标：

```python
class AdaptiveLoopAgentState(GoogleLoopAgentState):
    # 自我评估指标
    success_rate: float = 1.0        # 近期执行成功率
    avg_execution_time: float = 0.0  # 平均执行时间
    error_count: int = 0             # 错误计数
    
    # 自我优化参数
    learning_rate: float = 0.1       # 自适应调整学习率
    exploration_rate: float = 0.2    # 探索新配置的概率
    
    # 子代理性能跟踪
    sub_agent_performance: Dict[str, Dict[str, Any]] = {}  # 子代理性能指标
```

### 2. 主要方法

#### _pre_iteration_adjustment
迭代前的自适应调整，包括：
- 调整探索率（随时间降低）
- 基于错误率调整学习率
- 优化子代理顺序

#### _update_sub_agent_performance
更新子代理的性能指标，包括：
- 成功计数和错误计数
- 总执行时间和平均执行时间
- 成功率计算

#### _self_assess_and_correct
自我评估和修正的核心方法：
1. 评估当前迭代的性能
2. 更新全局性能指标
3. 必要时执行自我修正
4. 执行自我优化

#### _optimize_sub_agent_order
基于性能自动优化子代理的执行顺序：
- 按成功率降序排序
- 相同成功率下按执行时间升序排序

## 使用方法

### 基本用法

```python
from veadk import Agent
from adaptive_loop_agent import AdaptiveLoopAgent

# 创建子代理
judge_agent = Agent(
    name="judge_agent",
    description="负责评价客服回复",
    instruction=JUDGE_AGENT_PROMPT,
)

refine_agent = Agent(
    name="refine_agent",
    description="负责优化客服回复",
    instruction=REFINE_AGENT_PROMPT,
)

# 创建自适应循环智能体
adaptive_agent = AdaptiveLoopAgent(
    name="adaptive_refine_agent",
    description="自适应客服回复优化智能体",
    instruction=ADAPTIVE_INSTRUCTION,
    sub_agents=[judge_agent, refine_agent],
    max_iterations=5,  # 最大迭代次数
)

# 使用Runner运行智能体
from veadk import Runner
from veadk.memory.short_term_memory import ShortTermMemory

runner = Runner(
    agent=adaptive_agent,
    short_term_memory=ShortTermMemory(),
    app_name="adaptive_demo",
    user_id="demo_user",
)

# 运行智能体
response = await runner.run(
    messages="用户问题和客服回复...",
    session_id="demo_session",
)
```

### 自定义配置

#### 调整自适应参数
```python
# 创建智能体时调整初始参数
adaptive_agent = AdaptiveLoopAgent(
    # ... 其他参数 ...
    max_iterations=10,
    # 初始状态将包含这些参数
)
```

#### 扩展自我修正逻辑
```python
class CustomAdaptiveLoopAgent(AdaptiveLoopAgent):
    async def _perform_self_correction(self, agent_state, assessment, iteration):
        # 调用父类的自我修正逻辑
        await super()._perform_self_correction(agent_state, assessment, iteration)
        
        # 添加自定义的自我修正逻辑
        if assessment["execution_time"] > 5.0:  # 如果执行时间过长
            logger.info("执行时间过长，调整策略...")
            # 自定义调整逻辑
```

## 工作流程

1. **初始化**：创建AdaptiveLoopAgent实例，配置子代理和参数
2. **迭代执行**：
   - 迭代前调整：调整探索率、学习率，优化子代理顺序
   - 执行子代理：依次执行所有子代理
   - 性能跟踪：记录每个子代理的执行情况
3. **自我评估**：评估当前迭代的成功率、执行时间等指标
4. **自我修正**：如果评估结果不佳，调整参数或策略
5. **自我优化**：基于历史数据优化执行策略
6. **循环重复**：直到达到最大迭代次数或收到终止信号

## 设计理念

### 1. 闭环反馈系统
- 执行 → 评估 → 修正 → 优化 → 执行
- 每一次迭代都基于前一次的结果进行改进

### 2. 自适应参数调整
- 学习率：控制参数调整的幅度
- 探索率：平衡利用已有的最优策略和探索新策略

### 3. 基于性能的优化
- 子代理动态排序：优先执行表现更好的子代理
- 资源分配：根据执行时间调整资源分配

### 4. 鲁棒性设计
- 错误检测和恢复机制
- 性能下降时的自动重置
- 多样化探索以避免局部最优

## 应用场景

1. **客服回复优化**：自动迭代优化客服回复，直到达到满意的质量
2. **代码生成和优化**：自动生成代码并迭代优化，提高代码质量
3. **文档生成和改进**：自动生成文档并根据反馈进行改进
4. **多步骤任务处理**：处理复杂的多步骤任务，自动调整执行策略
5. **决策支持系统**：基于实时数据自动调整决策模型

## 与普通LoopAgent的区别

| 特性 | LoopAgent | AdaptiveLoopAgent |
|------|-----------|-------------------|
| 状态管理 | 基础状态 | 增强的自适应状态 |
| 自我评估 | 无 | 自动性能评估 |
| 自我修正 | 无 | 基于评估结果自动修正 |
| 自我优化 | 无 | 自动优化执行策略 |
| 子代理性能跟踪 | 无 | 实时跟踪和分析 |
| 动态参数调整 | 无 | 自适应调整参数 |
| 子代理动态排序 | 无 | 基于性能自动排序 |

## 性能优势

1. **提高成功率**：通过自我修正机制，不断改进执行策略
2. **降低执行时间**：通过优化子代理顺序和执行策略
3. **增强鲁棒性**：能够适应不同的环境和任务
4. **减少人工干预**：自动调整参数和策略，减少人工调整
5. **持续改进**：随着执行次数增加，性能不断提升

## 注意事项

1. **环境配置**：运行时需要配置Volcengine的访问密钥
2. **初始参数调整**：根据具体任务调整初始学习率和探索率
3. **最大迭代次数**：根据任务复杂度设置合适的最大迭代次数
4. **子代理设计**：子代理需要返回明确的成功/失败信号
5. **监控和日志**：建议启用详细日志，以便分析智能体的执行情况

## 未来扩展方向

1. **更复杂的评估指标**：引入更全面的评估指标，如准确性、相关性等
2. **多目标优化**：同时优化多个目标，如成功率和执行时间
3. **强化学习集成**：结合强化学习算法，进一步提高自适应能力
4. **迁移学习**：将从一个任务中学到的策略应用到其他任务
5. **可视化监控**：提供可视化界面，实时监控智能体的执行情况

## 结论

AdaptiveLoopAgent是一个强大的自适应自我修正、自我优化的智能体框架，能够自动调整执行策略，提高执行效率和成功率。它适用于各种复杂的多步骤任务，能够随着执行次数的增加不断改进性能，减少人工干预。