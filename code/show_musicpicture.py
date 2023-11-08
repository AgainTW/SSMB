import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# 讀取資料
t, d1, d2= np.loadtxt('DTMF_data.csv', dtype=float, delimiter=',', unpack=True)

# 產生繪圖物件
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15,8), dpi=72, sharex=True)

# 時刻 - 振幅關係圖
amp = d1+d2
ax1.plot(t, amp, linestyle='-', color='blue')
ax1.set_xlabel('time (s)', fontsize=14)
ax1.set_ylabel('amplitude', fontsize=14)

# 頻譜圖
cmap = mpl.cm.cool
if t[1]-t[0]==0:
	Fs = 1
else:
	Fs = int(1.0 / (t[1]-t[0]))
data, freqs, bins, im = ax2.specgram(amp, cmap=cmap, NFFT=1024, Fs=Fs, noverlap=128)
ax2.set_ylabel('frequency (Hz)', fontsize=14)
ax2.axis(ymax=2000)
fig.colorbar(im, ax=ax2, shrink=0.6, orientation='horizontal', pad=0.2)

# 儲存及顯示圖片
fig.savefig('DTMF_specgram.png')
fig.show()