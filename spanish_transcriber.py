# -*- coding: utf-8 -*-

import re

def ltsRules(text):
    '''
    Description:
        This function runs a series of replacement rules to convert from letters to sounds
        given the phonetics of Chilean Spanish.
    Input:
        text(str): any string in Spanish
    Output:
        a list of phones for the input text
    '''
    phones = []

    # letter sets
    letsets = {'LNS': ('l', 'n', 's'),
                'DNSR': ('d', 'n', 's', 'r'),
                'EI': ('e', 'i', u'é', u'í'),
                'AEIOUt': (u'á', u'é', u'í', u'ó', u'ú'),
                'V': ('a', 'e', 'i', 'o', 'u'),
                'C': ('b', 'c', 'd', 'f', 'g', 'h', 'j', 'k',
                      'l', 'm', 'n', u'ñ', 'p', 'q', 'r', 's',
                      't', 'v', 'w', 'x', 'y', 'z'),
                'noQ': ('b', 'c', 'd', 'f', 'g', 'h', 'j', 'k',
                      'l', 'm', 'n', 'ñ', 'p', 'r', 's',
                      't', 'v', 'w', 'x', 'y', 'z'),
                'AV': ('a', 'e', 'i', 'o', 'u', u'á', u'é', u'í', u'ó', u'ú'),
                'SN': ('p', 't', 'k', 'n', 'm', u'ñ'),
                'LN': ('l', 'n'),
                'LR': ('l', 'r') }

    letters = list(text)
    for let in range(0, len(letters)):
        if letters[let] != '#' and letters[let] != ' ':
            # Get a window of context for each letter
            c_let = letters[let]    # Current letter
            p_let = letters[let-1]  # Previous letter
            pp_let = letters[let-2] # Previous previous letter
            n_let = letters[let+1]  # Next letter
            nn_let = letters[let+2] # Next next letter
                                    # This is inspired by Festival

            # replace Q
            if c_let == 'q' and n_let == 'u' and n_let == 'a': phones.append('k')
            elif c_let == 'q' and n_let == 'u': phones.append('k')
            elif c_let == 'u' and p_let == 'q': pass
            elif c_let == 'q': phones.append('k')

            # u vowel with g
            elif c_let == 'u' and p_let == 'g' and n_let == 'i': pass
            elif c_let == 'u' and p_let == 'g' and n_let == 'e': pass
            elif c_let == 'u' and p_let == 'g' and n_let == u'í': pass
            elif c_let == 'u' and p_let == 'g' and n_let == u'é': pass

            # stress for written stress marks
            elif c_let == u'á': phones.append('aS')
            elif c_let == u'é': phones.append('eS')
            elif c_let == u'í': phones.append('iS')
            elif c_let == u'ó': phones.append('oS')
            elif c_let == u'ú': phones.append('uS')

            elif c_let == u'ü': phones.append('u')

            # semivowels
            elif c_let == u'u' and n_let in letsets[u'AV']: phones.append(u'uSC')
            elif c_let == u'u' and p_let in letsets[u'AV']: phones.append(u'uSV')
            elif c_let == u'i' and n_let in letsets[u'AV']: phones.append(u'iSC')
            elif c_let == u'i' and pp_let in letsets[u'noQ']: phones.append(u'iSV')

            # y as vowel and w
            elif c_let == 'y' and n_let == '#': phones.append('i')
            elif c_let == 'y' and n_let in letsets['C']: phones.append('i')
            elif c_let == 'w' and n_let == 'u': phones.append('uSC')
            elif c_let == 'w': phones.append('u')

            # fricatives
            elif c_let == 's' and p_let in letsets['AV'] and n_let in letsets['C']: phones.append('h')
            elif c_let == 's' and p_let in letsets['AV'] and n_let == '#': phones.append('h')
            elif c_let == 'c' and p_let == 's' and n_let in letsets['EI']: pass
            elif c_let == 'c' and n_let in letsets['EI']: phones.append('s')
            elif c_let == 'g' and n_let in letsets['EI']: phones.append('x')
            elif c_let == 'g': phones.append('g')
            elif c_let == 'j': phones.append('x')

            # keep z cause we'll need it to get stress
            elif c_let == 'z' and p_let in letsets['AV'] and n_let in letsets['C']: phones.append('hz')
            elif c_let == 'z' and p_let in letsets['AV'] and n_let == '#': phones.append('hz')
            elif c_let == 'z': phones.append('s')

            # affricates
            elif c_let == 'c' and n_let == 'h': phones.append('ch')
            elif c_let == 'h' and p_let == 'c': pass
            elif c_let == 'l' and n_let == 'l': phones.append('ll')
            elif c_let == 'l' and p_let == 'l': pass
            elif c_let == 'y' and p_let in letsets['LN']: phones.append('ll')
            elif c_let == 'y' and p_let == '#': phones.append('ll')
            elif c_let == 'l' and n_let == 'l' and p_let in letsets['LN']: phones.append('ll')
            elif c_let == 'l' and p_let == 'l' and pp_let in letsets['LN']: pass

            # unvoiced stops
            elif c_let == 'p' and n_let == 's': pass
            elif c_let == 'c': phones.append('k')

            # voiced stops
            elif c_let == 'v' and p_let == '#': phones.append('b')
            elif c_let == 'v' and p_let in letsets['SN']: phones.append('b')
            elif c_let == 'v' and n_let in letsets['LR']: phones.append('b')
            elif c_let == 'v' and p_let in letsets['LR']: phones.append('b')

            # approximants
            elif c_let == 'b' and p_let in letsets['AV'] and n_let in letsets['AV']: phones.append('bA')
            elif c_let == 'v' and p_let in letsets['AV'] and n_let in letsets['AV']: phones.append('bA')
            elif c_let == 'd' and p_let in letsets['AV'] and n_let in letsets['AV']: phones.append('dA')
            elif c_let == 'g' and p_let in letsets['AV'] and n_let in letsets['AV']: phones.append('gA')
            elif c_let == 'r' and p_let in letsets['AV'] and n_let in letsets['AV']: phones.append('rA')
            elif c_let == 'y': phones.append('llA')

            # nasals
            elif c_let == u'ñ': phones.append('ny')

            # laterals
            elif c_let == 'l' and n_let == 'l' and nn_let == '#': phones.append('l')
            elif c_let == 'l' and p_let == 'l' and n_let == '#': pass
            elif c_let == 'l' and n_let == 'l': phones.append('llA')
            elif c_let == 'l' and p_let == 'l': pass

            # vibrants
            elif c_let == 'r' and n_let == 'r': phones.append('rr')
            elif c_let == 'r' and p_let == 'r': pass
            elif c_let == 'r' and p_let == '#': phones.append('rr')
            elif c_let == 'r' and p_let in letsets['LNS']: phones.append('rr')

            elif c_let == 'x': phones += ['k','s']
            # get rid of h
            elif c_let == 'h': pass

            # else
            else: phones.append(c_let)

    return phones


