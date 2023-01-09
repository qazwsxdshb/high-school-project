#cpu use
#import os
#os.environ["CUDA_VISIBLE_DEVICES"]='-1'

import pyaudio
import wave
from tflite_support.task import audio
from tflite_support.task import core
from tflite_support.task import processor
import os

#語音錄製
os.system("arecord --format=S16_LE --rate=44100 -d 5 --file-type=wav out.wav")
while 1:
  #讀取訓練檔案
  base_options = core.BaseOptions("model.tflite")
  classification_options = processor.ClassificationOptions(max_results=2)
  options = audio.AudioClassifierOptions(base_options=base_options, classification_options=classification_options)
  classifier = audio.AudioClassifier.create_from_options(options)
  
  #辨識語音內容
  audio_file = audio.TensorAudio.create_from_wav_file("out.wav", classifier.required_input_buffer_size)
  audio_result = classifier.classify(audio_file)
  #拍手聲音相似處30%以上停止系統
  if( 0.3<=float(str(audio_result).split(" ")[6][6:-1]) or "clap"==str(audio_result).split(" ")[4][0:4]):
    print(str(audio_result).split()[6][6:-1])
    os.system("killall 'mpv'")
    print("kill")
    break
  
  else:
    print(audio_result)
    print()
    os.system("arecord --format=S16_LE --rate=44100 -d 5 --file-type=wav out.wav")