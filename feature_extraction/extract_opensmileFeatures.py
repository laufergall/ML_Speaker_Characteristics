"""
==================
Feature extraction
==================

Simple script to extract Opensmile speech features from speech wavfiles
NOTE: Need to change paths to Opensmile, NSC_sessions, sox

Wavfiles can either:
(see examples below)
    * 1. be one single file
    * 2. be all wavfiles found in a folder
    * 3. be chosen from the NSC database structure
    * 4. be all wavfiles found in a folder, splitted into segments

"""

import os
from subprocess import call
from subprocess import check_output

# ==================
# helper functions

def call_opensmile_once(confFileName, wavNamePath, wavName, outputFileName):
    """
    Call opensmile for the given wavfile
    Input: confFileName (str), wavNamePath (str), wavName (str), outputFileName (str)
    """

    # paths (change if necessary!)
    path_opensmile = r"D:\Users\fernandez.laura\Downloads\opensmile-2.3.0"
    path_confFile = path_opensmile + r"\config"
    path_output = r"..\data\extracted_features"

	# append filename to path
    confFile = path_confFile + '\\'+ confFileName;
    outputFile = path_output + '\\'+ outputFileName;

    # one call to opensmile
    c=[
        path_opensmile + r'\bin\Win32\SMILExtract_Release.exe',
        ' -C ', confFile, ' -I ', wavNamePath,' -instname ', wavName,
        ' -csvoutput ',outputFile, ' -timestampcsv 0'
        ]
    print(''.join(c))
    call(''.join(c))


def call_opensmile_list(confFileName, allWavs, allWavsNames, outputFileName):
    """
    Call opensmile for each wavfile of the given list
    Features are appended to outputFile (each row corresponds to one wavfile)
    Input: confFileName (str), allWavs (list), allWavsNames (list), outputFileName (str)
    """

    # paths (change if necessary!)
    path_opensmile = r"D:\Users\fernandez.laura\Downloads\opensmile-2.3.0"
    path_confFile = path_opensmile + r"\config"
    path_output = r"..\data\extracted_features"

	# append filename to path
    confFile = path_confFile + '\\'+ confFileName;
    outputFile = path_output + '\\'+ outputFileName;

    # loop over the list of files
    for i in range(0,len(allWavs)):
        c=[
            path_opensmile + r'\bin\Win32\SMILExtract_Release.exe',
            ' -C ', confFile, ' -I ', allWavs[i],' -instname ', allWavsNames[i],
            ' -csvoutput ',outputFile, ' -timestampcsv 0'
            ]
        call(''.join(c))


def walk_NSC_semispontaneous():
    """
    Get wavfiles (names and paths+names) from the NSC data
    Just those wavfiles corresponding to spontaneous dialogs
    """

    # paths to NSC data (change if necessary!)
    path_NSC_sessions = r"D:\Users\fernandez.laura\ownCloud\Shared\NSC_root_standmic_wav\sessions"

    # walk through the NSC database and get filenamepath of semispontaneous dialogs
    allWavs=[]
    allWavsNames=[]
    for root, dirs, files in os.walk(path_NSC_sessions):
        for fileName in files:
            relDir = os.path.relpath(root, path_NSC_sessions)
            if "semispontaneous_turns" in relDir and fileName.endswith(".wav"):
                allWavs.append(os.path.join(root, fileName))
                allWavsNames.append(fileName)
    return allWavs, allWavsNames

def all_in_folder(folder):
    """
    Get wavfiles (names and paths+names) in the indicated folder
    """
    allWavs=[]
    allWavsNames=[]
    for root, dirs, files in os.walk(folder):
        for fileName in files:
            if fileName.endswith(".wav"):
                allWavs.append(os.path.join(root, fileName))
                allWavsNames.append(fileName)
    return allWavs, allWavsNames


def split_and_extractfeatures_list(nsplits, allWavs, allWavsNames, confFileName, outputFileName):
    """
    For each of the given wavfiles: split into nsplits equal-length segments,
    extract features from each segment and append to outputFileName,
    and delete the generated segments.
    """

    # need to install sox (change path if necessary!)
    path_sox = r"C:\Program Files (x86)\sox-14-4-2"

    # loop to split allWavs, extract features, and delete generated segments
    for i in range(0,len(allWavs)):

        # get duration of wavfile in seconds
        c = [path_sox+r"\sox.exe ", "--i -D ",allWavs[i]]
        out = check_output(''.join(c))
        length_seconds = float(out)

        # loop over segments
        duration = str(int(round(length_seconds/nsplits, 0)))
        for s in range(0,nsplits):

            # trim original audio
            trimmedNamePath = allWavs[i][0:-4] + "_"+str(s+1).zfill(2)+".wav"
            trimmedName = allWavsNames[i][0:-4] + "_"+str(s+1).zfill(2)+".wav"
            start = str(int(round(length_seconds*s/nsplits, 0)))
            c = [
                path_sox+r"\sox.exe ", allWavs[i], " ", trimmedNamePath,
                " trim ", start, " ", duration
                ]
            call(''.join(c))

            # extract features from the generated segment
            call_opensmile_once(confFileName, trimmedNamePath, trimmedName, outputFileName)

            # remove generated segment
            os.remove(trimmedNamePath)


# ==================
# call opensmile given the desired data to extract features from
def main():

    # extract eGeMAPS features in all cases
    confFileName = r"gemaps\eGeMAPSv01a.conf"

    """
    1. extract eGeMAPS features from just one wavfile
    (uncomment the following lines to go for it)
    """
    # outputFileName = "eGeMAPSv01a_once.csv";
    # # must be a wavfile!
    # fileName = "m004_linden_d5.wav"
    # fileNamePath = r"D:\Users\fernandez.laura\Documents\Work\NSC_wavfiles\m004_linden_d5.wav"
    # call_opensmile_once(confFileName, fileNamePath, fileName, outputFileName)

    """
    2. extract eGeMAPS features from wavfiles in a folder
    (uncomment the following lines to go for it)
    """
    # outputFileName = "eGeMAPSv01a_allinfolder.csv";
    # folder = r"D:\Users\fernandez.laura\Documents\Work\folder_with_wavfiles"
    # allWavs, allWavsNames = all_in_folder(folder)
    # call_opensmile_list(confFileName, allWavs, allWavsNames, outputFileName)

    """
    3. extract eGeMAPS features from wavfiles from the NSC database structure
    (uncomment the following lines to go for it)
    """
    # outputFileName = "eGeMAPSv01a_NSC_semispontaneous3.csv";
    # allWavs, allWavsNames = walk_NSC_semispontaneous()
    # call_opensmile_list(confFileName, allWavs, allWavsNames, outputFileName)

    """
    4. Split the wavfiles of this folder into a number of segments,
    extract eGeMAPS features,
    and delete the wavfiles generated by the split
    """
    # opensmile features are appended to this file
    outputFileName = "eGeMAPSv01a_semispontaneous_splitted.csv";

    # set number of segments to split the wavfile into
    # for NSC semispontaneous, we set nsplits = 3 to get segments of ~20s
    nsplits = 3 # split wavFile into 3

    # get wavfiles to extract features from
    # allWavs, allWavsNames = walk_NSC_semispontaneous()
    folder = r"C:\tmp_NSC_wavfiles"
    allWavs, allWavsNames = all_in_folder(folder)

    # function to split and extract features for all wavfiles
    split_and_extractfeatures_list(nsplits, allWavs, allWavsNames, confFileName, outputFileName)


if __name__ == "__main__":
    main()
