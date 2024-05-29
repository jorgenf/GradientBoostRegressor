import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import pandas as pd

def add_features(df):
    df = df.copy()
    df["month"] = df.index.month.astype("category")
    df["dayofweek"] = df.index.day_of_week.astype("category")
    df["year"] = df.index.year.astype("category")
    df["dayofyear"] = df.index.dayofyear.astype("category")
    df["quarter"] = df.index.quarter.astype("category")
    return df


def train():
    df = pd.read_csv("fangst.csv")

    df["dato"] = pd.to_datetime(df["dato"], format='mixed')
    df.set_index("dato", inplace=True)


    new_df = add_features(df)
    features = ["dayofyear", "month", "quarter", "dayofweek"]
    train = new_df.loc[new_df.index < "2022-01-01"]
    test = new_df.loc[new_df.index >= "2022-01-01"]
    train = add_features(train)
    test = add_features(test)

    x_train = train[features]
    y_train = train[["fangst_i_kg"]]

    x_test = test[features]
    y_test = test[["fangst_i_kg"]]

    reg = GradientBoostingRegressor(random_state=0)
    reg.fit(x_train, y_train)
    print(x_test)
    print("___")
    print(reg.predict(x_test))
    #print(reg.score(x_test, y_test))
    result_df = pd.DataFrame({"prediction":reg.predict(x_test)}, index=x_test.index)


    ax = df.plot(style=".", ms=1, figsize=(20,6))
    result_df.plot(ax=ax, style=".", ms=1, figsize=(20,6))
    print(result_df)
    plt.savefig("plots/gradientboostreg.png")

train()

