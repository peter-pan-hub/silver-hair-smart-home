"""
智能家居适老化改造市场分析与预测
包括：市场规模预测、竞争格局分析、用户增长模型、技术趋势分析、投资风险评估
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import os
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class MarketAnalyzer:
    def __init__(self, data_dir=None):
        """初始化市场分析器"""
        if data_dir is None:
            self.data_dir = r"D:\panze（用户分身）\user\trae\data"
        else:
            self.data_dir = data_dir
            
        self.analysis_dir = os.path.join(self.data_dir, "analysis")
        self.visualization_dir = os.path.join(self.data_dir, "visualization")
        
        # 创建目录
        os.makedirs(self.visualization_dir, exist_ok=True)
        
        print("市场分析器初始化完成")
    
    def load_review_data(self):
        """加载评论分析结果"""
        try:
            # 查找最新的情感分析结果
            json_files = [f for f in os.listdir(self.analysis_dir) 
                         if f.startswith('sentiment_analysis') and f.endswith('.json')]
            
            if json_files:
                json_files.sort(reverse=True)
                filepath = os.path.join(self.analysis_dir, json_files[0])
                with open(filepath, 'r', encoding='utf-8') as f:
                    sentiment_data = json.load(f)
                print(f"加载情感分析结果：{json_files[0]}")
                return sentiment_data
            else:
                print("未找到情感分析结果，使用模拟数据")
                return self._generate_mock_sentiment_data()
        except Exception as e:
            print(f"加载评论数据失败：{e}")
            return self._generate_mock_sentiment_data()
    
    def _generate_mock_sentiment_data(self):
        """生成模拟情感分析数据"""
        return {
            'total_reviews': 8500,
            'avg_sentiment_score': 0.68,
            'avg_rating': 4.2,
            'sentiment_distribution': {'积极': 5200, '中性': 2200, '消极': 1100},
            'aspect_analysis': {
                '安全性': {'review_count': 3200, 'avg_sentiment': 0.72, 'avg_score': 4.3, 'coverage': 37.6},
                '易用性': {'review_count': 4500, 'avg_sentiment': 0.65, 'avg_score': 4.1, 'coverage': 52.9},
                '功能性': {'review_count': 2800, 'avg_sentiment': 0.70, 'avg_score': 4.2, 'coverage': 32.9},
                '可靠性': {'review_count': 2100, 'avg_sentiment': 0.62, 'avg_score': 3.9, 'coverage': 24.7},
                '价格': {'review_count': 1800, 'avg_sentiment': 0.58, 'avg_score': 3.8, 'coverage': 21.2}
            }
        }
    
    def generate_market_data(self):
        """生成市场数据（实际应用时应从数据库或API获取）"""
        print("生成市场数据...")
        
        # 市场规模历史数据（单位：亿元）
        market_size_data = {
            'year': [2019, 2020, 2021, 2022, 2023, 2024],
            'market_size': [28, 35, 45, 60, 75, 85],
            'growth_rate': [0, 25.0, 28.6, 33.3, 25.0, 13.3]  # 百分比
        }
        
        # 竞争格局数据
        competition_data = {
            'company': ['小米', '华为', '海尔', '安心加', '乐橙', '360', '其他'],
            'market_share_2023': [28, 18, 12, 8, 7, 6, 21],  # 百分比
            'market_share_2024': [30, 19, 11, 9, 8, 7, 16],  # 百分比
            'growth_rate': [7.1, 5.6, -8.3, 12.5, 14.3, 16.7, -23.8]  # 百分比
        }
        
        # 用户数据
        user_data = {
            'year': [2020, 2021, 2022, 2023, 2024],
            'elderly_population': [264, 268, 272, 276, 280],  # 百万
            'smart_home_penetration': [1.2, 1.8, 2.5, 3.2, 3.8],  # 百分比
            'user_satisfaction': [3.8, 4.0, 4.1, 4.2, 4.2]  # 1-5分
        }
        
        # 技术成熟度数据
        tech_data = {
            'technology': ['跌倒检测', '语音控制', '远程监控', '健康监测', '智能手环'],
            'maturity_score': [85, 80, 75, 65, 70],  # 0-100分
            'adoption_rate': [45, 40, 35, 25, 30],  # 百分比
            'growth_potential': [25, 30, 35, 45, 40]  # 百分比
        }
        
        # 政策数据
        policy_data = {
            'year': [2021, 2022, 2023, 2024, 2025],
            'policy_support': [60, 70, 75, 80, 85],  # 0-100分
            'subsidy_amount': [15, 20, 25, 30, 35]  # 亿元
        }
        
        return {
            'market_size': pd.DataFrame(market_size_data),
            'competition': pd.DataFrame(competition_data),
            'users': pd.DataFrame(user_data),
            'technology': pd.DataFrame(tech_data),
            'policy': pd.DataFrame(policy_data)
        }
    
    def market_size_forecast(self, market_df, forecast_years=5):
        """市场规模预测"""
        print(f"市场规模预测（未来{forecast_years}年）...")
        
        # 准备数据
        X = market_df['year'].values.reshape(-1, 1)
        y = market_df['market_size'].values
        
        # 线性回归预测
        model_lr = LinearRegression()
        model_lr.fit(X, y)
        
        # 随机森林回归（更复杂的关系）
        model_rf = RandomForestRegressor(n_estimators=100, random_state=42)
        model_rf.fit(X, y)
        
        # 生成预测年份
        future_years = np.arange(market_df['year'].max() + 1, 
                                market_df['year'].max() + forecast_years + 1).reshape(-1, 1)
        
        # 预测
        forecast_lr = model_lr.predict(future_years)
        forecast_rf = model_rf.predict(future_years)
        
        # 计算复合年增长率
        cagr_lr = (forecast_lr[-1] / y[-1]) ** (1/forecast_years) - 1
        cagr_rf = (forecast_rf[-1] / y[-1]) ** (1/forecast_years) - 1
        
        # 创建预测DataFrame
        forecast_df = pd.DataFrame({
            'year': future_years.flatten(),
            'forecast_lr': forecast_lr,
            'forecast_rf': forecast_rf,
            'avg_forecast': (forecast_lr + forecast_rf) / 2
        })
        
        print(f"线性回归预测CAGR：{cagr_lr*100:.1f}%")
        print(f"随机森林预测CAGR：{cagr_rf*100:.1f}%")
        print(f"平均预测CAGR：{((cagr_lr + cagr_rf)/2*100):.1f}%")
        
        return forecast_df, model_lr, model_rf
    
    def competition_analysis(self, comp_df):
        """竞争格局分析"""
        print("竞争格局分析...")
        
        # 计算集中度
        cr3_2023 = comp_df.nlargest(3, 'market_share_2023')['market_share_2023'].sum()
        cr3_2024 = comp_df.nlargest(3, 'market_share_2024')['market_share_2024'].sum()
        
        # 增长分析
        comp_df['share_change'] = comp_df['market_share_2024'] - comp_df['market_share_2023']
        
        # 识别领导者和挑战者
        leaders = comp_df.nlargest(2, 'market_share_2024')
        challengers = comp_df.nlargest(4, 'growth_rate').head(2)  # 增长最快的前2名
        
        # 市场集中度趋势
        concentration_trend = "提高" if cr3_2024 > cr3_2023 else "降低"
        
        print(f"市场集中度CR3：2023年{cr3_2023:.1f}% → 2024年{cr3_2024:.1f}%（{concentration_trend}）")
        print(f"市场领导者：{', '.join(leaders['company'].tolist())}")
        print(f"快速增长挑战者：{', '.join(challengers['company'].tolist())}")
        
        return {
            'cr3_2023': cr3_2023,
            'cr3_2024': cr3_2024,
            'concentration_trend': concentration_trend,
            'leaders': leaders[['company', 'market_share_2024']].to_dict('records'),
            'challengers': challengers[['company', 'growth_rate']].to_dict('records'),
            'share_changes': comp_df[['company', 'share_change']].to_dict('records')
        }
    
    def user_growth_model(self, user_df, sentiment_data):
        """用户增长模型"""
        print("用户增长模型分析...")
        
        # 计算渗透率增长
        user_df['penetration_growth'] = user_df['smart_home_penetration'].pct_change() * 100
        
        # 预测未来渗透率（简单线性外推）
        X = user_df['year'].values.reshape(-1, 1)
        y = user_df['smart_home_penetration'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # 预测未来5年
        future_years = np.arange(user_df['year'].max() + 1, user_df['year'].max() + 6).reshape(-1, 1)
        future_penetration = model.predict(future_years)
        
        # 结合老年人口增长预测
        # 假设老年人口年增长1.5%
        elderly_growth_rate = 0.015
        current_elderly = user_df['elderly_population'].iloc[-1]
        
        future_elderly = [current_elderly * (1 + elderly_growth_rate) ** i 
                         for i in range(1, 6)]
        
        # 计算潜在用户数
        future_users = [future_elderly[i] * future_penetration[i] / 100 
                       for i in range(5)]
        
        # 用户满意度对增长的影响
        avg_satisfaction = sentiment_data['avg_rating']
        satisfaction_impact = 0.1  # 满意度每提高0.1分，渗透率增长提高0.5%
        
        adjusted_growth = future_penetration * (1 + (avg_satisfaction - 4) * satisfaction_impact)
        
        print(f"当前渗透率：{user_df['smart_home_penetration'].iloc[-1]:.1f}%")
        print(f"预测2028年渗透率：{future_penetration[-1]:.1f}%")
        print(f"预测潜在用户数：{future_users[-1]:.1f}百万")
        print(f"用户满意度影响系数：{satisfaction_impact*100:.1f}%/0.1分")
        
        return {
            'current_penetration': user_df['smart_home_penetration'].iloc[-1],
            'future_penetration': future_penetration.tolist(),
            'future_years': future_years.flatten().tolist(),
            'future_users': future_users,
            'elderly_population': future_elderly,
            'satisfaction_impact': satisfaction_impact
        }
    
    def technology_trend_analysis(self, tech_df):
        """技术趋势分析"""
        print("技术趋势分析...")
        
        # 技术矩阵分析（成熟度 vs 增长潜力）
        tech_df['tech_score'] = tech_df['maturity_score'] * 0.4 + tech_df['growth_potential'] * 0.6
        
        # 分类：明星技术、现金牛技术、问题技术、瘦狗技术
        def classify_tech(row):
            if row['maturity_score'] >= 70 and row['growth_potential'] >= 35:
                return '明星技术'
            elif row['maturity_score'] >= 70 and row['growth_potential'] < 35:
                return '现金牛技术'
            elif row['maturity_score'] < 70 and row['growth_potential'] >= 35:
                return '问题技术'
            else:
                return '瘦狗技术'
        
        tech_df['tech_category'] = tech_df.apply(classify_tech, axis=1)
        
        # 技术采纳预测
        adoption_growth = []
        for idx, row in tech_df.iterrows():
            # 简单预测：成熟度高、增长潜力大的技术采纳增长快
            growth = row['growth_potential'] * 0.7 + (100 - row['maturity_score']) * 0.3
            adoption_growth.append(growth)
        
        tech_df['adoption_growth'] = adoption_growth
        
        print("技术分类：")
        for _, row in tech_df.iterrows():
            print(f"  {row['technology']}: {row['tech_category']}（成熟度{row['maturity_score']}，潜力{row['growth_potential']}）")
        
        return tech_df
    
    def risk_assessment(self, market_data, sentiment_data, competition_results):
        """投资风险评估"""
        print("投资风险评估...")
        
        risks = []
        
        # 1. 市场风险
        market_growth = market_data['market_size']['growth_rate'].iloc[-1]
        if market_growth < 10:
            risks.append({'type': '市场风险', 'level': '高', 'description': f'市场增长放缓（{market_growth:.1f}%）'})
        elif market_growth < 20:
            risks.append({'type': '市场风险', 'level': '中', 'description': f'市场平稳增长（{market_growth:.1f}%）'})
        else:
            risks.append({'type': '市场风险', 'level': '低', 'description': f'市场快速增长（{market_growth:.1f}%）'})
        
        # 2. 竞争风险
        cr3 = competition_results['cr3_2024']
        if cr3 > 70:
            risks.append({'type': '竞争风险', 'level': '高', 'description': f'市场高度集中（CR3={cr3:.1f}%）'})
        elif cr3 > 50:
            risks.append({'type': '竞争风险', 'level': '中', 'description': f'市场中等集中（CR3={cr3:.1f}%）'})
        else:
            risks.append({'type': '竞争风险', 'level': '低', 'description': f'市场竞争分散（CR3={cr3:.1f}%）'})
        
        # 3. 用户接受度风险
        satisfaction = sentiment_data['avg_rating']
        if satisfaction < 3.5:
            risks.append({'type': '用户风险', 'level': '高', 'description': f'用户满意度低（{satisfaction:.1f}分）'})
        elif satisfaction < 4.0:
            risks.append({'type': '用户风险', 'level': '中', 'description': f'用户满意度一般（{satisfaction:.1f}分）'})
        else:
            risks.append({'type': '用户风险', 'level': '低', 'description': f'用户满意度高（{satisfaction:.1f}分）'})
        
        # 4. 技术风险
        tech_maturity = market_data['technology']['maturity_score'].mean()
        if tech_maturity < 60:
            risks.append({'type': '技术风险', 'level': '高', 'description': f'技术成熟度低（{tech_maturity:.1f}分）'})
        elif tech_maturity < 75:
            risks.append({'type': '技术风险', 'level': '中', 'description': f'技术成熟度中等（{tech_maturity:.1f}分）'})
        else:
            risks.append({'type': '技术风险', 'level': '低', 'description': f'技术成熟度高（{tech_maturity:.1f}分）'})
        
        # 5. 政策风险
        policy_support = market_data['policy']['policy_support'].iloc[-1]
        if policy_support < 60:
            risks.append({'type': '政策风险', 'level': '高', 'description': f'政策支持不足（{policy_support:.1f}分）'})
        elif policy_support < 80:
            risks.append({'type': '政策风险', 'level': '中', 'description': f'政策支持一般（{policy_support:.1f}分）'})
        else:
            risks.append({'type': '政策风险', 'level': '低', 'description': f'政策支持充分（{policy_support:.1f}分）'})
        
        # 总体风险评估
        risk_levels = {'高': 3, '中': 2, '低': 1}
        avg_risk_score = sum(risk_levels[r['level']] for r in risks) / len(risks)
        
        if avg_risk_score >= 2.5:
            overall_risk = '高'
        elif avg_risk_score >= 1.5:
            overall_risk = '中'
        else:
            overall_risk = '低'
        
        print("风险评估结果：")
        for risk in risks:
            print(f"  {risk['type']}: {risk['level']} - {risk['description']}")
        print(f"总体风险等级：{overall_risk}")
        
        return {
            'risks': risks,
            'overall_risk': overall_risk,
            'avg_risk_score': avg_risk_score
        }
    
    def investment_recommendation(self, market_data, sentiment_data, tech_analysis, risk_assessment):
        """投资建议"""
        print("生成投资建议...")
        
        recommendations = []
        
        # 1. 市场增长性建议
        market_growth = market_data['market_size']['growth_rate'].iloc[-1]
        if market_growth > 20:
            recommendations.append({
                'area': '市场进入',
                'recommendation': '积极进入',
                'rationale': f'市场高速增长（{market_growth:.1f}%），机会窗口期'
            })
        else:
            recommendations.append({
                'area': '市场进入',
                'recommendation': '谨慎进入',
                'rationale': f'市场平稳增长（{market_growth:.1f}%），需差异化竞争'
            })
        
        # 2. 技术投资建议
        star_techs = tech_analysis[tech_analysis['tech_category'] == '明星技术']
        if len(star_techs) > 0:
            tech_list = ', '.join(star_techs['technology'].tolist())
            recommendations.append({
                'area': '技术投资',
                'recommendation': '重点投资',
                'rationale': f'明星技术：{tech_list}（高成熟度+高增长潜力）'
            })
        
        # 3. 产品改进建议
        aspects = sentiment_data['aspect_analysis']
        if aspects:
            worst_aspect = min(aspects.items(), key=lambda x: x[1]['avg_sentiment'])
            recommendations.append({
                'area': '产品改进',
                'recommendation': '优先改进',
                'rationale': f'用户最不满意的是{worst_aspect[0]}（情感得分{worst_aspect[1]["avg_sentiment"]:.3f}）'
            })
        
        # 4. 风险应对建议
        high_risks = [r for r in risk_assessment['risks'] if r['level'] == '高']
        if high_risks:
            risk_areas = ', '.join([r['type'] for r in high_risks])
            recommendations.append({
                'area': '风险管理',
                'recommendation': '重点监控',
                'rationale': f'需重点关注的风险领域：{risk_areas}'
            })
        
        print("投资建议：")
        for rec in recommendations:
            print(f"  {rec['area']}: {rec['recommendation']} - {rec['rationale']}")
        
        return recommendations
    
    def visualize_market_analysis(self, market_data, forecast_df, competition_results, 
                                user_growth, tech_analysis):
        """可视化市场分析结果"""
        print("生成市场分析可视化图表...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        fig = plt.figure(figsize=(16, 12))
        
        # 1. 市场规模预测
        ax1 = plt.subplot(3, 3, 1)
        market_df = market_data['market_size']
        ax1.plot(market_df['year'], market_df['market_size'], 'o-', linewidth=2, label='历史数据')
        ax1.plot(forecast_df['year'], forecast_df['avg_forecast'], 's--', linewidth=2, label='预测')
        ax1.set_xlabel('年份')
        ax1.set_ylabel('市场规模（亿元）')
        ax1.set_title('市场规模及预测')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. 竞争格局
        ax2 = plt.subplot(3, 3, 2)
        comp_df = market_data['competition']
        x = range(len(comp_df))
        ax2.bar(x, comp_df['market_share_2024'], alpha=0.7, label='2024')
        ax2.bar(x, comp_df['market_share_2023'], alpha=0.4, label='2023')
        ax2.set_xticks(x)
        ax2.set_xticklabels(comp_df['company'], rotation=45, ha='right')
        ax2.set_ylabel('市场份额（%）')
        ax2.set_title('竞争格局分析')
        ax2.legend()
        
        # 3. 用户增长预测
        ax3 = plt.subplot(3, 3, 3)
        years = user_growth['future_years']
        users = user_growth['future_users']
        ax3.plot(years, users, 'o-', linewidth=2)
        ax3.set_xlabel('年份')
        ax3.set_ylabel('潜在用户数（百万）')
        ax3.set_title('用户增长预测')
        ax3.grid(True, alpha=0.3)
        
        # 4. 技术矩阵
        ax4 = plt.subplot(3, 3, 4)
        tech_df = tech_analysis
        colors = {'明星技术': 'red', '现金牛技术': 'green', '问题技术': 'orange', '瘦狗技术': 'gray'}
        
        for _, row in tech_df.iterrows():
            ax4.scatter(row['maturity_score'], row['growth_potential'], 
                       c=colors[row['tech_category']], s=100, alpha=0.7)
            ax4.annotate(row['technology'], (row['maturity_score'], row['growth_potential']),
                        xytext=(5, 5), textcoords='offset points')
        
        ax4.axhline(y=35, color='gray', linestyle='--', alpha=0.5)
        ax4.axvline(x=70, color='gray', linestyle='--', alpha=0.5)
        ax4.set_xlabel('技术成熟度')
        ax4.set_ylabel('增长潜力')
        ax4.set_title('技术矩阵分析')
        ax4.grid(True, alpha=0.3)
        
        # 5. 市场增长率
        ax5 = plt.subplot(3, 3, 5)
        ax5.bar(market_df['year'], market_df['growth_rate'], alpha=0.7)
        ax5.set_xlabel('年份')
        ax5.set_ylabel('增长率（%）')
        ax5.set_title('市场增长率')
        ax5.grid(True, alpha=0.3)
        
        # 6. 政策支持趋势
        ax6 = plt.subplot(3, 3, 6)
        policy_df = market_data['policy']
        ax6.plot(policy_df['year'], policy_df['policy_support'], 'o-', linewidth=2, label='政策支持度')
        ax6_twin = ax6.twinx()
        ax6_twin.plot(policy_df['year'], policy_df['subsidy_amount'], 's--', linewidth=2, 
                     color='orange', label='补贴金额')
        ax6.set_xlabel('年份')
        ax6.set_ylabel('政策支持度')
        ax6_twin.set_ylabel('补贴金额（亿元）')
        ax6.set_title('政策支持趋势')
        lines1, labels1 = ax6.get_legend_handles_labels()
        lines2, labels2 = ax6_twin.get_legend_handles_labels()
        ax6.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        plt.suptitle('智能家居适老化改造市场分析', fontsize=16)
        plt.tight_layout()
        
        viz_file = os.path.join(self.visualization_dir, f"market_analysis_{timestamp}.png")
        plt.savefig(viz_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"市场分析可视化图表已保存：{viz_file}")
        return viz_file
    
    def save_market_analysis(self, market_data, forecast_results, competition_results,
                           user_growth, tech_analysis, risk_assessment, recommendations):
        """保存市场分析结果"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 创建汇总报告
        summary = {
            'analysis_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'market_overview': {
                'current_size': market_data['market_size']['market_size'].iloc[-1],
                'growth_rate': market_data['market_size']['growth_rate'].iloc[-1],
                'forecast_cagr': ((forecast_results[0]['avg_forecast'].iloc[-1] / 
                                  market_data['market_size']['market_size'].iloc[-1]) ** 
                                 (1/5) - 1) * 100
            },
            'competition_analysis': competition_results,
            'user_growth_analysis': user_growth,
            'technology_analysis': tech_analysis.to_dict('records'),
            'risk_assessment': risk_assessment,
            'investment_recommendations': recommendations,
            'key_findings': [
                f"市场规模：{market_data['market_size']['market_size'].iloc[-1]}亿元，增长率{market_data['market_size']['growth_rate'].iloc[-1]:.1f}%",
                f"市场集中度：CR3={competition_results['cr3_2024']:.1f}%，趋势{competition_results['concentration_trend']}",
                f"用户渗透率：当前{user_growth['current_penetration']:.1f}%，预测2028年{user_growth['future_penetration'][-1]:.1f}%",
                f"技术热点：{', '.join(tech_analysis[tech_analysis['tech_category']=='明星技术']['technology'].tolist())}",
                f"总体风险：{risk_assessment['overall_risk']}级"
            ]
        }
        
        # 保存报告
        report_file = os.path.join(self.analysis_dir, f"market_analysis_report_{timestamp}.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"市场分析报告已保存：{report_file}")
        return report_file
    
    def run_full_analysis(self):
        """运行完整的市场分析流程"""
        print("=" * 50)
        print("开始市场分析流程")
        print("=" * 50)
        
        # 1. 加载数据
        print("\n1. 加载数据...")
        sentiment_data = self.load_review_data()
        market_data = self.generate_market_data()
        
        # 2. 市场规模预测
        print("\n2. 市场规模预测...")
        forecast_df, model_lr, model_rf = self.market_size_forecast(market_data['market_size'])
        
        # 3. 竞争格局分析
        print("\n3. 竞争格局分析...")
        competition_results = self.competition_analysis(market_data['competition'])
        
        # 4. 用户增长模型
        print("\n4. 用户增长分析...")
        user_growth = self.user_growth_model(market_data['users'], sentiment_data)
        
        # 5. 技术趋势分析
        print("\n5. 技术趋势分析...")
        tech_analysis = self.technology_trend_analysis(market_data['technology'])
        
        # 6. 风险评估
        print("\n6. 投资风险评估...")
        risk_assessment = self.risk_assessment(market_data, sentiment_data, competition_results)
        
        # 7. 投资建议
        print("\n7. 生成投资建议...")
        recommendations = self.investment_recommendation(
            market_data, sentiment_data, tech_analysis, risk_assessment
        )
        
        # 8. 可视化
        print("\n8. 生成可视化图表...")
        viz_file = self.visualize_market_analysis(
            market_data, forecast_df, competition_results, user_growth, tech_analysis
        )
        
        # 9. 保存结果
        print("\n9. 保存分析结果...")
        report_file = self.save_market_analysis(
            market_data, forecast_df, competition_results, user_growth,
            tech_analysis, risk_assessment, recommendations
        )
        
        # 10. 输出关键结论
        print("\n" + "=" * 50)
        print("市场分析完成！关键结论：")
        print("=" * 50)
        
        print(f"1. 市场规模：2024年{market_data['market_size']['market_size'].iloc[-1]}亿元")
        print(f"2. 增长预测：未来5年CAGR约{((forecast_df['avg_forecast'].iloc[-1] / market_data['market_size']['market_size'].iloc[-1]) ** (1/5) - 1)*100:.1f}%")
        print(f"3. 市场集中度：CR3={competition_results['cr3_2024']:.1f}%，趋势{competition_results['concentration_trend']}")
        print(f"4. 用户渗透率：当前{user_growth['current_penetration']:.1f}%，2028年预测{user_growth['future_penetration'][-1]:.1f}%")
        print(f"5. 技术热点：{', '.join(tech_analysis[tech_analysis['tech_category']=='明星技术']['technology'].tolist())}")
        print(f"6. 投资风险：总体{risk_assessment['overall_risk']}级")
        print(f"7. 投资建议：共{len(recommendations)}条具体建议")
        
        print(f"\n分析报告已保存：{report_file}")
        print(f"可视化图表：{viz_file}")
        
        return {
            'sentiment_data': sentiment_data,
            'market_data': market_data,
            'forecast_results': forecast_df,
            'competition_results': competition_results,
            'user_growth': user_growth,
            'tech_analysis': tech_analysis,
            'risk_assessment': risk_assessment,
            'recommendations': recommendations,
            'report_file': report_file,
            'visualization_file': viz_file
        }

def main():
    """主函数"""
    try:
        # 创建市场分析器
        analyzer = MarketAnalyzer()
        
        # 运行完整分析
        results = analyzer.run_full_analysis()
        
        # 显示详细建议
        print("\n详细投资建议：")
        print("-" * 40)
        for rec in results['recommendations']:
            print(f"{rec['area']}: {rec['recommendation']}")
            print(f"  理由：{rec['rationale']}")
            print()
        
        # 风险详情
        print("风险详情：")
        print("-" * 40)
        for risk in results['risk_assessment']['risks']:
            print(f"{risk['type']}: {risk['level']} - {risk['description']}")
        
    except Exception as e:
        print(f"市场分析出错：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()