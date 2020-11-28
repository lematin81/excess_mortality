"""人口学的分析のために都道府県別の変数とメソッドを定義するクラス.
コンストラクタを導入。
バージョン0.2
"""

import local_g_code
import pandas
from dateutil.relativedelta import relativedelta

# todo このクラスの役割を整理する（あまり使っていない）
class Prefecture():
    pref = "a"
    code = "a"
    prefa = "a"

    def set(self, prefdata):
        Prefecture.pref = prefdata[0]
        Prefecture.prefa = prefdata[3]
        self.list_for_carc_pref = ["市部", "町村部"]
        Prefecture.code = prefdata[1]


def for_pref1(df, date, pref):
    # 「市部」と「町村部」を足して、県のデータをつくる
    p_total = df.at["市部", "total"] + df.at["町村部", "total"]
    p_death = df.at["市部", "death"] + df.at["町村部", "death"]
    df.loc[pref] = [p_total, p_death, date]
    return (df)

class Aomori:
    pref = "a"
    prefa = "a"


    def __init__(self):
        prefdata = []
        prefdata = local_g_code.search_code("青森県")
        prefdata.append("aomori")
        self.pref = prefdata[0]
        self.prefa = prefdata[3]
        aomori = Prefecture()
        aomori.set(prefdata)

    # キーワードを修正する
    def modify_keywords(self, keywords):
        return(keywords)

    # データフレームを修正する
    def modify(self, df):
        pass

    #  関数を呼び出す
    def calc_pref(self, date, df):
        df = for_pref1(self.df, date, self.pref)
        return(df)

class Hyogo:
    pref = "a"
    prefa ="a"

    def __init__(self):
        prefdata = []
        prefdata = local_g_code.search_code("兵庫県")
        prefdata.append("hyogo")
        self.pref = prefdata[0]
        self.prefa = prefdata[3]
        aomori = Prefecture()
        aomori.set(prefdata)

    # キーワードを修正する
    def modify_keywords(self, keywords):
        keywords = ["市町名", "総数", "死亡"]
        return(keywords)

    #データフレームを修正する
    def modify(self, df):
        #df.iat[1, 3] = "市町村"
        #df = df.replace("市町名", "市町村")
        df = df.replace("県合計", "兵庫県")
        return(df)

    #県集計（すでにできているので何もしない）
    def calc_pref(self, date, df):
        return(df)

class Osaka:
    pref = "a"
    prefa = "a"
    df = "a"

    def __init__(self):
        prefdata = []
        prefdata = local_g_code.search_code("大阪府")
        prefdata.append("osaka")
        self.pref = prefdata[0]
        self.prefa = prefdata[3]
        # self.df = df
        aomori = Prefecture()
        aomori.set(prefdata)

    # dem_prefix.Course.set_motalのキーワードを修正する
    def modify_keywords(self, keywords):
        keywords = ["市区町村", "総数", "死亡"]
        return(keywords)


    # データフレームを修正する
    def modify(self, df):
        # 2016年10月以降のファイルから一年間の累計の部分を除く
        pandas.set_option('display.max_columns', 100)
        #print(df)
        if "～" in df.loc[2, "Unnamed: 6"]:
            print(df.loc[2, "Unnamed: 6"] + "以下の列を削除しました。")
            df = df.drop(df.columns[[6, 7, 8, 9, 10]], axis=1)
        return(df)


    #  必要がないので、何もしない。
    def calc_pref(self, date, df):
        return (df)

class Kyoto:
    pref = "a"
    prefa = "a"
    df = "a"

    def __init__(self):
        prefdata = []
        prefdata = local_g_code.search_code("京都府")
        prefdata.append("kyoto")
        self.pref = prefdata[0]
        self.prefa = prefdata[3]
        # self.df = df
        aomori = Prefecture()
        aomori.set(prefdata)

    # 必要がないので、何もしない
    def modify_keywords(self, keywords):
        return(keywords)

    #データフレームを修正する
    def modify(self, df):
        df = df.replace("京都府計", "京都府")
        df = df.drop(columns=["Unnamed: 20", "Unnamed: 21"])
        #df = df.drop(df.columns[[21, 22]], axis=1)
        return(df)


    #  必要がないので、何もしない。
    def calc_pref(self, date, df):
        return (df)

