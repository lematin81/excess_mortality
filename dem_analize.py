"""正規化されたデータを使って死亡の計算をするスクリプト。
人口学的分析全般に拡張する汎用性は組み込んでいない。
バージョン0.3。
「平年」と「コロナ後」を自動的に区別できるようにしたバージョン。
"""


import tkinter
from tkinter import filedialog
import pandas
import datetime
from dateutil.relativedelta import relativedelta
from set_pref import *
import dem_graph
import os
import sys


#データを作成するクラス
class MakeData():
    df = "データフレーム"
    dfo = "平年"
    dft = "対象時期"
    s_year = 0

    def __init__(self):
        path = tkinter.filedialog.askopenfilename(initialdir="./", multiple=True)  #ファイルダイアログ
        dfs = []  #リストを順に開けていく
        for p in path:
            df = pandas.read_csv(p, encoding="shift_jis")
            dfs.append(df)
        a = len(dfs)  #リストに入ったデータフレームを縦に結合する
        if a == 0:
            self.df = dfs[0]
        else:  # データフレームが２個以上の場合なので１から
            n = 1
            df = dfs[0]
            while n < a:
                df = pandas.concat([df, dfs[n]])
                n += 1
        #df = df.reset_index() #インデックスを振りなおす
        self.df = df

    # 重複をチェックする
    def check_dupulicate(self):
        # todo バグフィックス必要。１.重複がなくても削除inputが出る。２.重複削除後の死亡数がおかしくなっている可能性がある
        df = self.df
        dfdu = df.duplicated(subset= ["date", "place"], keep=False)
        if dfdu.empty:
            pass
        else:
            print("データに重複があります")
            pandas.set_option("display.max_rows", None)
            print(df[df.duplicated(subset= ["date", "place"], keep=False)])
            u_c = input("重複データの片方を削除しますか？(Y/N) :").lower()
            if u_c == "y":
                self.df  = df.drop_duplicates(subset= ["date", "place"])
            else:
                sys.exit(0)


    # 日付をひと月前にリセットする。データを「平年」と「検討年」に分ける。
    def divide_df(self):
        df = self.df
        df["date"] = pandas.to_datetime(df["date"])  # date列を日付データとして使う
        f_lastmonth = lambda x: x + relativedelta(months=-1)  # 日付を一月前にする（前月のデータのため）
        df["date"] = df["date"].apply(f_lastmonth)
        # 平年の開始位置を聞く
        dfd = df["date"]
        dfd = dfd.sort_values()
        dfd = dfd.tolist() #pandas.Seriesをリストにする
        print("データは{}から始まっています。".format(dfd[0].strftime("%Y-%m-%d")))
        star_year = int(input("平均の計算を始める年を半角4文字で入力してください :"))
        df1 = df[(df["date"] >= datetime.datetime(star_year, 1, 1)) & (df["date"] <= datetime.datetime(2019, 12, 31))]
        self.dfo = df1
        df2 = df[df["date"] >= datetime.datetime(2020, 1, 1)]
        self.dft = df2
        self.s_year = star_year


# 集計対象とする地点を決めるクラス
class SelectPlece:  #todo Makedataのメソッドにするか検討
    list_of_place_code = []

    # データフレームを受け取り、リストに選択結果を入れる
    def __init__(self, df):
        df = df.sort_values(["date", "code"])
        # 一番下の行のdateを取得
        recent_date = df.iloc[-1]["date"]
        # そのdateの行のpleceとcodeを抽出
        dfp = df[df["date"] == recent_date]
        #コードのnoneをドロップする
        dfp = dfp[dfp["code"] != "none"]
        p = dfp[["place", "code"]]
        # リストにする
        list_of_place = p.values.tolist()
        n = len(list_of_place)
        for i in range(n):
            print(str(i) + ": " + str(list_of_place[i][0]))
        while True:
            c = input("計算したい地点を選んでください（1　2　3　…　または all で入力) :")
            if c != "all":
                cl = c.split()
                flag = False #誤入力チェック
                try:
                    cl = list(map(int, cl))
                except ValueError as e:
                    print(e)
                    continue
                for d in cl:
                    if d > n:
                        flag = True
                    else:
                        city = list_of_place[d]
                        self.list_of_place_code.append(city)
                if flag == True:
                    print("数値入力エラーです。")
                    continue
                return
            if c == "all":
                for p in list_of_place:
                    self.list_of_place_code.append(p)
                return


#計算を行うクラス
class Calc:
    # 変数を初期化する
    def __init__(self, code):
        sv = 0  #標準偏差と平均
        pvt = 0  #クロス表
        self.code = code

    def mortality(self, df):
        df = df.assign(month = df["date"].dt.month) #月と年を抽出する
        df = df.assign(year = df["date"].dt.year)
        df.set_index("month", inplace=True)
        dfamr = df.query("code == @self.code") # 地点のデータだけを抽出
        pamr = pandas.pivot_table(dfamr, values="death", index="year", columns="month")  #クロス表
        self.pvt = pamr
        pamr_mean = pamr.mean()  #月ごとの平均
        pamr_std = pamr.std()  #月ごとの標準偏差
        svamr = pandas.concat([pamr_mean,pamr_std], axis=1, join="outer")  #平均と標準偏差
        svamr.columns = ["平均", "標準偏差"]
        self.sv = svamr


