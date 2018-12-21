
import re
import glob
import pickle

DIPHONES = {}

class Diphone(object):
    def setDiphone(self, filename, c_line, n_line):
        self.filename = filename
        if re.findall(r'text = \"(\w+)\"', c_line):
            self.c_diphone = re.findall(r'text = \"(\w+)\"', c_line)[0]
        else:
            self.c_diphone = 'sp'
        if re.findall(r'text = \"(\w+)\"', n_line):
            self.n_diphone = re.findall(r'text = \"(\w+)\"', n_line)[0]
        else:
            self.n_diphone = 'sp'
        self.c_start = re.findall(r'xmin = (\d+\.?\d+)', c_line)[0]
        self.n_start = re.findall(r'xmin = (\d+\.?\d+)', n_line)[0]
        self.c_end = re.findall(r'xmax = (\d+\.?\d+)', c_line)[0]
        self.n_end = re.findall(r'xmax = (\d+\.?\d+)', n_line)[0]

        diphone = self.c_diphone+'_'+self.n_diphone
        if diphone not in DIPHONES:
            DIPHONES[diphone] = [(filename, self)]
        else:
            DIPHONES[diphone] += [(filename, self)]

    def getTimes(self):
        return (self.c_start, self.n_start, self.c_end, self.n_end)
    def getFilename(self):
        return self.filename
    def getDiphone(self):
        return (self.c_diphone, self.n_diphone)


def setDiphoneLibrary(wav_path, lab_path):
    for filepath in glob.iglob(lab_path+'/*.TextGrid'):
        # Checking wav exists for lab file
        wav_list = [wav_file.split('/')[-1].replace('.wav','') for wav_file in glob.iglob(wav_path+'/*.wav')]
        if filepath.split('/')[-1].replace('.TextGrid','') in wav_list:
            data = open(filepath, 'r').read().replace('\n', ' ').replace('\t', ' ')
            # Extract phone tier
            tier = re.findall(r'item \[1\]:(.*)item \[2\]:', data)
            data = tier[0].split('intervals')
            # Range over each line to build diphone dictionary
            for l in range(0, len(data)-1):
                if l and l != len(data):
                    c_line = data[l]
                    n_line = data[l+1]
                    if re.findall(r'\[[0-9]+\]', c_line):
                        diphone = Diphone()
                        diphone.setDiphone(filepath, c_line, n_line)
        # Warn if alike
        else:
            print filepath+' does not have wav file with the same name'

    # Save diphone dictionary
    pickle.dump(DIPHONES, open("diphone_library.pckl", "wb"))
    return DIPHONES


# Input path to wav folder and label folder
setDiphoneLibrary('./data','./data')
