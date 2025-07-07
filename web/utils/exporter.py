"""
报告导出工具
负责将分析结果导出为不同格式的文件 (Markdown, HTML, PDF)
"""

import os
import markdown
from datetime import datetime
from pathlib import Path
import re

# PDF导出需要weasyprint
try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
# OSError通常意味着底层的GTK+库没有安装
except (ImportError, OSError) as e:
    WEASYPRINT_AVAILABLE = False
    print("⚠️ WeasyPrint 依赖未完全满足, PDF导出功能不可用。")
    print("   - 错误信息:", e)
    print("   - 要启用PDF导出, 请确保已安装 'pip install weasyprint' 并已正确安装GTK+运行库。")

# 定义结果保存目录
RESULTS_DIR = Path(__file__).parent.parent.parent / "results"
os.makedirs(RESULTS_DIR, exist_ok=True)


def _sanitize_filename(filename):
    """清理文件名，移除无效字符"""
    return re.sub(r'[\\/*?:"<>|]', "", filename)


def _generate_filename(stock_symbol, extension):
    """生成包含时间戳的文件名"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_symbol = _sanitize_filename(stock_symbol)
    return f"{sanitized_symbol}_analysis_{timestamp}.{extension}"


def extract_risk_assessment(state):
    """从分析状态中提取风险评估数据 (从analysis_runner迁移)"""
    try:
        risk_debate_state = state.get('risk_debate_state', {})

        if not risk_debate_state:
            return ""

        risky_analysis = risk_debate_state.get('risky_history', '')
        safe_analysis = risk_debate_state.get('safe_history', '')
        neutral_analysis = risk_debate_state.get('neutral_history', '')
        judge_decision = risk_debate_state.get('judge_decision', '')

        return f"""
## ⚠️ 风险评估报告

### 🔴 激进风险分析师观点
{risky_analysis if risky_analysis else '暂无激进风险分析'}

### 🟡 中性风险分析师观点
{neutral_analysis if neutral_analysis else '暂无中性风险分析'}

### 🟢 保守风险分析师观点
{safe_analysis if safe_analysis else '暂无保守风险分析'}

### 🏛️ 风险管理委员会最终决议
{judge_decision if judge_decision else '暂无风险管理决议'}
        """.strip()
    except Exception as e:
        print(f"提取风险评估数据时出错: {e}")
        return "风险评估数据提取失败。"


def generate_markdown_report(results):
    """将分析结果格式化为Markdown字符串 (从analysis_runner迁移并增强)"""
    stock_symbol = results.get('stock_symbol', 'N/A')
    analysis_date = results.get('analysis_date', 'N/A')
    final_decision = results.get('final_decision', {})
    state = results.get('state', {})

    action = final_decision.get('action', 'N/A')
    confidence = final_decision.get('confidence', 0)
    risk_score = final_decision.get('risk_score', 0)
    reasoning = final_decision.get('reasoning', '无')
    pt_low = final_decision.get('pt_low', 'N/A')
    pt_high = final_decision.get('pt_high', 'N/A')

    # 从state中提取更详细的报告
    market_report = state.get('market_report', '无市场分析报告')
    social_report = state.get('sentiment_report', '无社交媒体分析报告')
    news_report = state.get('news_report', '无新闻分析报告')
    fundamentals_report = state.get('fundamentals_report', '无基本面分析报告')

    # 提取研究员辩论
    invest_debate_state = state.get('invest_debate_state', {})
    debate_history = invest_debate_state.get('history', '无辩论记录')
    debate_summary = invest_debate_state.get('summary', '无辩论总结')

    # 提取风险评估
    risk_assessment_report = extract_risk_assessment(state)

    # 新增：直接从state中获取模块化报告内容
    market_report_content = state.get('market_report', '无市场技术分析报告。')
    fundamentals_report_content = state.get('fundamentals_report', '无基本面分析报告。')
    social_report_content = state.get('sentiment_report', '无社交媒体情绪分析报告。')
    news_report_content = state.get('news_report', '无新闻分析报告。')
    risk_assessment_content = state.get('risk_assessment', '无风险评估报告。')
    investment_plan_content = state.get('investment_plan', '无投资建议。')

    report_content = f"""
