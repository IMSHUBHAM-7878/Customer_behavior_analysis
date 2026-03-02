import pandas as pd
df = pd.read_csv('customer_shopping_behavior.csv')
print(df.columns)
# print(df.isna().sum()) #check how many null values
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x : x.fillna(x.median()))
# print(df.isna().sum())
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ','_')
df = df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})
# print(df.columns)
labels = ['Young Adult','Adult','Middle_aged','Senior']
df['age_group'] = pd.qcut(df['age'],q = 4 , labels = labels)
frequency_mapping = {
    'Fortnightly' : 14,
    'Weekly' : 7,
    'Monthly':30,
    'Quarterly' : 90,
    'Bi-Weekly' : 14,
    'Annually' : 365,
    'Every 3 Months' : 90
}
# df['purchase_freq_days'] = df['frequency_of_purchases'].map(frequency_mapping)
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
# print(df[['purchase_frequency_days','frequency_of_purchases']])
df = df.drop('promo_code_used',axis = 1)
# print(df.columns)
from sqlalchemy import create_engine
username = "root"
password = "admin123"
host = "localhost"
port = "3306"
database = "customer1"
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")
table_name = "mytable"
df.to_sql(table_name,engine,if_exists = "replace",index = False)
pd.read_sql("SELECT * FROM mytable LIMIT 5;",engine)
print(df.columns)
print(df.shape)
# print(df.discount_applied.head(10))


