import pyaudio
import wave
import random
import wavio
import matplotlib
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from PIL import Image

##### 鋼琴頻率list
#             A        A#       B        C        C#       D        D#       E        F        F#       G        G#
f_list = [ 27.5000, 29.1352, 30.8677, 32.7032, 34.6478, 36.7081, 38.8909, 41.2034, 43.6535, 46.2493, 48.9994, 51.9131,
           55.0000, 58.2705, 61.7354, 65.4064, 69.2957, 73.4162, 77.7817, 82.4069, 87.3071, 92.4986, 97.9989, 103.826,
           110.000, 116.541, 123.471, 130.813, 138.591, 146.832, 155.563, 164.814, 174.614, 184.997, 184.997, 207.652,
           220.000, 233.082, 246.942, 261.626, 277.183, 293.665, 311.127, 329.628, 349.228, 369.994, 391.995, 415.305,
           440.000, 466.164, 493.883, 523.251, 554.365, 587.330, 622.254, 659.255, 698.456, 739.989, 783.991, 830.609,
           880.000, 932.328, 987.767, 1046.50, 1108.73, 1174.66, 1244.51, 1318.51, 1396.91, 1479.98, 1567.98, 1661.22,
           1760.00, 1864.66, 1975.53, 2093.00, 2217.46, 2349.32, 2489.02, 2637.02, 2793.83, 2959.96, 3135.96, 3322.44,
           3520.00, 3729.31, 3951.07, 4186.01 ]

##### sine_sin波製造
def sine( frequency, t, sampleRate, amp):
	# 播放數量
	n = int(t * sampleRate)
	# 每秒轉動的角度再細分為取樣間隔
	interval = 2 * np.pi * frequency / sampleRate
	if amp==0:
		return np.arange(n)/sampleRate , 0*np.arange(n)
	else:
		return np.arange(n)/sampleRate , amp*np.sin(np.arange(n) * interval)

##### generator_sin波疊加
def generator( f, duration, rate, start, amp, bool):
  t1, d1 = sine( f, duration, rate, amp)
  data = np.stack(d1, axis=0)
  if bool==1:
    data = np.stack(d1, axis=0)
  elif bool==0:
    data = np.stack(t1+start, axis=0)
  return data

##### main_1_圖片縮放
img_1_1=Image.open( "file_001.jpg" )
img_1_2=np.array(Image.open("file_001.jpg").convert('L'))
rows,cols=img_1_2.shape
if cols<200:
	img_1_3=img_1_1.resize((cols,88), Image.BILINEAR )			#(cols,88)==(X,Y)
else:
	img_1_3=img_1_1.resize((200,88), Image.BILINEAR )
img_1_3.save("Resizefile_001.jpg")

##### main_2_圖片轉成二階
data_1 = []*(rows*cols)                  		# 儲存圖片二階布林值
data_count = []*cols
img_2_1=np.array(Image.open("Resizefile_001.jpg").convert('L'))
rows,cols=img_2_1.shape
for j in range(cols):                    		# 圖 i 2 3 4 
	count=0             
	for i in range(rows):                  		# j             
		if (0<img_2_1[i,j]<=50):             	# 2   
			data_1=np.append(data_1,bool(0))   	# 3
		else:                                	# 4
			data_1=np.append(data_1,bool(1))	# 0是黑色,255 & 1是白色
			count+=1
	data_count=np.append(data_count,count)
data_1 = data_1.reshape( 88, int(len(data_1)/88))

##### main_5_聲音儲存
data_2 = []
a_1=np.zeros(3)
data_2 = np.append(data_2, a_1, axis=0)

data_tmp = []
for j in range(cols):				     		# 249 X 88 = j X i
	tmp_1 = generator( f=f_list[0], duration=0.2, rate=44100, start=j*0.5, amp=1,bool=0)
	data_tmp = np.append(data_tmp, tmp_1, axis=0)
	tmp_2 = generator( f=f_list[i], duration=0.2, rate=44100, start=j*0.5, amp=0,bool=1)
	if data_count[j]==0:
		tmp_2 = generator( f=f_list[i], duration=0.2, rate=44100, start=j*0.5, amp=0,bool=1)
	else:
		for i in range(rows):
			if data_1[i][j]==1:
				tmp_2 = tmp_2+generator( f=f_list[i], duration=0.2, rate=44100, start=j*0.5, amp=1/data_count[j],bool=1)
	data_tmp = np.append(data_tmp, tmp_2, axis=0)
	data_tmp = np.append(data_tmp, tmp_2, axis=0)
	data_tmp = data_tmp.reshape(3, int(len(data_tmp)/3))
	data_tmp = data_tmp.T
	data_2 = np.vstack((data_2,data_tmp))
	data_tmp = []

	sys.stdout.write('\r')
	sys.stdout.write("[%-50s] %d%%" % ('='*int(j/(cols/50)), 2*int(j/(cols/50))))
	sys.stdout.flush()
sys.stdout.write('\r')
sys.stdout.write("[%-50s] %d%%" % ('='*50, 2*50))
print("hello")
np.savetxt('DTMF_data.csv', data_2, delimiter=',')
sf.write('star_sound.wav', data_2, 44100, subtype='PCM_24')