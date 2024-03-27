import pandas as pd
import matplotlib.pyplot as plt

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

zillow_data.infer_objects(copy=False)

# Combine both

fed_data = fed_data.dropna()
zillow_data = zillow_data.dropna()

zillow_data.index = zillow_data.index + pd.DateOffset(days=5)

fed_data.set_index('DATE', inplace=True)

combined_data = fed_data.merge(zillow_data, left_index=True, right_index=True)

combined_data.columns = ["interest", "vacancy", "cpi", "price", "value"]

combined_data["adj_price"] = combined_data["price"] / combined_data["cpi"] * 100
combined_data["adj_value"] = combined_data["value"] / combined_data["cpi"] * 100

# plt.plot(combined_data.index, combined_data["adj_price"])
# plt.show()

combined_data["next_quarter_price"] = combined_data["adj_price"].shift(-13)
combined_data = combined_data.dropna()

combined_data["change"] = (combined_data["next_quarter_price"] > combined_data["adj_price"]).astype(int)
print(combined_data["change"].value_counts())

predictors = ["interest", "vacancy", "adj_price", "adj_value"]
target = "change"
 