import pandas as pd






def add_columns(df):
    df["timestamp"] = df["timestamp"].astype(str)

    bins = [-100,18,25,150]
    labels = ["cold", "moderate", "hot"]
    df["temperature_category"] = pd.cut(df["temperature"], bins=bins, labels=labels)

    bins = [-100,10,150]
    labels = ["calm","windy"]

    df["wind_category"] =pd.cut(df["wind_speed"], bins=bins, labels=labels)
    return df.to_dict(orient="records")

