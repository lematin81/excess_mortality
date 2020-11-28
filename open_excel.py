"""エクセルファイルを開くスクリプト。ファイルダイアログで選択されたファイルからパスを取得して開く。
シートが複数ある場合は、コンソールにリストを表示して選択を待つ。
バージョン0.1"""

from tkinter import filedialog
import pandas as pd


file = "filepath"

def read_file(filepath):
    """pandasで全てのシートを開く"""
    # シート名とコンテンツをリストに収容する
    sheets = ["list of sheetnames"]
    contents_of_sheets = []
    # シート名をリストに収容する
    book = pd.ExcelFile(filepath)
    sheets = book.sheet_names
    # シート名とコンテンツをリストに収容する
    for s in sheets:
        temp_list = []
        df = pd.read_excel(filepath, sheet_name=s, dtype="object")
        temp_list.append(s)
        temp_list.append(df)
        contents_of_sheets.append(temp_list)
    # シートタイトルだけ出力する
    c = contents_of_sheets
    n = len(c)
    for i in range(n):
        print(str(i) + ": " + c[i][0])
    # シートを選択させる
    sheetnum = input("処理したいシートの番号を選んでください: ")
    sheetnum = int(sheetnum)
    df = c[sheetnum][1]
    # pandasに省略させないで表示
    # pd.set_option("display.max_columns", 50)
    # pd.set_option("display.max_rows", 100)
    # print(df)
    return(df)

def open_filedialog():
    """ファイルダイアログを開いてファイルを選択させる"""
    dir = "./"
    fle = filedialog.askopenfilename(initialdir = dir)
    return(fle)

def open():
    file = open_filedialog()
    df = read_file(file)
    return(df)


if __name__ == "__main__":
    file = open_filedialog()
    df = read_file(file)




