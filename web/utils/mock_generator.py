"""
模拟分析结果生成器
"""
import random
from datetime import datetime

def generate_mock_analysis_results():
    """
    生成一个完整的、合规的模拟分析结果，用于测试报告生成和导出功能。
    """
    stock_symbol = "MOCK"
    analysis_date = datetime.now().strftime("%Y-%m-%d")
    
    actions = ['BUY', 'HOLD', 'SELL']
    action = random.choice(actions)

    # 模拟 final_decision
    final_decision = {
        'action': action,
        'confidence': round(random.uniform(0.65, 0.95), 2),
        'risk_score': round(random.uniform(0.15, 0.60), 2),
        'pt_low': round(random.uniform(100, 150), 2),
        'pt_high': round(random.uniform(180, 250), 2),
        'reasoning': f"""
基于对 **{stock_symbol} (模拟)** 的全面模拟分析，AI决策系统得出以下结论：

**核心投资建议**: **{action}**

**关键驱动因素**:
1.  **宏观经济面**: 模拟数据显示，当前市场环境对科技股（模拟类别）{'极为有利' if action == 'BUY' else '构成挑战' if action == 'SELL' else '保持中性'}。
2.  **技术指标**: 关键技术指标（如模拟RSI和MACD）呈现出强烈的{'买入' if action == 'BUY' else '卖出' if action == 'SELL' else '盘整'}信号。
3.  **基本面健康度**: 公司的模拟财务报表显示其盈利能力强劲，资产负债表健康。
"""
    }

    # 模拟 state
    state = {
        'company_of_interest': stock_symbol,
        'trade_date': analysis_date,
        'market_report': """
### 📈 模拟市场技术分析报告

- **价格趋势**: 当前股价处于上升通道中，已成功突破关键阻力位 $150。
- **成交量**: 近期成交量放大，显示市场参与度活跃。
- **技术指标**:
    - **RSI(14)**: 68 (进入超买区边缘，但强势特征明显)
    - **MACD**: 金叉向上发散，多头动能强劲。
- **支撑/阻力**:
    - **强支撑位**: $135.50
    - **主要阻力位**: $180.00
""",
        'sentiment_report': """
### 💭 模拟社交媒体情绪分析报告

- **整体情绪**: 市场情绪整体偏向乐观，正面讨论占比75%。
- **热门话题**: 投资者主要关注公司即将发布的新产品（模拟）及其对未来营收的潜在影响。
- **意见领袖观点**: 多位知名科技博主（模拟）对该股持正面评价。
""",
        'news_report': """
### 📰 模拟新闻分析报告

- **正面新闻**: 《环球财经报》报道称，该公司获得一项重要的国际专利（模拟）。
- **中性新闻**: 公司宣布将在下季度进行常规的系统维护升级。
- **负面新闻**: 无显著负面新闻。
""",
        'fundamentals_report': """
### 💰 模拟公司基本面分析报告

- **市盈率(PE)**: 25.5 (低于行业平均水平30.2)
- **净资产收益率(ROE)**: 18.5% (高于行业平均水平15%)
- **营收增长**: 连续三个季度实现超过15%的同比增长。
- **现金流**: 经营性现金流健康，能够覆盖所有资本支出。
""",
        'risk_assessment': """
### ⚠️ 模拟风险评估报告

- **主要风险点**:
    1. **技术性回调风险**: 股价短期涨幅较大，RSI指标处于超买区边缘，可能面临获利了结带来的回调压力。
    2. **行业竞争风险**: 科技行业竞争激烈，需要持续关注公司新产品的市场表现。
    3. **宏观经济风险**: 全球宏观经济的不确定性可能对板块估值产生影响。
- **风险等级**: **中等**。虽然基本面强劲，但技术面和宏观面存在不确定性。
""",
        'investment_plan': f"""
### 📋 模拟投资计划

- **操作建议**: **{action}**
- **策略**: 鉴于目前情况，建议采用"分批建仓"策略。
- **首次仓位**: 建议不超过总资金的15%。
- **买入价位区间**: ${final_decision['pt_low']} - ${final_decision['pt_low'] + 10}
- **止损点**: 设置在 $130，跌破应严格执行。
""",
        'invest_debate_state': {
            'history': """
**第1轮辩论:**
- **[看涨研究员]**: 基于强劲的基本面和积极的市场情绪，我认为应该买入。
- **[看跌研究员]**: 我同意基本面不错，但技术指标显示超买，存在短期回调风险。

**第2轮辩论:**
- **[看涨研究员]**: 短期回调是健康调整，为长期投资者提供了更好的入场点。公司的护城河依然坚固。
- **[看跌研究员]**: 宏观经济存在不确定性，可能会影响整个板块，我们需要更谨慎。
""",
            'summary': "经过两轮辩论，共识认为尽管存在短期技术性回调风险，但公司长期基本面强劲，看涨理由更为充分。"
        },
        'risk_debate_state': {
            'risky_history': "**[激进风险分析师]**: 机会大于风险，应立即重仓买入，抓住主升浪。",
            'safe_history': "**[保守风险分析师]**: 建议等待股价回调至140美元附近再分批建仓，以控制风险。",
            'neutral_history': "**[中性风险分析师]**: 同意买入，但建议仓位不超过30%，并设置130美元为止损点。",
            'judge_decision': "风险管理委员会决议：同意采取中性偏乐观的建仓策略。建议以30%的初始仓位在现价附近买入，并设置严格的止损计划。"
        },
        'final_trade_decision': final_decision
    }

    # 组装成最终的 analysis_results 结构
    mock_results = {
        'stock_symbol': stock_symbol,
        'analysis_date': analysis_date,
        'market_type': '美股 (模拟)',
        'analysts': ['market', 'social', 'news', 'fundamentals'],
        'research_depth': 4,
        'llm_provider': 'mock_provider',
        'llm_model': 'mock_model_v1',
        'state': state,
        'final_decision': final_decision,
        'success': True,
        'is_mock': True # 添加一个标志位
    }

    return mock_results 