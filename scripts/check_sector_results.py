#!/usr/bin/env python3
"""
板块投资分析结果检查工具
帮助用户找到并查看板块投资分析的结果
"""

import os
import sys
import json
import glob
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def check_streamlit_session():
    """检查Streamlit会话状态中的分析结果"""
    print("🔍 检查Streamlit会话状态...")
    
    # Streamlit会话状态文件通常存储在系统临时目录
    import tempfile
    temp_dir = tempfile.gettempdir()
    
    # 查找可能的会话文件
    streamlit_files = []
    for pattern in ["*streamlit*", "*analysis*", "*trading*"]:
        files = glob.glob(os.path.join(temp_dir, pattern))
        streamlit_files.extend(files)
    
    if streamlit_files:
        print(f"✅ 找到 {len(streamlit_files)} 个可能的会话文件")
        for file in streamlit_files[:5]:  # 只显示前5个
            print(f"   📄 {file}")
    else:
        print("❌ 未找到Streamlit会话文件")
    
    return streamlit_files

def check_analysis_logs():
    """检查分析日志中的板块投资分析记录"""
    print("\n📋 检查分析日志...")
    
    log_dirs = [
        project_root / "logs",
        project_root / "web" / "logs", 
        Path.home() / "Documents" / "TradingAgents" / "logs"
    ]
    
    sector_analysis_logs = []
    
    for log_dir in log_dirs:
        if log_dir.exists():
            print(f"🔍 搜索日志目录: {log_dir}")
            
            # 查找包含板块投资分析的日志文件
            for log_file in log_dir.glob("*.log"):
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if "板块投资分析" in content or "sector_investment" in content:
                            sector_analysis_logs.append(str(log_file))
                            print(f"   ✅ 找到相关日志: {log_file.name}")
                except Exception as e:
                    continue
    
    return sector_analysis_logs

def check_results_directory():
    """检查结果存储目录"""
    print("\n📁 检查结果存储目录...")
    
    # 可能的结果目录
    possible_dirs = [
        project_root / "results",
        project_root / "web" / "results",
        Path.home() / "Documents" / "TradingAgents" / "results",
        Path(os.getenv("TRADINGAGENTS_RESULTS_DIR", "")) if os.getenv("TRADINGAGENTS_RESULTS_DIR") else None
    ]
    
    results_found = []
    
    for results_dir in possible_dirs:
        if results_dir and results_dir.exists():
            print(f"🔍 搜索结果目录: {results_dir}")
            
            # 查找板块投资分析结果文件
            patterns = ["*sector*", "*板块*", "*investment*", "*.json"]
            
            for pattern in patterns:
                files = list(results_dir.glob(pattern))
                for file in files:
                    try:
                        if file.suffix == '.json':
                            with open(file, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                if data.get('analysis_mode') == '板块投资分析':
                                    results_found.append(str(file))
                                    print(f"   ✅ 找到板块投资分析结果: {file.name}")
                        else:
                            results_found.append(str(file))
                            print(f"   📄 找到相关文件: {file.name}")
                    except Exception as e:
                        continue
    
    return results_found

def check_session_state_files():
    """检查可能的会话状态文件"""
    print("\n💾 检查会话状态文件...")
    
    # 查找项目中可能存储会话状态的文件
    state_patterns = [
        project_root / "web" / "*session*",
        project_root / "*state*", 
        project_root / "cache" / "*",
        project_root / "temp" / "*"
    ]
    
    state_files = []
    for pattern in state_patterns:
        files = glob.glob(str(pattern))
        state_files.extend(files)
    
    relevant_files = []
    for file in state_files:
        try:
            if os.path.isfile(file):
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "板块投资" in content or "sector_investment" in content:
                        relevant_files.append(file)
                        print(f"   ✅ 找到相关状态文件: {Path(file).name}")
        except Exception:
            continue
    
    return relevant_files

def provide_guidance():
    """提供查找和查看结果的指导"""
    print("\n💡 板块投资分析结果查看指南:")
    print("=" * 50)
    
    print("📍 1. Web界面查看 (推荐):")
    print("   - 启动Web应用: python start_web.py")
    print("   - 选择「板块投资分析」模式")
    print("   - 运行分析后，结果会直接显示在页面上")
    print("   - 结果包括: 市场热点分析、板块投资机会排序、投资配置方案等")
    
    print("\n📍 2. 日志文件查看:")
    print("   - 查看 logs/ 目录下的日志文件")
    print("   - 搜索包含「板块投资分析」的条目")
    print("   - 日志会记录分析过程和主要结果")
    
    print("\n📍 3. 结果文件位置:")
    print("   - 默认位置: results/ 目录")
    print("   - 环境变量: TRADINGAGENTS_RESULTS_DIR")
    print("   - 用户文档: ~/Documents/TradingAgents/results/")
    
    print("\n📍 4. 会话状态:")
    print("   - Web应用运行时，结果保存在内存中")
    print("   - 关闭浏览器或重启应用后需要重新分析")
    print("   - 建议使用导出功能保存重要结果")
    
    print("\n🔧 5. 故障排除:")
    print("   - 如果没有结果，检查API配置")
    print("   - 运行: python scripts/check_api_config.py")
    print("   - 确保分析过程没有报错")
    print("   - 查看日志文件了解详细错误信息")

def main():
    """主函数"""
    print("🔍 TradingAgents-CN 板块投资分析结果检查工具")
    print("=" * 60)
    
    # 检查各个可能的位置
    streamlit_files = check_streamlit_session()
    log_files = check_analysis_logs()
    result_files = check_results_directory()
    state_files = check_session_state_files()
    
    # 汇总结果
    print("\n📊 检查汇总:")
    print("-" * 30)
    print(f"Streamlit会话文件: {len(streamlit_files)} 个")
    print(f"相关日志文件: {len(log_files)} 个")
    print(f"结果文件: {len(result_files)} 个") 
    print(f"状态文件: {len(state_files)} 个")
    
    total_files = len(streamlit_files) + len(log_files) + len(result_files) + len(state_files)
    
    if total_files > 0:
        print(f"\n✅ 共找到 {total_files} 个相关文件")
        print("建议优先查看结果文件和日志文件")
    else:
        print(f"\n❌ 未找到板块投资分析结果")
        print("可能原因:")
        print("1. 尚未运行过板块投资分析")
        print("2. 分析过程中出现错误")
        print("3. 结果存储在其他位置")
    
    # 提供指导
    provide_guidance()

if __name__ == "__main__":
    main()
