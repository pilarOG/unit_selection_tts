
import re
from pydub import AudioSegment
import spanish_transcriber
import pickle
import set_diphone_library
import sys
import random
from scipy.signal import fftconvolve
import numpy as np

DIPHONES = pickle.load(open('diphone_library.pckl', 'rb'))

def similarity(template, test):
    corr = fftconvolve(template, test, mode='same')
    return max(abs(corr))

def synthesize(text):
    # Get diphone list
    transcription = []
    for word in text.split(' '):
        transcription += spanish_transcriber.transcribe(word)

    # Postlex rules
    # 2 subsequental equal sounds
    transcribed_diphones = []
    for n in range(0, len(transcription)):
        if n != len(transcription)-1 and transcription[n] == transcription[n+1]: pass
        else: transcribed_diphones.append(transcription[n])
    print transcribed_diphones

    sentence_diphones = []
    for p in range(0, len(transcribed_diphones)-1):
        if p != len(transcribed_diphones):
            diphone = transcribed_diphones[p]+'_'+transcribed_diphones[p+1]
            sentence_diphones.append(diphone)

    # Select diphones from database
    silence = AudioSegment.from_wav('./wav/silence.wav')
    generated_audio = AudioSegment.from_wav('./wav/silence.wav')

    # Get first diphone
    first_diphone = random.choice(DIPHONES[sentence_diphones[0]])
    target = first_diphone[1]
    filename = first_diphone[0]
    t1 = float((float(target.c_end) - float(target.c_start)) / 2 + float(target.c_start)) * 1000
    t2 = float((float(target.n_end) - float(target.n_start)) / 2 + float(target.n_start)) * 1000
    first_file = AudioSegment.from_wav('./wav'+filename.replace('.TextGrid', '.wav').replace('./data',''))
    slice_audio = first_file[t1:t2]
    print t1, t2, filename
    slice_audio = first_file[t1:t2]
    generated_audio += slice_audio


    previous_diphone = (filename, t1, t2)
    # rest of the diphones, try to find the one that fits the best
    for diphone in range(1, len(sentence_diphones)):
        all_candidates = []
        # Backoff rules
        if sentence_diphones[diphone] not in DIPHONES:
            if 'sp_' in sentence_diphones[diphone]:
                diphone = sentence_diphones[diphone].replace('sp_', 'sil_')
        diphone = sentence_diphones[diphone]
        # If diphone exists
        for candidate in DIPHONES[diphone]:
            target = candidate[1]
            filename = candidate[0]
            t1 = float((float(target.c_end) - float(target.c_start)) / 2 + float(target.c_start)) * 1000
            t2 = float  ((float(target.n_end) - float(target.n_start)) / 2 + float(target.n_start)) * 1000
            target_file = AudioSegment.from_wav('./wav'+filename.replace('.TextGrid', '.wav').replace('./data',''))
            previous_file = AudioSegment.from_wav('./wav'+previous_diphone[0].replace('.TextGrid', '.wav').replace('./data',''))

            # Slice both
            target_slice = target_file[t1:t2]
            target_array = target_slice.get_array_of_samples()
            previous_slice = previous_file[float(previous_diphone[1]):float(previous_diphone[2])]
            previous_array = previous_slice.get_array_of_samples()

            # Score diphones
            all_candidates.append([similarity(target_array,previous_array), filename, t1, t2])

            previous_diphone = (filename, t1, t2)

        all_candidates = sorted(all_candidates, key=lambda x: x[0])
        target = all_candidates[0]
        target_file = AudioSegment.from_wav('./wav'+target[1].replace('.TextGrid', '.wav').replace('./data',''))

        print target[2],target[3], target[1]
        # Get audio slice
        slice_audio = target_file[target[2]:target[3]]
        generated_audio += slice_audio

    # end with silence
    generated_audio += silence
    generated_audio.export('generated2.wav', format="wav")

synthesize(sys.argv[1].decode('utf-8'))
