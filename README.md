# Predictive modeling for speaker characterization

## Under construction!

Still TODO:

- Classification: evaluate on test data
- regression
- demo
- clustering
- recommender



## Overview

The ability to assess speakers' social and personality-related characteristics automatically is desired in multiple human-computer interaction systems systems that aim at offering individualized services. Recent developments have led to speech assistants with excellent natural language understanding and synthesis capabilities [1]. However, the characterization of individuals and their intentions and behavior still needs to be improved in order to achieve even more human-like communications.

In particular, I am interested in evaluating the performance of speaker characterization over a range of telephone degradations. When such systems encounter transmitted instead of clean speech, e.g. in call centers, the speaker characterization accuracy might be impaired by the degradations inserted by communication channels in the speech signal.

The goal of my project is to automatically characterize users from their speech signals, i.e. recognizing their traits (confidence, friendliness, competence, etc.) by the sound of their voices and manner of speaking. Predictive models will be then tested with speech degraded through telephone channel impairments to assess their influence on speaker characterization.

I will be adding my predictive modeling scripts and results to this repository, as a manner of communicating my ideas combining code, data, and visualizations.

My research profile is outlined [here](http://www.qu.tu-berlin.de/?id=lfernandez) and my publications can also be followed in [ResearchGate](https://www.researchgate.net/profile/Laura_Fernandez_Gallardo).

This work has been supported by the German Research Foundation ([DFG](http://www.dfg.de/en/), Grant FE 1603/1-1).



## Speech database

I use the speech data from the  [Nautilus Speaker Characterization (NSC) Corpus](http://www.qu.tu-berlin.de/?id=nsc-corpus) [2]

- clean conversational speech from 300 German speakers and 34-dimensional labels of interpersonal traits (likability, confidence, maturity, etc.) obtained by subjective listening. 
- freely available for non-commercial research at the [CLARIN](hdl.handle.net/11022/1009-0000-0007-C05F-6) or [ELRA](http://catalog.elra.info/product_info.php?products_id=1318) repositories.

This repository **does not contain speakers' sensible data**, complying with the NSC license. All speakers names were pseudonymised. There is no possibility to retrieve the original recorded speech from the provided material.

Taking advantage of the NSC signals' sampling frequency of 48 kHz, the influence of the newly deployed SWB telephone channels can also be studied together with the NB and WB effects (NB, WB, and SWB signals have 8, 16, and 32 kHz sampling frequency, respectively).



## About the speech degradations  

Speech degraded through [simulated](https://github.com/laufergall/ML_Speaker_Characteristics/tree/master/data/distortions) telecommunication channels with different parameters was employed as test data to evaluate the effects of degradations on classification and regression performance. 

The degradations involved: 

* a bandwidth filter, which limits the range of speech frequencies transmitted. Narrowband (NB, 300 - 3400 Hz), Wideband (WB, 50 - 7000 Hz), and SWB (50 - 14000 Hz) standard telephony bandwidths were considered. 
* a transmission codec to compress/decompress the speech signals for transmission. 
* for each of the codecs a random packet loss rate was applied, indicating how frequently packets are lost in the transmission.
* jitter conditions were also considered for each packet loss condition. 

My many thanks to Dr. Ramón Sánchez Iborra for the application of packet loss and jitter conditions using the [FFmpeg](https://www.ffmpeg.org/) library.



## Folder structure

#### \data

Contains subjective speaker and voice ratings, extracted speech features (see \feature_extraction) and speakers' i-vectors, and similarity matrices between speakers. 

Besides, data generated from this repository's scripts is stored under this folder: pre-processed features, trained models, etc.

#### \feature_extraction

Scripts for speech feature extraction [3] from the NSC speech files (not on this repository) using the [OpenSMILE tool](https://audeering.com/technology/opensmile/) (not on this repository).

#### \exploratory_analysis

Exploring subjective labels.

#### \classification

Evaluating classification techniques for predictive modeling of user traits.

#### \regression

Evaluating regression techniques for predictive modeling of user traits.

#### \demo

Demonstrating the detection of users' interpersonal characteristics by employing the trained classification and regression models.

#### \clustering

Clustering users by their voices and examining the clusters' dominating characteristics.

#### \recommender

Given the subjective ratings of speaker likability and attractiveness (preferences for voices), similarities among raters, and similarities among speakers, generate recommended voices.

#### \doc

Papers, slides, etc.



## Contributing

You are welcome to contribute to this project in any way. Please feel free to fix any errors or send me any suggestion for improvement. If you work at a research institution, you can get the NSC speech files from [here](https://clarin.phonetik.uni-muenchen.de/BASRepository/index.php?target=Public/Corpora/NSC/NSC.1.php).



## References

[1] J. Masche and N.-T. Le, "A Review of Technologies for Conversational Systems," in Advances in Intelligent Systems and Computing, pp. 212–225. Springer, 2018.

[2] L. Fernández Gallardo and B. Weiss, "The Nautilus Speaker Characterization Corpus: Speech Recordings and Labels of Speaker Characteristics and Voice Descriptions," in International Conference on Language Resources and Evaluation (LREC), 2018.

[3] F. Eyben, K. R. Scherer, B. W. Schuller, J. Sundberg, E. André, C. Busso, L. Y. Devillers, J. Epps, P. Laukka, S. S. Narayanan, and K. P. Truong, "The Geneva Minimalistic Acoustic Parameter Set (GeMAPS) for Voice Research and Affective Computing," IEEE Transactions on Affective Computing, vol. 7, no. 2, pp. 190–202, 2016.