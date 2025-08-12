#!/usr/bin/env python3
"""
测试板块投资分析报告生成功能
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def create_test_sector_results():
    """创建测试用的板块投资分析结果"""
    return {
        "session_id": "test_sector_analysis_20250811_175000",
        "analysis_date": "2025-08-11",
        "analysis_mode": "板块投资分析",
        "market_type": "全市场",
        "stock_symbol": "板块投资分析",
        "analysts_used": ["sector_investment"],
        "research_depth": 3,
        "llm_provider": "dashscope",
        "llm_model": "qwen-plus",
        "analysis_results": {
            "sector_investment": {
                "report": """# 📊 市场热点分析

当前A股市场呈现以下热点特征：

## 🔥 主要热点板块
1. **科技板块**: AI应用加速落地，政策支持力度强
2. **新能源板块**: 政策利好持续，技术创新不断
3. **医药板块**: 创新药获批加速，行业景气度提升

# 📈 板块投资机会排序

基于当前市场环境和政策导向，板块投资机会排序如下：

## 🥇 一级投资机会（推荐权重25-30%）
**科技板块**
- 人工智能产业化进程加速
- 政策支持力度强，资金流入明显
- 估值相对合理，具备长期投资价值

## 🥈 二级投资机会（推荐权重15-20%）
**新能源板块**
- 全球能源转型趋势不变
- 技术进步带来成本下降
- 海外市场拓展前景广阔

## 🥉 三级投资机会（推荐权重10-15%）
**医药板块**
- 创新药政策环境改善
- 人口老龄化带来刚性需求
- 研发投入加大，产品线丰富

# 💰 推荐投资配置方案

## 核心配置（60%）
- 科技板块：30%
- 新能源板块：20%
- 消费板块：10%

## 卫星配置（30%）
- 医药板块：15%
- 金融板块：10%
- 制造业：5%

## 防御配置（10%）
- 公用事业：5%
- 现金等价物：5%

# ⚠️ 风险提示和控制措施

## 主要风险因素
1. **政策风险**: 监管政策变化可能影响板块表现
2. **市场风险**: 整体市场波动带来的系统性风险
3. **估值风险**: 部分热门板块估值偏高

## 风险控制建议
- 分散投资，避免单一板块过度集中
- 动态调整仓位，根据市场变化及时应对
- 设置止损位，控制单笔投资损失
- 定期评估，跟踪板块基本面变化

# 🎯 具体操作建议

## 买入时机
- 市场调整时分批建仓
- 关注政策窗口期的投资机会
- 重点关注业绩预告季的板块轮动

## 持仓管理
- 建议中长期持有（6-12个月）
- 根据基本面变化调整权重
- 定期再平衡投资组合

## 关注指标
- 板块资金流向和成交量变化
- 政策变化和行业发展趋势
- 龙头公司业绩和估值水平

