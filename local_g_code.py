"""自治体名から自治体コードを表示するスクリプト。自治体名、自治体コード、都道府県名をリストにして返す。
local_g_numモジュールによってあらかじめ作成されたjson形式のデータファイルを必要とする。
local_g_numモジュールによってあらかじめ作成されたjson形式の市町村コード変更データファイルを必要とする。
input_local_g_numモジュールによってあらかじめ作成されたjson形式の市町村コード追加データファイルを必要とする。
バージョン0.5。手入力された自治体データにも対応したバージョン"""
import json

class LoadGovData: #jsonファイルを読み込んでデータを生成するクラス。
    path = "c:/Users/lemat/lempy/poll/local_goverment_code.json"
    path2 = "c:/Users/lemat/lempy/poll/changed_local_goverment_code.json"
    path3 = "c:/Users/lemat/lempy/poll/added_local_goverment_code.json"
    datafile = "json"

    # 市町村コードの出力
    def data(self):
        path = self.path
        load_file = open(path, "r")
        data = json.load(load_file)
        self.datafile = data

    #　変更データを出力
    def r_data(self):
        path = self.path2
        load_file = open(path, "r")
        data = json.load(load_file)
        self.datafile = data

    # 合併後データを出力
    def a_data(self):
        path = self.path3
        load_file = open(path, "r")
        data = json.load(load_file)
        self.datafile = data


# 都道府県データを補う
class CheckPref:
    list_of_prefs = []

    def __init__(self):
        pd = LoadGovData()
        pd.data()
        for d in pd.datafile:
            if d["city"] == d["pref"]:
                self.list_of_prefs.append(d["city"])


    def add_pref(self, local_g):
        cityname = local_g[0]
        for p in self.list_of_prefs:
            if p == cityname:
                local_g.pop(1)
                local_g.append(p)
        return(local_g)


# 重複に対処する
def check_data(citydata, local_g):
    #市町村データが二つ以上ある場合
    if len(citydata) > 1:
        #誤入力だったらパスする
        if citydata[0][2] == citydata[1][2]:
            return(citydata)
        #入力された県名と比較する
        if local_g[1]:
            pref = local_g[1]
        else:
            pref = input("同名の市町村があります。都道府県名を入力してください :")
        #正しい市町村をリストの先頭に移動
        for i, city in enumerate(citydata):
            if city[2] == pref:
                citydata.pop(i)
                citydata.insert(0, city)
    else:
        pass
    return(citydata)


def show_code(citydata): #データを出力する
    city = citydata[0][0]
    code = citydata[0][1]
    pref = citydata[0][2]
    print("自治体名　：" + city)
    print("自治体コード　：" + str(code))
    print("都道府県名　：" + pref)

def get_code(local_g): #自治体名からコードを表示する
    code = LoadGovData()
    citydata = [["none", "none", "none"]]
    code.data()
    for d in code.datafile:
        city = d["city"]
        if city == local_g[0]:
            templist = []
            templist.append(d["city"])
            templist.append(d["code"])
            templist.append(d["pref"])
            citydata.append(templist)
    code.r_data()
    for d in code.datafile:
        city = d["old_city"]
        if city == local_g[0]:
            templist = []
            templist.append(d["city"])
            templist.append(d["code"])
            templist.append(d["pref"])
            citydata.append(templist)
    code.a_data()
    for d in code.datafile:
        city = d["old_city"]
        if city == local_g[0]:
            templist = []
            templist.append(d["city"])
            templist.append(d["code"])
            templist.append(d["pref"])
            citydata.append(templist)
    return(citydata)

def search_code(cityname, pref=None): #外部からの呼び出し用
    local_g = [cityname, pref]
    cp = CheckPref()
    local_g = cp.add_pref(local_g)
    citydata = get_code(local_g)
    citydata = check_data(citydata, local_g)
    return(citydata[0])

def cityname():
    local_g = []
    city = input("自治体名を入力してください　：")
    local_g.append(city)
    pref = input("都道府県名を入力してください（省略可） ：")
    local_g.append(pref)
    return(local_g)

if __name__ == "__main__":
    local_g = cityname() #todo [{}]の形にする
    cp = CheckPref()
    local_g = cp.add_pref(local_g)
    citydata = get_code(local_g)
    citydata = check_data(citydata, local_g) # todo 都道府県名の場合の対処
    show_code(citydata)

