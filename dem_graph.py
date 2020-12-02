"""超過死亡のデータをグラフにするスクリプト。
バージョン0.1。"""

import pandas
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager


class Graph:
    def graph(self, df, city, prefa, year, s_year):
        # グラフの日本語表示
        font_manager.fontManager.addfont("C:/Users/lemat/lempy/poll/fonts/ipaexg.ttf")
        matplotlib.rc("font", family="IPAexGothic")
        print(df)
        # グラフを表示する
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title(city + "の超過死亡")
        ax.bar(df.index.values, df["2020年"], width=0.4, tick_label=df.index, label="2020年")
        ax.plot(df["平均"], "orange", label="平均")
        ax.plot(df["95%区間上限"], "red", label="95%区間")
        ax.set_xlabel = "月"
        fig.legend(loc="upper right")
        #plt.show()
        file = "result/{0}/{2}_2019vs{3}/graph_{1}{2}_2019vs{3}.png".format(prefa, city, s_year, year)
        print(file)
        plt.savefig(file)


    def modify_df(self, df):
        print(df.columns)
        df["95%区間上限"] = df.apply(self.calc, axis=1)
        return(df)

    def calc(self, x):
        return x.loc["標準偏差"] * 2 + x.loc["平均"]



def main(df, city, prefa, year, s_year):
    g = Graph()
    df = g.modify_df(df)
    g.graph(df, city, prefa, year, s_year)

if __name__ == "__main_":
    main()