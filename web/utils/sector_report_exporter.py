#!/usr/bin/env python3
"""
板块投资分析报告导出工具
专门处理板块投资分析的报告生成和保存
"""

import os
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# 简化日志导入，避免依赖问题
import logging
logger = logging.getLogger('sector_report_exporter')

def save_sector_analysis_reports(results: Dict[str, Any], session_id: str) -> Dict[str, str]:
    """保存板块投资分析报告到results目录"""
    try:
        # 获取项目根目录
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent

        # 获取results目录配置
        results_dir_env = os.getenv("TRADINGAGENTS_RESULTS_DIR")
        if results_dir_env:
            if not os.path.isabs(results_dir_env):
                results_dir = project_root / results_dir_env
            else:
                results_dir = Path(results_dir_env)
        else:
            results_dir = project_root / "results"

        # 创建板块投资分析专用目录
        analysis_date = results.get('analysis_date', datetime.now().strftime('%Y-%m-%d'))
        sector_dir = results_dir / "板块投资分析" / analysis_date
        reports_dir = sector_dir / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)

        # 创建session记录文件
        session_file = sector_dir / f"session_{session_id}.log"
        session_file.touch(exist_ok=True)

        analysis_results = results.get('analysis_results', {})
        sector_data = analysis_results.get('sector_investment', {})
        saved_files = {}

        # 1. 保存主要的板块投资分析报告
        sector_report = sector_data.get('report', '')
        if sector_report:
            report_content = f"""# 全市场板块投资分析报告

**分析日期**: {analysis_date}
**会话ID**: {session_id}
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

{sector_report}

---

## 分析信息

- **分析模式**: {results.get('analysis_mode', '板块投资分析')}
- **研究深度**: {results.get('research_depth', 'N/A')}
- **AI模型**: {results.get('llm_provider', 'N/A')}/{results.get('llm_model', 'N/A')}
- **分析耗时**: {sector_data.get('duration', 0):.1f}秒
- **完成状态**: {'✅ 已完成' if sector_data.get('completed', False) else '⏳ 处理中'}

## 分析总结

{results.get('analysis_summary', {}).get('main_conclusion', '板块投资分析已完成')}

**风险等级**: {results.get('analysis_summary', {}).get('risk_level', '中等')}
**置信度**: {results.get('analysis_summary', {}).get('confidence_score', 85)}%

---

*本报告由TradingAgents-CN自动生成，仅供参考，投资有风险，决策需谨慎。*
"""
            
            # 保存主报告
            main_report_file = reports_dir / "sector_investment_analysis.md"
            with open(main_report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            saved_files['main_report'] = str(main_report_file)
            logger.info(f"✅ 保存板块投资分析主报告: {main_report_file}")

        # 2. 保存分析摘要信息
        analysis_summary = results.get('analysis_summary', {})
        if analysis_summary:
            summary_content = f"""# 板块投资分析摘要

**分析日期**: {analysis_date}
**会话ID**: {session_id}

## 完成状态
- **状态**: {analysis_summary.get('completion_status', '未知')}
- **总分析师数**: {analysis_summary.get('total_analysts', 1)}
- **分析耗时**: {analysis_summary.get('analysis_duration', 0):.1f}秒

## 核心结论
{analysis_summary.get('main_conclusion', '板块投资分析已完成')}

## 风险评估
- **风险等级**: {analysis_summary.get('risk_level', '中等')}
- **置信度评分**: {analysis_summary.get('confidence_score', 85)}%

## 成本信息
- **总分析成本**: ¥{results.get('total_cost', 0):.4f}

---
*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
            
            summary_file = reports_dir / "analysis_summary.md"
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(summary_content)
            saved_files['summary'] = str(summary_file)
            logger.info(f"✅ 保存分析摘要: {summary_file}")

        # 3. 保存配置信息
        config_content = f"""# 板块投资分析配置信息

**分析配置**
- **分析日期**: {analysis_date}
- **会话ID**: {session_id}
- **分析模式**: {results.get('analysis_mode', '板块投资分析')}
- **市场类型**: {results.get('market_type', '全市场')}
- **研究深度**: {results.get('research_depth', 'N/A')}

**AI模型配置**
- **LLM提供商**: {results.get('llm_provider', 'N/A')}
- **模型名称**: {results.get('llm_model', 'N/A')}
- **分析师列表**: {', '.join(results.get('analysts_used', []))}

**技术信息**
- **分析开始时间**: {sector_data.get('timestamp', 'N/A')}
- **分析耗时**: {sector_data.get('duration', 0):.1f}秒
- **分析状态**: {'✅ 已完成' if sector_data.get('completed', False) else '❌ 未完成'}

---
*配置记录时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        config_file = reports_dir / "analysis_config.md"
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config_content)
        saved_files['config'] = str(config_file)
        logger.info(f"✅ 保存配置信息: {config_file}")

        # 4. 生成汇总的Markdown报告（用于导出）
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        export_filename = f"sector_analysis_{timestamp}.md"
        
        export_content = f"""# 全市场板块投资分析报告

**报告生成**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**分析日期**: {analysis_date}
**会话ID**: {session_id}

---

## 📊 执行摘要

{analysis_summary.get('main_conclusion', '板块投资分析已完成')}

**关键指标**:
- 风险等级: {analysis_summary.get('risk_level', '中等')}
- 置信度: {analysis_summary.get('confidence_score', 85)}%
- 分析耗时: {sector_data.get('duration', 0):.1f}秒

---

## 📋 详细分析报告

{sector_report}

---

## ⚙️ 分析配置

- **分析模式**: {results.get('analysis_mode', '板块投资分析')}
- **研究深度**: {results.get('research_depth', 'N/A')}
- **AI模型**: {results.get('llm_provider', 'N/A')}/{results.get('llm_model', 'N/A')}
- **总成本**: ¥{results.get('total_cost', 0):.4f}

---

*本报告由 TradingAgents-CN 自动生成*
*⚠️ 投资有风险，决策需谨慎*
"""
        
        export_file = reports_dir / export_filename
        with open(export_file, 'w', encoding='utf-8') as f:
            f.write(export_content)
        saved_files['export'] = str(export_file)
        logger.info(f"✅ 保存导出报告: {export_file}")

        logger.info(f"✅ 板块投资分析报告保存完成，共保存 {len(saved_files)} 个文件")
        logger.info(f"📁 保存目录: {reports_dir}")

        return saved_files

    except Exception as e:
        logger.error(f"❌ 保存板块投资分析报告失败: {e}")
        logger.error(f"❌ 详细错误: {traceback.format_exc()}")
        return {}


def auto_save_sector_analysis(results: Dict[str, Any]) -> Optional[Dict[str, str]]:
    """分析完成后自动保存板块投资分析报告"""
    try:
        # 检查是否是板块投资分析
        analysis_mode = results.get('analysis_mode', '')
        if analysis_mode != '板块投资分析':
            return None
        
        # 检查是否有有效的分析结果
        analysis_results = results.get('analysis_results', {})
        sector_data = analysis_results.get('sector_investment', {})
        
        if not sector_data.get('completed', False):
            logger.warning("⚠️ 板块投资分析未完成，跳过自动保存")
            return None
        
        # 获取会话ID
        session_id = results.get('session_id', f"sector_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        logger.info(f"🔄 开始自动保存板块投资分析报告，会话ID: {session_id}")
        saved_files = save_sector_analysis_reports(results, session_id)
        
        if saved_files:
            logger.info(f"✅ 板块投资分析报告自动保存成功，共 {len(saved_files)} 个文件")
            return saved_files
        else:
            logger.warning("⚠️ 板块投资分析报告自动保存失败")
            return None
            
    except Exception as e:
        logger.error(f"❌ 板块投资分析报告自动保存错误: {e}")
        return None