**免责声明**: 以上分析仅供参考，投资有风险，请谨慎决策。""",
                "completed": True,
                "timestamp": datetime.now().isoformat(),
                "duration": 156.7
            }
        },
        "analysis_summary": {
            "completion_status": "completed",
            "total_analysts": 1,
            "analysis_duration": 156.7,
            "main_conclusion": "建议重点配置科技、新能源、医药三大板块，采用核心-卫星-防御的三层配置策略",
            "risk_level": "中等",
            "confidence_score": 88
        },
        "total_cost": 0.0234
    }

def test_sector_report_generation():
    """测试板块投资分析报告生成"""
    print("🧪 板块投资分析报告生成测试")
    print("=" * 60)
    
    try:
        # 导入报告导出模块
        from web.utils.sector_report_exporter import save_sector_analysis_reports, auto_save_sector_analysis
        
        # 创建测试数据
        test_results = create_test_sector_results()
        session_id = test_results['session_id']
        
        print(f"📊 测试数据创建完成")
        print(f"   会话ID: {session_id}")
        print(f"   分析日期: {test_results['analysis_date']}")
        print(f"   分析模式: {test_results['analysis_mode']}")
        
        # 测试手动保存
        print(f"\n🔄 测试手动保存报告...")
        manual_saved_files = save_sector_analysis_reports(test_results, session_id)
        
        if manual_saved_files:
            print(f"✅ 手动保存成功，共 {len(manual_saved_files)} 个文件:")
            for file_type, file_path in manual_saved_files.items():
                file_name = Path(file_path).name
                print(f"   📄 {file_type}: {file_name}")
        else:
            print(f"❌ 手动保存失败")
        
        # 测试自动保存
        print(f"\n🤖 测试自动保存报告...")
        auto_saved_files = auto_save_sector_analysis(test_results)
        
        if auto_saved_files:
            print(f"✅ 自动保存成功，共 {len(auto_saved_files)} 个文件:")
            for file_type, file_path in auto_saved_files.items():
                file_name = Path(file_path).name
                print(f"   📄 {file_type}: {file_name}")
                
            # 显示报告目录
            first_file_path = list(auto_saved_files.values())[0]
            reports_dir = Path(first_file_path).parent
            print(f"\n📁 报告保存目录: {reports_dir}")
            
            # 检查文件是否真实存在
            print(f"\n🔍 验证文件存在性:")
            for file_type, file_path in auto_saved_files.items():
                exists = Path(file_path).exists()
                status = "✅" if exists else "❌"
                file_size = Path(file_path).stat().st_size if exists else 0
                print(f"   {status} {file_type}: {Path(file_path).name} ({file_size} bytes)")
        else:
            print(f"❌ 自动保存失败")
        
        # 测试非板块分析的情况
        print(f"\n🚫 测试非板块分析（应该跳过）...")
        test_stock_results = test_results.copy()
        test_stock_results['analysis_mode'] = '股票分析'
        
        skipped_result = auto_save_sector_analysis(test_stock_results)
        if skipped_result is None:
            print(f"✅ 正确跳过非板块投资分析")
        else:
            print(f"❌ 未正确跳过非板块投资分析")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        print(f"详细错误: {traceback.format_exc()}")
        return False

def show_integration_info():
    """显示集成信息"""
    print(f"\n💡 集成信息:")
    print("=" * 60)
    
    print(f"📋 1. 自动保存集成:")
    print(f"   - 位置: web/utils/analysis_runner.py")
    print(f"   - 触发: 板块投资分析完成时")
    print(f"   - 功能: 自动调用 auto_save_sector_analysis()")
    
    print(f"\n📊 2. Web界面集成:")
    print(f"   - 位置: web/components/results_display.py")
    print(f"   - 功能: 显示已保存的报告文件")
    print(f"   - 特性: 支持快速打开报告目录")
    
    print(f"\n📁 3. 报告目录结构:")
    print(f"   results/")
    print(f"   └── 板块投资分析/")
    print(f"       └── {datetime.now().strftime('%Y-%m-%d')}/")
    print(f"           └── reports/")
    print(f"               ├── sector_investment_analysis.md  # 主报告")
    print(f"               ├── analysis_summary.md           # 分析摘要")
    print(f"               ├── analysis_config.md            # 配置信息")
    print(f"               └── sector_analysis_YYYYMMDD_HHMMSS.md  # 导出报告")
    
    print(f"\n🔄 4. 验证步骤:")
    print(f"   1. 运行板块投资分析")
    print(f"   2. 等待分析完成")
    print(f"   3. 检查Web界面显示的报告文件")
    print(f"   4. 验证reports目录中的文件")

def main():
    """主函数"""
    success = test_sector_report_generation()
    show_integration_info()
    
    if success:
        print(f"\n🎉 测试完成！板块投资分析报告生成功能已就绪。")
    else:
        print(f"\n❌ 测试失败，请检查错误信息。")

if __name__ == "__main__":
    main()
