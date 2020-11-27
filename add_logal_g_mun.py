"""自治体コードの変更を一括入力するスクリプト。csvファイルから入力する。あらかじめ作成されたadded_local_goverment_code.jsonに加筆する"""

import json
import pandas
import tkinter
from tkinter import filedialog
import local_g_code
import open_excel


class InandOut:
    pathj = "c:/Users/lemat/lempy/poll/added_local_goverment_code.json"
    df = "datafreme"
    dfc = "datafreme from csv"


    # jsonファイルをpandasで開く
    def read_file(self):
        df = pandas.read_json(self.pathj)
        self.df = df

    """# jsonファイルにpandasで書き込む
    def write_file(self, df):
        df.to_json(self.pathj, orient="records")"""

    # csvファイルをpandasで開く
    def read_csv_file(self):
        path = tkinter.filedialog.askopenfilename(initialdir="./", filetypes=[("CSVファイル","*.csv")]) # ファイルダイアログ
        df = pandas.read_csv(path, encoding="shift_jis")
        self.dfc = df


# 読み込んだファイルの内容をadded_local_goverment_code.jsonファイルに加筆する
class AddLocalGovCode2:
    df = "data"
    list_of_citycodes = []

    # codeを補う
    def make_up_for_code(self, df):
        n = len(df)
        for i in range(n):
            city = df.iloc[i, 3]
            pr = df.iloc[i, 5]
            datalist_of_city = local_g_code.search_code(city, pr)
            citycode = datalist_of_city[1]
            pref = datalist_of_city[2]
            if df.iloc[i, 5] != pref:
                c = df.iloc[i, 3]
                print(c + "のコード" + citycode + "は" + pref + c + "のものである可能性があります。")
                correct_code = input("正しいコードを入力してください。 :")
                citycode = correct_code
            else:
                pass
            self.list_of_citycodes.append(citycode)


    #読み込んだファイルからのデータを整形する
    def shape_data(self, df, citycodes):
        df = df.drop(columns=["date", "event", "code"])
        df["code"] = citycodes
        df = df[["old_city", "city", "code", "pref"]]
        self.df = df

    #jsonからのデータとcsvからのデータを結合してjsonファイルにする
    def joint_files(self, df1, df2):
        df = pandas.concat([df1, df2])
        #  重複をチェックする
        dfd = df.duplicated(subset="old_city", keep="last")
        df = df[~dfd]
        print(df)
        #  jsonファイルを出力する
        df.to_json(InandOut.pathj, orient="records")



if __name__ == "__main__":
    base = InandOut()
    base.read_file()
    add = InandOut()
    add.read_csv_file()
    shape = AddLocalGovCode2()
    shape.make_up_for_code(add.dfc)
    shape.shape_data(add.dfc, shape.list_of_citycodes)
    make = AddLocalGovCode2()
    make.joint_files(base.df, shape.df)
