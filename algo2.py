import ffmpegio
import numpy as np
import os 
import glob as glob
import csv
import re
import sys

all_files = sys.argv[1:]
nsamples = 16 
base_volume = 1
min_duration = 0.15
min_cut_duration = 0.14

for file in all_files:

    cur_csv = file[0:(len(file) - 3)] + "csv"
    cur_csv = open(cur_csv, "w")
    cur_csv = csv.writer(cur_csv, delimiter = ",", lineterminator = "\n")
   
    for i in os.listdir("cur_split"): os.remove(f"cur_split/{i}")

    duration = float(ffmpegio.probe.audio_streams_basic(file)[0]['duration']) / ffmpegio.audio.read(file)[1].shape[0] * nsamples

    timestamps_lst = [["start", "end"]]
    cur_lst = []
    with ffmpegio.open(file, 'ra', blocksize = nsamples, sample_fmt = 'dbl') as file_opened:
        over_val = False
        for i, indata in enumerate(file_opened):
            volume_norm = np.linalg.norm(indata) * 10
            if volume_norm > base_volume:
                cur_lst.append(i)
                over_val = True
            elif over_val:
                cur_lst.append("end")
                over_val = False

    v_strt = cur_lst[0] 
    v_end = v_strt
    v_af = 0

    for i in range(0, len(cur_lst)):
        if cur_lst[i] == "end":
            if i + 1 < len(cur_lst):
                if (cur_lst[i + 1] - cur_lst[i - 1]) * duration > min_cut_duration:
                    cur_duration = (cur_lst[i - 1] - v_strt) * duration 
                    if cur_duration > min_duration:
                        v_end = cur_lst[i - 1] * duration
                        if v_strt - 1 > 0:
                            v_strt -= 1
                        v_strt *= duration
                        os.system(f'ffmpeg -i {file} -acodec copy -ss {v_strt} -to {v_end} cur_split/{v_af}.mp3')
                        timestamps_lst.append([v_strt, v_end])
                        if i + 1 < len(cur_lst):
                            v_strt = cur_lst[i + 1] 
                            v_af += 1
            else:
                cur_duration = (cur_lst[i - 1] - v_strt) * duration 
                if cur_duration > min_duration:
                    v_end = cur_lst[i - 1] * duration
                    if v_strt - 1 > 0:
                        v_strt -= 1
                    v_strt *= duration
                    os.system(f'ffmpeg -i {file} -acodec copy -ss {v_strt} -to {v_end} cur_split/{v_af}.mp3')
                    timestamps_lst.append([v_strt, v_end])
                    if i + 1 < len(cur_lst):
                        v_strt = cur_lst[i + 1] 
                        v_af += 1

    cur_csv.writerows(timestamps_lst)
    cur_glob = []
    for i in range(0, len(glob.glob("cur_split/*.mp3"))): cur_glob.append(f"file 'cur_split/{i}.mp3'")
    cur_files = open("cur_files.txt", "w")
    cur_files.write("\n".join(cur_glob))
    cur_files.close()

    os.system(f"ffmpeg -f concat -i cur_files.txt -acodec copy output_dir/{file}")




