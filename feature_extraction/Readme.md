As speech features I considered the extended Geneva Minimalistic Acoustic Parameter Set ([eGeMAPS](http://ieeexplore.ieee.org/document/7160715/)). The [openSMILE toolkit](http://audeering.com/technology/opensmile/) was employed to extract this speech feature set. Frequency-, energy-, spectral, and temporal-related parameters are extracted from windowed speech. After smoothing over time with a symmetric 3-frame moving average, functionals such as mean, coefficient of variation, and percentiles are computed and included in the final set of 88 speech features.

- This folder contains necessary code for feaure extraction with OpenSMILE
- The last version needs to be downloaded and unzipped from [here](https://audeering.com/technology/opensmile/)
- I used OpenSMILE version 2.3.0 on Windows 10
- Need to adjust the paths to OpenSMILE and to wav files in the python code
- NSC speech features are writen to csvoutput files in the ../data/extracted_features folder

