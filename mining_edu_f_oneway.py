from scipy import stats
import pandas as pd
import psycopg2
# 获取数据库数据
conn = psycopg2.connect(database="lagou_job", user="postgres", password="774110919", host="127.0.0.1", port="5432")
cursor = conn.cursor()
sql = "select * from job"
df = pd.read_sql(sql, conn)
# 清洗数据,生成薪水列
dom = []
for i in df['job_salary']:
    i = ((float(i.split('-')[0].replace('k', '').replace('K', '')) + float(i.split('-')[1].replace('k', '').replace('K', ''))) / 2) * 1000
    dom.append(i)
df['salary'] = dom
# 去除无效列
data = df[df.job_education != '不限']
# 生成不同学历的薪水列表
edu = []
for i in ['大专', '本科', '硕士']:
    edu.append(data[data['job_education'] == i]['salary'])
# 单因素方差分析
print(stats.f_oneway(*edu))
