"""
经过观察发现，b站的页面是静态页面，因此抓取信息的时候难度较小
本次实现主要是抓取b站全站排行榜的具体信息
"""
import re
import requests
import xlsxwriter

def bilibili_craw():
    # 创建一个工作薄并添加一张工作表，当然工作表是可以命名的
    workbook = xlsxwriter.Workbook('bilibili_rank.xlsx')
    worksheet = workbook.add_worksheet('Data')
    row0 = ['排名', '标题', '视频链接', '播放量', '评论人数', '视频作者']
    for i in range(0,len(row0)):
        worksheet.write(0,i,row0[i])
    url = "https://www.bilibili.com/ranking"
    req = requests.get(url)
    result = req.text  #获取网页的html
    #抓取从排名1到100的视频具体html
    for i in range(1,101):
        try:
            pattern = '<li class="rank-item"><div class="num">{0}</div><div class="content"><div class="img">(.+)'.format(i)
            news = re.compile(pattern).findall(result)
            # 具体分析
            print("排名第", i)
            if len(news)!=0:
                pattern_title = '<img alt="(.*?)" src="">'
                video_title = re.compile(pattern_title).findall(news[0])
                print("标题为:",video_title[0])
                pattern_url = '<a href="//(.*?)" target="_blank">'
                video_url = re.compile(pattern_url).findall(news[0])
                print("视频链接:","https://"+video_url[0])
                pattern_view = '<span class="data-box"><i class="b-icon play"></i>(.*?)</span>'
                video_view = re.compile(pattern_view).findall(news[0])
                print("播放量:",video_view[0])
                pattern_comment = '<span class="data-box"><i class="b-icon view"></i>(.*?)</span>'
                video_comment = re.compile(pattern_comment).findall(news[0])
                print("评论人数:",video_comment[0])
                pattern_writer = '<span class="data-box"><i class="b-icon author"></i>(.*?)</span>'
                video_writer = re.compile(pattern_writer).findall(news[0])
                print("视频作者:",video_writer[0])
                print("--------------------------------------------")
                #把各项信息写进excel
                row1 = [i,video_title[0],video_url[0],video_view[0],video_comment[0],video_writer[0]]
                for j in range(0,len(row1)):
                    worksheet.write(i, j, row1[j])
            else:
                worksheet.write(i, 0, "找不到视频相关信息")
                print("找不到排名第",i,"的视频的相关信息！")
                print("--------------------------------------------")
        except:
            continue
    #关闭excel
    workbook.close()
#实例化
bilibili_craw()
