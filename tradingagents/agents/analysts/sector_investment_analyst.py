#!/usr/bin/env python3
"""
板块投资分析师
专门分析市场新闻，给出板块投资建议
当用户没有输入具体股票代码时使用
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json
from datetime import datetime, timedelta

# 导入统一日志系统和分析模块日志装饰器
from tradingagents.utils.logging_init import get_logger
from tradingagents.utils.tool_logging import log_analyst_module
# 导入统一新闻工具
from tradingagents.tools.unified_news_tool import create_unified_news_tool

logger = get_logger("analysts.sector_investment")


def create_sector_news_tool(toolkit):
    """创建板块新闻获取工具"""
    
    def get_sector_news(date_str: str = None, hours_back: int = 24):
        """
        获取全市场板块新闻
        
        Args:
            date_str (str): 分析日期
            hours_back (int): 回溯小时数，默认24小时
        
        Returns:
            str: 格式化的新闻内容
        """
        try:
            curr_date = date_str or datetime.now().strftime("%Y-%m-%d")
            logger.info(f"[板块新闻工具] 开始获取全市场新闻，日期: {curr_date}")
            
            # 获取多个不同领域的新闻
            sector_news_data = []
            
            # GICS板块分类关键词（按照国际标准与A股对应关系）
            sector_keywords = {
                "能源板块": ["石油石化", "煤炭", "能源板块", "石油板块", "煤炭板块", "能源行业", "原油", "天然气"],
                "原材料板块": ["基础化工", "钢铁", "有色金属", "建筑材料", "非金属材料", "化工板块", "钢铁板块", "有色板块"],
                "工业板块": ["机械设备", "国防军工", "建筑装饰", "交通运输", "环保", "轻工制造", "工业板块", "制造业"],
                "可选消费板块": ["汽车", "家用电器", "商贸零售", "社会服务", "传媒", "汽车板块", "家电板块", "零售板块"],
                "日常消费品板块": ["食品饮料", "农林牧渔", "纺织服饰", "美容护理", "白酒板块", "食品板块", "农业板块"],
                "医疗保健板块": ["医药生物", "医药板块", "生物医药", "医疗器械", "创新药", "疫苗", "CXO"],
                "金融地产板块": ["银行", "非银金融", "房地产", "保险", "证券", "银行板块", "保险板块", "地产板块"],
                "信息技术板块": ["电子", "计算机", "软件服务", "科技板块", "AI板块", "芯片板块", "半导体", "云计算"],
                "电信服务板块": ["通信", "通信板块", "电信运营", "5G", "通信设备", "互联网服务"],
                "公用事业板块": ["公用事业", "电力设备", "电力板块", "水务", "燃气", "新能源发电", "电网"]
            }
            
            # 1. 获取热点新闻
            try:
                if hasattr(toolkit, 'get_global_news_openai'):
                    logger.info(f"[板块新闻工具] 获取OpenAI全球新闻...")
                    global_news = toolkit.get_global_news_openai.invoke({"curr_date": curr_date})
                    if global_news and len(global_news.strip()) > 50:
                        sector_news_data.append(("全球热点", global_news))
                        logger.info(f"[板块新闻工具] ✅ 全球新闻获取成功: {len(global_news)} 字符")
            except Exception as e:
                logger.warning(f"[板块新闻工具] 全球新闻获取失败: {e}")
            
            # 2. 获取Google新闻 - 多个板块查询
            try:
                if hasattr(toolkit, 'get_google_news'):
                    for sector_name, keywords in list(sector_keywords.items())[:3]:  # 限制查询数量
                        try:
                            # 使用更专注于板块层面的查询
                            query = f"A股 {keywords[0]} 投资机会 板块表现 行业前景"
                            logger.info(f"[板块新闻工具] 查询{sector_name}: {query}")
                            
                            sector_news = toolkit.get_google_news.invoke({
                                "query": query, 
                                "curr_date": curr_date
                            })
                            if sector_news and len(sector_news.strip()) > 50:
                                sector_news_data.append((sector_name, sector_news))
                                logger.info(f"[板块新闻工具] ✅ {sector_name}新闻获取成功")
                            
                            time.sleep(0.5)  # 避免请求过于频繁
                        except Exception as e:
                            logger.warning(f"[板块新闻工具] {sector_name}新闻获取失败: {e}")
            except Exception as e:
                logger.warning(f"[板块新闻工具] Google新闻获取失败: {e}")
            
            # 3. 获取宏观经济和市场板块新闻（不使用个股代码）
            try:
                if hasattr(toolkit, 'get_google_news'):
                    # 获取宏观经济和市场整体新闻
                    macro_queries = [
                        "中国股市 宏观经济 政策 A股",
                        "股市板块轮动 资金流向 投资机会",
                        "A股市场 行业分析 板块表现"
                    ]
                    
                    for i, query in enumerate(macro_queries):
                        try:
                            logger.info(f"[板块新闻工具] 获取宏观市场新闻: {query}")
                            macro_news = toolkit.get_google_news.invoke({
                                "query": query, 
                                "curr_date": curr_date
                            })
                            if macro_news and len(macro_news.strip()) > 100:
                                sector_news_data.append((f"宏观市场分析({i+1})", macro_news))
                                logger.info(f"[板块新闻工具] ✅ 宏观市场新闻获取成功")
                                break  # 获取到一个就够了
                            
                            time.sleep(0.5)  # 避免请求过于频繁
                        except Exception as e:
                            logger.warning(f"[板块新闻工具] 宏观市场新闻获取失败: {e}")
            except Exception as e:
                logger.warning(f"[板块新闻工具] 宏观市场新闻获取失败: {e}")
            
            # 格式化新闻数据
            if not sector_news_data:
                return "❌ 无法获取板块新闻数据，所有新闻源均不可用"
            
            formatted_result = f"""
