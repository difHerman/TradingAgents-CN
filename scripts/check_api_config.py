#!/usr/bin/env python3
"""
API配置检查和诊断工具
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from web.utils.api_checker import check_api_keys, get_api_key_status_message
from dotenv import load_dotenv

def main():
    """主函数"""
    print("🔍 TradingAgents-CN API配置检查工具")
    print("=" * 50)
    
    # 检查.env文件
    env_file = project_root / ".env"
    if env_file.exists():
        print(f"✅ 找到配置文件: {env_file}")
        load_dotenv(env_file, override=True)
    else:
        print(f"❌ 未找到配置文件: {env_file}")
        print(f"📝 请参考 .env.example 创建 .env 文件")
        return
    
    print("\n📊 API密钥配置状态:")
    print("-" * 30)
    
    # 检查API密钥状态
    status = check_api_keys()
    
    for key, info in status["details"].items():
        status_icon = "✅" if info["configured"] else "❌"
        required_text = "(必需)" if info["required"] else "(可选)"
        print(f"{status_icon} {key} {required_text}: {info['display']}")
        print(f"   描述: {info['description']}")
    
    print(f"\n📈 总体状态:")
    print(f"   总计: {status['summary']['total']} 个API密钥")
    print(f"   已配置: {status['summary']['configured']} 个")
    print(f"   必需配置: {status['summary']['required']} 个")
    
    print(f"\n🎯 状态消息: {get_api_key_status_message()}")
    
    # 提供解决建议
    if not status["required_configured"]:
        print(f"\n🔧 解决建议:")
        print(f"1. 申请必需的API密钥:")
        for key in status["missing_required"]:
            info = status["details"][key]
            print(f"   - {key}: {info['description']}")
            if key == "DASHSCOPE_API_KEY":
                print(f"     申请地址: https://dashscope.console.aliyun.com/")
            elif key == "FINNHUB_API_KEY":
                print(f"     申请地址: https://finnhub.io/dashboard")
        
        print(f"2. 在.env文件中配置API密钥")
        print(f"3. 重新启动应用")
    
    # 检查新闻源可用性
    print(f"\n📰 新闻源配置检查:")
    print("-" * 30)
    
    news_sources = {
        "东方财富": "内置数据源，无需配置",
        "Google新闻": "需要GOOGLE_API_KEY" if not os.getenv("GOOGLE_API_KEY") else "已配置",
        "OpenAI新闻": "需要OPENAI_API_KEY" if not os.getenv("OPENAI_API_KEY") else "已配置"
    }
    
    for source, status_msg in news_sources.items():
        print(f"📡 {source}: {status_msg}")
    
    print(f"\n💡 优化建议:")
    print(f"- 为了获得最佳新闻覆盖，建议配置 GOOGLE_API_KEY 和 OPENAI_API_KEY")
    print(f"- 即使只有DASHSCOPE_API_KEY，系统也会尝试使用内置数据源")

if __name__ == "__main__":
    main()