def syllabify(phones):
    '''
    Description:
        This function inserts syllable boundaries '-' for a list of phones
        given the phonetics of Chilean Spanish. Rules are looking only for general
        cases, and probably can't cope with loans or proper names.
    Input:
        phones(list): a list of phones in Spanish
    Output:
        a list of phones with syllable boundaries for the input text
    '''
    syllables = []
    phones = ['#','#']+phones+['#','#']

    sylsets = {'V': ('aS', 'iS', 'uS', 'eS', 'oS', 'a', 'i', 'u', 'e', 'o',
                     'iSC', 'uSC', 'iSV', 'uSV'),
               'VV': ('aS', 'iS', 'uS', 'eS', 'oS', 'a', 'i', 'u', 'e', 'o'),
               'IUT': ('iS', 'uS'),
               'C': ('b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'ch',
                      'l', 'm', 'n', 'ny', 'p', 'q', 'r', 's',
                      't', 'v', 'w', 'x', 'y', 'z','bA', 'dA', 'gA','llA', 'rA'),
               'CC': ('bl', 'br', 'kl', 'kr', 'ks', 'dr', 'fl', 'fr', 'gl',
                      'gr', 'pl', 'pr', 'tl', 'tr'),
               'H': ('ia', 'ie', 'io', 'ua', 'ue', 'uo', 'ai', 'ei', 'oi', 'au',
                    'eu', 'ou', 'iu', 'ui','iaS', 'ieS', 'ioS', 'uaS', 'ueS', 'uoS',
                    'aSi', 'eSi', 'oSi', 'aSu', 'eSu', 'oSu', 'iuS', 'uiS') }

    for let in range(0, len(phones)):
        if phones[let] != '#':
            c_let = phones[let]
            p_let = phones[let-1]
            pp_let = phones[let-2]
            n_let = phones[let+1]
            nn_let = phones[let+2]

            # consonant clusters
            if c_let+n_let in sylsets['CC'] and n_let in sylsets['V']: syllables.append('-')

            # hiatus
            elif c_let+n_let in sylsets['H'] and p_let in sylsets['IUT']: syllables.append('-')

            # two strong vowels
            elif c_let in sylsets['VV'] and p_let in sylsets['VV']: syllables.append('-')

            # break other CC not allowed
            elif c_let in sylsets['C'] and p_let in sylsets['C'] and pp_let in sylsets['V']: syllables.append('-')

            # usual CV
            elif c_let in sylsets['C'] and p_let in sylsets['V'] and n_let in sylsets['V']: syllables.append('-')

            syllables.append(c_let)

    return syllables

