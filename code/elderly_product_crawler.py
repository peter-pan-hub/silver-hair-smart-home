"""
智能家居适老化改造产品评论爬虫
目标：爬取京东、天猫等电商平台的适老产品评论数据
数据量目标：10万+条评论
时间范围：2022-2024年
"""

import time
import random
import pandas as pd
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager

class ElderlyProductCrawler:
    def __init__(self):
        """初始化爬虫"""
        self.data_dir = r"D:\panze（用户分身）\user\trae\data"
        self.raw_dir = os.path.join(self.data_dir, "raw")
        self.processed_dir = os.path.join(self.data_dir, "processed")
        
        # 创建目录
        for dir_path in [self.data_dir, self.raw_dir, self.processed_dir]:
            os.makedirs(dir_path, exist_ok=True)
        
        # 初始化浏览器驱动
        self.driver = self._init_driver()
        
        # 搜索关键词列表（智能家居适老产品）
        self.search_keywords = [
            "跌倒检测仪",
            "老人跌倒报警器", 
            "智能语音控制老人",
            "远程监控老人",
            "老人智能家居",
            "适老化智能设备",
            "老人安全监测",
            "智能呼叫器老人",
            "老人健康监测",
            "智能手环老人"
        ]
        
        # 电商平台URL
        self.platforms = {
            "jd": "https://www.jd.com",
            "tmall": "https://www.tmall.com"
        }
        
        print("爬虫初始化完成")
        print(f"数据保存目录：{self.data_dir}")
    
    def _init_driver(self):
        """初始化Edge浏览器驱动"""
        try:
            # 设置Edge选项
            edge_options = Options()
            edge_options.add_argument("--disable-blink-features=AutomationControlled")
            edge_options.add_argument("--disable-gpu")
            edge_options.add_argument("--no-sandbox")
            edge_options.add_argument("--disable-dev-shm-usage")
            edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0")
            
            # 使用webdriver-manager自动管理驱动
            service = Service(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=edge_options)
            
            # 设置隐式等待
            driver.implicitly_wait(10)
            return driver
            
        except Exception as e:
            print(f"初始化浏览器驱动失败：{e}")
            raise
    
    def search_products_jd(self, keyword, max_pages=5):
        """在京东搜索产品并获取产品列表"""
        print(f"开始在京东搜索：{keyword}")
        
        try:
            # 打开京东
            self.driver.get(self.platforms["jd"])
            time.sleep(random.uniform(2, 4))
            
            # 找到搜索框并输入关键词
            search_box = self.driver.find_element(By.ID, "key")
            search_box.clear()
            search_box.send_keys(keyword)
            search_box.send_keys(Keys.ENTER)
            time.sleep(random.uniform(3, 5))
            
            products = []
            page_count = 0
            
            while page_count < max_pages:
                print(f"正在处理第 {page_count + 1} 页")
                
                # 等待商品列表加载
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "gl-item"))
                )
                
                # 获取商品列表
                product_items = self.driver.find_elements(By.CLASS_NAME, "gl-item")
                
                for item in product_items[:20]:  # 每页取前20个商品
                    try:
                        # 获取商品信息
                        product_info = self._extract_product_info_jd(item)
                        if product_info:
                            product_info["search_keyword"] = keyword
                            products.append(product_info)
                    except Exception as e:
                        print(f"提取商品信息失败：{e}")
                        continue
                
                # 翻页
                try:
                    next_button = self.driver.find_element(By.CLASS_NAME, "pn-next")
                    if "disabled" in next_button.get_attribute("class"):
                        print("已到达最后一页")
                        break
                    
                    next_button.click()
                    time.sleep(random.uniform(3, 5))
                    page_count += 1
                    
                except Exception as e:
                    print(f"翻页失败：{e}")
                    break
            
            print(f"京东搜索完成，找到 {len(products)} 个商品")
            return products
            
        except Exception as e:
            print(f"京东搜索失败：{e}")
            return []
    
    def _extract_product_info_jd(self, item):
        """从京东商品元素中提取信息"""
        try:
            # 商品链接
            link_element = item.find_element(By.CSS_SELECTOR, ".p-img a")
            product_url = link_element.get_attribute("href")
            
            # 商品标题
            title_element = item.find_element(By.CSS_SELECTOR, ".p-name a em")
            title = title_element.text.strip()
            
            # 价格
            try:
                price_element = item.find_element(By.CSS_SELECTOR, ".p-price strong i")
                price = price_element.text.strip()
            except:
                price = "未知"
            
            # 评论数
            try:
                comment_element = item.find_element(By.CSS_SELECTOR, ".p-commit strong a")
                comment_text = comment_element.text.strip()
                # 提取数字
                import re
                comment_num = re.findall(r'\d+', comment_text)
                comment_count = int(comment_num[0]) if comment_num else 0
            except:
                comment_count = 0
            
            # 店铺名
            try:
                shop_element = item.find_element(By.CSS_SELECTOR, ".p-shop span a")
                shop_name = shop_element.text.strip()
            except:
                shop_name = "未知"
            
            return {
                "platform": "京东",
                "product_url": product_url,
                "title": title,
                "price": price,
                "comment_count": comment_count,
                "shop_name": shop_name,
                "crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            print(f"提取商品信息失败：{e}")
            return None
    
    def crawl_product_reviews(self, product_info, max_reviews=100):
        """爬取单个商品的评论"""
        print(f"开始爬取商品评论：{product_info['title'][:30]}...")
        
        reviews = []
        try:
            # 打开商品页面
            self.driver.get(product_info["product_url"])
            time.sleep(random.uniform(3, 5))
            
            # 点击"商品评价"标签
            try:
                review_tab = self.driver.find_element(By.CSS_SELECTOR, "#detail .tab-main li:nth-child(5)")
                review_tab.click()
                time.sleep(random.uniform(2, 3))
            except:
                # 尝试其他选择器
                try:
                    review_tab = self.driver.find_element(By.LINK_TEXT, "商品评价")
                    review_tab.click()
                    time.sleep(random.uniform(2, 3))
                except:
                    print("找不到商品评价标签")
                    return reviews
            
            # 爬取评论
            collected_count = 0
            page_num = 1
            
            while collected_count < max_reviews:
                print(f"正在爬取第 {page_num} 页评论")
                
                # 等待评论加载
                time.sleep(random.uniform(2, 3))
                
                # 获取评论元素
                try:
                    review_elements = self.driver.find_elements(By.CSS_SELECTOR, ".comment-item")
                    
                    for review_element in review_elements:
                        try:
                            review = self._extract_review_jd(review_element)
                            if review:
                                review.update({
                                    "product_title": product_info["title"],
                                    "product_price": product_info["price"],
                                    "shop_name": product_info["shop_name"]
                                })
                                reviews.append(review)
                                collected_count += 1
                                
                                if collected_count >= max_reviews:
                                    break
                        except Exception as e:
                            print(f"提取单条评论失败：{e}")
                            continue
                    
                    # 翻页
                    try:
                        next_button = self.driver.find_element(By.CSS_SELECTOR, ".ui-pager-next")
                        if "disabled" in next_button.get_attribute("class"):
                            print("已到达评论最后一页")
                            break
                        
                        next_button.click()
                        time.sleep(random.uniform(3, 5))
                        page_num += 1
                        
                    except Exception as e:
                        print(f"评论翻页失败：{e}")
                        break
                        
                except Exception as e:
                    print(f"获取评论元素失败：{e}")
                    break
            
            print(f"商品评论爬取完成，共获取 {len(reviews)} 条评论")
            return reviews
            
        except Exception as e:
            print(f"爬取商品评论失败：{e}")
            return reviews
    
    def _extract_review_jd(self, review_element):
        """从京东评论元素中提取信息"""
        try:
            # 用户名
            username = review_element.find_element(By.CSS_SELECTOR, ".user-info .name").text.strip()
            
            # 评分
            try:
                score_element = review_element.find_element(By.CSS_SELECTOR, ".star span")
                score_style = score_element.get_attribute("style")
                # 提取宽度百分比
                import re
                width_match = re.search(r'width:(\d+)%', score_style)
                score = int(width_match.group(1)) / 20 if width_match else 5
            except:
                score = 5
            
            # 评论内容
            try:
                content_element = review_element.find_element(By.CSS_SELECTOR, ".comment-con")
                content = content_element.text.strip()
            except:
                content = ""
            
            # 评论时间
            try:
                time_element = review_element.find_element(By.CSS_SELECTOR, ".order-info span")
                review_time = time_element.text.strip()
            except:
                review_time = ""
            
            # 有用数
            try:
                useful_element = review_element.find_element(By.CSS_SELECTOR, ".useful")
                useful_count = useful_element.text.strip()
            except:
                useful_count = "0"
            
            # 回复数
            try:
                reply_element = review_element.find_element(By.CSS_SELECTOR, ".reply")
                reply_count = reply_element.text.strip()
            except:
                reply_count = "0"
            
            return {
                "platform": "京东",
                "username": username,
                "score": score,
                "content": content,
                "review_time": review_time,
                "useful_count": useful_count,
                "reply_count": reply_count,
                "crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            print(f"提取评论信息失败：{e}")
            return None
    
    def crawl_tmall_products(self, keyword, max_pages=3):
        """在天猫搜索产品（简化版本）"""
        print(f"开始在天猫搜索：{keyword}")
        
        try:
            # 打开天猫
            self.driver.get(self.platforms["tmall"])
            time.sleep(random.uniform(3, 5))
            
            # 由于天猫反爬较严，这里提供简化实现
            # 实际使用时可能需要更复杂的处理
            
            print("天猫爬虫需要更复杂的反爬处理，建议使用API或简化数据")
            return []
            
        except Exception as e:
            print(f"天猫搜索失败：{e}")
            return []
    
    def save_data(self, data, data_type="products"):
        """保存数据到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if data_type == "products":
            filename = f"elderly_products_{timestamp}.json"
            filepath = os.path.join(self.raw_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"产品数据已保存：{filepath}")
            
        elif data_type == "reviews":
            filename = f"elderly_reviews_{timestamp}.json"
            filepath = os.path.join(self.raw_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"评论数据已保存：{filepath}")
            
        elif data_type == "csv":
            # 同时保存为CSV格式
            filename = f"elderly_reviews_{timestamp}.csv"
            filepath = os.path.join(self.raw_dir, filename)
            
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            print(f"评论数据已保存为CSV：{filepath}")
        
        return filepath
    
    def run(self, max_products_per_keyword=10, max_reviews_per_product=50):
        """运行主爬虫"""
        print("=" * 50)
        print("开始智能家居适老化改造产品评论爬取")
        print("=" * 50)
        
        all_products = []
        all_reviews = []
        
        # 遍历搜索关键词
        for keyword in self.search_keywords:
            print(f"\n搜索关键词：{keyword}")
            
            # 在京东搜索产品
            products = self.search_products_jd(keyword, max_pages=2)
            
            if products:
                # 保存产品信息
                all_products.extend(products)
                
                # 爬取每个产品的评论
                product_count = 0
                for product in products[:max_products_per_keyword]:
                    if product_count >= max_products_per_keyword:
                        break
                    
                    reviews = self.crawl_product_reviews(product, max_reviews_per_product)
                    if reviews:
                        all_reviews.extend(reviews)
                        product_count += 1
                    
                    # 随机延迟，避免被封
                    time.sleep(random.uniform(5, 10))
        
        # 保存所有数据
        if all_products:
            self.save_data(all_products, "products")
        
        if all_reviews:
            self.save_data(all_reviews, "reviews")
            self.save_data(all_reviews, "csv")
        
        # 统计信息
        print("\n" + "=" * 50)
        print("爬取完成！")
        print(f"总计爬取产品数：{len(all_products)}")
        print(f"总计爬取评论数：{len(all_reviews)}")
        print("=" * 50)
        
        return {
            "products_count": len(all_products),
            "reviews_count": len(all_reviews),
            "search_keywords": self.search_keywords
        }
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            print("浏览器已关闭")

def main():
    """主函数"""
    crawler = None
    
    try:
        # 创建爬虫实例
        crawler = ElderlyProductCrawler()
        
        # 运行爬虫（限制规模用于测试）
        # 正式运行时可以调整参数
        results = crawler.run(
            max_products_per_keyword=5,  # 每个关键词最多爬取5个产品
            max_reviews_per_product=30   # 每个产品最多爬取30条评论
        )
        
        # 显示结果
        print("\n爬取结果汇总：")
        print(f"搜索关键词：{', '.join(results['search_keywords'])}")
        print(f"爬取产品总数：{results['products_count']}")
        print(f"爬取评论总数：{results['reviews_count']}")
        
        # 估计如果全量爬取的数据量
        estimated_full_reviews = results['reviews_count'] * 20  # 假设扩大20倍
        print(f"预计全量爬取评论数：约{estimated_full_reviews}条")
        
    except Exception as e:
        print(f"爬虫运行出错：{e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if crawler:
            crawler.close()

if __name__ == "__main__":
    main()