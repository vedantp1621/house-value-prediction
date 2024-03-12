import pandas as pd

fed_data = ["MORTGAGE30US.csv", "RRVRUSQ156N.csv", "CPIAUCSL.csv"]
zillow_data = ["Metro_median_sale_price_uc_sfrcondo_week.csv", "Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_month.csv"]

# Setting up Fed Data
dfs = [pd.read_csv(path, parse_dates=["DATE"], index_col = ["DATE"]) for path in fed_data]
fed_data = pd.merge_asof(dfs[0],dfs[1], on="DATE")
fed_data = pd.merge_asof(fed_data, dfs[2], on="DATE")


# Setting up Zillow Price Data
dfs = [pd.read_csv(f) for f in zillow_data]

dfs = [pd.DataFrame(df.iloc[3,5:]) for df in dfs]

for df in dfs:
    df.index = pd.to_datetime(df.index)
    df["Month"] = df.index.to_period("M")

zillow_data = dfs[0].merge(dfs[1], on="Month")

zillow_data.index = dfs[0].index

del zillow_data["Month"];

zillow_data.columns = ["Price", "Value"]

zillow_data.ffill()

print(zillow_data.tail(50))


# Combine both

# from datetime import timedelta

# fed_data.index = fed_data.index + timedelta(days=2);
# fed_data = fed_data.dropna(); 



