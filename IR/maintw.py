#coding=utf-8
import speech_recognition as sr
import os
import requests
from bs4 import BeautifulSoup
import subprocess


def siri_function():
  print("Do you need any help")
  #詢問幫助
  os.system("aplay hello.wav")
  pid=0
  command='espeak -vzh+f3 '
  while 1:
    ans=record()
    c=0
    ans=str(ans)
    num=len(ans)
    
    for i in range(num-1):
      req=ans[i]+ans[i+1]
      c=c+1
      
      #接收紅外線編碼
      if(req=="讀取" or req=="錄製"):
        os.system("python record.py")
        break
        
      #發射紅外線編碼
      elif(req=="射出" or req=="發射"):
        os.system("python send.py")
        break
        
      #取得天氣資訊
      elif(req=="溫度" or req=="天氣"):
        hotpage=requests.get("https://www.google.com/search?q=weather")
        main=BeautifulSoup(hotpage.text,'html.parser')
        a=main.text.split("weather")[1]
        a=a.split(" / ")[1].replace("\n"," ")
        a=a.replace('C',' ')
        os.system(command+"'"+a[2:4]+"度 "+a.split(" ")[3]+"'")
        print(command+"'"+a[2:4]+"度'"+a.split(" ")[3])
        break
        
      #播放youtube音頻內容
      elif(req=="影片" or req=="視頻"):
        os.system("aplay video.wav")
        vname=""
        x=record()
        for i in x:
          vname=vname+i
        print(vname)
        a="ytfzf -m -a "+vname
        print(a)
        pid=subprocess.Popen(a.split())
        print(pid)
        os.system("python clap.py")
        
      #無法理解語音內容
      elif((num-1)==c):
        os.system(command+"'我不知道你想說什麼?'")
        print("I don't understand")
        
      #關閉youtube音頻內容
      elif(req=="關閉" and len(pid)>=3):
        os.system("killall 'mpv'")
        print("ok")
        
      #系統關閉
      elif(req=="再見" or req=="退出"):
        os.system("aplay bye.wav")
        exit()

#檢驗是否含有中文字符    
def is_contains_chinese(strs):
  for _char in strs:
    if '\u4e00' <= _char <= '\u9fa5':
      return True
  return False

#語音錄製和語音辨識
def record():
  #錄製聲音
  record="aplay ok.wav | arecord --format=S16_LE --rate=16000 -d 5 --file-type=wav out.wav"
  os.system(record)
  r=sr.Recognizer()
  
  #讀取音檔
  WAV=sr.AudioFile("/home/easn/out.wav")
  
  #語音辨識
  with WAV as source:
    audio=r.record(source)
  a=r.recognize_google(audio,show_all=True,language='zh-tw')
  print(a)
  
  #提取內容
  if(str(a)!="[]"):
    a=str(a).split("\'")[5]
    a=a.split(" ")
    print(is_contains_chinese(str(a)))
  else:
    record()  
  print(a)
  return a


while 1:
  siri_function()