=== 📰 板块投资新闻分析 ===
获取时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
分析日期: {curr_date}
数据来源: {len(sector_news_data)}个新闻源

=== 📋 各板块新闻概览 ===
"""
            
            for i, (source_name, news_content) in enumerate(sector_news_data, 1):
                formatted_result += f"""

【{i}. {source_name}】
{news_content[:1000]}{'...' if len(news_content) > 1000 else ''}

{'='*50}
"""
            
            formatted_result += f"""

=== ✅ 数据状态 ===
状态: 成功获取
数据源数量: {len(sector_news_data)}
总字符数: {sum(len(content) for _, content in sector_news_data)}
时间戳: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
            
            logger.info(f"[板块新闻工具] ✅ 板块新闻获取完成，共{len(sector_news_data)}个数据源")
            return formatted_result.strip()
            
        except Exception as e:
            error_msg = f"❌ 板块新闻获取失败: {str(e)}"
            logger.error(f"[板块新闻工具] {error_msg}")
            return error_msg
    
    # 设置工具属性
    get_sector_news.name = "get_sector_news"
    get_sector_news.description = """
GICS板块新闻获取工具 - 基于全球行业分类标准获取板块投资新闻

功能:
- 获取全球财经新闻热点和宏观经济动态
- 按GICS分类获取10大板块新闻：能源、原材料、工业、可选消费、日常消费品、医疗保健、金融地产、信息技术、电信服务、公用事业
- 获取A股市场整体趋势和GICS板块轮动分析
- 专注于行业政策、板块表现、资金流向等宏观信息
- 返回基于GICS标准的板块投资决策新闻内容
"""
    
    return get_sector_news


