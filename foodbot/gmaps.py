from abc import ABC, abstractmethod
import requests
import googlemaps
import pandas as pd

gmaps = googlemaps.Client(key='AIzaSyBk6_8ZvLIHbbfiZMmcEM5zO6Ey8bq8aTA')
class Food(ABC):

    def __init__(self, area):
        self.area = area  # 搜尋地區
        
        
    @abstractmethod
    def scrape(self):
        pass

class Restaurant(Food):
    
    def scrape(self):
        try:
            keywords = gmaps.geocode(self.area)
            area_geo = keywords[0]['geometry']['location']

            res = gmaps.places(query=None, location=area_geo, radius=1000, language='zh-tw', open_now=True, type='restaurant')
            
            # 預防搜尋沒有結果
            if res['status'] != 'ZERO_RESULTS':
                name = [res['results'][i]['name'] for i in range(len(res['results'])) if res['results'][i]['rating'] >=4]
                address = [res['results'][i]['formatted_address'] for i in range(len(res['results'])) if res['results'][i]['rating'] >=4]
                rating = [res['results'][i]['rating'] for i in range(len(res['results'])) if res['results'][i]['rating'] >=4]
 
                res_dataframe = pd.DataFrame.from_dict(res['results'])
                price = res_dataframe['price_level']
                mapping = {
                    0.0: '隨便吃',
                    1.0: '便宜',
                    2.0: '中等價格',
                    3.0: '有點昂貴',
                    4.0: '非常昂貴'
                }
                price = price.map(mapping)
                price = [p if p== p else '沒有價格帶' for p in price ]   # nan無法跟自己比較 
 
                content = ''
                for n, a, r, p in zip(name, address, rating, price):
                    content += n+ '  '+ str(r)+ '顆星'+ '  *價格:'+ str(p)+ '\n'+ a+ '\n\n'
                             # 店名 + 幾顆星 + 價格 + 地址

                    
                return content
            else:
                return 'Sorry 我好像搜尋不到結果'
        except:
            error = 'Sorry 你的需求怪怪的'
            return error
        