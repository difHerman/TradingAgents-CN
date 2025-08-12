#!/usr/bin/env python3
"""
分析报告目录查看工具
显示分析报告的存储位置和目录结构
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def get_report_directories():
    """获取报告存储目录配置"""
    
    # 获取projects根目录
    current_file = Path(__file__)
    project_root = current_file.parent.parent
    
    print(f"📁 项目根目录: {project_root}")
    print("=" * 60)
    
    # 1. 检查环境变量配置
    results_dir_env = os.getenv("TRADINGAGENTS_RESULTS_DIR")
    print(f"🔧 环境变量配置:")
    print(f"   TRADINGAGENTS_RESULTS_DIR = {results_dir_env or '未设置'}")
    
    # 2. 确定实际使用的results目录
    if results_dir_env:
        if not os.path.isabs(results_dir_env):
            results_dir = project_root / results_dir_env
        else:
            results_dir = Path(results_dir_env)
    else:
        results_dir = project_root / "results"
    
    print(f"\n📊 实际报告目录:")
    print(f"   主目录: {results_dir}")
    print(f"   存在: {'✅ 是' if results_dir.exists() else '❌ 否'}")
    
    # 3. 显示目录结构规则
    print(f"\n📋 目录结构规则:")
    print(f"   股票分析: {results_dir}/{{股票代码}}/{{分析日期}}/reports/")
    print(f"   板块分析: {results_dir}/板块投资分析/{{分析日期}}/reports/")
    print(f"   示例: {results_dir}/000001/2025-08-11/reports/")
    
    # 4. 报告文件类型
    print(f"\n📄 报告文件类型:")
    file_types = {
        "market_report.md": "市场技术分析报告",
        "fundamentals_report.md": "基本面分析报告", 
        "news_report.md": "新闻事件分析报告",
        "sentiment_report.md": "市场情绪分析报告",
        "investment_plan.md": "投资决策报告",
        "final_trade_decision.md": "最终投资决策",
        "{股票代码}_analysis_{时间戳}.pdf": "PDF汇总报告",
        "{股票代码}_analysis_{时间戳}.html": "HTML汇总报告",
        "{股票代码}_analysis_{时间戳}.md": "Markdown汇总报告"
    }
    
    for filename, description in file_types.items():
        print(f"   📝 {filename}: {description}")
    
    return results_dir

def show_existing_reports(results_dir):
    """显示现有的报告文件"""
    print(f"\n📂 现有报告文件:")
    print("=" * 60)
    
    if not results_dir.exists():
        print(f"❌ 报告目录不存在: {results_dir}")
        return
    
    # 按日期排序显示所有报告
    all_files = []
    
    for root, dirs, files in os.walk(results_dir):
        for file in files:
            file_path = Path(root) / file
            try:
                stat = file_path.stat()
                all_files.append({
                    'path': file_path,
                    'relative_path': file_path.relative_to(results_dir),
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime)
                })
            except Exception:
                continue
    
    if not all_files:
        print("📭 暂无报告文件")
        return
    
    # 按修改时间排序（最新的在前）
    all_files.sort(key=lambda x: x['modified'], reverse=True)
    
    print(f"📊 共找到 {len(all_files)} 个报告文件:")
    print()
    
    current_dir = None
    for i, file_info in enumerate(all_files):
        # 按目录分组显示
        file_dir = file_info['relative_path'].parent
        if file_dir != current_dir:
            current_dir = file_dir
            print(f"📁 {file_dir}/")
        
        # 显示文件信息
        size_mb = file_info['size'] / 1024 / 1024
        size_str = f"{size_mb:.2f}MB" if size_mb >= 1 else f"{file_info['size']}B"
        modified_str = file_info['modified'].strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"   📄 {file_info['relative_path'].name}")
        print(f"      大小: {size_str}, 修改时间: {modified_str}")
        
        if i < len(all_files) - 1 and all_files[i+1]['relative_path'].parent != current_dir:
            print()

def show_export_options():
    """显示导出选项"""
    print(f"\n💾 报告导出方式:")
    print("=" * 60)
    
    print(f"🔄 1. 自动保存 (分析完成时):")
    print(f"   - 位置: Web界面中的「导出报告」按钮")
    print(f"   - 格式: PDF、Word、Markdown、HTML")
    print(f"   - 包含: 完整分析报告 + 分模块报告")
    
    print(f"\n📋 2. 分模块报告:")
    print(f"   - 市场技术分析")
    print(f"   - 基本面分析") 
    print(f"   - 新闻事件分析")
    print(f"   - 市场情绪分析")
    print(f"   - 投资决策建议")
    print(f"   - 最终交易决策")
    
    print(f"\n📊 3. 汇总报告:")
    print(f"   - PDF格式 (推荐)")
    print(f"   - HTML格式 (网页查看)")
    print(f"   - Markdown格式 (纯文本)")
    print(f"   - Word格式 (需要pandoc)")
    
def provide_usage_tips():
    """提供使用建议"""
    print(f"\n💡 使用建议:")
    print("=" * 60)
    
    print(f"📍 1. 查看最新报告:")
    print(f"   - 打开Web界面")
    print(f"   - 查看分析结果页面")
    print(f"   - 点击「导出报告」按钮保存")
    
    print(f"\n📍 2. 自定义报告目录:")
    print(f"   - 设置环境变量: TRADINGAGENTS_RESULTS_DIR")
    print(f"   - 可使用绝对路径或相对路径")
    print(f"   - 例如: TRADINGAGENTS_RESULTS_DIR=D:/MyReports")
    
    print(f"\n📍 3. 管理历史报告:")
    print(f"   - 报告按股票代码和日期组织")
    print(f"   - 可定期清理旧报告")
    print(f"   - 重要报告建议备份到其他位置")
    
    print(f"\n📍 4. 板块投资分析报告:")
    print(f"   - 存储在: 板块投资分析/{{日期}}/reports/")
    print(f"   - 包含: 全市场分析、板块配置建议")
    print(f"   - 格式: 与股票分析报告相同")

def main():
    """主函数"""
    print("📊 TradingAgents-CN 分析报告目录查看工具")
    print("=" * 70)
    
    # 获取报告目录配置
    results_dir = get_report_directories()
    
    # 显示现有报告
    show_existing_reports(results_dir)
    
    # 显示导出选项
    show_export_options()
    
    # 提供使用建议
    provide_usage_tips()
    
    print(f"\n🎯 快速访问:")
    print(f"   📁 报告目录: {results_dir}")
    print(f"   🌐 Web界面: python start_web.py")
    print(f"   📄 最新日志: logs/tradingagents.log")

if __name__ == "__main__":
    main()
