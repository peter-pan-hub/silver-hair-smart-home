"""
智能家居适老化改造产品评论数据清洗与预处理
包括：数据清洗、文本预处理、特征提取、模拟数据生成
"""

import pandas as pd
import numpy as np
import re
import jieba
import json
import os
from datetime import datetime, timedelta
import random
from collections import Counter

class DataProcessor:
    def __init__(self, data_dir=None):
        """初始化数据处理器"""
        if data_dir is None:
            self.data_dir = r"D:\panze（用户分身）\user\trae\data"
        else:
            self.data_dir = data_dir
            
        self.raw_dir = os.path.join(self.data_dir, "raw")
        self.processed_dir = os.path.join(self.data_dir, "processed")
        self.analysis_dir = os.path.join(self.data_dir, "analysis")
        
        # 创建目录
        for dir_path in [self.data_dir, self.raw_dir, self.processed_dir, self.analysis_dir]:
            os.makedirs(dir_path, exist_ok=True)
        
        # 初始化jieba分词
        self._init_jieba()
        
        print("数据处理器初始化完成")
    
    def _init_jieba(self):
        """初始化jieba分词器，添加适老产品领域词汇"""
        # 适老产品相关词汇
        elderly_terms = [
            "跌倒检测", "语音控制", "远程监控", "一键呼叫", "安全警报",
            "智能手环", "健康监测", "用药提醒", "睡眠监测", "活动轨迹",
            "煤气泄漏", "门窗感应", "紧急求助", "心率监测", "血压监测",
            "血糖监测", "体温监测", "呼吸监测", "防走失", "定位功能",
            "视频通话", "亲情相册", "娱乐功能", "简单易用", "操作方便",
            "误报率低", "电池续航", "充电方便", "信号稳定", "网络连接",
            "售后服务", "安装简单", "使用说明", "老人友好", "界面清晰",
            "反应灵敏", "准确率高", "质量可靠", "价格合理", "性价比高"
        ]
        
        for term in elderly_terms:
            jieba.add_word(term)
    
    def load_data(self, filepath=None):
        """加载数据文件"""
        if filepath is None:
            # 查找最新的数据文件
            json_files = [f for f in os.listdir(self.raw_dir) if f.endswith('.json')]
            csv_files = [f for f in os.listdir(self.raw_dir) if f.endswith('.csv')]
            
            if csv_files:
                csv_files.sort(reverse=True)
                filepath = os.path.join(self.raw_dir, csv_files[0])
                print(f"加载最新的CSV文件：{csv_files[0]}")
                return pd.read_csv(filepath, encoding='utf-8-sig')
            elif json_files:
                json_files.sort(reverse=True)
                filepath = os.path.join(self.raw_dir, json_files[0])
                print(f"加载最新的JSON文件：{json_files[0]}")
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return pd.DataFrame(data)
            else:
                print("未找到数据文件，将使用模拟数据")
                return self.generate_sample_data()
        else:
            # 根据文件扩展名加载
            if filepath.endswith('.csv'):
                return pd.read_csv(filepath, encoding='utf-8-sig')
            elif filepath.endswith('.json'):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return pd.DataFrame(data)
            else:
                raise ValueError("不支持的文件格式，请使用CSV或JSON格式")
    
    def generate_sample_data(self, n_reviews=1000):
        """生成模拟评论数据（用于测试和分析）"""
        print(f"生成 {n_reviews} 条模拟评论数据")
        
        # 产品列表（智能家居适老产品）
        products = [
            {"title": "小米智能跌倒检测仪", "price": "399", "shop": "小米官方旗舰店"},
            {"title": "华为老人语音控制中心", "price": "599", "shop": "华为官方旗舰店"},
            {"title": "海康威视远程监控摄像头", "price": "299", "shop": "海康威视旗舰店"},
            {"title": "360老人安全监测套装", "price": "899", "shop": "360官方旗舰店"},
            {"title": "乐橙智能呼叫器", "price": "199", "shop": "乐橙官方旗舰店"},
            {"title": "安心加跌倒报警手环", "price": "499", "shop": "安心加旗舰店"}
        ]
        
        # 用户列表
        users = ["张大爷", "李奶奶", "王大妈", "赵爷爷", "刘阿姨", "陈叔叔", 
                "周伯伯", "吴婆婆", "郑爷爷", "孙奶奶", "钱大爷", "冯阿姨"]
        
        # 评论模板（正面、中性、负面）
        positive_templates = [
            "这个{product}非常好用，{feature}功能特别适合老人，操作简单，{benefit}。",
            "{product}质量不错，{feature}很实用，老人用起来很方便，{benefit}。",
            "给父母买的{product}，他们很喜欢，{feature}功能反应灵敏，{benefit}。",
            "{product}的设计很人性化，{feature}特别贴心，老人一学就会，{benefit}。",
            "这款{product}性价比很高，{feature}功能超出预期，{benefit}。"
        ]
        
        neutral_templates = [
            "{product}还可以，{feature}功能一般，{issue}但还能接受。",
            "{product}中规中矩，{feature}功能有待改进，{issue}。",
            "买的{product}用了一段时间，{feature}功能还行，{issue}。",
            "{product}没有想象中好，{feature}功能还可以，{issue}。"
        ]
        
        negative_templates = [
            "{product}不太好用，{feature}功能有问题，{issue}让人失望。",
            "买的{product}质量不行，{feature}功能经常出问题，{issue}。",
            "{product}设计不合理，{feature}功能不好用，{issue}。",
            "后悔买了{product}，{feature}功能完全没用，{issue}。"
        ]
        
        # 特征词
        features = ["跌倒检测", "语音控制", "远程监控", "一键呼叫", "安全警报", 
                   "健康监测", "电池续航", "安装使用", "售后服务", "信号稳定"]
        
        # 收益词
        benefits = ["解决了我们的后顾之忧", "老人用得很安心", "子女可以远程关注", 
                   "操作简单老人容易上手", "响应速度快", "准确率高误报少"]
        
        # 问题词
        issues = ["偶尔会误报", "电池不耐用", "安装有点麻烦", "说明书看不懂",
                 "信号不稳定", "反应有点慢", "价格有点贵", "功能太多用不上"]
        
        reviews = []
        
        for i in range(n_reviews):
            # 随机选择产品
            product = random.choice(products)
            
            # 随机选择用户
            username = random.choice(users) + str(random.randint(1, 99))
            
            # 随机生成评分（正面评论4-5分，中性3分，负面1-2分）
            sentiment = random.choices(["positive", "neutral", "negative"], 
                                      weights=[0.6, 0.2, 0.2])[0]
            
            if sentiment == "positive":
                score = random.uniform(4.0, 5.0)
                template = random.choice(positive_templates)
                feature = random.choice(features)
                benefit = random.choice(benefits)
                content = template.format(product=product["title"], 
                                        feature=feature, benefit=benefit)
            elif sentiment == "neutral":
                score = random.uniform(2.5, 3.5)
                template = random.choice(neutral_templates)
                feature = random.choice(features)
                issue = random.choice(issues)
                content = template.format(product=product["title"], 
                                        feature=feature, issue=issue)
            else:  # negative
                score = random.uniform(1.0, 2.5)
                template = random.choice(negative_templates)
                feature = random.choice(features)
                issue = random.choice(issues)
                content = template.format(product=product["title"], 
                                        feature=feature, issue=issue)
            
            # 随机生成时间（2022年1月到2024年12月）
            start_date = datetime(2022, 1, 1)
            end_date = datetime(2024, 12, 31)
            days_diff = (end_date - start_date).days
            random_days = random.randint(0, days_diff)
            review_time = start_date + timedelta(days=random_days)
            
            # 有用数和回复数
            useful_count = random.randint(0, 50)
            reply_count = random.randint(0, 20)
            
            # 平台
            platform = random.choice(["京东", "天猫"])
            
            reviews.append({
                "platform": platform,
                "username": username,
                "score": round(score, 1),
                "content": content,
                "review_time": review_time.strftime("%Y-%m-%d"),
                "useful_count": useful_count,
                "reply_count": reply_count,
                "product_title": product["title"],
                "product_price": product["price"],
                "shop_name": product["shop"],
                "crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        
        df = pd.DataFrame(reviews)
        
        # 保存模拟数据
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sample_file = os.path.join(self.raw_dir, f"sample_reviews_{timestamp}.csv")
        df.to_csv(sample_file, index=False, encoding='utf-8-sig')
        print(f"模拟数据已保存：{sample_file}")
        
        return df
    
    def clean_data(self, df):
        """数据清洗"""
        print("开始数据清洗...")
        
        # 复制数据，避免修改原始数据
        df_clean = df.copy()
        
        # 1. 处理缺失值
        missing_counts = df_clean.isnull().sum()
        print(f"缺失值统计：\n{missing_counts}")
        
        # 删除关键字段缺失的行
        required_cols = ['content', 'score', 'product_title']
        df_clean = df_clean.dropna(subset=required_cols)
        
        # 填充其他缺失值
        df_clean['platform'] = df_clean['platform'].fillna('未知平台')
        df_clean['shop_name'] = df_clean['shop_name'].fillna('未知店铺')
        df_clean['useful_count'] = df_clean['useful_count'].fillna(0)
        df_clean['reply_count'] = df_clean['reply_count'].fillna(0)
        
        # 2. 去除重复评论
        before_dedup = len(df_clean)
        df_clean = df_clean.drop_duplicates(subset=['username', 'content', 'review_time'])
        after_dedup = len(df_clean)
        print(f"去重：{before_dedup} -> {after_dedup} 条（去除 {before_dedup - after_dedup} 条重复）")
        
        # 3. 规范评分（确保在1-5分之间）
        df_clean['score'] = pd.to_numeric(df_clean['score'], errors='coerce')
        df_clean['score'] = df_clean['score'].clip(1, 5)
        
        # 4. 处理文本内容
        df_clean['content_length'] = df_clean['content'].apply(len)
        
        # 删除过短的评论（少于5个字符）
        df_clean = df_clean[df_clean['content_length'] >= 5]
        
        # 5. 提取产品类别
        df_clean['product_category'] = df_clean['product_title'].apply(self._extract_product_category)
        
        # 6. 提取价格数值
        df_clean['price_numeric'] = df_clean['product_price'].apply(self._extract_price)
        
        # 7. 标准化平台名称
        platform_mapping = {
            '京东': '京东', 'JD.com': '京东', 'jd': '京东',
            '天猫': '天猫', 'Tmall': '天猫', 'tmall': '天猫',
            '淘宝': '淘宝', 'Taobao': '淘宝'
        }
        df_clean['platform'] = df_clean['platform'].map(platform_mapping).fillna('其他平台')
        
        print(f"清洗完成，剩余 {len(df_clean)} 条有效评论")
        
        return df_clean
    
    def _extract_product_category(self, title):
        """从产品标题提取类别"""
        title = str(title).lower()
        
        categories = {
            '跌倒检测': ['跌倒', '摔倒', '跌倒检测', '防跌倒'],
            '语音控制': ['语音', '声控', '语音控制', '语音助手'],
            '远程监控': ['监控', '摄像头', '远程', '视频监控'],
            '安全警报': ['报警', '警报', '安全', '紧急呼叫'],
            '健康监测': ['健康', '心率', '血压', '血糖', '体温', '睡眠'],
            '智能手环': ['手环', '手表', '穿戴'],
            '其他': []
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in title:
                    return category
        
        return '其他'
    
    def _extract_price(self, price_str):
        """从价格字符串提取数值"""
        try:
            if pd.isna(price_str):
                return None
            
            # 提取数字
            price_str = str(price_str)
            numbers = re.findall(r'\d+\.?\d*', price_str)
            if numbers:
                return float(numbers[0])
            else:
                return None
        except:
            return None
    
    def preprocess_text(self, df):
        """文本预处理"""
        print("开始文本预处理...")
        
        df_processed = df.copy()
        
        # 1. 文本清洗
        def clean_text(text):
            if pd.isna(text):
                return ""
            
            text = str(text)
            
            # 去除HTML标签
            text = re.sub(r'<.*?>', '', text)
            
            # 去除特殊字符和表情符号
            text = re.sub(r'[^\w\u4e00-\u9fff\s]', '', text)
            
            # 去除多余空格
            text = re.sub(r'\s+', ' ', text).strip()
            
            return text
        
        df_processed['content_clean'] = df_processed['content'].apply(clean_text)
        
        # 2. 分词
        def tokenize(text):
            if not text:
                return []
            
            # 使用jieba分词
            words = jieba.lcut(text)
            
            # 去除停用词
            stopwords = self._load_stopwords()
            words = [word for word in words if word not in stopwords and len(word) > 1]
            
            return words
        
        df_processed['tokens'] = df_processed['content_clean'].apply(tokenize)
        
        # 3. 提取关键词（基于词频）
        all_tokens = []
        for tokens in df_processed['tokens']:
            all_tokens.extend(tokens)
        
        word_freq = Counter(all_tokens)
        top_keywords = word_freq.most_common(50)
        
        print(f"前10个高频关键词：{top_keywords[:10]}")
        
        # 4. 情感分类（基于评分）
        def categorize_sentiment(score):
            if score >= 4:
                return '正面'
            elif score >= 3:
                return '中性'
            else:
                return '负面'
        
        df_processed['sentiment'] = df_processed['score'].apply(categorize_sentiment)
        
        # 5. 提取评论长度特征
        df_processed['word_count'] = df_processed['tokens'].apply(len)
        
        print("文本预处理完成")
        
        return df_processed, top_keywords
    
    def _load_stopwords(self):
        """加载中文停用词表"""
        # 常用中文停用词
        stopwords = {
            '的', '了', '和', '是', '就', '都', '而', '及', '与', '着',
            '或', '一个', '没有', '我们', '你们', '他们', '这个', '那个',
            '一些', '一切', '这样', '那样', '那么', '怎么', '什么', '为什么',
            '因为', '所以', '但是', '而且', '如果', '虽然', '然后', '已经',
            '可以', '可能', '应该', '一定', '非常', '很', '太', '更', '最',
            '比较', '有点', '一些', '一点', '这种', '那种', '这些', '那些',
            '这样', '那样', '这么', '那么', '怎么', '什么', '为什么', '如何',
            '是否', '有无', '不是', '就是', '也是', '都是', '就是', '而是',
            '而是', '而是', '而是', '而是', '而是', '而是', '而是', '而是'
        }
        
        return stopwords
    
    def extract_features(self, df):
        """特征提取"""
        print("开始特征提取...")
        
        features = {}
        
        # 1. 基本统计特征
        features['total_reviews'] = len(df)
        features['avg_score'] = df['score'].mean()
        features['score_distribution'] = {
            '正面(4-5分)': len(df[df['score'] >= 4]),
            '中性(3-4分)': len(df[(df['score'] >= 3) & (df['score'] < 4)]),
            '负面(1-3分)': len(df[df['score'] < 3])
        }
        
        # 2. 平台分布
        platform_dist = df['platform'].value_counts().to_dict()
        features['platform_distribution'] = platform_dist
        
        # 3. 产品类别分布
        category_dist = df['product_category'].value_counts().to_dict()
        features['category_distribution'] = category_dist
        
        # 4. 时间趋势（如果有时间信息）
        if 'review_time' in df.columns:
            try:
                df['review_date'] = pd.to_datetime(df['review_time'])
                df['review_month'] = df['review_date'].dt.to_period('M')
                monthly_counts = df['review_month'].value_counts().sort_index()
                features['monthly_trend'] = monthly_counts.to_dict()
            except:
                features['monthly_trend'] = {}
        
        # 5. 文本特征
        features['avg_word_count'] = df['word_count'].mean() if 'word_count' in df.columns else 0
        features['avg_useful_count'] = df['useful_count'].mean() if 'useful_count' in df.columns else 0
        features['avg_reply_count'] = df['reply_count'].mean() if 'reply_count' in df.columns else 0
        
        # 6. 价格分析
        if 'price_numeric' in df.columns:
            price_data = df['price_numeric'].dropna()
            if len(price_data) > 0:
                features['avg_price'] = price_data.mean()
                features['price_range'] = {
                    'min': price_data.min(),
                    'max': price_data.max(),
                    'median': price_data.median()
                }
        
        print("特征提取完成")
        
        return features
    
    def save_processed_data(self, df, features, top_keywords):
        """保存处理后的数据和特征"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. 保存清洗后的数据
        cleaned_file = os.path.join(self.processed_dir, f"cleaned_reviews_{timestamp}.csv")
        df.to_csv(cleaned_file, index=False, encoding='utf-8-sig')
        print(f"清洗后数据已保存：{cleaned_file}")
        
        # 2. 保存特征
        features_file = os.path.join(self.analysis_dir, f"features_{timestamp}.json")
        with open(features_file, 'w', encoding='utf-8') as f:
            json.dump(features, f, ensure_ascii=False, indent=2)
        print(f"特征数据已保存：{features_file}")
        
        # 3. 保存关键词
        keywords_file = os.path.join(self.analysis_dir, f"keywords_{timestamp}.json")
        with open(keywords_file, 'w', encoding='utf-8') as f:
            json.dump(dict(top_keywords), f, ensure_ascii=False, indent=2)
        print(f"关键词数据已保存：{keywords_file}")
        
        return {
            'cleaned_data': cleaned_file,
            'features': features_file,
            'keywords': keywords_file
        }
    
    def run_pipeline(self, input_file=None):
        """运行完整的数据处理流程"""
        print("=" * 50)
        print("开始数据处理流程")
        print("=" * 50)
        
        # 1. 加载数据
        print("\n1. 加载数据...")
        df = self.load_data(input_file)
        print(f"  加载 {len(df)} 条评论数据")
        
        # 2. 数据清洗
        print("\n2. 数据清洗...")
        df_clean = self.clean_data(df)
        
        # 3. 文本预处理
        print("\n3. 文本预处理...")
        df_processed, top_keywords = self.preprocess_text(df_clean)
        
        # 4. 特征提取
        print("\n4. 特征提取...")
        features = self.extract_features(df_processed)
        
        # 5. 保存结果
        print("\n5. 保存结果...")
        saved_files = self.save_processed_data(df_processed, features, top_keywords)
        
        # 6. 输出摘要
        print("\n" + "=" * 50)
        print("数据处理完成！")
        print("=" * 50)
        print(f"原始数据：{len(df)} 条")
        print(f"清洗后数据：{len(df_clean)} 条")
        print(f"平均评分：{features['avg_score']:.2f}")
        print(f"情感分布：{features['score_distribution']}")
        print(f"产品类别分布：{features['category_distribution']}")
        
        return {
            'dataframe': df_processed,
            'features': features,
            'top_keywords': top_keywords,
            'saved_files': saved_files
        }

def main():
    """主函数"""
    try:
        # 创建数据处理器
        processor = DataProcessor()
        
        # 运行完整流程
        results = processor.run_pipeline()
        
        # 输出关键信息
        print("\n关键发现：")
        print(f"1. 数据规模：{results['features']['total_reviews']} 条有效评论")
        print(f"2. 整体满意度：{results['features']['avg_score']:.2f} 分")
        
        sentiment_dist = results['features']['score_distribution']
        total = sum(sentiment_dist.values())
        positive_rate = sentiment_dist['正面(4-5分)'] / total * 100
        print(f"3. 正面评价比例：{positive_rate:.1f}%")
        
        # 显示热门产品类别
        categories = results['features']['category_distribution']
        if categories:
            top_category = max(categories.items(), key=lambda x: x[1])
            print(f"4. 最热门产品类别：{top_category[0]} ({top_category[1]} 条评论)")
        
        # 显示高频关键词
        print("5. 高频关键词（前10个）：")
        for word, freq in results['top_keywords'][:10]:
            print(f"   {word}: {freq} 次")
        
    except Exception as e:
        print(f"数据处理出错：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()