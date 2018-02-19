## I-vectors
These i-vectors were extracted as part of Renzo Verastegui's master thesis.

The i-vectors have been extracted with dimensions 100 and 200 from the different semi-spontaneous dialog turns uttered by the 300 (174 f, 126 m) German speakers of the [NSC corpus](http://www.qu.tu-berlin.de/?id=nsc-corpus).

Mel-Frequency Cepstral Coefficients (MFCC) were extracted as speech features using [VoiceBox](http://www.ee.ic.ac.uk/hp/staff/dmb/voicebox/voicebox.html). We employed a Hamming window with a frame length of 25 ms and a frame shift of 10 ms. The resulting feature vectors had 63 dimensions, consisting of log energy, 20 MFCCs, and delta and delta delta coefficients.

UBM training and i-vector extraction were performed with the [MSR Identity Toolbox](https://www.microsoft.com/en-us/download/details.aspx?id=52279&from=http%3A%2F%2Fresearch.microsoft.com%2Fen-us%2Fdownloads%2F2476c44a-1f63-4fe0-b805-8c2de395bb2c%2F).

### UBM

Several German speech databases have been combined to gather sufficient speech material to train gender-dependent Universal Background Models (UBMs). Of all databases available to us, we have selected those in German, having large number of speakers, and presenting similar recording conditions (microphone speech). 

These databases were: 

* Verbomobil 1 (320 f, 353 m)
* Verbomobil 2 (119 f , 95 m)
* Regional Variants of German 1 (218 f, 282 m)
* Phon Dat I (100 f, 101 m)
* Voxforge (50 f, 130 m)
* BAS Alcohol Language Corpus (77 f, 85 m)
* Oldenburg Logatome Corpus (25 f, 25 m)
* internal corpora at [our institution](http://www.qu.tu-berlin.de/) (43 f, 53 m)

This results on a combined development corpora involving 248207 and 214803 audio files from 1124 male and 952 female speakers, respectively.
