import os
import random
import shutil
from concurrent.futures import ThreadPoolExecutor
import os
from concurrent.futures import ThreadPoolExecutor
import subprocess
from moviepy.editor import AudioFileClip
import threading
import torchaudio
import youtube_dl


basepath = os.getcwd()

video_dir = "./video_data/"
raw_audio_dir = "./raw_audio/"
denoise_audio_dir = "./denoised_audio/"
demucs_audio_dir = "./demucs/"


# download video
class downloadVideo(object):

    def generate_infos(self):
        infos = []
        with open("./links.txt", 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            line = line.replace("\n", "").replace(" ", "")
            if line == "":
                continue
            speaker, link = line.split("|")
            filename = speaker + "_" + str(random.randint(0, 1000000))
            infos.append({"link": link, "filename": filename})
            print('infos', infos)
        return infos


    def download_video(self, info):
        link = info["link"]
        filename = info["filename"]

        print("youtube-dl -f 0 {0} -o ./video_data/{1}.wav".format(link, filename))
        os.system("youtube-dl -f 0 {0} -o ./video_data/{1}.wav".format(link, filename))


    def downloadVideoRun(self):
        try:
            infos = self.generate_infos()
            with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                executor.map(self.download_video, infos)
            print('Download successed')
        except:
            print('Download error')


# v2a transform
class video2AudioTransform(object):

    def generate_infos(self,filelist):
        videos = []
        for file in filelist:
            if file.endswith(".wav"):
                videos.append(file)
        return videos


    def clip_file(self, file):
        my_audio_clip = AudioFileClip(video_dir + file)
        my_audio_clip.write_audiofile(raw_audio_dir + file.rstrip(".wav") + ".mp3")


    def video2AudioRun(self):
        threading.Thread(target=downloadVideo().downloadVideoRun()).start()


        # infos = self.generate_infos(filelist)
        try:
            filelist = list(os.walk(video_dir))[0][2]
            print('All of filelist r', filelist)
            for wavs in filelist:
                with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                    executor.submit(self.clip_file(wavs))
        except:
            print('Transform error')

# denoise process
class denoiseAudio(object):
    def denoiseRun(self):
        threading.Thread(target=video2AudioTransform().video2AudioRun()).start()
        try:
            filelist = list(os.walk(raw_audio_dir))[0][2]
            for file in filelist:
                if file.endswith(".mp3"):
                    audio_file = raw_audio_dir + file
                    demucs_audio_file = demucs_audio_dir + file
                    cmd = "demucs \"{0}\" -o \"{1}\" -n mdx_extra_q --two-stems=vocals".format(audio_file, demucs_audio_file)
                    # print("cmd is:", cmd)
                    sp = subprocess.Popen(cmd, shell=True)
                    out, err = sp.communicate()
                    print(err)

            for file in filelist:
                # file = file.replace(".wav", "")
                demucs_method = "mdx_extra_q"
                vocal_file = os.path.join(demucs_audio_dir, file, demucs_method, file.split('.')[0], 'vocals.wav')
                wav, sr = torchaudio.load(vocal_file, frame_offset=0, num_frames=-1, normalize=True,
                                          channels_first=True)

                # merge two channels into one
                wav = wav.mean(dim=0).unsqueeze(0)
                if sr != 22050:
                    wav = torchaudio.transforms.Resample(orig_freq=sr, new_freq=22050)(wav)
                save_file = os.path.join(denoise_audio_dir, file.split('.')[0] + '.wav')
                torchaudio.save(save_file , wav, 22050, channels_first=True)
                print('preprocess successed')
        except Exception as e:
            print(e)


denoiseAudio().denoiseRun()

