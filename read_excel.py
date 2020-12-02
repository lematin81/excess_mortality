"""人口統計のエクセル表を処理のできる形にするスクリプト。バージョン0.4。
コードを洗練したバージョン。"""


import open_poll_excel
import pandas
import globalize
import local_g_code


class Date:
    date = 0

def add_gcode(df, pref): #自治体コードを追加する
    list_of_local_gov = list(df.index) #自治体名が行名になっているのでリストで取得
    df["code"] = "none" #コードを入れる列を加える
    for name in list_of_local_gov: #コードを取得してデータフレームに加えるループ
        citydata = local_g_code.search_code(name,pref)
        df.at[name, "code"] = citydata[1]
    return(df)

def shape_data(df, list_of_index, list_of_keywords):
    #list_of_index = ["place", "total", "death"]  # インデックスにする変数のリスト
    #list_of_keywords = ["市町村", "総数", "死亡"]  # 数値を特定するキーワードのリスト
    # 和暦を取得する
    # インデックス行をリストにする
    get_date = list(df.columns.values)
    # 「現在」 という言葉が入っている要素を探す
    get_date = [str(day) for day in get_date]
    nen_getsu = [s for s in get_date if ("現在" in s) or ("平成" in s) or ("令和" in s)]
    # インデックスに入っていない場合は、3行目までを探す
    if not nen_getsu:
        search_date = df[0:3].values.tolist()
        for get_date in search_date:
            nen_getsu = [s for s in get_date if ("現在" in s) or ("平成" in s) or ("令和" in s)]
            break
    # 和暦を西暦に換算する
    date = globalize.wareki(str(nen_getsu))
    Date.date = date
    # 先頭から5行をスライスして90度回転する
    df_check = df[:5]
    #print(df_check)
    stacked_dfc = df_check.stack()
    # キーワードの位置を取得し、エラーがないかチェックする
    list_of_cell = []  # キーワードの座標のリストを収容するリスト
    n = 0
    for header, keyword in zip(list_of_index, list_of_keywords):
        cell = []  # キーワードの座標のリスト
        cell.append(stacked_dfc[stacked_dfc == keyword].index)
        # print(str(header) + ": " + str(cell))
        list_of_cell.append(cell)
        n += 1
    cs = len(list_of_index)
    if n == cs:
        pass
    else:
        raise Exception("見出しの抽出でエラーが発生しました")  #todo このエラーチェックは機能していない
    """この時点でのlist_of_cellの構造
    四次元のリスト
    1　キーワードの情報のリスト（キーワード3つの場合は3要素）
    2　マルチインデックスであるという情報のリスト（1要素）
    3　各キーワードのアドレス情報のリスト（キーワードが2回出てくる場合は2要素）
    4　アドレス情報本体のタプル。列番号と行番号（したがって2要素）"""
    # dfから「市町村」「総数」「死亡」の列を取り出し、データフレームを作る
    a = len(list_of_cell[0][0])   # 市町村の出現回数からデータフレームサブセットの個数を決める
    list_of_dfs = []  # dfを記録しておくリスト
    i = 0
    while i < a: #データフレームサブセットを作るループ
        index_for_df = []
        for j in range(len(list_of_index)):  #取り出す列名を取得するループ
            cell_addres = []
            for p in range(len(list_of_cell[j][0])):#見出しの位置を取得するル―プ
                cell_addres.append(list_of_cell[j][0][p][1])
            index_for_df.append(cell_addres)
        index_for_dfn = []
        for p in range(len(list_of_index)): #データフレームサブセットで使う列名リストを作るためのループ
            index_for_dfn.append(index_for_df[p][i])
        dfn = df.loc[:, index_for_dfn]  # データフレームサブセットを生成
        pandas.set_option("display.max_columns", None)
        for k in range(len(list_of_index)):#データフレームサブセットの列名を変更するループ。
            for o in range(len(list_of_cell[k][0])):#K番目のキーワードが出てくる列名をすべて書き換える
                dfn = dfn.rename(columns={index_for_df[k][o]: list_of_index[k]})
                pandas.set_option("display.max_columns", None)
        list_of_dfs.append(dfn)#データフレームサブセットをリストに収容する
        i += 1
    # サブセットを縦に結合してデータフレームを作る
    if a == 0:
        df = list_of_dfs[0]
    else:  # サブセットが２個以上の場合なので１から
        m = 1
        df = list_of_dfs[0]
        while m < a:
            df = pandas.concat([df, list_of_dfs[m]])
            m += 1
    # データフレームを整形する
    # total,deathの列の文字が入っているセルをNaNにする
    df["total"] = pandas.to_numeric(df["total"], errors="coerce")
    df["death"] = pandas.to_numeric(df["death"], errors="coerce")
    df = df.dropna(how="any") #NaNセルのある行を削除する。
    df = df.astype({"total": "int", "death": "int"}) #小数点表示をなくすために整数型に変換する
    df = df.replace("[ケ]", "ヶ", regex=True) #表記を総務省形式にそろえる
    df = df.set_index("place") #自治体名をインデックスにする
    df["date"] = date #新しい列を作って日付を入れる
    return(df)

'''def analyse_file(df):
    # ファイルの中身を読む
    # pandasに省略させないで表示
    pandas.set_option("display.max_columns", 50)
    pandas.set_option("display.max_rows", 100)
    print(df.columns.values)'''


if __name__ == "__main__":
    df = open_poll_excel.main() #シートを自動選択する
    #analyse_file(df)  #初期の分析用
    df = shape_data(df)
    df = add_gcode(df)


