"""元号Ｙ年Ｍ月Ｄ日、等の表現をyyyymmddに直すスクリプト。前後に書かれている文字は無視する。西暦が併記されている場合はエラーになる"""
import re

def wareki(jtime):
    #数字を半角に直す
    zen = "０１２３４５６７８９"
    han = "0123456789"
    trans_table = str.maketrans(zen, han)
    jtime = jtime.translate(trans_table)
    #yearを換算する
    # 直後に「年」がある「元」を１に置換する
    if "元" in jtime:
        jtime = re.sub(r'元(?=年)', "1", jtime)
    else:
        pass
    #直後に「年」がある1-2桁の数字を取得し、2桁の整数型にする（行内内包）
    nen = int(re.search(r'\d{1,2}(?=年)', jtime).group().zfill(2))
    if "昭和" in jtime:
        year = nen + 1925
    elif "平成" in jtime:
        year = nen + 1988
    elif "令和" in jtime:
        year = nen + 2018
    #月数と日数を2ケタの数字にする
    #直後に「月」がある１-2桁の数字を取得し、ゼロパティングする(複数行表記）
    tuki = re.search(r'\d{1,2}(?=月)', jtime)
    tuki = tuki.group()
    #月の数字をゼロパティングする
    month = tuki.zfill(2)
    # 直後に「日」がある1－2桁の数字を取得し、ゼロパティングする(行内内包表記）
    day = re.search(r'\d{1,2}(?=日)', jtime).group().zfill(2)
    #「年」「月」「日」を消す
    date = str(year) + "-" + month + "-" + day
    return(date)

if __name__ =="__main__":
    jtime = "２　平成元年12月1日"
    date = wareki(jtime)
    print(date)

"""年まで、月までの表現にも対応できたらする"""