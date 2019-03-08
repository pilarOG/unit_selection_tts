
import re
from pydub import AudioSegment
import spanish_transcriber
import pickle
import set_diphone_library
import sys
import random
from scipy.signal import fftconvolve
import numpy as np

# Load diphone library
DIPHONES = pickle.load(open('diphone_library.pckl', 'rb'))

def similarity(template, test):
    '''
    Description:
        This function compares two pieces of audio and computes the cross-correlation between them
        to obtain a score of similarity between the two
    Input:
        template(list): first chunk of audio
        test(list): second chunk of audio
    Output:
        a cross-correlation score
    '''
    corr = fftconvolve(template, test, mode='same')
    return max(abs(corr))

def synthesize(text):
    '''
    Description:
        This function takes as input text and generates a wave file for it using a simplified
        method inspired by unit selection TTS.
    Input:
        text(str): text in Spanish
    Output:
        there is no output in code, the wave file is generated in the same folder
    '''
    # Get phonetic transcription for input text
    transcription = []
    for word in text.split(' '):
        transcription += spanish_transcriber.transcribe(word)

    # Postlex rules
    # 2 subsequental equal sounds
    transcribed_diphones = []
    for n in range(0, len(transcription)):
        if n != len(transcription)-1 and transcription[n] == transcription[n+1]: pass
        else: transcribed_diphones.append(transcription[n])
    print
    print 'This is the phonetic transcription of the sentence: '+' '.join(transcribed_diphones)

    # Get diphone transcription for input text
    sentence_diphones = []
    for p in range(0, len(transcribed_diphones)-1):
        if p != len(transcribed_diphones):
            diphone = transcribed_diphones[p]+'_'+transcribed_diphones[p+1]
            sentence_diphones.append(diphone)

    # Start waveform generation
    # All waveforms start with a pre-recorded silence
    silence = AudioSegment.from_wav('./wav/silence.wav')
    generated_audio = AudioSegment.from_wav('./wav/silence.wav')

    # Get first diphone, as we don't a previous context to compare with,
    # a random example is picked in the list for that diphone
    first_diphone = random.choice(DIPHONES[sentence_diphones[0]])
    target = first_diphone[1]
    filename = first_diphone[0]
    # Obtaining start and end times for the diphone
    t1 = float((float(target.c_end) - float(target.c_start)) / 2 + float(target.c_start)) * 1000
    t2 = float((float(target.n_end) - float(target.n_start)) / 2 + float(target.n_start)) * 1000
    # Retrieving the correct audio file
    first_file = AudioSegment.from_wav('./wav'+filename.replace('.TextGrid', '.wav').replace('./data',''))
    # Slice audio file and concatenate sound to the waveform that is being built
    slice_audio = first_file[t1:t2]
    print 'Diphone '+'_'.join(target.getDiphone())+' retrieved from file '+filename+' at times '+str(t1)+' and '+str(t2)
    generated_audio += slice_audio

    # Now that we have the first diphone, we can score the most suitable next candidate
    previous_diphone = (filename, t1, t2)
    for diphone in range(1, len(sentence_diphones)):
        all_candidates = []
        # Backoff rules TODO: this is a very simplified of back-off, that basically says,
        # that if the diphone we are looking fo doesn't exist, insert a silence
        if sentence_diphones[diphone] not in DIPHONES:
            if 'sp_' in sentence_diphones[diphone]:
                diphone = sentence_diphones[diphone].replace('sp_', 'sil_')
        diphone = sentence_diphones[diphone]
        # If the diphone exists, all the examples in that diphone list are retrieved and scored as candidates
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

        # The candidate list is sorted and the one with the best cross-correlation is chosen
        all_candidates = sorted(all_candidates, key=lambda x: x[0])
        target = all_candidates[0]
        target_file = AudioSegment.from_wav('./wav'+target[1].replace('.TextGrid', '.wav').replace('./data',''))
        print 'Diphone '+diphone+' retrieved from file '+target[1]+' at times '+str(target[2])+' and '+str(target[3])

        # Get audio slice
        slice_audio = target_file[target[2]:target[3]]
        generated_audio += slice_audio

    # End with silence
    generated_audio += silence
    # Save the generated wave file
    generated_audio.export('generated.wav', format="wav")
    print 'Synthesis is done! :)'

# In terminal, use first argument with the text you want synthesize, with the text in quotes
# Example: python synthesize.py 'hola'
synthesize(sys.argv[1].decode('utf-8'))
