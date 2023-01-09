#coding=utf-8
import pymysql
import os
import subprocess
import time
import speech_recognition as sr

#檢驗是否含有中文字符
def is_contains_chinese(strs):
  for _char in strs:
    if '\u4e00' <= _char <= '\u9fa5':
      return True
  return False

def record():
  #錄製語音
  record="aplay ok.wav | arecord --format=S16_LE --rate=16000 -d 6 --file-type=wav out.wav"
  os.system(record)
  r=sr.Recognizer()
  WAV=sr.AudioFile("/home/easn/out.wav")
  
  #語音辨識
  with WAV as source:
    audio=r.record(source)
  #b=r.recognize_google(audio,show_all=True)
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
  
#過濾字串
def filt(name):
  name=str(name)[2:-2]
  a=0
  for i in range(len(name)-1):
    if("OK"==name[i:i+2]):
      name=name[i+2:]
      print(name)
      return name
  if(name==""):
    print("error")
    os.system("aplay error.wav")
    exit()
  else:
    return name

name=record()
name=filt(name)

#資料庫連接
db = pymysql.connect(host="127.0.0.1",user="root",password="1qaz2wsx",database="data")
cursor=db.cursor()
  
sql="SELECT * FROM `infrared` WHERE name LIKE '%"+name+"%';"
print(sql)
try:
  cursor.execute(sql)
  db.commit()
  print('success')
except:
  db.rollback()
  print('error')

#關閉資料庫
db.close()

data=[]
name=[]

#判斷紅外線編碼
for i in cursor:
  num=0
  for x in i:
    num=num+1
    if(num==2):
      name.append(x)
    if(num==4):
      data.append(x)
print(name)
print(data)
if(str(data)=="[]"):
  print("can't find")
  exit()
protocol=["rc5","RC5X_20","RC5_SZ","JVC","SONY12","SONY15","SONY20","NEC","NECX","NEC32","SANYO","MCIR2_MSE","RC6_0","RC6_6A_20","RC6_6A_24","RC6_6A_32","RC6_MCE","SHARP","IMON"]

#射出紅外線
command="aplay magic.wav | sleep 11.5"
os.system(command)
for i in protocol:
  print(i)
  command="ir-ctl -d /dev/lirc0 -S "+i+":'0x"+data[0]+"'"
  a=os.system(command)
  time.sleep(0.1)
  
