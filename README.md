# Vits-video2txt-preprocess
Vits video2txt preprocess
# Whats the impact
Generate datasets based on links, use VITS model train your data.
# How to start
**add the link of video in links.txt** <br>
```
download video <br>
cd VITS-video2txt and run download_video.py 

# output traintext & trainwaves 
python long_audio_transcribe.py --languages C --whisper_size large   
```

# train
```
# goto the index
cd ..  <br>
cd vits-main  <br>
split the train&test data

# preprocess txt file to .cleaned
python preprocess.py --text_index 2 --filelists path/to/train.txt path/to/test.txt  

# train model
python train_ms.py -c {path/to/config} -m {path/to/pth} ``` <br>
