# -*- coding=utf-8 -*-
# Ver 1.0

import json
from urllib.request import urlopen
from urllib.parse import quote_plus
from pandas.io.json import json_normalize

# 政府統計の総合窓口(e-Stat)
# 統計表のカタログ取得

# keywordをURLエンコーディングする。
# python2ではurllib.quote
field_code = quote_plus(field_code, encoding="utf-8")

# 取得したいデータの統計表IDを指定します。
stat_code = '0003021328'

# ファイルに保存しているIDをセットする。
# ファイルには”appId=アプリケーションID”の形式で記述
with open('data/app_id.txt', encoding='utf-8') as a_file:
    for a_line in a_file:
        app_id = a_line

request = 'http://api.e-stat.go.jp/rest/2.0/app/json/getStatsData?'
stat_id = '&statsDataId=' + stat_code

request_set = request + app_id + stat_id

# urlopen(...).read()はByte型を返すので、decode('utf-8')でstr型に変換している。
resp = urlopen(request_set).read().decode('utf-8')

resp = json.loads(resp)
print('===============================[PARAMETER]============================')
print(resp['GET_STATS_DATA']['PARAMETER'])
print('===============================[RESULT]===============================')
print(resp['GET_STATS_DATA']['RESULT'])
print('==============================[RESULT_INF]============================')
print(resp['GET_STATS_DATA']['STATISTICAL_DATA']['RESULT_INF'])
print('======================================================================')
resp_list = resp['GET_STATS_DATA']['STATISTICAL_DATA']['CLASS_INF']['CLASS_OBJ']
result = json_normalize(resp_list)

for i in range(len(resp_list)):
    result_dict = resp_list[i]
    result = json_normalize(result_dict['CLASS'])
    result.to_excel('data/Stat_Catalog_'+result_dict['@id']+'.xlsx', 
                    sheet_name=result_dict['@id'])
