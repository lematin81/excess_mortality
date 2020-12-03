'''深い階層のフォルダからファイルをすべてコピーするスクリプト。最深部のフォルダ以外は無視する'''

import os
import shutil

def walk_copy(folder, ext, new_folder):
    os.makedirs(new_folder, exist_ok=True)
    lower_ext = ext.lower()
    for foldername, subfolders, filenames in os.walk(folder):
        for filename in filenames:
            if filename.lower().endswith(lower_ext):
                print(os.path.join(foldername, filename), "を", new_folder, "にコピーします。")
                shutil.copy(os.path.join(foldername, filename), new_folder)


if __name__ == "__main__":
    # 必要に応じて、拡張子はxlsとxlsxを使い分けること
    walk_copy("C:/Users/lemat/Downloads/青森県", ".xlsx", "data/aomori/pre")