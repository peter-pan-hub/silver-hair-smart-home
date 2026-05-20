"""
智能家居适老化改造产品评论NLP深度分析
包括：情感分析、主题建模、关键词提取、词云生成、情感趋势分析
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import jieba
import jieba.analyse
from snownlp import SnowNLP
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import warnings
warnings.filterwarnings('ignore')
import os
import json
from datetime import datetime
from collections import Counter
import re

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

class ElderlyProductNLP:
    def __init__(self, data_dir=None):
        """初始化NLP分析器"""
        if data_dir is None:
            self.data_dir = r"D:\panze（用户分身）\user\trae\data"
        else:
            self.data_dir = data_dir
            
        self.processed_dir = os.path.join(self.data_dir, "processed")
        self.analysis_dir = os.path.join(self.data_dir, "analysis")
        self.visualization_dir = os.path.join(self.data_dir, "visualization")
        
        # 创建目录
        os.makedirs(self.visualization_dir, exist_ok=True)
        
        # 初始化jieba
        self._init_jieba()
        
        print("NLP分析器初始化完成")
    
    def _init_jieba(self):
        """初始化jieba，添加领域词汇"""
        # 添加适老产品专业词汇
        domain_words = [
            "跌倒检测", "语音控制", "远程监控", "一键呼叫", "安全警报",
            "智能手环", "健康监测", "用药提醒", "睡眠监测", "活动轨迹",
            "煤气泄漏", "门窗感应", "紧急求助", "心率监测", "血压监测",
            "血糖监测", "体温监测", "呼吸监测", "防走失", "定位功能",
            "视频通话", "亲情相册", "娱乐功能", "简单易用", "操作方便",
            "误报率低", "电池续航", "充电方便", "信号稳定", "网络连接",
            "售后服务", "安装简单", "使用说明", "老人友好", "界面清晰",
            "反应灵敏", "准确率高", "质量可靠", "价格合理", "性价比高",
            "小米", "华为", "海尔", "360", "乐橙", "安心加", "海康威视"
        ]
        
        for word in domain_words:
            jieba.add_word(word)
    
    def load_data(self, filepath=None):
        """加载已清洗的数据"""
        if filepath is None:
            # 查找最新的清洗后数据
            csv_files = [f for f in os.listdir(self.processed_dir) if f.endswith('.csv')]
            if csv_files:
                csv_files.sort(reverse=True)
                filepath = os.path.join(self.processed_dir, csv_files[0])
                print(f"加载清洗后数据：{csv_files[0]}")
                df = pd.read_csv(filepath, encoding='utf-8-sig')
            else:
                raise FileNotFoundError("未找到清洗后的数据文件")
        else:
            df = pd.read_csv(filepath, encoding='utf-8-sig')
        
        print(f"加载 {len(df)} 条评论数据")
        return df
    
    def sentiment_analysis(self, df):
        """情感分析（使用SnowNLP）"""
        print("开始情感分析...")
        
        # 使用SnowNLP计算情感得分
        def calculate_sentiment(text):
            try:
                if pd.isna(text) or str(text).strip() == "":
                    return 0.5
                s = SnowNLP(str(text))
                return s.sentiments
            except:
                return 0.5
        
        # 计算情感得分
        df['sentiment_score'] = df['content_clean'].apply(calculate_sentiment)
        
        # 情感分类
        def categorize_sentiment(score):
            if score >= 0.7:
                return '积极'
            elif score >= 0.4:
                return '中性'
            else:
                return '消极'
        
        df['sentiment_label'] = df['sentiment_score'].apply(categorize_sentiment)
        
        # 与评分对比分析
        def compare_with_rating(row):
            sentiment_label = row['sentiment_label']
            score = row['score']
            
            if score >= 4 and sentiment_label == '积极':
                return '一致'
            elif score <= 2 and sentiment_label == '消极':
                return '一致'
            elif 2 < score < 4 and sentiment_label == '中性':
                return '一致'
            else:
                return '不一致'
        
        df['sentiment_consistency'] = df.apply(compare_with_rating, axis=1)
        
        # 统计情感分布
        sentiment_dist = df['sentiment_label'].value_counts().to_dict()
        consistency_rate = len(df[df['sentiment_consistency'] == '一致']) / len(df) * 100
        
        print(f"情感分布：{sentiment_dist}")
        print(f"情感与评分一致性：{consistency_rate:.1f}%")
        
        return df, sentiment_dist, consistency_rate
    
    def extract_keywords_tfidf(self, df, top_n=20):
        """使用TF-IDF提取关键词"""
        print("使用TF-IDF提取关键词...")
        
        # 将所有评论合并为一个文本
        all_text = ' '.join(df['content_clean'].dropna().astype(str).tolist())
        
        # 使用jieba的TF-IDF提取关键词
        keywords_tfidf = jieba.analyse.extract_tags(
            all_text, 
            topK=top_n, 
            withWeight=True,
            allowPOS=('n', 'vn', 'v', 'a')  # 名词、动名词、动词、形容词
        )
        
        print(f"TF-IDF前{top_n}关键词：")
        for word, weight in keywords_tfidf[:10]:
            print(f"  {word}: {weight:.4f}")
        
        return keywords_tfidf
    
    def extract_keywords_textrank(self, df, top_n=20):
        """使用TextRank提取关键词"""
        print("使用TextRank提取关键词...")
        
        # 将所有评论合并为一个文本
        all_text = ' '.join(df['content_clean'].dropna().astype(str).tolist())
        
        # 使用jieba的TextRank提取关键词
        keywords_textrank = jieba.analyse.textrank(
            all_text, 
            topK=top_n, 
            withWeight=True,
            allowPOS=('n', 'vn', 'v', 'a')
        )
        
        print(f"TextRank前{top_n}关键词：")
        for word, weight in keywords_textrank[:10]:
            print(f"  {word}: {weight:.4f}")
        
        return keywords_textrank
    
    def topic_modeling_lda(self, df, n_topics=5, n_words=10):
        """主题建模（LDA）"""
        print(f"开始LDA主题建模（{n_topics}个主题）...")
        
        # 准备文本数据
        texts = df['content_clean'].dropna().astype(str).tolist()
        
        # 使用jieba分词
        tokenized_texts = []
        for text in texts:
            words = jieba.lcut(text)
            # 去除停用词和单字
            words = [word for word in words if len(word) > 1]
            tokenized_texts.append(' '.join(words))
        
        # 创建词袋模型
        vectorizer = CountVectorizer(
            max_df=0.95, 
            min_df=2,
            max_features=1000
        )
        X = vectorizer.fit_transform(tokenized_texts)
        
        # LDA模型
        lda = LatentDirichletAllocation(
            n_components=n_topics,
            max_iter=50,
            learning_method='online',
            random_state=42
        )
        lda.fit(X)
        
        # 提取主题词
        feature_names = vectorizer.get_feature_names_out()
        topics = []
        
        for topic_idx, topic in enumerate(lda.components_):
            top_words_idx = topic.argsort()[:-n_words-1:-1]
            top_words = [feature_names[i] for i in top_words_idx]
            topics.append({
                'topic_id': topic_idx,
                'words': top_words,
                'weights': topic[top_words_idx].tolist()
            })
        
        # 打印主题
        print("\nLDA主题发现：")
        for topic in topics:
            print(f"主题 {topic['topic_id']+1}: {', '.join(topic['words'][:5])}")
        
        return topics, lda, X
    
    def generate_wordcloud(self, df, save_path=None):
        """生成词云图"""
        print("生成词云图...")
        
        # 合并所有评论
        all_text = ' '.join(df['content_clean'].dropna().astype(str).tolist())
        
        # 生成词云
        wordcloud = WordCloud(
            font_path='simhei.ttf',
            width=800,
            height=600,
            background_color='white',
            max_words=200,
            max_font_size=100,
            random_state=42
        ).generate(all_text)
        
        # 保存或显示
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.visualization_dir, f"wordcloud_{timestamp}.png")
        
        plt.figure(figsize=(10, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('智能家居适老产品评论词云图', fontsize=16)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"词云图已保存：{save_path}")
        return save_path
    
    def sentiment_trend_analysis(self, df):
        """情感趋势分析（按时间）"""
        print("开始情感趋势分析...")
        
        if 'review_time' not in df.columns:
            print("缺少时间信息，跳过趋势分析")
            return None
        
        try:
            # 转换时间格式
            df['review_date'] = pd.to_datetime(df['review_time'])
            df['review_month'] = df['review_date'].dt.to_period('M')
            
            # 按月分组计算平均情感得分
            monthly_sentiment = df.groupby('review_month').agg({
                'sentiment_score': 'mean',
                'score': 'mean',
                'content': 'count'
            }).reset_index()
            
            monthly_sentiment.columns = ['month', 'avg_sentiment', 'avg_score', 'review_count']
            monthly_sentiment['month'] = monthly_sentiment['month'].astype(str)
            
            print("月度情感趋势：")
            for _, row in monthly_sentiment.iterrows():
                print(f"  {row['month']}: 情感{row['avg_sentiment']:.3f}, 评分{row['avg_score']:.1f}, 评论{row['review_count']}条")
            
            return monthly_sentiment
            
        except Exception as e:
            print(f"情感趋势分析失败：{e}")
            return None
    
    def aspect_based_analysis(self, df):
        """基于方面的情感分析"""
        print("开始基于方面的情感分析...")
        
        # 定义关键方面
        aspects = {
            '安全性': ['安全', '危险', '可靠', '信任', '放心', '担心', '风险'],
            '易用性': ['简单', '复杂', '方便', '麻烦', '容易', '困难', '操作'],
            '功能性': ['功能', '实用', '有用', '无用', '强大', '丰富', '缺乏'],
            '可靠性': ['质量', '耐用', '稳定', '故障', '问题', '维修', '服务'],
            '价格': ['价格', '贵', '便宜', '价值', '性价比', '划算', '昂贵']
        }
        
        aspect_results = {}
        
        for aspect_name, keywords in aspects.items():
            # 查找包含关键词的评论
            aspect_reviews = []
            for idx, row in df.iterrows():
                content = str(row['content_clean']).lower()
                if any(keyword in content for keyword in keywords):
                    aspect_reviews.append({
                        'content': row['content_clean'],
                        'sentiment': row['sentiment_score'],
                        'score': row['score']
                    })
            
            if aspect_reviews:
                aspect_df = pd.DataFrame(aspect_reviews)
                avg_sentiment = aspect_df['sentiment'].mean()
                avg_score = aspect_df['score'].mean()
                count = len(aspect_df)
                
                aspect_results[aspect_name] = {
                    'review_count': count,
                    'avg_sentiment': avg_sentiment,
                    'avg_score': avg_score,
                    'coverage': count / len(df) * 100
                }
                
                print(f"  {aspect_name}: {count}条评论，情感{avg_sentiment:.3f}，评分{avg_score:.1f}，覆盖率{aspect_results[aspect_name]['coverage']:.1f}%")
        
        return aspect_results
    
    def visualize_results(self, df, sentiment_dist, monthly_sentiment, aspect_results):
        """可视化分析结果"""
        print("生成可视化图表...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. 情感分布饼图
        plt.figure(figsize=(10, 8))
        
        plt.subplot(2, 2, 1)
        labels = list(sentiment_dist.keys())
        sizes = list(sentiment_dist.values())
        colors = ['#66b3ff', '#99ff99', '#ff9999']
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.title('情感分布')
        
        # 2. 评分分布直方图
        plt.subplot(2, 2, 2)
        plt.hist(df['score'], bins=20, edgecolor='black', alpha=0.7)
        plt.xlabel('评分')
        plt.ylabel('频数')
        plt.title('评分分布')
        plt.grid(True, alpha=0.3)
        
        # 3. 情感得分分布
        plt.subplot(2, 2, 3)
        plt.hist(df['sentiment_score'], bins=20, edgecolor='black', alpha=0.7, color='orange')
        plt.xlabel('情感得分')
        plt.ylabel('频数')
        plt.title('情感得分分布')
        plt.grid(True, alpha=0.3)
        
        # 4. 方面分析雷达图（如果有数据）
        if aspect_results:
            plt.subplot(2, 2, 4)
            aspects = list(aspect_results.keys())
            sentiments = [aspect_results[a]['avg_sentiment'] for a in aspects]
            
            # 归一化到0-1
            sentiments_norm = [(s - 0.5) * 2 for s in sentiments]  # 0.5为中性
            
            angles = np.linspace(0, 2*np.pi, len(aspects), endpoint=False).tolist()
            sentiments_norm += sentiments_norm[:1]
            angles += angles[:1]
            
            ax = plt.subplot(2, 2, 4, polar=True)
            ax.plot(angles, sentiments_norm, 'o-', linewidth=2)
            ax.fill(angles, sentiments_norm, alpha=0.25)
            ax.set_thetagrids(np.degrees(angles[:-1]), aspects)
            ax.set_title('方面情感分析')
            ax.grid(True)
        
        plt.suptitle('智能家居适老产品评论NLP分析', fontsize=16)
        plt.tight_layout()
        
        viz_file = os.path.join(self.visualization_dir, f"nlp_analysis_{timestamp}.png")
        plt.savefig(viz_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"可视化图表已保存：{viz_file}")
        return viz_file
    
    def save_analysis_results(self, df, sentiment_dist, keywords_tfidf, 
                            keywords_textrank, topics, monthly_sentiment, 
                            aspect_results, consistency_rate):
        """保存分析结果"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. 保存情感分析结果
        sentiment_file = os.path.join(self.analysis_dir, f"sentiment_analysis_{timestamp}.json")
        sentiment_summary = {
            'total_reviews': len(df),
            'sentiment_distribution': sentiment_dist,
            'avg_sentiment_score': df['sentiment_score'].mean(),
            'avg_rating': df['score'].mean(),
            'sentiment_consistency_rate': consistency_rate,
            'aspect_analysis': aspect_results
        }
        
        with open(sentiment_file, 'w', encoding='utf-8') as f:
            json.dump(sentiment_summary, f, ensure_ascii=False, indent=2)
        
        # 2. 保存关键词
        keywords_file = os.path.join(self.analysis_dir, f"keywords_analysis_{timestamp}.json")
        keywords_summary = {
            'tfidf_keywords': dict(keywords_tfidf),
            'textrank_keywords': dict(keywords_textrank),
            'topics': topics
        }
        
        with open(keywords_file, 'w', encoding='utf-8') as f:
            json.dump(keywords_summary, f, ensure_ascii=False, indent=2)
        
        # 3. 保存趋势数据
        if monthly_sentiment is not None:
            trend_file = os.path.join(self.analysis_dir, f"trend_analysis_{timestamp}.json")
            monthly_sentiment.to_json(trend_file, orient='records', force_ascii=False, indent=2)
        
        # 4. 保存带有情感标签的数据
        labeled_file = os.path.join(self.processed_dir, f"labeled_reviews_{timestamp}.csv")
        df.to_csv(labeled_file, index=False, encoding='utf-8-sig')
        
        print(f"分析结果已保存到：{self.analysis_dir}")
        
        return {
            'sentiment_file': sentiment_file,
            'keywords_file': keywords_file,
            'labeled_file': labeled_file
        }
    
    def run_full_analysis(self, input_file=None):
        """运行完整的NLP分析流程"""
        print("=" * 50)
        print("开始NLP深度分析流程")
        print("=" * 50)
        
        # 1. 加载数据
        print("\n1. 加载数据...")
        df = self.load_data(input_file)
        
        # 2. 情感分析
        print("\n2. 情感分析...")
        df, sentiment_dist, consistency_rate = self.sentiment_analysis(df)
        
        # 3. 关键词提取
        print("\n3. 关键词提取...")
        keywords_tfidf = self.extract_keywords_tfidf(df)
        keywords_textrank = self.extract_keywords_textrank(df)
        
        # 4. 主题建模
        print("\n4. 主题建模...")
        topics, lda_model, X = self.topic_modeling_lda(df)
        
        # 5. 情感趋势分析
        print("\n5. 情感趋势分析...")
        monthly_sentiment = self.sentiment_trend_analysis(df)
        
        # 6. 基于方面的分析
        print("\n6. 基于方面的情感分析...")
        aspect_results = self.aspect_based_analysis(df)
        
        # 7. 生成词云
        print("\n7. 生成词云...")
        wordcloud_file = self.generate_wordcloud(df)
        
        # 8. 可视化
        print("\n8. 生成可视化图表...")
        viz_file = self.visualize_results(df, sentiment_dist, monthly_sentiment, aspect_results)
        
        # 9. 保存结果
        print("\n9. 保存分析结果...")
        saved_files = self.save_analysis_results(
            df, sentiment_dist, keywords_tfidf, keywords_textrank,
            topics, monthly_sentiment, aspect_results, consistency_rate
        )
        
        # 10. 输出关键发现
        print("\n" + "=" * 50)
        print("NLP分析完成！关键发现：")
        print("=" * 50)
        
        # 情感分析发现
        pos_rate = sentiment_dist.get('积极', 0) / sum(sentiment_dist.values()) * 100
        print(f"1. 整体情感倾向：{pos_rate:.1f}%的评论为积极情绪")
        print(f"2. 情感与评分一致性：{consistency_rate:.1f}%")
        
        # 关键词发现
        top_keywords = [word for word, _ in keywords_tfidf[:5]]
        print(f"3. 核心关注点：{', '.join(top_keywords)}")
        
        # 方面分析发现
        if aspect_results:
            best_aspect = max(aspect_results.items(), key=lambda x: x[1]['avg_sentiment'])
            worst_aspect = min(aspect_results.items(), key=lambda x: x[1]['avg_sentiment'])
            print(f"4. 表现最好的方面：{best_aspect[0]}（情感得分{best_aspect[1]['avg_sentiment']:.3f}）")
            print(f"5. 需要改进的方面：{worst_aspect[0]}（情感得分{worst_aspect[1]['avg_sentiment']:.3f}）")
        
        # 趋势发现
        if monthly_sentiment is not None and len(monthly_sentiment) > 1:
            first_month = monthly_sentiment.iloc[0]['avg_sentiment']
            last_month = monthly_sentiment.iloc[-1]['avg_sentiment']
            trend = "上升" if last_month > first_month else "下降"
            print(f"6. 情感趋势：整体呈{trend}趋势（{first_month:.3f} → {last_month:.3f}）")
        
        print(f"\n所有分析结果已保存到：{self.analysis_dir}")
        print(f"可视化文件：{viz_file}")
        print(f"词云文件：{wordcloud_file}")
        
        return {
            'dataframe': df,
            'sentiment_distribution': sentiment_dist,
            'keywords_tfidf': keywords_tfidf,
            'topics': topics,
            'aspect_results': aspect_results,
            'saved_files': saved_files,
            'visualization_files': {
                'wordcloud': wordcloud_file,
                'analysis_charts': viz_file
            }
        }

def main():
    """主函数"""
    try:
        # 创建NLP分析器
        nlp_analyzer = ElderlyProductNLP()
        
        # 运行完整分析流程
        results = nlp_analyzer.run_full_analysis()
        
        # 显示详细结果
        print("\n详细分析结果：")
        print("-" * 40)
        
        # 主题分析
        print("\n主题分析：")
        for topic in results['topics']:
            print(f"主题 {topic['topic_id']+1}: {', '.join(topic['words'][:5])}")
        
        # 方面分析详情
        if results['aspect_results']:
            print("\n方面情感分析详情：")
            for aspect, data in results['aspect_results'].items():
                print(f"  {aspect}: {data['review_count']}条评论，情感得分{data['avg_sentiment']:.3f}，覆盖率{data['coverage']:.1f}%")
        
        # 关键词统计
        print("\nTF-IDF权重最高的10个关键词：")
        for word, weight in results['keywords_tfidf'][:10]:
            print(f"  {word}: {weight:.4f}")
        
    except Exception as e:
        print(f"NLP分析出错：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()