# 表を作るクラス
class MakeTable:
    def __init__(self, city, prefa):
        self.table = "dataframe"
        self.year = 0
        self.city = city
        self.prefa = prefa
        dirpath = "result" + "/" + prefa
        os.makedirs(dirpath, exist_ok=True)

    def excess_motality(self, df1, df2):
        df2 = df2.reset_index(level=0)  #マルチインデックスになっているので解除する
        print(df2)
        y = str(df2.at[2, "year"]) + "年" #年列（全て同じ年）の2行目を取得し、2列目の列名にする todo 2021年対応必要
        df2.columns = ["year", y]
        df2 = df2.drop("year", axis=1)  #年列を削除
        df = pandas.concat([df1, df2],axis=1)  #ふたつの表を結合
        df["平均からの超過"] = 0
        df["平均からの超過"] = df.apply(self.clc_exess, axis=1)
        df["標準偏差との比"] = 0
        df["標準偏差との比"] = df.apply(self.clc_rate, axis=1)
        df["超過"] = 0
        df["超過"] = df.apply(self.clc_sfa, axis=1)
        df.insert(0, "place", self.city)
        self.table = df
        self.year = y


    def clc_exess(self, x):
        return x.loc["2020年"] - x.loc["平均"]


    def clc_rate(self, x):
        return x.loc["平均からの超過"] / x.loc["標準偏差"]


    def clc_sfa(self, x):
        nf = x.loc["標準偏差"] * 2
        sfa = x.loc["平均"] + nf
        return x.loc["2020年"] - sfa

    def show_message(self, s_year):
        df = self.table
        dfq = df.query("超過 > 0")
        dfq_index = dfq.index.values # 超過死亡のある月名を返す
        dfq_n = len(dfq_index)
        if dfq_n > 0:
            for index in dfq_index:
                print(self.city + "の" + str(self.year) + str(index) + "月に超過死亡があります。")
            print(dfq)
            o_year = str(s_year) + "_2019vs"
            path = "result/{0}/{1}{2}/".format(self.prefa, o_year, str(self.year), self.city)
            os.makedirs(path, exist_ok=True)
            dem_graph.main(df, self.city, self.prefa, self.year, s_year)
            return(dfq)
        else:
            print(self.city + "には超過死亡はありません。")

    def make_csv(self, s_year):
        df = self.table
        o_year = str(s_year) + "_2019vs"
        path =  "result/{0}/{1}{2}/".format(self.prefa, o_year, str(self.year))
        os.makedirs(path, exist_ok=True)
        file = "{0}{3}{1}{2}.csv".format(path, o_year, str(self.year), self.city)
        print(file)
        df.to_csv(file, encoding="shift_jis")


# 超過死亡のみの表を作るクラス
class MakeExcessTable:
    df = False

    def make_df(self, dfqs):
        a = len(dfqs)
        #print(a)
        if a == 0:
            return
        else:  # データフレームが２個以上の場合なので１から
            n = 1
            df = dfqs[0]
            while n < a:
                df = pandas.concat([df, dfqs[n]])
                n += 1
        self.df = df

    def make_csv(self, prefa, pref, year, s_year):
        df = self.df
        file = "result/" + prefa + "/" + pref + "超過死亡" + str(s_year) + "_2019vs" + str(year) + ".csv"
        dir = "result/{0}/{1}超過死亡{2}_2019vs{3}.csv".format(prefa, pref, str(s_year), str(year))
        # os.makedirs(dir, exist_ok=True)
        print(file)
        df.to_csv(file, encoding="shift_jis")


def main():
    #分析する県を決める
    pref = Aichi()
    print(pref.pref) #注意喚起用
    # 分析の準備をする
    bind = MakeData()
    bind.check_duplicate()
    bind.divide_df()
    select = SelectPlece(bind.df)
    execss_dfs = []
    for placedata in select.list_of_place_code:
        city = placedata[0]
        code = placedata[1]
        # 平年のデータを作成する
        ordinaryyeal = Calc(code)
        ordinaryyeal.mortality(bind.dfo)
        #目標年のデータを作成する
        targetyear = Calc(code)
        targetyear.mortality(bind.dft)
        #超過死亡を計算する
        df1 = ordinaryyeal.sv
        df2 = targetyear.pvt
        df2 = df2.stack()
        #表に整理する
        show = MakeTable(city, pref.prefa)
        show.excess_motality(df1, df2)
        dfq = show.show_message(bind.s_year)
        execss_dfs.append(dfq)
        show.make_csv(bind.s_year)
    execss_dfs = [dfq for dfq in execss_dfs if dfq is not None]
    summary = MakeExcessTable()
    summary.make_df(execss_dfs)
    summary.make_csv(pref.prefa, pref.pref, show.year, bind.s_year)


if __name__ == "__main__":
    main()
    #make_graph()