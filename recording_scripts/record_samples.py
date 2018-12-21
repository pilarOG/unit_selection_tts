# -*- coding: utf-8 -*-
''' Script to record audio samples read from text to train/test STT apps'''

import pyaudio
import wave
import codecs
import random
import os

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 # channels, must be one for forced alignment toolkit to work
RATE = 16000 # sample rate
RECORD_SECONDS = 3 # seconds to allow recording per sample

# recording function

def record(text, file_name):
    print
    print("** Grabando **")
    print
    print("Lee en voz alta:   \'{}\'   ".format(text))

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(file_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    os.system('clear')

## MAIN

def main(subject_n, sentence_txt):
    sentence_set = codecs.open(sentence_txt, 'r', ).read().split('\n')
    random.shuffle(sentence_set)
    if raw_input("Si estas listo escribe \'comenzar\': ") == 'comenzar':
        os.system('clear')
        for n in range(0, len(sentence_set)):
            if sentence_set[n]:
                record(str(n)+':'+'\t'+sentence_set[n], 'data/'+str(n)+'_'+subject_n+'.wav' )
                outxt = open('data/'+str(n)+'_'+subject_n+'.lab', 'w')
                outxt.write(sentence_set[n])
                outxt.close()
    else:
        raise Exception
    print
    print( '** Fin de la grabación ** gracias!')

main('pilar', 'sentences2read.txt')
