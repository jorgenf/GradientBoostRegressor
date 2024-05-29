import datetime
import xgboost as xgb
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns



class Model():
    def __init__(self):
        self.features = ["dayofyear", "month", "quarter", "dayofweek"]

    def add_features(self, df, plot=False):
        df = df.copy()
        df["month"] = df.index.month.astype("category")
        df["dayofweek"] = df.index.day_of_week.astype("category")
        df["year"] = df.index.year.astype("category")
        df["dayofyear"] = df.index.dayofyear.astype("category")
        df["quarter"] = df.index.quarter.astype("category")
        if plot:
            sns.boxplot(data=df, x="month", y="fangst_i_kg")
            plt.savefig("month")
            plt.clf()

            sns.boxplot(data=df, x="dayofweek", y="fangst_i_kg")
            plt.savefig("dayofweek")
            plt.clf()

            sns.boxplot(data=df, x="year", y="fangst_i_kg")
            plt.savefig("year")
            plt.clf()

            sns.boxplot(data=df, x="dayofyear", y="fangst_i_kg")
            plt.savefig("dayofyear")
            plt.clf()

            sns.boxplot(data=df, x="quarter", y="fangst_i_kg")
            plt.savefig("quarter")
            plt.clf()

        return df

    def train(self):
        self.df = pd.read_csv("fangst.csv")

        self.df["dato"] = pd.to_datetime(self.df["dato"], format='mixed')
        self.latest_date = self.df["dato"].max()
        self.df.set_index("dato", inplace=True)

        train = self.df.loc[self.df.index < "2022-01-01"]
        test = self.df.loc[self.df.index >= "2022-01-01"]

        train = self.add_features(train)
        test = self.add_features(test)


        self.x_train = train[self.features]
        self.y_train = train[["fangst_i_kg"]]

        self.x_test = test[self.features]
        self.y_test = test[["fangst_i_kg"]]

        self.regmodel = xgb.XGBRegressor(base_score=0.5, booster='gbtree',
                               n_estimators=1000,
                               early_stopping_rounds=50,
                               objective='reg:squarederror',
                               max_depth=5,
                               learning_rate=0.01, enable_categorical=True)
        self.regmodel.fit(self.x_train, self.y_train,
                eval_set=[(self.x_train, self.y_train), (self.x_test, self.y_test)],
                verbose=100)




    def predict(self, date):
        date = datetime.datetime.strptime(date, "%d%m%y")
        dates = pd.date_range(self.latest_date,date + datetime.timedelta(days=1) - datetime.timedelta(days=1),freq='d')
        df = pd.DataFrame(dates, columns=["dato"])
        df.set_index("dato", inplace=True)
        df = self.add_features(df)
        prediction = self.regmodel.predict(df[self.features])
        data = {"dato" : dates, "prediction" : prediction}
        prediction_df = pd.DataFrame(data)
        prediction_df.set_index("dato", inplace=True)
        return prediction_df.tail(1)

    def plot_prediction(self):
        prediction = self.regmodel.predict(self.x_test)
        result_df = pd.DataFrame({"prediction": prediction}, index=self.x_test.index)
        ax = self.df.plot(style=".", ms=1, figsize=(20,6))
        ax = result_df.plot(ax=ax, style=".", ms=1, figsize=(20,6))
        plt.savefig("plots/xboostreg.png")

m = Model()
m.train()
m.plot_prediction()

