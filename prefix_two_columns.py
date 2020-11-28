'''2コラム型のエクセルファイルを処理するためのスクリプト。完成したdfはcomplete_dataframe.pyに渡す'''
import pandas
import datetime
import os
import local_g_code
import complete_dataframe


def make_file(df, prefa): #作ったが、使わないことに（予備用に保存）
    dfd = df["date"]
    firstyear = str(dfd.iloc[0])
    lastyear = str(dfd.iloc[-1])
    firstyear = firstyear[0:4] + firstyear[5:7]
    lastyear = lastyear[0:4] + lastyear[5:7]
    #print("1sty:{}, lstyear:{}".format(firstyear, lastyear))
    sheetname = str(firstyear + "_" + lastyear)
    path = "C:/Users/lemat/lempy/poll/data/" + prefa + "/" + prefa + sheetname + ".csv"
    dirpath = "C:/Users/lemat/lempy/poll/data/" + prefa
    os.makedirs(dirpath, exist_ok=True)
    df.to_csv(path, encoding="shift_jis")
    print(path)
    print("最終月が既存のデータと重複している可能性があります。ファイルを確認してください。")

def shape_df(df, pref):
    # deathの列の文字が入っているセルをNaNにする
    df["death"] = pandas.to_numeric(df["death"], errors="coerce")
    df = df.dropna(how="any")  # NaNセルのある行を削除する。
    df = df.astype({"death": "int"})  # 小数点表示をなくすために整数型に変換する
    df = df.replace("[ケ]", "ヶ", regex=True)  # 表記を総務省形式にそろえる
    # df = df.set_index("place")  # 自治体名をインデックスにする
    # コードを入れる
    dfc = df["place"]
    list_of_cities = dfc.values.tolist()
    list_of_codes = []
    print("自治体コードを取得します。{}件あります。少し時間がかかります。".format(len(list_of_cities)))
    for city in list_of_cities:
        code = local_g_code.search_code(city, pref)
        list_of_codes.append(code[1])
    df["code"] = list_of_codes
    # 日付とコードでソートする
    df = df.sort_values(["date", "code"])
    # データを渡すための加工
    df = df.astype({"date": str})
    df = df.set_index("place")  # インデックスを他の場合と一緒にする
    return(df)


def make_df(list_of_dfs):
    a = len(list_of_dfs)  # リストに入ったデータフレームを縦に結合する
    n = 1 # データフレームが２個以上の場合なので１から
    df = list_of_dfs[0]
    while n < a:
        df = pandas.concat([df, list_of_dfs[n]])
        n += 1
    return(df)


def main(list_of_dfs, pref, prefa):
    df = make_df(list_of_dfs)
    df = shape_df(df,pref)
    l_d = [df]
    complete_dataframe.main(l_d, prefa)
    #make_file(df, prefa)
