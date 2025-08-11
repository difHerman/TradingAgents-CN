import time
import json
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def create_neutral_debator(llm, toolkit):
    def neutral_node(state) -> dict:
        risk_debate_state = state["risk_debate_state"]
        history = risk_debate_state.get("history", "")
        neutral_history = risk_debate_state.get("neutral_history", "")

        current_risky_response = risk_debate_state.get("current_risky_response", "")
        current_safe_response = risk_debate_state.get("current_safe_response", "")

        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        trader_decision = state["trader_investment_plan"]

        tools = [
                toolkit.get_stock_news_openai,
                toolkit.get_reddit_stock_info,
        ]

        system_message = f"""作为一名中立的风险分析师，您的职责是提供一个平衡的、客观的视角，既承认潜在的收益，也承认相关的风险。在评估交易员的决策或计划时，您的目标是促进不同观点之间的建设性对话，并确定一条既能利用机会又能有效管理风险的中间道路。利用所提供的市场数据和情绪分析来支持您的平衡论点，并帮助调和对立的观点。具体来说，请直接回应激进和保守分析师提出的每一个观点，以一种公正的方式，既验证他们担忧的合理性，又承认他们提议的优点。以下是交易员的决策：

{trader_decision}

您的任务是通过找到一个综合了两种极端观点的共同点来促进一个富有成效的讨论，并为交易员的决策提出一个平衡的风险回报方案。将以下来源的见解融入到您的论点中：

市场研究报告：{market_research_report}
社交媒体情绪报告：{sentiment_report}
最新世界事务报告：{news_report}
公司基本面报告：{fundamentals_report}
以下是当前的对话历史：{history}
以下是激进分析师的最后论点：{current_risky_response}
以下是保守分析师的最后论点：{current_safe_response}。如果其他观点没有回应，请不要虚构，只需提出您的观点。

通过作为一个调解人来参与，提出探索性的问题，并确定可以达成共识的领域。专注于建立一个平衡的、数据驱动的叙述，而不是偏袒任何一方。挑战这两种观点，以找到最佳的风险回报平衡点。请用中文以对话方式输出，就像您在说话一样，不使用任何特殊格式。"""

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "您是一位有用的AI助手，与其他助手协作。"
                    " 使用提供的工具来推进回答问题。"
                    " 如果您无法完全回答，没关系；具有不同工具的其他助手"
                    " 将从您停下的地方继续帮助。执行您能做的以取得进展。"
                    " 您可以访问以下工具：{tool_names}。\n{system_message}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        
        prompt = prompt.partial(system_message=system_message)
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))

        chain = prompt | llm.bind_tools(tools)

        response = chain.invoke(state["messages"])

        argument = f"Neutral Analyst: {response.content}"

        new_risk_debate_state = {
            "history": history + "\n" + argument,
            "risky_history": risk_debate_state.get("risky_history", ""),
            "safe_history": risk_debate_state.get("safe_history", ""),
            "neutral_history": neutral_history + "\n" + argument,
            "latest_speaker": "Neutral",
            "current_risky_response": risk_debate_state.get(
                "current_risky_response", ""
            ),
            "current_safe_response": risk_debate_state.get("current_safe_response", ""),
            "current_neutral_response": argument,
            "count": risk_debate_state["count"] + 1,
        }

        return {"risk_debate_state": new_risk_debate_state}

    return neutral_node
