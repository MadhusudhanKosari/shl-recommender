import pandas as pd

def load_train_data():
    df = pd.read_excel("data/shl_data.xlsx")

    df = df[["Query", "Assessment_url"]]
    df = df.dropna()

    return df
