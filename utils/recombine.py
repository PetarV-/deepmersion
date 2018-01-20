import os

nb_sounds = 10

base_cmd = 'ffmpeg -y '
options = '-acodec libmp3lame -ac 2 -ab 128k -ar 48000 '

fnames = []

with open('classes.txt', 'r') as f:
    for line in f:
        fnames.append(line[:-1] + '-1.00.mp3')

for i in range(1, 1 << nb_sounds):
    bitstring = ''
    input_spec = ''
    inps = 0
    for j in range(nb_sounds):
        if i & (1 << j):
            bitstring += '1'
            inps += 1
            input_spec += '-i ' + fnames[j] + ' '
        else:
            bitstring += '0'
    input_spec += '-filter_complex amix=inputs=' + str(inps) + ' '
    out_name = '~/public_html/db/' + bitstring + '.mp3'
    ffmpeg_cmd = base_cmd + input_spec + options + out_name
    os.system(ffmpeg_cmd)