# 📈 股票分析报告: {stock_symbol}

- **分析日期**: {analysis_date}
- **报告生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 🎯 最终投资决策

| 项目 | 内容 |
| :--- | :--- |
| **股票代码** | **{stock_symbol}** |
| **推荐动作** | **{action}** |
| **置信度** | **{confidence:.1%}** |
| **风险评分** | **{risk_score:.1%}** |
| **目标价位(低)** | {pt_low} |
| **目标价位(高)** | {pt_high} |

### 🔑 核心逻辑
{reasoning}

---

## 🔬 深度分析详情 (对应UI中的Tab页)

### 1. 📈 市场技术分析
{market_report_content}

---
### 2. 💰 基本面分析
{fundamentals_report_content}

---
### 3. 💭 市场情绪分析
{social_report_content}

---
### 4. 📰 新闻事件分析
{news_report_content}

---
### 5. ⚠️ 风险评估
{risk_assessment_content}

---
### 6. 📋 投资建议
{investment_plan_content}

---

## 💬 附录：详细辩论记录

### 🗣️ 投研辩论摘要
<details>
<summary><strong>辩论总结 (点击展开)</strong></summary>

{debate_summary}
</details>

<details>
<summary><strong>完整辩论记录 (点击展开)</strong></summary>

{debate_history}
</details>

---

### ⚖️ 风险管理委员会详细决议
{risk_assessment_report}

---
*免责声明: 本报告由AI生成，仅供研究和学习使用，不构成任何投资建议。*
"""
    return report_content.strip()


def export_to_markdown(results):
    """导出为Markdown文件"""
    stock_symbol = results.get('stock_symbol', 'unknown')
    markdown_content = generate_markdown_report(results)
    filename = _generate_filename(stock_symbol, "md")
    filepath = RESULTS_DIR / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown_content)
        
    return str(filepath)


def export_to_html(results):
    """导出为具有交互式Tab页的HTML文件"""
    stock_symbol = results.get('stock_symbol', 'unknown')
    
    # 1. 准备所有内容模块
    state = results.get('state', {})
    decision_summary_md = _get_decision_summary_md(results)
    
    analysis_modules = [
        {'id': 'Market', 'title': '📈 市场技术分析', 'content': state.get('market_report', '无内容')},
        {'id': 'Fundamentals', 'title': '💰 基本面分析', 'content': state.get('fundamentals_report', '无内容')},
        {'id': 'Sentiment', 'title': '💭 市场情绪分析', 'content': state.get('sentiment_report', '无内容')},
        {'id': 'News', 'title': '📰 新闻事件分析', 'content': state.get('news_report', '无内容')},
        {'id': 'Risk', 'title': '⚠️ 风险评估', 'content': state.get('risk_assessment', '无内容')},
        {'id': 'Plan', 'title': '📋 投资建议', 'content': state.get('investment_plan', '无内容')}
    ]
    
    # 2. 构建Tab按钮和内容
    tab_buttons_html = ""
    tab_contents_html = ""
    for i, module in enumerate(analysis_modules):
        active_class = "active" if i == 0 else ""
        display_style = "block" if i == 0 else "none"
        
        tab_buttons_html += f'<button class="tablinks {active_class}" onclick="openTab(event, \'{module["id"]}\')">{module["title"]}</button>'
        
        # 将每个模块的Markdown内容转换为HTML
        module_html_content = markdown.markdown(module['content'], extensions=['tables', 'fenced_code'])
        tab_contents_html += f'<div id="{module["id"]}" class="tabcontent" style="display: {display_style};"><h3>{module["title"]}</h3>{module_html_content}</div>'

    # 3. 将决策摘要转换为HTML
    decision_summary_html = markdown.markdown(decision_summary_md, extensions=['tables'])

    # 4. 创建完整的HTML模板
    html_template = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>股票分析报告: {stock_symbol}</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: 20px auto; padding: 20px; background-color: #f9f9f9; }}
            .container {{ background-color: #fff; padding: 25px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1, h2, h3 {{ color: #1f77b4; }}
            h1 {{ text-align: center; border-bottom: 2px solid #eee; padding-bottom: 15px; margin-bottom: 20px;}}
            table {{ border-collapse: collapse; width: 100%; margin: 1.5em 0; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #f2f2f2; font-weight: bold; }}
            .tab {{ overflow: hidden; border: 1px solid #ccc; background-color: #f1f1f1; border-radius: 5px 5px 0 0;}}
            .tab button {{ background-color: inherit; float: left; border: none; outline: none; cursor: pointer; padding: 14px 16px; transition: background-color 0.3s; font-size: 16px;}}
            .tab button:hover {{ background-color: #ddd; }}
            .tab button.active {{ background-color: #fff; border-bottom: 2px solid #1f77b4; font-weight: bold; color: #1f77b4; border-top: 2px solid #1f77b4; margin-top: -2px;}}
            .tabcontent {{ padding: 15px 12px; border: 1px solid #ccc; border-top: none; background-color: #fff; border-radius: 0 0 5px 5px; animation: fadeEffect 0.5s; }}
            @keyframes fadeEffect {{ from {{opacity: 0;}} to {{opacity: 1;}} }}
            .disclaimer {{ font-size: 0.8em; color: #777; text-align: center; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📈 股票分析报告: {stock_symbol}</h1>
            
            <h2>🎯 最终投资决策</h2>
            {decision_summary_html}

            <h2>🔬 深度分析详情</h2>
            <div class="tab">
                {tab_buttons_html}
            </div>
            {tab_contents_html}

            <p class="disclaimer">
                *免责声明: 本报告由AI生成，仅供研究和学习使用，不构成任何投资建议。*
            </p>
        </div>
        <script>
            function openTab(evt, tabName) {{
                var i, tabcontent, tablinks;
                tabcontent = document.getElementsByClassName("tabcontent");
                for (i = 0; i < tabcontent.length; i++) {{
                    tabcontent[i].style.display = "none";
                }}
                tablinks = document.getElementsByClassName("tablinks");
                for (i = 0; i < tablinks.length; i++) {{
                    tablinks[i].className = tablinks[i].className.replace(" active", "");
                }}
                document.getElementById(tabName).style.display = "block";
                evt.currentTarget.className += " active";
            }}
        </script>
    </body>
    </html>
    """

    filename = _generate_filename(stock_symbol, "html")
    filepath = RESULTS_DIR / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_template)
        
    return str(filepath)


