"""死亡の分析のためにエクセルファイルを開くスクリプト。
ファイルダイアログで選択されたファイルからパスを取得して開く。
シートが複数ある場合は、市町村別の死亡数データのあるシートを選んで開く。
複数のファイルを連続して開けるようにしたバージョン。
バージョン0.2"""

import tkinter
from tkinter import filedialog
import pandas as pd

#生成したpandasのデータフレームを格納するクラス
class OeStore:
    dataframes = [] #データフレームを格納するリスト
    path = ["filepath"]  # 複数のパスを収容するリスト


#ファイルを開いて、全てのシートの内容を取得するクラス
class OpenBook:
    contents_of_sheets = [] #2次元のリスト。シート名とコンテンツのリストを複数格納する

    def __init__(self, p):
        #ファイルを一つずつ開く
        #pandasで全てのシートを開いて内容を取得する
        # シート名をリストに収容する
        self.contents_of_sheets.clear() #リストを空にする
        book = pd.ExcelFile(p)
        sheets = book.sheet_names #一次的に利用するシート名のリスト
        # シート名とコンテンツをリストに収容する
        print(p + "を調べています。")
        for s in sheets:
            temp_list = []
            df = pd.read_excel(p, sheet_name=s, dtype="object")
            #スペースを除去するループ
            columns_of_sheet = df.columns.values
            for column in columns_of_sheet:
                df[column] = df[column].astype("str")
                df[column] = df[column].str.replace(" ", "")
                df[column] = df[column].str.replace("　", "")
            temp_list.append(s)
            temp_list.append(df)
            self.contents_of_sheets.append(temp_list)


# シートを自動選択するクラス
class SelectSheet:
    keywords = [] #ここはdem_prefixで決めている変数と連動する
    df = "none" #この後で分析するシート
    errorflag = "none"

    def __init__(self):
        #print("OpenBook.contents_of_sheets :")
        #print(OpenBook.contents_of_sheets)
        self.errorflag = "none"
        c_of_s = OpenBook.contents_of_sheets
        for sheet in c_of_s: #keywordが含まれるかどうか調べるループ
            df = sheet[1] #リスト内リストの２つめ（１つ目にはシート名が入っている）
            print(sheet[0] + "を調べています。")
            dfc = df.iloc[0:5, :] #各データフレームから5行づつ取り出す
            for keyword in self.keywords: #キーワードのループ。Trueならループ継続
                keyword_is_in = False
                for row in dfc.itertuples():  # １行ずつ取り出す（タプルになる）。Trueでストップ
                    if keyword in row:
                        print(keyword + "があります。")
                        keyword_is_in = True
                        break #行のループを抜ける
                else:
                    print(keyword + "がありません。")
                    break #キーワードのループを抜ける
                #print(keyword_is_in)
            if keyword_is_in == True: #シートのループの最後でTrueだった場合（キーワード3つともあり）
                self.df = df
                print(sheet[0] + "を開きます。")
                break
            else:
                print(sheet[0] + "には" + "、".join(map(str, self.keywords)) + "のいずれかが含まれていません。")
        else:
            print("分析できるデータがありません。")
            self.errorflag = "error"

def file_open():
    typ =[("エクセル","xlsx"), ("エクセル", "xls")]
    OeStore.path = tkinter.filedialog.askopenfilename(initialdir="data/", filetypes=typ, multiple=True)


def main(keywords):
    SelectSheet.keywords = keywords
    file_open()
    path = OeStore.path
    for p in path:
        read = OpenBook(p)
        #read.read_sheet(p)
        #print(read.contents_of_sheets) #正しい
        read = SelectSheet()
        if read.errorflag == "error":
            continue
        OeStore.dataframes.append(read.df)
    if read.errorflag == "error":
        raise Exception("error")
    return(OeStore.dataframes)


if __name__ == "__main__":
    file_open()
    for p in OeStore.path:
        read = OpenBook()
        read.read_sheet(p)
        read = SelectSheet()
        if read.errorflag == "error":
            continue
        OeStore.dataframes.append(read.df)
    print(OeStore.dataframes)




