# 指定したファイルの文字コードを調べるスクリプト
import tkinter as tk
from tkinter import filedialog
import cchardet
import pprint

def open_filedialog():
    dir = "C:/user/lemat/lempy"
    fle = filedialog.askopenfilename(initialdir = dir)
    return(fle)

def check_encoding(fle):
    with open(fle, mode="rb") as f:
        b = f.read()
    r = cchardet.detect(b)
    r = r["encoding"]
    result = []
    result.append(str(fle))
    result.append("encoding:")
    result.append(r)
    return(result)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("文字コード")
    root.geometry("400x200")

    fle = open_filedialog()
    result = check_encoding(fle)
    rt = "\n".join(map(str,result))
    # print(rt)

    mg = tk.Message(root, text=rt, width=380, anchor="w").pack()
    root.mainloop()