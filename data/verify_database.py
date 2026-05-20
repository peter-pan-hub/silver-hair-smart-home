import sqlite3

# 数据库路径
db_path = r'D:\panze（用户分身）\user\trae\file\校赛\elderly_data.db'

# 创建数据库连接
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 查询人口统计数据
print('=== 人口统计数据 ===')
cursor.execute('SELECT * FROM demographic_stats')
demographic_rows = cursor.fetchall()
for row in demographic_rows:
    print(f"年份: {row[11]}, 总人口: {row[1]}, 60岁以上人口: {row[2]} ({row[3]}%), 65岁以上人口: {row[4]} ({row[5]}%), 城镇化率: {row[6]}%, 出生率: {row[7]}‰, 死亡率: {row[8]}‰, 自然增长率: {row[9]}‰, 来源: {row[10]}")

# 查询老龄化产业数据
print('\n=== 老龄化产业数据 ===')
cursor.execute('SELECT * FROM aging_industry')
industry_rows = cursor.fetchall()
for row in industry_rows:
    print(f"产业类型: {row[1]}, 市场规模: {row[2]}亿元, 增长率: {row[3]}%, 年份: {row[4]}, 来源: {row[5]}")

# 查询老年人健康数据
print('\n=== 老年人健康数据 ===')
cursor.execute('SELECT * FROM elderly_health')
health_rows = cursor.fetchall()
for row in health_rows:
    print(f"年龄组: {row[1]}, 慢性病患病率: {row[2]}%, 心理健康评分: {row[3]}, 体育活动率: {row[4]}%, 年份: {row[5]}, 来源: {row[6]}")

# 查询养老服务设施数据
print('\n=== 养老服务设施数据 ===')
cursor.execute('SELECT * FROM elderly_facilities')
facilities_rows = cursor.fetchall()
for row in facilities_rows:
    print(f"设施类型: {row[1]}, 数量: {row[2]}, 床位: {row[3]}, 覆盖率: {row[4]}%, 年份: {row[5]}, 来源: {row[6]}")

# 关闭连接
conn.close()
print('\n数据库验证完成')
