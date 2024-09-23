import ffmpegio
import numpy as np
import os 
import glob as glob
import csv
import re

all_files = ["k.mp3"]
nframes = 16 
base_volume = 1
min_duration = 0.15
min_sound_per_sec = 1100

for file in all_files:
    
    for i in os.listdir("cur_split"): os.remove(f"cur_split/{i}")

    os.system(f'echo $(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {file}) > duration.txt')
    duration = open("duration.txt", "r")
    duration = float(duration.read())

    cur_lst = []
    cur_lst2 = []
    with ffmpegio.open(file, 'ra', blocksize = nframes, sample_fmt = 'dbl') as file_opened:
        over_val = False
        for i, indata in enumerate(file_opened):
            volume_norm = np.linalg.norm(indata) * 10
            cur_lst2.append(volume_norm)
            if volume_norm > base_volume:
                cur_lst.append(i)
                over_val = True
            elif over_val:
                cur_lst.append("end")
                over_val = False
        duration = duration / i 

    v_strt = cur_lst[0] 
    v_end = v_strt
    v_af = 0
 
    for i in range(0, len(cur_lst)):
        if cur_lst[i] == "end":
            cur_duration = (cur_lst[i - 1] - v_strt) * duration 
            if cur_duration > min_duration:
                v_end = cur_lst[i - 1] * duration
                idx1 = cur_lst.index(cur_lst[i - 1])
                idx2 = cur_lst.index(v_strt)
                if idx1 - idx2 - cur_lst[idx1:idx2].count("end") > min_sound_per_sec * cur_duration:
                    os.system(f'ffmpeg -i {file} -acodec copy -ss {(v_strt - 1) * duration} -to {v_end} cur_split/{v_af}.mp3')
                    if i + 1 < len(cur_lst):
                        v_strt = cur_lst[i + 1] 
                        v_af += 1
                elif i + 1 < len(cur_lst):
                    v_strt = cur_lst[i + 1]

    cur_glob = []
    for i in range(0, len(glob.glob("cur_split/*.mp3"))): cur_glob.append(f"file 'cur_split/{i}.mp3'")
    cur_files = open("cur_files.txt", "w")
    cur_files.write("\n".join(cur_glob))
    cur_files.close()

    os.system(f"ffmpeg -f concat -i cur_files.txt -acodec copy output_dir/{file}")


