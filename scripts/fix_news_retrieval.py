#!/usr/bin/env python3
"""
新闻获取问题修复工具
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def check_environment():
    """检查环境配置"""
    print("🔍 检查新闻获取环境配置...")
    
    # 检查关键环境变量
    critical_vars = {
        "DASHSCOPE_API_KEY": "阿里百炼API密钥 (用于LLM)",
        "FINNHUB_API_KEY": "FinnHub API密钥 (用于财经数据)",
        "OPENAI_API_KEY": "OpenAI API密钥 (用于新闻获取)",
        "GOOGLE_API_KEY": "Google API密钥 (用于新闻搜索)"
    }
    
    config_status = {}
    for var, desc in critical_vars.items():
        value = os.getenv(var)
        config_status[var] = {
            "configured": bool(value),
            "description": desc,
            "display": f"{value[:20]}..." if value else "未配置"
        }
    
    return config_status

def print_diagnosis(config_status):
    """打印诊断信息"""
    print("\n📊 配置状态诊断:")
    print("=" * 50)
    
    for var, info in config_status.items():
        status = "✅" if info["configured"] else "❌"
        print(f"{status} {var}: {info['display']}")
        print(f"   {info['description']}")
    
    # 分析新闻获取失败原因
    print(f"\n🔍 新闻获取失败原因分析:")
    print("-" * 30)
    
    if not config_status["DASHSCOPE_API_KEY"]["configured"]:
        print("❌ 缺少DASHSCOPE_API_KEY - 这会导致整个系统无法运行")
    
    news_apis = ["OPENAI_API_KEY", "GOOGLE_API_KEY"]
    configured_news_apis = [api for api in news_apis if config_status[api]["configured"]]
    
    if not configured_news_apis:
        print("⚠️ 所有新闻API都未配置 - 这是新闻获取失败的主要原因")
        print("   系统将只依赖内置数据源，可能导致数据获取失败")
    elif len(configured_news_apis) == 1:
        print(f"⚠️ 只配置了 {configured_news_apis[0]} - 建议配置更多新闻源以提高成功率")
    else:
        print(f"✅ 已配置多个新闻源: {', '.join(configured_news_apis)}")

def generate_env_template():
    """生成环境变量模板"""
    template = '''# TradingAgents-CN 环境变量配置
# 请根据需要填写相应的API密钥

# 阿里百炼API密钥 (必需)
DASHSCOPE_API_KEY=sk-your_dashscope_api_key_here

# FinnHub金融数据API密钥 (必需)
FINNHUB_API_KEY=your_finnhub_api_key_here

# OpenAI API密钥 (推荐，用于新闻获取)
OPENAI_API_KEY=sk-your_openai_api_key_here

# Google AI API密钥 (推荐，用于新闻搜索)
GOOGLE_API_KEY=your_google_api_key_here

# DeepSeek API密钥 (可选)
DEEPSEEK_API_KEY=sk-your_deepseek_api_key_here
'''
    
    env_file = project_root / ".env"
    if not env_file.exists():
        try:
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(template)
            print(f"✅ 已创建环境变量模板: {env_file}")
            print("📝 请编辑.env文件，填入你的API密钥")
        except Exception as e:
            print(f"❌ 创建.env文件失败: {e}")
            print("📝 请手动创建.env文件")
    else:
        print(f"📄 .env文件已存在: {env_file}")

def provide_solutions():
    """提供解决方案"""
    print(f"\n🔧 解决方案:")
    print("=" * 50)
    
    print("1. 🔑 获取API密钥:")
    print("   - 阿里百炼: https://dashscope.console.aliyun.com/")
    print("   - FinnHub: https://finnhub.io/dashboard")
    print("   - OpenAI: https://platform.openai.com/api-keys")
    print("   - Google AI: https://ai.google.dev/")
    
    print(f"\n2. 📝 配置环境变量:")
    print("   - 编辑项目根目录的.env文件")
    print("   - 填入获取到的API密钥")
    print("   - 确保格式正确 (KEY=value)")
    
    print(f"\n3. 🔄 重启应用:")
    print("   - 保存.env文件后重启应用")
    print("   - 新的配置将在下次启动时生效")
    
    print(f"\n4. 🧪 测试配置:")
    print("   - 运行: python scripts/check_api_config.py")
    print("   - 验证所有必需的API密钥已配置")

def main():
    """主函数"""
    print("🚨 TradingAgents-CN 新闻获取问题修复工具")
    print("=" * 60)
    
    # 检查环境配置
    config_status = check_environment()
    
    # 打印诊断信息
    print_diagnosis(config_status)
    
    # 生成环境变量模板
    print(f"\n📄 环境变量配置:")
    print("-" * 30)
    generate_env_template()
    
    # 提供解决方案
    provide_solutions()
    
    print(f"\n💡 快速解决方案:")
    print("1. 至少配置 DASHSCOPE_API_KEY 和 FINNHUB_API_KEY")
    print("2. 推荐额外配置 OPENAI_API_KEY 或 GOOGLE_API_KEY 以提高新闻获取成功率")
    print("3. 配置完成后重启应用")

if __name__ == "__main__":
    main()
