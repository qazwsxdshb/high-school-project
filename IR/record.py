#coding=utf-8
import speech_recognition as sr
import datetime
import pymysql
import os
import time

#資料庫連接
db = pymysql.connect(host="127.0.0.1",user="root",password="1qaz2wsx",database="data")
cursor=db.cursor()

#檢驗是否含有中文字符
def is_contains_chinese(strs):
  for _char in strs:
    if '\u4e00' <= _char <= '\u9fa5':
      return True
  return False
#錄製音檔
def record():
  record="aplay record.wav | arecord --format=S16_LE --rate=17000 -d 9 --file-type=wav out.wav"
  os.system(record)
  r=sr.Recognizer()
  WAV=sr.AudioFile("/home/easn/out.wav")
  
  #語音辨識
  with WAV as source:
    audio=r.record(source)
  a=r.recognize_google(audio,show_all=True,language='zh-tw')
  print(a)
  
  if(str(a)!="[]"):
    a=str(a).split("\'")[5]
    a=a.split(" ")
    print(is_contains_chinese(str(a)))
  else:
    print("i don't understand")
    exit()
  
  print(a)
  return a



name=record()
name=filt(name)

#過濾字串
def filt(name):
  name=str(name)[2:-2]
  a=0
  for i in range(len(name)-1):
    if("什麼"==name[i:i+2]):
      name=name[i+2:]
      print(name)
      return name
  if(name==""):
    print("error")
    os.system("aplay error.wav")
    exit()
  else:
    return name

else:
  #讀取紅外線
  command="aplay enableread.wav && timeout 6s evtest /dev/input/event0 > test.txt "
  os.system(command)
  txt=open("test.txt","r").read().split()
  num=0
  dat=''
  
  #過濾無效字串
  for i in txt:
      if ("value"==i):
        num=1
      elif(num==1 and i!="fffffff" and i!="7fffffbf" and i!="7ffffebf" and i!="7fffffff" and i!="7fbfffff" and i!="7ffff7ff" and i!="Event:" and i!="time" and i!="7ffffffb" and i!="7ffffffd" and i!="7fefffff" and i!="7fdfffff" and i!="7ffdffff"):
        dat=dat+" "+i
        num=0
  dat=dat.split()
  
  #判斷是否為空值
  if(str(dat)=="[]"):
    print("error")
    os.system("aplay error.wav")
    exit()
  
  content=max(dat,key=dat.count)
  print(content)
  
  #讀取時間
  time=datetime.datetime.today()
  time="\'"+time.strftime("%Y/%m/%d %H:%M:%S")+"\'"
  sql="INSERT INTO `infrared`(`name`,`drivename`,`content`,`time`,`decode`) VALUES('"+name+"','raspberrypi','"+content+"',"+time+",'unknow');"
  print(sql)
  
  #資料庫連線
  try:
    cursor.execute(sql)
    db.commit()
    print('success')
    
  #資料庫連線失敗
  except:
    db.rollback()
    print('error')
    os.system("aplay error.wav")
    
  #資料庫關閉
  db.close()
