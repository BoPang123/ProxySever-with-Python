#coding=utf-8

import requests
def GET(url):
    r = requests.get(url)
    print(r.text)
def DELETE(url):
    r=requests.delete(url)
    print(r.text)
if __name__ == '__main__':
    url=input("Input the url:   ")
    type=input("GET or DELETE?    ")
    if(type=="GET"):
        GET(url)
    elif (type == "DELETE"):
        DELETE(url)
    else:
        print("No this type!")

#url ='http://10.129.133.17:8080/index.html'
