## This folder

Extracted features are appended to the csvoutput file (one row per wavfile).

This repository does not contain speakers' sensible data, complying with the NSC license. All speakers names were pseudonymised. There is no possibility to retrieve the original recorded speech from the provided material.



## csv files

* [eGeMAPS](http://ieeexplore.ieee.org/document/7160715/) stands for extended Geneva Minimalistic Acoustic Parameter Set (88 features extracted from each speech segment)

* Extracted with the [openSMILE toolkit](http://audeering.com/technology/opensmile/) (see [feature_extraction](https://github.com/laufergall/ML_Speaker_Characteristics/tree/master/feature_extraction))

* eGeMAPSv01a_semispontaneous_splitted.csv -> features from all semispontaneous dialogs from the 300 speakers of the [NSC corpus](http://www.qu.tu-berlin.de/?id=nsc-corpus): d5 (car rental booking), d6 (pizza order), d7 (book from the library), and d8 (doctor's appointment). Clean microphone speech (fs = 48 kHz). Each dialog was split into 3 segments of approximately 10 seconds each. From each segment, the eGeMAPS features were extracted. 

* eGeMAPSv01a_stimuli_splitted.csv, _degraded.csv, and _distorted.csv -> The "stimuli" segments of the NSC corpus (a shortened version of the semispontaneous dialog 6) were splitted into 2 segments of approximately 10 seconds each and the eGeMAPS features were extracted from each of the segments. 

  * eGeMAPSv01a_stimuli_splitted.csv correspond to features extracted from clean microphone speech (fs = 48 kHz)
  * eGeMAPSv01a_stimuli_splitted_degraded.csv correspond to features extracted from degraded speech: transmitted though a communication channel involving a bandwidth filter and a codec. More details in the [distortions](https://github.com/laufergall/ML_Speaker_Characteristics/tree/master/data/distortions) folder.
  * eGeMAPSv01a_stimuli_splitted_distorted.csv correspond to features extracted from degraded and distorted speech: transmitted though a communication channel involving a bandwidth filter and a codec and distorted by jitter and packet loss conditions. More details in the [distortions](https://github.com/laufergall/ML_Speaker_Characteristics/tree/master/data/distortions) folder.

  ​