def _get_decision_summary_md(results):
    """辅助函数：提取决策摘要为Markdown表格"""
    final_decision = results.get('final_decision', {})
    stock_symbol = results.get('stock_symbol', 'N/A')
    
    action = final_decision.get('action', 'N/A')
    confidence = final_decision.get('confidence', 0)
    risk_score = final_decision.get('risk_score', 0)
    pt_low = final_decision.get('pt_low', 'N/A')
    pt_high = final_decision.get('pt_high', 'N/A')
    reasoning = final_decision.get('reasoning', '无')

    md_table = f"""
| 项目 | 内容 |
| :--- | :--- |
| **股票代码** | **{stock_symbol}** |
| **推荐动作** | **{action}** |
| **置信度** | **{confidence:.1%}** |
| **风险评分** | **{risk_score:.1%}** |
| **目标价位(低)** | {pt_low} |
| **目标价位(高)** | {pt_high} |

**核心逻辑**: {reasoning}
"""
    return md_table.strip()


def export_to_pdf(results):
    """导出为PDF文件"""
    if not WEASYPRINT_AVAILABLE:
        raise ImportError("PDF导出功能需要安装weasyprint库。请运行 'pip install weasyprint'")

    stock_symbol = results.get('stock_symbol', 'unknown')
    html_path_str = export_to_html(results)
    
    filename = _generate_filename(stock_symbol, "pdf")
    filepath = RESULTS_DIR / filename
    
    html = HTML(filename=html_path_str)
    html.write_pdf(filepath)
    
    # 清理临时的HTML文件
    os.remove(html_path_str)
    
    return str(filepath) 