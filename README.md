# Vits-video2txt-preprocess
Vits video2txt preprocess
# Whats the impact
Generate datasets based on links, use VITS model train your data.
# How to start
add the link of video in links.txt 
cd VITS-video2txt and run download_video.py
python long_audio_transcribe.py --languages C --whisper_size large 
# output
traintext & trainwaves
# train
cd ..
cd vits-main 
split the train&test data
python preprocess.py --text_index 2 --filelists path/to/train.txt path/to/test.txt
python train_ms.py -c {path/to/config} -m {path/to/pth}
