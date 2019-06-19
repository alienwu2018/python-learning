from flask import request
from flask import Flask,render_template
import json
import requests
from  gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()
app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        header = request.headers
        h=parse_request_header(header)
        data = json.loads(request.get_data().decode("utf-8"))
        try:
            url=data.get('url')   #获取请求的url
            content=crawler(url,h)
            return content
        except:
            return '请求失败，请以{"url":"..."}方式进行post请求'
    elif request.method == 'GET':
        return render_template('form.html')

@app.route('/use_http', methods=['POST'])
def use_http():
    header = request.headers
    ua = header['User-Agent']  #用户代理
    Content_Type = header['Content-Type']
    Accept_Encoding = header['Accept-Encoding']
    Connection = header['Connection']
    dict2 = { 'User-Agent':ua,'Content-Type':Content_Type,'Accept-Encoding':Accept_Encoding,'Connection':Connection}  #构造默认请求头
    name = request.form.get('name')
    data=crawler(name,dict2).decode('utf-8')
    return data

def crawler(url,header):
    try:
        response = requests.get(url,headers=header).content
        return response
    except:
        return '代理失败!'

def parse_request_header(header):
    header_key = []
    header_value = []
    for i in dict(header).keys():
        if i != 'Host'and i !='Content-Length':
            header_key.append(i)
            header_value.append(dict(header)[i])
    dict1=dict(zip(header_key,header_value))  #构造使用者自定义的请求头
    hd = dict1
    return hd


if __name__ == '__main__':
    # app.run(debug=True)
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    http_server.serve_forever()
