package main

import (
	"encoding/json"
	"fmt"
	"gopkg.in/mgo.v2"
	"io/ioutil"
	"net/http"
	"os"
	"strconv"
	"time"
)


func lagou_crawl(){
	page := "1"
	count := int(1)
	for {
		client := &http.Client{}
		resp, err := http.NewRequest("GET", "https://gate.lagou.com/v1/neirong/positions/similarPositions/"+page, nil)
		if err != nil {
			fmt.Println(err)
		}
		resp.Header.Add("Accept-Encoding", "gzip")
		resp.Header.Add("Connection", "keep-alive")
		resp.Header.Add("Host", "gate.lagou.com")
		resp.Header.Add("Referer", "https://m.lagou.com/search.html")
		resp.Header.Add("X-L-JANUS-STRATEGY", `{"strategies":[{"key":"unlimited_deliver","value":"A"}]}`)
		resp.Header.Add("X-L-REQ-HEADER", `{"userToken":"(APP抓包获取token)","reqVersion":71000,"lgId":"008796754926520_1560423518612","appVersion":"7.10.1","userType":0,"deviceType":200}`)
		resp.Header.Add("User-Agent", "okhttp/3.11.0")
		response, err := client.Do(resp)
		if err != nil {
			fmt.Println(err)
		}
		defer response.Body.Close()
		body, err := ioutil.ReadAll(response.Body)
		if err != nil {
			fmt.Println(err)
		}
		data := string(body)
		if (len([]rune(data))>58) {
			fmt.Println(data)
			go insert_mgdb(data)
		}
		go make_file(page)
		count +=1
		page = strconv.Itoa(count)
	}
   }

func make_file(page string){
	filename,err := os.Create("./src/拉勾网爬虫/pageId.txt")
	if err != nil{
		fmt.Println(err.Error())
		return
	}
	defer filename.Close()
	s := page
	filename.WriteString(s)
	return
}

func insert_mgdb(data string){
	url :="mongodb://localhost"
	session,err :=mgo.Dial(url)
	if err!=nil{
		panic(err)
	}
	defer session.Close()
	//打开数据库
	session.SetMode(mgo.Monotonic,true)
	c :=session.DB("拉勾网Go").C("招聘信息")

	//插入数据
	s := data
	var d map[string]interface{}
	json.Unmarshal([]byte(s), &d)
	c.Insert(d)
	return
}

func main()  {
	go lagou_crawl()
	i := 0
	//main goroutine 循环打印
	for {
		i++
		fmt.Printf("main goroutine: i = %d\n", i)
		time.Sleep(1 * time.Second) //延时1s
	}
}

