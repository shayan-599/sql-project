from pathlib import Path
import pandas as pd

print("Starting data cleaning script")
file_path = r"c:\Users\PC\Downloads\first project\supermarket-sales-analysis\Sample - Superstore.csv"
df = pd.read_csv(file_path, encoding="latin1")
print(df.shape)
print(df.columns.to_list())
df.info()
print(df.isnull().sum())
print(df.head(5))

#replacing space and hyphen 
df.columns=(
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
    )
print(df.columns.to_list())

#proper date format
df['order_date']= pd.to_datetime(df['order_date'])
df['ship_date']= pd.to_datetime(df['ship_date'])
df["shipping_days"] = (df["ship_date"] - df["order_date"]).dt.days
df["profit_margin"] = df["profit"] / df["sales"]
print(df.dtypes)


#duplicate(row id is foreign key)
print(df.duplicated().sum())
print(df['row_id'].duplicated().sum())

#unique(saves storage)
print(df['region'].unique())
print(df['category'].unique())
print(df['ship_mode'].unique())
print(df['segment'].unique())


#useful date
df["order_year"] = df['order_date'].dt.year
df["order_month_num"]= df['order_date'].dt.month
df["order_day_of_week"]= df['order_date'].dt.day_name()
df["order_month"]= df['order_date'].dt.to_period("M").astype(str)


#loking impossile values
print(df[['sales','quantity','discount','profit']].describe())

#save cleaned data
output_dir = Path("c:/Users/PC/Downloads/first project/supermarket-sales-analysis/output")
output_dir.mkdir(parents=True, exist_ok=True)   
df.to_csv(output_dir / "cleaned_superstore_data.csv", index=False)
print('clean file saved')
