from langchain_core.messages import AIMessage
import time
import json
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def create_safe_debator(llm, toolkit):
    def conservative_node(state) -> dict:
        risk_debate_state = state["risk_debate_state"]
        history = risk_debate_state.get("history", "")
        safe_history = risk_debate_state.get("safe_history", "")

        current_risky_response = risk_debate_state.get("current_risky_response", "")
        current_neutral_response = risk_debate_state.get(
            "current_neutral_response", ""
        )

        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        trader_decision = state["trader_investment_plan"]

        tools = [
                toolkit.get_stock_news_openai,
                toolkit.get_reddit_stock_info,
        ]

        system_message = f"""作为一名保守的风险分析师，您的主要职责是识别、强调和优先处理与交易员决策或计划相关的潜在风险。当评估一项投资提案时，您的首要任务是保护资本和最小化下行风险。利用所提供的市场数据和情绪分析来支持您的谨慎立场，并挑战对立的观点。具体来说，请直接回应激进和中性分析师提出的每一个观点，用数据驱动的反驳和稳健的风险管理原则来反击。突出他们可能忽视的潜在陷阱，或者他们的假设可能过于乐观的地方。以下是交易员的决策：

{trader_decision}

您的任务是通过提供一个令人信服的案例来质疑和批评激进和中性的立场，说明为什么在当前情况下，谨慎和风险规避的方法是最好的。将以下来源的见解融入到您的论点中：

市场研究报告：{market_research_report}
社交媒体情绪报告：{sentiment_report}
最新世界事务报告：{news_report}
公司基本面报告：{fundamentals_report}
以下是当前的对话历史：{history}
以下是激进分析师的最后论点：{current_risky_response}
以下是中性分析师的最后论点：{current_neutral_response}。如果其他观点没有回应，请不要虚构，只需提出您的观点。

倡导严格的风险控制，质疑每一个假设，并确保每一个潜在的缺点都得到充分的考虑。专注于辩论和说服，而不仅仅是呈现数据。挑战每一个乐观的预测，强调为什么资本保全是至高无上的。请用中文以对话方式输出，就像您在说话一样，不使用任何特殊格式。"""

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

        argument = f"Safe Analyst: {response.content}"

        new_risk_debate_state = {
            "history": history + "\n" + argument,
            "risky_history": risk_debate_state.get("risky_history", ""),
            "safe_history": safe_history + "\n" + argument,
            "neutral_history": risk_debate_state.get("neutral_history", ""),
            "latest_speaker": "Safe",
            "current_risky_response": risk_debate_state.get(
                "current_risky_response", ""
            ),
            "current_safe_response": argument,
            "current_neutral_response": risk_debate_state.get(
                "current_neutral_response", ""
            ),
            "count": risk_debate_state["count"] + 1,
        }

        return {"risk_debate_state": new_risk_debate_state}

    return conservative_node