class Tokyo:
    pref = "a"
    prefa = "a"
    df = "a"

    def __init__(self):
        prefdata = []
        prefdata = local_g_code.search_code("東京都")
        prefdata.append("tokyo")
        self.pref = prefdata[0]
        self.prefa = prefdata[3]
        # self.df = df
        aomori = Prefecture()
        aomori.set(prefdata)

    # 必要がないので、何もしない
    def modify_keywords(self, keywords):
        return (keywords)

    # データフレームを修正する
    def modify(self, df):
        df = df.replace({"Unnamed: 11": {"-": 0}})
        df.iat[4, 2] = "東京都"
        df.iat[5, 2] = "東京都区部"
        return (df)

    #何もしない
    def calc_pref(self, date, df):
        return (df)

class Chiba:
    pref = "a"
    prefa = "a"
    df = "a"

    def __init__(self):
        prefdata = []
        prefdata = local_g_code.search_code("千葉県")
        prefdata.append("chiba")
        self.pref = prefdata[0]
        self.prefa = prefdata[3]
        # self.df = df
        aomori = Prefecture()
        aomori.set(prefdata)

    # 必要がないので、何もしない
    def modify_keywords(self, keywords):
        return (keywords)

    # データフレームを修正する
    def modify(self, df):
        df.iat[3, 2] = "千葉県"
        return (df)

    # データフレームの日付を修正する
    def calc_pref(self, date, df):
        df["date"] = pandas.to_datetime(df["date"])  # date列を日付データとして使う
        f_nextmonth = lambda x: x + relativedelta(months=+1)  # 月を一月後にする（同月のデータのため）
        df["date"] = df["date"].apply(f_nextmonth)
        f_firstday = lambda x: x + relativedelta(day=1) # 日付を１日にする（はっきりさせるため）
        df["date"] = df["date"].apply(f_firstday)
        return (df)


class Kanagawa:
    pref = "a"
    prefa = "a"
    df = "a"

    def __init__(self):
        prefdata = []
        prefdata = local_g_code.search_code("神奈川県")
        prefdata.append("kanagawa")
        self.pref = prefdata[0]
        self.prefa = prefdata[3]
        # self.df = df
        aomori = Prefecture()
        aomori.set(prefdata)

    # 必要がないので、何もしない
    def modify_keywords(self, keywords):
        return (keywords)

    #
    def modify(self, df):
        df = df.replace("県計", self.pref)
        return (df)

    # データフレームの日付を修正する
    def calc_pref(self, date, df):
        df["date"] = pandas.to_datetime(df["date"])  # date列を日付データとして使う
        f_nextmonth = lambda x: x + relativedelta(months=+1)  # 月を一月後にする（同月のデータのため）
        df["date"] = df["date"].apply(f_nextmonth)
        f_firstday = lambda x: x + relativedelta(day=1)  # 日付を１日にする（はっきりさせるため）
        df["date"] = df["date"].apply(f_firstday)
        return (df)

class Saitama:
    pref = "a"
    prefa = "a"
    df = "a"

    def __init__(self):
        prefdata = []
        prefdata = local_g_code.search_code("埼玉県")
        prefdata.append("saitama")
        self.pref = prefdata[0]
        self.prefa = prefdata[3]
        # self.df = df
        aomori = Prefecture()
        aomori.set(prefdata)

    # 必要がないので、何もしない
    def modify_keywords(self, keywords):
        return (keywords)

    #
    def modify(self, df):
        df = df.replace("総計", self.pref)
        return (df)

    # 必要がないので、何もしない
    def calc_pref(self, date, df):
        return(df)

class Aichi:
    pref = "a"
    prefa = "a"
    df = "a"

    def __init__(self):
        prefdata = []
        prefdata = local_g_code.search_code("愛知県")
        prefdata.append("aichi")
        self.pref = prefdata[0]
        self.prefa = prefdata[3]
        # self.df = df
        aomori = Prefecture()
        aomori.set(prefdata)

    # dem_prefix.Course.set_motalのキーワードを修正する
    def modify_keywords(self, keywords):
        keywords = ["自治体", "総数", "死亡"]
        return (keywords)

    #
    def modify(self, df):
        df = df.replace("増減数", "総数")
        # todo 翌月のデータにする
        return (df)

    # 必要がないので、何もしない
    def calc_pref(self, date, df):
        return(df)