def stress(syllables):
    '''
    Description:
        This function assigns stress when it corresponds to the vowel of a word,
        given Spanish rules
    Input:
        syllables(list): a list of phones and syllable boundaries
    Output:
        a list of phones with syllable boundaries and stress for the input text
    '''
    stressed = []
    syllables = ['#','#']+syllables+['#','#']
    strsets = {'notNSV': ('p', 't', 'k', 'b', 'd', 'g', 'bA', 'dA', 'gA', 'f', 'hz',
                          'x', 'ch', 'll', 'm', 'ny', 'l', 'llA', 'rA', 'r', 'rr'),
               'V': ('a', 'e', 'i', 'o', 'u'),
               'C': ('b', 'c', 'd', 'f', 'g', 'h', 'j', 'k',
                      'l', 'm', 'n', 'ny', 'p', 'q', 'r', 's',
                      't', 'v', 'w', 'x', 'y', 'z','bA', 'dA', 'gA','llA', 'rA'),
               'VNS': ('n', 's', 'a', 'i', 'u', 'e', 'o')}

    strVow = {'a': 'aS',
              'e': 'eS',
              'i': 'iS',
              'o': 'oS',
              'u': 'uS'}
    lastSyl = False
    plastSyl = False
    c = 0
    S = False
    if '-' in syllables:
        # We are counting syllables from the end of the word
        for let in reversed(range(0, len(syllables))):
            if syllables[let] == '-':
                c += 1
            if c == 1 and lastSyl == False:
                lastSyl = True
            elif c == 2:
                plastSyl = True

            # Words that are stressed in the last syllable
            if syllables[let] == '-' and lastSyl == True and not plastSyl:
                lastSyl = let
                c =+ 1
                last = ['#','#']+syllables[let:]
                for l in reversed(range(0, len(last))):
                    if last[l] != '#':
                        c_let = last[l]
                        p_let = last[l+1]
                        pp_let = last[l+2]
                        n_let = last[l-1]
                        nn_let = last[l-2]
                        if c_let in strsets['V'] and p_let in strsets['C'] and n_let in strsets['notNSV'] and nn_let == '#':
                            stressed.append(strVow[c_let])
                            S = True
                        else: stressed.append(c_let)
            # Words that are stressed in the previous to last syllable
            elif syllables[let] == '-' and plastSyl == True:
                plastSyl = let
                plast = ['#','#']+syllables[let:lastSyl]+['#','#']
                for l in reversed(range(0, len(plast))):
                    if plast[l] != '#':
                        c_let = plast[l]
                        p_let = plast[l+1]
                        pp_let = plast[l+2]
                        n_let = plast[l-1]
                        nn_let = plast[l-2]
                        if c_let in strsets['V'] and stressed[0] in strsets['VNS']:
                            stressed.append(strVow[c_let])
                            S = True
                        else: stressed.append(c_let)
            # 2 syllabe words
            elif '-' not in syllables[:let+1] and syllables[let] != '#':
                syl = []
                for n in syllables[:let+1]:
                    if n in 'aeuio' and S != True:
                        syl.append(n+'S')
                    else:
                        syl.append(n)
                stressed += list(reversed(syl))
                break

        stressed += list(reversed(syllables[:plastSyl]))
        stressed = list(reversed(stressed))
    else:
        stressed = syllables

    # Get rid of extra symbols
    stressed_phones = []
    for n in stressed:
        if n == 'hz': stressed_phones.append('s')
        elif n == '-': pass
        elif n == '#': pass
        else: stressed_phones.append(n)

    return stressed_phones

def transcribe(text):
    '''
    Description:
        This function runs a text processing pipeline to obtain a full phonetic transcription
        of a given text in Spanish.
    Input:
        text(str): any string in Spanish
    Output:
        a list of phones and stress assignment for the input text
    '''
    # Step 1: lower case
    # '##' are silence phones that will be used as boundaries latter
    text = '##'+text.lower()+'##'
    # Step 2: text normalization
    # TODO: currently, we are not supporting text normalization
    # Step 3: LTS rules
    phones = ltsRules(text)
    # Step 4: Syllabification
    syllables = syllabify(phones)
    # Step 5: stress assignment
    # The stress assignment is only run if the word doesn't have the stress mark written
    if not re.findall(u'[áéúíó]', text):
        stressed = stress(syllables)
        return stressed
    # In this case, syllable marks are only used to assign stress and then removed
    return ' '.join(syllables).replace('-','').split()
