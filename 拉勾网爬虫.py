#encoding:utf-8
import aiohttp
import asyncio
import pymongo


async def lagou_crawl():
    header = {
        'Accept-Encoding': 'gzip',
        'Connection': 'keep-alive',
        'Host': 'gate.lagou.com',
        'Referer': 'https://m.lagou.com/search.html',
        'X-L-JANUS-STRATEGY': '{"strategies":[{"key":"unlimited_deliver","value":"A"}]}',
        'X-L-REQ-HEADER': '{"userToken":"(APP抓包获取token)","reqVersion":71000,"lgId":"008796754926520_1560423518612","appVersion":"7.10.1","userType":0,"deviceType":200}',
        'User-Agent': 'okhttp/3.11.0',
    }
    url_format = "https://gate.lagou.com/v1/neirong/positions/similarPositions/{0}/"
    pageNo = 1
    while True:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url=url_format.format(pageNo),headers=header) as r:
                    req=await r.json(encoding='utf-8')
                    if len(req['content'])>0:
                        print(req)
                        await inser_msg(table,req)
            except Exception as e:
                print(e)
                break
        pageNo+=1

async def inser_msg(table,item):
    table.insert_one(dict(item))
    return True



if __name__ == '__main__':
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    db = myclient['拉勾网']
    table = db['招聘数据']
    asyncio.get_event_loop().run_until_complete(lagou_crawl())

