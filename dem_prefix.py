"""死亡率の計算をするためのデータの正規化を行うシステム全体を動かすスクリプト。
将来的には人口学的分析全般に使うように拡張したい。
別ファイルに定義した都道府県パターンのクラスを必要とする。"""

import open_poll_excel
import read_excel
from read_excel import Date
import complete_dataframe
from set_pref import * #都道府県パターンのインポート


class DeStore: #データを格納するクラス
    list_of_shaped_df = []

class ShapeKeys: #データセット整形のプロセスをスタートさせる
    #分析のタイプを決める変数
    pass

class Course(ShapeKeys): #分析のタイプを決めるためのクラス
    keywords = []  # 利用するデータの列を見つけるためのキーワード
    index = []  # 作成するデータフレームの列名（キーワードと対応する必要がある）

    def set_motal(self):
        keywords = ["市町村", "総数", "死亡"]
        for kw in keywords:
            self.keywords.append(kw)
        index = ["place", "total", "death"]
        for ix in index:
            self.index.append(ix)


class Shape(Course): #データ整形を動かすクラス。県別にクラスをセットする必要がある
    prefa = "a"

    def shape(self):
        dfs = open_poll_excel.main(self.keywords)
        temp_list_of_df = dfs
        t = len(temp_list_of_df)
        i = 1
        print("データを整形しています（少しお待ちください）。")
        for df in temp_list_of_df:
            df = pr.modify(df)
            df = read_excel.shape_data(df, sh.index, sh.keywords)
            df = pr.calc_pref(Date.date, df)
            self.prefa = pr.prefa
            df = read_excel.add_gcode(df, pr.pref)
            DeStore.list_of_shaped_df.append(df)
            print("{}件中、{}件を処理しました。".format(t,i))
            i += 1


pr = Aichi()
print(pr.pref) #注意喚起用
sh = Shape()
sh.set_motal()
sh.keywords = pr.modify_keywords(sh.keywords)
sh.shape()
complete_dataframe.main(DeStore.list_of_shaped_df, pr.prefa)





