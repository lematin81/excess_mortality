"""自治体コードの変換表をつくるスクリプト。
自治体コード表からつくる関数と、市町村コード変更表からつくる関数をもつ。
2005年以前の変更には対応できていない"""
import pandas
import open_excel
import json



#  jsonファイルを作るクラス
class MakejsonFile:
    path = "c:/Users/lemat/lempy/poll/local_goverment_code.json"
    path2 = "c:/Users/lemat/lempy/poll/changed_local_goverment_code.json"

    def data(self, df):
        #jsonファイルを作る
        df.to_json(self.path, orient="records")
        #作ったデータを読み込む
        open_json = open(self.path, "r")
        json_load = json.load(open_json)
        print(json_load)

    def r_data(self, df):
        # jsonファイルを作る
        df.to_json(self.path2, orient="records")
        # 作ったデータを読み込む
        open_json = open(self.path2, "r")
        json_load = json.load(open_json)
        print(json_load)


class RCode():

    # 加工のために分解したデータフレームを再結合し、CSVにし、整形する
    def remake_df(self, list_of_divided_dfs):
        # ddfを再結合する
        n = len(list_of_divided_dfs)
        df = list_of_divided_dfs[0]
        for i in range(1, n - 1):
            #print(i)
            df = pandas.concat([df, list_of_divided_dfs[i]])
        #df.to_csv("整形中2.csv", encoding="shift_jis")
        # 不要な行を削除
        df = df[df["g"] != "削除"] #不要でない行だけを残す
        #行名と列名を付けなおす
        df = df.reset_index(drop=True)
        df = df.rename(columns={"a": "pref", "b": "old_code", "c": "old_city",
                        "d": "old_city_kana", "e": "mode", "f": "date",
                        "g": "code", "h": "city", "i": "city_kana", "j": "event"})
        # csvに
        df.to_csv("整形済.csv", encoding="shift_jis")
        #整形する
        df = df.replace("white", "")
        df = df.drop(columns =["old_city_kana", "mode", "date", "city_kana", "event"])
        return(df)


    #自治体コード変更エクセルを分割して処理する
    def shape_table2_2(self, df):
        # 処理すべきケースの数を確認する（必要に応じて使う）
        df_bool = (df == "名称変更")
        # print(df_bool.sum())
        #分割するためにセクションの最初と終わりを確定する
        list_of_start = []  #セクション開始行のリスト
        for row in df.itertuples():
            if row.a != "white":
                list_of_start.append(row[0])
        secn = len(list_of_start)
        list_of_divided_dfs = []  #分割したdfを格納するリスト
        for i in range(secn - 1): #セクション開始、終了位置を把握してdfを切り出す
            start_row = list_of_start[i]
            end_row = list_of_start[i+1] - 1
            ddf = df.loc[start_row:end_row, :]
            ddf = ddf.reset_index(drop=True)
            list_of_divided_dfs.append(ddf)
            #print("start_row: " + str(start_row))
        ddf = df.loc[1438] #最終行の処理（ここだけが単独行で1セクション）
        list_of_divided_dfs.append(ddf)

        #分割したデータフレームごとに処理する
        print("ケース数: " + str(len(list_of_divided_dfs)))
        # 市制施行のケース　（全11件。処理が必要でない１件を除き、全件完了）
        n = 0  # チェック用
        for ddf in list_of_divided_dfs:
            try:
                if ddf.iloc[0, 9] == "市制施行":
                    ddf.iat[1, 1] = ddf.iat[0, 1]
                    ddf.iat[1, 2] = ddf.iat[0, 2]
                    n += 1
                    #print(ddf)
            except pandas.core.indexing.IndexingError as e:
                print("市制施行 を処理中に" + str(e) + "が発生しましたが、処理を続行します。")
                pass

        # 編入合併ケースの処理　127ケース 完了
        n = 0 #チェック用
        for ddf in list_of_divided_dfs:
            try:
                if ddf.iloc[0, 9] == "編入合併":
                    if ddf.iloc[0, 6] != "削除":
                        r = len(ddf)
                        for i in range(1,r):
                            ddf.iat[i, 6] = ddf.iat[0, 6]
                            ddf.iat[i, 7] = ddf.iat[0, 7]
                        #print("ケース１")
                        #print(ddf)
                    else:
                        r = len(ddf)
                        for l in range(r-1):
                            ddf.iat[l, 6] = ddf.iat[r-1, 6]
                            ddf.iat[l, 7] = ddf.iat[r-1, 7]
                        #print("ケース２")
                        #print(ddf)
                    #print("編入合併: " + str(n))
                    n += 1
            except pandas.core.indexing.IndexingError as e:
                print("編入合併 を処理中に" + str(e) + "が発生しましたが、処理を続行します。")
                pass

        # 「編入合併後は」とあるケースを処理。全3件。処理終了
        n = 0
        for ddf in list_of_divided_dfs:
            try:
                if ddf.iloc[0, 9] == "編入合併後は":
                    if ddf.iloc[0, 6] != "削除":
                        r = len(ddf)
                        for i in range(1,r):
                            ddf.iat[i, 6] = ddf.iat[0, 6]
                            ddf.iat[i, 7] = ddf.iat[0, 7]
                        #print("ケース１")
                        #print(ddf)
                    else:  #「編入合併後は」では、ケース２は存在しない
                        r = len(ddf)
                        for l in range(r - 1):
                            ddf.iat[l, 6] = ddf.iat[r - 1, 6]
                        #print("ケース２")
                        #print(ddf)
                #print("編入合併後は: " + str(n))
                n += 1
            except pandas.core.indexing.IndexingError as e:
                print("編入合併後は を処理中に" + str(e) + "が発生しましたが、処理を続行します。")
                pass

        #政令指定都市へ移行のケースを処理。全5件、完了
        n = 0
        for ddf in list_of_divided_dfs:
            try:
                if ddf.iloc[0, 9] == "政令指定都市へ移行":
                    r = len(ddf)
                    for i in range(2, r):  #新区名を入れる
                        a = ddf.iat[0, 2] + ddf.iat[i, 7]
                        #print(a)
                        ddf.iat[i, 7] = a
                    for j in range(1, r):  #旧市名と旧コードを入れる
                        ddf.iat[j, 2] = ddf.iat[0, 2]
                        ddf.iat[j, 1] = ddf.iat[0, 1]
                        #print(ddf)
                    #print(n)
                    n += 1
            except pandas.core.indexing.IndexingError as e:
                print("政令都市へ移行 を処理中に" + str(e) + "が発生しましたが、処理を続行します。")
                pass

        #「政令指定都市」ケースの処理。　1件。
        for ddf in list_of_divided_dfs:
            try:
                if ddf.iloc[0, 9] == "政令指定都市":
                    r = len(ddf)
                    for i in range(2, r):  # 新区名と旧コードを入れる
                        a = ddf.iat[0, 2] + ddf.iat[i, 7]
                        #print(a)
                        ddf.iat[i, 7] = a
                    for j in range(1, r):  # 旧市名を入れる
                        ddf.iat[j, 2] = ddf.iat[0, 2]
                        ddf.iat[j, 1] = ddf.iat[0, 1]
                    #print(ddf)
                # print(n)
            except pandas.core.indexing.IndexingError as e:
                print("政令指定都市 を処理中に" + str(e) + "が発生しましたが、処理を続行します。")
                pass

        #「政令指定」ケースの処理。1件
        for ddf in list_of_divided_dfs:
            try:
                if ddf.iloc[0, 9] == "政令指定\n都市へ移行":
                    r = len(ddf)
                    for i in range(2, r):  # 新区名と旧コードを入れる
                        a = ddf.iat[0, 2] + ddf.iat[i, 7]
                        #print(a)
                        ddf.iat[i, 7] = a
                    for j in range(1, r):  # 旧市名を入れる
                        ddf.iat[j, 2] = ddf.iat[0, 2]
                        ddf.iat[j, 1] = ddf.iat[0, 1]
                    #print(ddf)
                # print(n)
            except pandas.core.indexing.IndexingError as e:
                print("政令指定\n都市へ移行 を処理中に" + str(e) + "が発生しましたが、処理を続行します。")
                pass
        #新設合併を処理　262件
        n = 0
        for ddf in list_of_divided_dfs:
            try:
                if ddf.iloc[0, 9] == "新設合併":
                    if ddf.iloc[0, 6] != "削除":
                        r = len(ddf)
                        for i in range(1, r):
                            ddf.iat[i, 6] = ddf.iat[0, 6]
                            ddf.iat[i, 7] = ddf.iat[0, 7]
                        #print("ケース１")
                        #print(ddf)
                    else:
                        r = len(ddf)
                        for j in range(r-1):
                            ddf.iat[j, 6] = ddf.iat[r - 1, 6]
                            ddf.iat[j, 7] = ddf.iat[r - 1, 7]
                        #print("ケース２")
                        #print(ddf)
                        #n += 1
                        #print(n)
            except pandas.core.indexing.IndexingError as e:
                print("新設合併 を処理中に" + str(e) + "が発生しましたが、処理を続行します。")
                pass
        # 「さいたま市区の…」　1件。処理不要
        #  名称変更　3件。　処理不要
        #  北海道における支庁制度改革に伴う所管区域の変更　全1件。処理不要
        #  取りこぼしが一件あるかもしれない。エラー対応でなんとかする。
        #  県名のwhiteを消す
        try:
            for ddf in list_of_divided_dfs:
                r = len(ddf)
                for i in range(1, r):
                    if ddf.iat[i, 0] == "white":
                        ddf.iat[i, 0] = ddf.iat[0, 0]
        except TypeError as e:
            print("データフレームの処理中に" + str(e) + "が発生しましたが、処理を続行します。")
            pass
        return(list_of_divided_dfs)

    #自治体コード変更エクセルを整形する（2－2に引き継ぐ）
    def shape_table2(self, df):
        # 　列の型を決めて、コードの0脱落を防ぐ
        # df = df.astype(str)
        df = df.dropna(how="all")
        #df = df.dropna(thresh=2, axis=1)  #欠損値でない要素が一つ以下の行を削除(うまくいかない）
        df = df.fillna("white") #人間用の記号を除去する
        df = df.replace("〃", None) #勝手にffillが行われている
        # 列名を変更する
        df.columns = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
        # 行ごとに空白等を埋めるループ
        for row in df.itertuples():
            # コード名の「同左」を消す
            if row.g == "同左":
                df.at[row[0], "g"] = row.b
            # 市町村名の「同左」を消す
            if row.h == "同左":
                df.at[row[0], "h"] = row.c
            urn = int(row[0]) - 1
            """# 県名のnashiを消す
            if row.a == "white":
                pref = df.at[urn, "a"]
                df.at[row[0], "a"] = pref #KeyErorr: 533　ここは放棄。index533が存在してない！"""
        #df.to_csv("整形中.csv", encoding="shift_jis")
        return(df)


class Code:
    def shape_table(self, df):  #自治体コードファイルを作る関数
        #列名を変更する
        list_of_columns = list(df.columns.values)
        list_of_headers = ["code", "pref", "city", "pref_kana", "city_kana"]
        n = 0
        for header in list_of_columns:
            df = df.rename(columns={header : list_of_headers[n]})
            n += 1
        #　列の型を決めて、コードの0脱落を防ぐ
        df = df.astype({"code": str})
        #都道府県行の「city」列のNanを埋める
        df = df.fillna("欠損")
        stacked_df = df.stack()
        stacked_df = stacked_df.replace("欠損", None)
        stacked_df = stacked_df.fillna(method="ffill")
        df = stacked_df.unstack()
        df = df.iloc[:,:-2]
        return(df)

if __name__ == "__main__":
    df = open_excel.open()
    code = Code()
    df = code.shape_table(df)
    print(df)
    mk = MakejsonFile()
    mk.data(df)

    """df = open_excel.open()
    rcode = RCode()
    df = rcode.shape_table2(df)
    list_of_divided_dfs = rcode.shape_table2_2(df)
    df = rcode.remake_df(list_of_divided_dfs)
    mk2 = MakejsonFile()
    mk2.r_data(df)"""
