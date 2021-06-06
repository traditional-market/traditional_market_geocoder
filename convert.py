import os
import json
from urllib.request import urlopen
from urllib import parse
from urllib.request import Request
from urllib.error import HTTPError

now_path = os.path.dirname(os.path.realpath(__file__))

file = open(f'{now_path}\\config.json',
        'r', encoding='utf-8-sig')
config_data = json.load(file)

def request_geo_code(address):
    address = parse.quote_plus(address)
    API_URL = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query='+address
    request = Request(API_URL)
    request.add_header('X-NCP-APIGW-API-KEY-ID', config_data['CLIENT_ID'])
    request.add_header('X-NCP-APIGW-API-KEY', config_data['CLIENT_SECRET'])
    try:
        response = urlopen(request)
    except HTTPError as e:
        print('HTTP Error!')
        latitude = None
        longitude = None
    else:
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read().decode('utf-8')
            response_body = json.loads(response_body)   # json
            if response_body['addresses'] == [] :
                print("'result' not exist!")
                latitude = None
                longitude = None
            else:
                latitude = response_body['addresses'][0]['y']
                longitude = response_body['addresses'][0]['x']
                print("Success!")
        else:
            print('Response error code : %d' % rescode)
            latitude = None
            longitude = None
    print('RESULT : ',[latitude, longitude])

    return latitude,longitude

def test ():
    a = str(1)
    b = str(2)
    return a,b

def main ():
    file = open(f'{now_path}\\raw_market_data.json',
            'r', encoding='utf-8-sig')
    raw_market = json.load(file)
    list_len = len(raw_market)

    res_list = []

    for idx,item in enumerate(raw_market):
        print(f'\n[{str(idx)} / {list_len}] ...')
        
        cur_item_dict = item
        road_address = item['address_r']
        
        print(road_address)

        latitude, longitude =  request_geo_code(road_address)
        cur_item_dict['position'] = {"latitude":latitude,"longitude":longitude}
        res_list.append(cur_item_dict)
    
    with open(f'{now_path}\\market_data.json', 'w', encoding='UTF8') as make_file:
        json.dump(res_list, make_file,
                ensure_ascii=False, indent="\t")



        

    

if __name__ == "__main__":
    main()
