
import re
import glob
import pickle

DIPHONES = {}

class Diphone(object):
    '''Diphone class to store diphones as objetcs into the diphone library where to make the diphone search'''
    def setDiphone(self, filename, c_line, n_line):
        '''
        Description:
            This method creates the attributes for a diphone object using as source
            a Praat TextGrid file. Reading two lines at the time, each one with a phone,
            we build the diphones by taking the middle time of the current phone and
            the middle time of next one. We don't really "build" the diphones at this stage,
            we just store their identity and where they are (the starting, end times and file)
            into a dictionary where they are sorted by diphone identity, and each one has a list
            of all the examples found in the data for that diphone
        Input:
            filename(str): string with the path of the wave file where the diphone is
            c_lines(str): is the current line in the textGrid being read, which corresponds to the current phone
            n_line(str): is the next line in the textGrid to the one being read, which corresponds to the next phone
        Output:
            a list of phones and stress assignment for the input text
        '''
        # Save filename of the wave file
        self.filename = filename
        if re.findall(r'text = \"(\w+)\"', c_line):
            # Set identity of current phone
            self.c_diphone = re.findall(r'text = \"(\w+)\"', c_line)[0]
        else:
            self.c_diphone = 'sp'
        if re.findall(r'text = \"(\w+)\"', n_line):
            # Set identity of the next phone
            self.n_diphone = re.findall(r'text = \"(\w+)\"', n_line)[0]
        else:
            self.n_diphone = 'sp'
        # Save starting and end times for both phones
        self.c_start = re.findall(r'xmin = (\d+\.?\d+)', c_line)[0]
        self.n_start = re.findall(r'xmin = (\d+\.?\d+)', n_line)[0]
        self.c_end = re.findall(r'xmax = (\d+\.?\d+)', c_line)[0]
        self.n_end = re.findall(r'xmax = (\d+\.?\d+)', n_line)[0]
        # Save identity of diphone by concatenating the two phones by an underscore
        diphone = self.c_diphone+'_'+self.n_diphone
        # Add to the dictionary by diphone identity as key, storing a list of the different
        # appearences of the same diphone
        if diphone not in DIPHONES:
            DIPHONES[diphone] = [(filename, self)]
        else:
            DIPHONES[diphone] += [(filename, self)]

    '''
    Description:
        Classic "get" methods to obtain the attributes of a desired diphone
        getTimes returns timestamps for both phones in the diphone
        getFilename returns name of wave file where the diphone is
        getDiphone returns identity of the two phones that compose the diphone
    '''
    def getTimes(self):
        return (self.c_start, self.n_start, self.c_end, self.n_end)
    def getFilename(self):
        return self.filename
    def getDiphone(self):
        return (self.c_diphone, self.n_diphone)


def setDiphoneLibrary(wav_path, lab_path):
    '''
    Description:
        This function iterates over the whole set of textGrids to store the specifications
        for each diphone in the dataset. The wave files paths is used as a reference to
        warn the user if they have a textGrid that doesn't have a paired wave file
    Input:
        wav_path(str): path to folder with wave files
        lab_path(str): path to folder with textGrids
    Output:
        a dictionary with the timestamps, identity and files of all the diphones in the database provided
    '''
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

        # Warn if a textGrid is missing a paired wav file
        else:
            print filepath+' does not have wav file with the same name'

    # Save diphone dictionary
    pickle.dump(DIPHONES, open("diphone_library.pckl", "wb"))
    return DIPHONES


# Input path to wav folder and label folder
setDiphoneLibrary('./data','./data')
