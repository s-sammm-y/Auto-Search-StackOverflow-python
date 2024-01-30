#!/usr/bin/env python
import shlex
import requests
import webbrowser
from subprocess import Popen, PIPE

def execute_return(cmd):
    args=cmd.split()
    process = Popen(args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return stdout,stderr

def mak_req(error):
    resp=requests.get("https://api.stackexchange.com/"+"/2.3/search?order=desc&sort=activity&tagged=python&intitle={}&site=stackoverflow".format(error))
    return resp.json()

def get_urls(json_dict):
    urls=[]
    flag=0
    for i in json_dict['items']:
        if i['is_answered']:
            urls.append(i['link'])
        flag+=1
        if flag==3 or flag == len(json_dict['items']):
            break
    for url in urls:
        webbrowser.open(url)


if __name__ == "__main__":
    stdout, stderr = execute_return("python error.py")
    error_message = stderr.decode("utf-8").strip().split("\r\n")[-1]
    print(error_message)
    if error_message:
        filter_out = error_message.split(":")
        print(filter_out)
        print(filter_out[0])
        json1 = mak_req(filter_out[0])
        json2 = mak_req(filter_out[1])
        json = mak_req(error_message)
        get_urls(json1)
        get_urls(json2)
        get_urls(json)
    else:
        print("No errors")