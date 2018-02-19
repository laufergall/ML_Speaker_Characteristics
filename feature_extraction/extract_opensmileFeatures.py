"""
==================
Feature extraction
==================

Simple script to extract Opensmile speech features from speech wavfiles
"""
import os
from subprocess import call

# paths
path_NSC_sessions = r"D:\Work\NSC_root_standmic_wav\sessions"
path_opensmile = r"D:\Users\fernandez.laura\Downloads\opensmile-2.3.0"
path_confFile = path_opensmile + r"\config\gemaps"
path_output = r"..\data\extracted_features"

# variables
confFile = path_confFile + r"\eGeMAPSv01a.conf"
outputFile = path_output + r"\eGeMAPSv01a_NSC_semispontaneous.csv";

# walk through the NSC database and get filenamepath of semispontaneous dialogs
allWavs=[]
allWavsNames=[]
for root, dirs, files in os.walk(path_NSC_sessions):
    for fileName in files:
        relDir = os.path.relpath(root, path_NSC_sessions)
        if "semispontaneous_turns" in relDir and fileName.endswith(".wav"):   
            allWavs.append(os.path.join(root, fileName))
            allWavsNames.append(fileName)

# call opensmile for each wavfile
# features are appended to outputFile (each row corresponds to one wavfile)
for i in range(0,len(allWavs)):
    c=[path_opensmile + r'\bin\Win32\SMILExtract_Release.exe',' -C ', confFile, ' -I ', allWavs[i],' -instname ', allWavsNames[i], ' -csvoutput ',outputFile, ' -timestampcsv 0']
	#print(''.join(c))
    call(''.join(c))

