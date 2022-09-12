import json
import codecs
with codecs.open("myfile.json", "w", "utf-8") as myfile: #以 utf-8 覆寫模式 開啟
    
    data = { "a": 1, "b": 2, "c": 3, "d": 4, "e": 5 }

    json.dump(data, myfile) #將 data 字典使用json模組丟入 myfile.json檔案

    print(json.load(myfile)) #以json模組讀取全部檔案內容 並印出 (會是字典型態)
