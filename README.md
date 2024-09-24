# sound_cutr

Algorithms used to extract parts of an mp3 file that are over a given value of decibel.

# Requirements

# Python

version 3

## python modules

- `ffmpegio` version 0.10.0
- `ffmpegio-core` version 0.10.0

## other

- `ffmpeg` (used with 7.0.2)

# Settings



# Examples

Play the original `a.mp3` audio file and run one of these algos:

`python3 algo1.py a.mp3`


`python3 algo2.py a.mp3`


The output file will be `output_dir/a.mp3`

You can run these algos on multiple files at once:

`python3 algo1or2.py file1.mp3 file2.mp3 ...`


# Timestamps

Timestamps for each audio file is outputed as a csv in `output_dir/name_of_the_audio_file.csv`



