#encoding:utf-8
import time
import requests
import urllib.request
import json
import pymongo
import asyncio
import aiohttp

class Get_from_Interface:
    def __init__(self,keyword):
        self.header={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
        }
        self.t = str(('%.3f' % time.time())).replace('.', '')
        self.id = int(self.t)+55
        self.np= 2
        self.keyword1 = keyword
        self.keyword2=urllib.request.quote(keyword)
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["唯品会"]
        table=self.db.list_collection_names()
        if keyword not in table:
            self.col = self.db[keyword]

    async def demo(self):
        while True:
            t = str(('%.3f' % time.time())).replace('.', '')
            data = {"method":"SearchRpc.getSearchList","params":{"page":"searchlist.html","channel_id":"","keyword":"{0}".format(self.keyword1),"np":self.np,"ep":20,"brand_ids":"","brand_store_sn":"","props":"","sort":0,"category_id_1_show":"","category_id_1_5_show":"","category_id_2_show":"","category_id_3_show":"","query":"q={0}&channel_id=".format(self.keyword2)},"id":self.id,"jsonrpc":"2.0"}
            url = "https://m.vip.com/server.html?rpc&method=SearchRpc.getSearchList&f=www&_={}".format(t)
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.post(url=url,json=data,headers=self.header)as r:
                        req = await r.text(encoding='utf-8')
                        data = json.loads(req)[0]['result']['data']['products']
                        if len(data) == 0:
                            print('抓取完毕!')
                            break
                        else:
                            for i in data:
                                await self.inser_intoMG(i)
                except Exception as e:
                    print(e)
                    break
            self.id+=1
            self.np+=2

    async def inser_intoMG(self,item):
        self.col.insert_one(dict(item))
        print(item)
        return True


if __name__ == '__main__':
    keyword=input("输入要爬取的关键字:")
    a=Get_from_Interface(keyword)
    asyncio.get_event_loop().run_until_complete(a.demo())