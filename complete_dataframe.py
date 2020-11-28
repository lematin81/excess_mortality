"""整形されたデータファイル群を結合し、チェックするスクリプト
バージョン0.1"""

import pandas
from datetime import datetime
from dateutil.relativedelta import relativedelta


class CdStore:
    list_of_arrays = []
    df = "df"  #完成したデータフレーム

#データフレームの中身を確認するクラス
class CheckDf:
    date_in_df = [] #データフレーム（チェック用）に含まれる日付データのリスト

    def count_freq(self):  #確認のために日付と自治体の出現回数を見る
        df = CdStore.df
        dfcf = pandas.crosstab(df["code"], df["date"])  #チェック用のデータフレーム
        print("データフレームに含まれる日付\n" + str(dfcf.columns.values))
        m = len(dfcf.columns)
        if m < 12:
            print("データフレームに含まれる月数が{}ヶ月分しかありません。".format(m))
        d_in_d = dfcf.columns.values #月付を取得する
        d_in_d = d_in_d.tolist() #numpy.ndarrayなのでリストに
        d_in_d.sort()
        for date in d_in_d:
            date = datetime.strptime(date, "%Y-%m-%d") #日付データに変換
            self.date_in_df.append(date)

    # 日付が連続しているかどうかをチェックする
    def check_date(self):
        date_array = self.date_in_df
        n = len(date_array)
        for i in range(1, n):
            firstday = date_array[i - 1] #当該データの直前の日付データ
            #firstday = datetime.strptime(firstday, "%Y-%m-%d")
            secondday = firstday + relativedelta(months=1) #当該データの翌月の日付
            if date_array[i] != firstday:
                if date_array[i] != secondday:
                    print("データエラーの可能性があります！")
                    print("{}の次の日付が{}になっています。".format(firstday.strftime("%Y-%m-%d"), date_array[i].strftime("%Y-%m-%d")))


def make_csv(prefa):  #csvファイルを作成する
    df = CdStore.df
    date_in_df = list(map(str, CheckDf.date_in_df))
    if len(CdStore.list_of_arrays) == 1:
        m1 = date_in_df[0][0:4] + date_in_df[0][5:7]
        m2 = date_in_df[-1][0:4] + date_in_df[-1][5:7]
    else:
        m1 = date_in_df[0][0:4] + date_in_df[0][5:7]
        m2 = date_in_df[-1][0:4] + date_in_df[-1][5:7]
    m = str(m1) + "_" + str(m2)
    file = "data/" + prefa + "/" + prefa + m + ".csv"
    print(file)
    # dfのcode行の型を確認。問題ない。csvファイルがおかしく見えるのはexcel側の問題。
    df.to_csv(file, encoding="shift_jis")

def set_date(): #月末付けの日付を修正する
    df = CdStore.df
    # 月末かどうかを判別する
    date_d = df.at[0, "date"]
    day = date_d[-2:]
    if int(day) == 28:
        print(day)
        df["date"] = pandas.to_datetime(df["date"])  # date列を日付データとして使う
        f_nextmonth = lambda x: x + relativedelta(months=+1)  # 月を一月後にする（同月のデータのため）
        df["date"] = df["date"].apply(f_nextmonth)
        f_firstday = lambda x: x + relativedelta(day=1)  # 日付を１日にする（はっきりさせるため）
        df["date"] = df["date"].apply(f_firstday)
        # todo 日付の形式を修正する（plefix_excelにも適用）pandas.to_datetimeについて調べる
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")
        CdStore.df = df


def combine_dfs():  #データフレームを縦に結合する
    a = len(CdStore.list_of_arrays)
    if a == 0:
        CdStore.df = CdStore.list_of_arrays[0]
    else:  #データフレームが２個以上の場合なので１から
        n = 1
        df = CdStore.list_of_arrays[0]
        while n < a:
            df = pandas.concat([df, CdStore.list_of_arrays[n]])
            n += 1
    df = df.reset_index()
    CdStore.df = df


def main(array, prefa):
    CdStore.list_of_arrays = array
    combine_dfs()
    set_date()
    check = CheckDf()
    check.count_freq()
    check.check_date()
    make_csv(prefa)

