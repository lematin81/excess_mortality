"""自治体コードを手動入力するスクリプト。あらかじめ作成されたadded_local_goverment_code.jsonに加筆する"""

import json
import pandas


class InputLocalGovCode:
    path = "c:/Users/lemat/lempy/poll/added_local_goverment_code.json"
    newdata = []

    # 入力を受け付ける
    def input(self):
        while True:
            c = input("自治体のデータはありません。手動で入力しますか？（Y/N):").lower()
            if c in ("y", "yes", "n", "no"):
                c = c.startswith("y")
                break
        else:
            print("Y/Nを入力してください")
        if c is True:
            old_city = input("かつての自治体名を入力してください: ")
            city = input("現在の自治体名を入力してください: ")
            code = input("現在の自治体コードを入力してください: ")
            pref = input("都道府県名を入力してください: ")
            tmp_list = [old_city, city, code, pref]
            self.newdata.append(tmp_list)
        else:
            return(None)

    #内容を確認して、出力する（pandasを経由する）
    def comfirm(self):
        print("かつての自治体名: " + self.newdata[0][0])
        print("現在の自治体名: " + self.newdata[0][1])
        print("現在の自治体コード: " + self.newdata[0][2])
        print("都道府県名: " + self.newdata[0][3])
        while True:
            c = input("上記の内容で登録してよろしいですか？（Y/N):").lower()
            if c in ("y", "yes", "n", "no"):
                c = c.startswith("y")
                break
        else:
             print("Y/Nを入力してください")
        if c is True:
            df1 = pandas.read_json(self.path)
            """ open_json = open(self.path, "r")
            jcity = json.load(open_json)
            df1 = jcity #todo jsonファイルをデータフレームに変換する"""
            #print(df1)
            df2 = pandas.DataFrame(self.newdata, columns=["old_city", "city", "code", "pref"])
            #print(df2)
            df = pandas.concat([df1, df2])
            #df = pandas.DataFrame(self.newdata, columns=["old_city", "city", "code", "pref"]) #初回用
            df.to_json(self.path, orient="records")
        else:
            import sys
            sys.exit(0)


# 外部からの呼び出し用
class AddLGData:
    @classmethod
    def start(cls):
        add = InputLocalGovCode()
        add.input()
        add.comfirm()
        return(add.newdata)


if __name__ == "__main__":
    add = InputLocalGovCode()
    add.input()
    add.comfirm()
    print(add.newdata)