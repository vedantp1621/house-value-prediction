# Fed Data needs cleaning

import pandas as pd

fed_data = ["MORTGAGE30US.csv", "RRVRUSQ156N.csv", "CPIAUCSL.csv"]
zillow_data = ["Metro_median_sale_price_uc_sfrcondo_week.csv", "Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_month.csv"]

# Fed Data
dfs = [pd.read_csv(f, parse_dates=True, index_col=0) for f in fed_data]

fed_data = pd.concat(dfs, axis=1)

fed_data = fed_data.ffill()

# Zillow Price Data
dfs = [pd.read_csv(f) for f in zillow_data]

dfs = [pd.DataFrame(df.iloc[3,5:]) for df in dfs]

for df in dfs:
    df.index = pd.to_datetime(df.index)
    df["Month"] = df.index.to_period("M")

price_data = dfs[0].merge(dfs[1], on="Month")

print(price_data)



