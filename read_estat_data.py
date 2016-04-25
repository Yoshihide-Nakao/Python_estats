# -*- coding=utf-8 -*-
# ver 2.0

import json
from urllib.request import urlopen
from urllib.parse import quote_plus
from pandas.io.json import json_normalize

# 政府統計の総合窓口(e-Stat)
# 統計表データ取得

# 取得項目：東京の老年人口割合［65歳以上人口]
field_code = '#A03503'
# keywordをURLエンコーディングする。
# python2ではurllib.quote
field_code = quote_plus(field_code, encoding="utf-8")

# 取得したいデータの統計表IDを指定します。
# 東京都の社会・人口統計体系のデータの場合は、C0020050201300を指定します。
stat_code = '0003021328'

#e-statにアクセスするためのIDをセットする。
with open('data/app_id.txt', encoding='utf-8') as a_file:
    for a_line in a_file:
        app_id = a_line

request = 'http://api.e-stat.go.jp/rest/2.0/app/json/getStatsData?'
stat_id = '&statsDataId=' + stat_code
field_id = '&cdCat01=' + field_code

request_set = request + app_id + stat_id # + field_id

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
#print(resp['GET_STATS_DATA']['STATISTICAL_DATA']['CLASS_INF'])
print('======================================================================')

resp_list = resp['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE']
result = json_normalize(resp_list)
#result.index = result['@time']
#result.index = result['@cat01']

result.to_excel('data/Stat_Data.xlsx', sheet_name='Data')