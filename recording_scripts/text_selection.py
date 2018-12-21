# -*- coding: utf-8 -*-

import sys
sys.path.append('../')
from spanish_transcriber import transcribe
import codecs
import re

phoneDict = {}
selectedSentences = []

def broadSelection(corpora):
    sentences = codecs.open(corpora, 'r', encoding='utf-8').read().replace('\n', '.').split('.')
    for sentence in sentences:
        sentence = sentence.replace(u'—', '').replace('_', '').replace('*', '').replace('"', '').replace(',', '').replace(u'¿', '').replace('  ', ' ')
        sentence = sentence.replace(u'!', '').replace(u'¡', '').replace(':', '').replace(';', '').replace('\f', '').replace(u'?', '')
        if not re.findall(r'[0-9]', sentence) and len(sentence) < 100:
            transcription = transcribe(sentence)
            for phone in transcription:
                if phone not in phoneDict:
                    phoneDict[phone] = 0
                    selectedSentences.append((sentence, transcription))
                    break

def scoreSelection(transcripted_sentences):
    scores = []
    for transcription in transcripted_sentences:
        scores.append((len(set(transcription[1])), transcription))
    scores = sorted(scores, key=lambda x: x[0])
    print scores
    return scores

def countCoverage(transcripted_sentences):
    for transcription in transcripted_sentences:
        for phone in transcription[1][1]: phoneDict[phone] += 1

outf = codecs.open('sentences2read.txt', 'w', encoding='utf-8')
broadSelection('ultima_niebla.txt')
scoresSentences = scoreSelection(selectedSentences)
countCoverage(scoresSentences)
for p in phoneDict:
    print p, phoneDict[p]
N = 20
for sentence in scoresSentences[N:]:
    outf.writelines(sentence[1][0].strip()+'\n')
outf.close()