def create_sector_investment_analyst(llm, toolkit):
    """创建板块投资分析师"""
    
    @log_analyst_module("sector_investment")
    def sector_investment_analyst_node(state):
        start_time = datetime.now()
        current_date = state.get("trade_date", datetime.now().strftime("%Y-%m-%d"))
        
        logger.info(f"[板块投资分析师] 开始分析全市场板块投资机会，交易日期: {current_date}")
        session_id = state.get("session_id", "未知会话")
        logger.info(f"[板块投资分析师] 会话ID: {session_id}，开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 创建板块新闻工具
        sector_news_tool = create_sector_news_tool(toolkit)
        tools = [sector_news_tool]
        logger.info(f"[板块投资分析师] 已加载板块新闻工具: get_sector_news")
        
        system_message = """您是一位专业的板块投资分析师，专门负责分析宏观市场新闻并提供板块层面的投资建议。

⚠️ 重要：请专注于板块层面的分析，不要分析具体个股。

您的主要职责包括：
1. 获取和分析宏观经济、政策动态和板块层面的新闻
2. 识别各行业板块的投资机会和风险
3. 分析市场热点、资金流向对不同板块的影响
4. 提供具体的板块投资建议和行业配置方案
5. 给出板块轮动策略和风险控制建议

GICS板块分类体系（按照国际标准与A股对应关系）：

**一级板块 (GICS Sectors)**：
- ⚡ 能源 (Energy)：石油石化、煤炭
- 🏗️ 原材料 (Materials)：基础化工、钢铁、有色金属、建筑材料、非金属材料
- 🏭 工业 (Industrials)：机械设备、国防军工、建筑装饰、交通运输、环保、轻工制造
- 🛒 可选消费 (Consumer Discretionary)：汽车、家用电器、商贸零售、社会服务、传媒
- 🥘 日常消费品 (Consumer Staples)：食品饮料、农林牧渔、纺织服饰、美容护理
- 💊 医疗保健 (Health Care)：医药生物
- 🏦 金融地产 (Financials & Real Estate)：银行、非银金融、房地产
- 💻 信息技术 (Information Technology)：电子、计算机、软件服务
- 📡 电信服务 (Communication Services)：通信
- 🔌 公用事业 (Utilities)：公用事业、电力设备

分析要求：
- 基于真实的宏观和板块新闻数据进行分析，避免空泛推测
- 识别当前市场热点和板块轮动机会
- 评估各行业板块的投资价值和风险等级
- 提供具体的板块配置建议（权重分配）
- 推荐3-5个最具投资价值的行业板块
- 从宏观角度提供板块投资时机和风险控制建议
- 专注于板块层面分析，不涉及具体个股推荐

输出格式要求：
📊 **市场热点分析**
📈 **板块投资机会排序**
💰 **推荐投资配置方案**
⚠️ **风险提示和控制措施**
🎯 **具体操作建议**

⚠️ 重要提示：
- 所有分析必须基于获取到的真实宏观和板块新闻数据
- 专注于板块层面的分析，严格避免提及具体个股代码或个股分析
- 避免使用过于通用的模板化内容
- 提供具体的、可操作的板块投资建议
- 必须包含板块风险评估和控制措施
- 分析结果要有逻辑性和时效性，符合板块投资的宏观视角
"""
        
        # 构建提示模板
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", f"""请对当前市场({current_date})进行全面的板块投资分析。

您的任务：
1. 首先调用 get_sector_news 工具获取全市场最新新闻数据
2. 基于获取到的新闻数据，分析各板块的投资机会
3. 提供具体的板块投资建议和配置方案

请立即开始分析：调用 get_sector_news(date_str='{current_date}')
"""),
            MessagesPlaceholder(variable_name="messages", optional=True),
        ])
        
        # 创建LLM工具链
        llm_with_tools = llm.bind_tools(tools)
        
        # 准备初始消息
        messages = [
            ("human", f"请开始板块投资分析，分析日期: {current_date}")
        ]
        
        logger.info(f"[板块投资分析师] 准备调用LLM进行板块投资分析，模型: {llm.__class__.__name__}")
        
        # 调用LLM
        llm_start_time = time.time()
        response = llm_with_tools.invoke(prompt.format_messages(messages=messages))
        llm_time_taken = time.time() - llm_start_time
        
        logger.info(f"[板块投资分析师] LLM调用完成，耗时: {llm_time_taken:.2f}秒")
        
        # 检查是否有工具调用
        tool_calls = getattr(response, 'tool_calls', [])
        content = getattr(response, 'content', str(response))
        
        # 如果有工具调用，执行工具并获取结果
        if tool_calls:
            logger.info(f"[板块投资分析师] 检测到 {len(tool_calls)} 个工具调用")
            
            for tool_call in tool_calls:
                try:
                    tool_name = tool_call.get('name', '未知工具')
                    tool_args = tool_call.get('args', {})
                    logger.info(f"[板块投资分析师] 执行工具: {tool_name}，参数: {tool_args}")
                    
                    if tool_name == 'get_sector_news':
                        # 执行板块新闻获取
                        news_result = sector_news_tool(
                            date_str=tool_args.get('date_str', current_date)
                        )
                        
                        if news_result and len(news_result.strip()) > 100:
                            logger.info(f"[板块投资分析师] ✅ 板块新闻获取成功: {len(news_result)} 字符")
                            
                            # 基于新闻数据重新生成分析
                            analysis_prompt = f"""
基于以下获取到的全市场新闻数据，请提供详细的板块投资分析：

=== 最新市场新闻数据 ===
{news_result}

请基于上述真实新闻数据，提供详细的中文板块投资分析报告，包含：

📊 **市场热点分析**
- 当前市场关注的主要热点
- 政策导向和市场情绪
- 资金流向分析

📈 **GICS板块投资机会排序**（按投资价值排序）
1. **信息技术/医疗保健/可选消费** - 成长型板块（说明理由和新闻支撑）
2. **工业/金融地产/日常消费品** - 价值型板块（说明理由和新闻支撑）  
3. **能源/原材料/电信服务/公用事业** - 周期/防御型板块（说明理由和新闻支撑）

💰 **GICS板块配置方案**
- 核心增长配置：60% （信息技术、医疗保健、可选消费等成长型板块）
- 价值稳健配置：25% （工业、金融地产、日常消费品等价值型板块）
- 周期防御配置：15% （能源、原材料、公用事业等周期/防御型板块）

⚠️ **风险提示和控制措施**
- 主要风险因素识别
- 风险控制建议
- 止损和仓位管理

🎯 **具体操作建议**
- 买入时机建议
- 持仓周期建议
- 关注指标和信号

请确保所有分析都基于获取到的真实新闻数据，避免空泛的推测。
"""
                            
                            # 重新调用LLM生成基于新闻的分析
                            final_response = llm.invoke([("human", analysis_prompt)])
                            content = getattr(final_response, 'content', str(final_response))
                            
                            logger.info(f"[板块投资分析师] ✅ 基于新闻数据生成分析报告，长度: {len(content)} 字符")
                        else:
                            logger.warning(f"[板块投资分析师] ⚠️ 板块新闻获取失败或数据不足")
                            
                except Exception as e:
                    logger.error(f"[板块投资分析师] 工具调用失败: {e}")
        
        # 如果没有工具调用，提供基础的板块投资建议
        if not tool_calls:
            logger.warning(f"[板块投资分析师] ⚠️ LLM没有调用工具，提供通用板块投资建议")
            
            content = f"""
# 📊 板块投资分析报告

**分析日期**: {current_date}
**分析师**: 板块投资分析师

## 📈 当前市场环境分析

根据当前市场环境({current_date})，以下是主要板块的投资建议：

### 🔥 GICS板块投资机会评级

**1. 信息技术 (Information Technology)** ⭐⭐⭐⭐⭐
- 人工智能和数字化转型持续推进
- 政策强力支持数字经济发展
- 建议配置权重：20-25%

**2. 医疗保健 (Health Care)** ⭐⭐⭐⭐⭐
- 人口老龄化和健康需求增长
- 创新药和医疗器械政策利好
- 建议配置权重：15-20%

**3. 可选消费 (Consumer Discretionary)** ⭐⭐⭐⭐
- 消费升级和内需政策支持
- 汽车电动化和智能化趋势
- 建议配置权重：12-18%

**4. 工业 (Industrials)** ⭐⭐⭐⭐
- 制造业升级和新基建推动
- 国防军工和环保产业机会
- 建议配置权重：10-15%

### 💰 GICS板块配置建议

**核心增长配置 (60%)**
- 信息技术：25%
- 医疗保健：20% 
- 可选消费：15%

**价值稳健配置 (25%)**
- 工业：10%
- 金融地产：8%
- 日常消费品：7%

**周期防御配置 (15%)**
- 公用事业：6%
- 原材料：5%
- 能源：4%

### ⚠️ 风险控制建议

1. **分散投资**：避免单一板块过度集中
2. **动态调整**：根据市场变化及时调整配置
3. **止损纪律**：设置合理止损位
4. **定期评估**：每月评估投资组合表现

### 🎯 操作建议

- **买入时机**：市场调整时分批建仓
- **持仓周期**：建议中长期持有（6-12个月）
- **关注指标**：市场估值、政策变化、资金流向

**免责声明**: 以上分析仅供参考，投资有风险，请谨慎决策。
"""
        
        # 计算总耗时
        time_taken = time.time() - start_time.timestamp()
        
        logger.info(f"[板块投资分析师] 板块投资分析完成，总耗时: {time_taken:.2f}秒")
        
        # 返回状态更新
        return {
            "sector_investment_report": content,
            "sector_analysis_completed": True,
            "sector_analysis_timestamp": datetime.now().isoformat(),
            "sector_analysis_duration": time_taken
        }
    
    return sector_investment_analyst_node
