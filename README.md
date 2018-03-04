# Predictive modeling for speaker characterization

## Overview

The ability to assess speakers' social and personality-related characteristics automatically is desired in multiple novel systems that aim at offering individualized services. Recent developments have led to speech assistants with excellent natural language understanding and synthesis capabilities [1]. However, the characterization of individuals and their intentions and behavior still needs to be improved in order to achieve even more human-like communications.

The goal of this project is to automatically characterize users from their speech signals, i.e. recognizing their traits (confidence, friendliness, competence, etc.) by the sound of their voices and manner of speaking.

I will be adding my predictive modeling scripts and results to this repository, as a manner of communicating my ideas combining code, data, and visualizations.

My research profile is outlined [here](http://www.qu.tu-berlin.de/?id=lfernandez) and my publications can also be followed in [ResearchGate](https://www.researchgate.net/profile/Laura_Fernandez_Gallardo).



## Speech database

I use the speech data from the  [Nautilus Speaker Characterization (NSC) Corpus](http://www.qu.tu-berlin.de/?id=nsc-corpus) [2]

- clean conversational speech from 300 German speakers and 34-dimensional labels of interpersonal traits (likability, confidence, maturity, etc.) obtained by subjective listening. 
- freely available for non-commercial research at the [CLARIN](hdl.handle.net/11022/1009-0000-0007-C05F-6) or [ELRA](http://catalog.elra.info/product_info.php?products_id=1318) repositories.

This repository **does not contain speakers' sensible data**, complying with the NSC license. All speakers names were pseudonymised. There is no possibility to retrieve the original recorded speech from the provided material.

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



## About the speech degradations  

Speech degraded through telecommunicaiton channels with different parameters was employed as test data to evaluate the effects of degradations on classification and regression performance. 

The degradations involved: 

* a bandwidth filter, which limits the range of speech frequencies transmitted. Narrowband (NB, 300 - 3400 Hz), Wideband (WB, 50 - 7000 Hz), and SWB (50 - 14000 Hz) standard telephony bandwidths were considered. 
* a transmission codec to compress/decompress the speech signals for transmission. Each codec implements a compression algorithm of different characteristics with certain levels of information loss and introduced non-linear distortions. They can operate at different bitrates (kbit/s). 
*  Narrowband codecs:  
  * G.711(A-law)@64 and G.711(u-law)@64 
  * G.723.1@5.3 and @6.3
  *  GSM-EFR@12.2 
  * AMR-NB@4.75, @5.15, @5.9, @6.7, @7.4, @7.95, @10.2, and @12.2
  * Speex-NB@2.15, @11, and @24.6 
* Wideband codecs:  
  * G.722@64 
  * AMR-WB@6.6, @8.85, @12.65, @14.25, @15.85, @18.25, @19.85, @23.05, and @23.85 
  * Speex-WB@3.95, @23.8, and @42.2 
  * AMR-WB+@10.4, @12, @13.6, @15.2, @16.8, @19.2, @20.8, and @24 
* Super-wideband codecs: 
  * G.722.1C@24, @32, and @48 
  * EVS@7.2, @24.4, @32, @48, @64, @96, and @128 
  * Opus@24, @32, @48, @64, @128, and @160 
* for each of the codecs: a random packet loss rate was applied, indicating how frequently packets are lost in the transmission: 0%, 1%, 3%, 5%, and 10% were considered. 
* jitter conditions (no jitter and 10ms jitter) were also considered for each packet loss condition. 

My many thanks to Dr. Ramón Sánchez Iborra for the application of packet loss and jitter conditions using the [FFmpeg](https://www.ffmpeg.org/) library.



## Under construction!

Still TODO:

* Classification: evaluate on test data
* regression
* demo
* clustering
* recommender



## Contributing

You are welcome to contribute to this project in any way. Please feel free to fix any errors or send me any suggestion for improvement. If you work at a research institution, you can get the NSC speech files from [here](https://clarin.phonetik.uni-muenchen.de/BASRepository/index.php?target=Public/Corpora/NSC/NSC.1.php).



## References

[1] J. Masche and N.-T. Le, "A Review of Technologies for Conversational Systems," in Advances in Intelligent Systems and Computing, pp. 212–225. Springer, 2018.

[2] L. Fernández Gallardo and B. Weiss, "The Nautilus Speaker Characterization Corpus: Speech Recordings and Labels of Speaker Characteristics and Voice Descriptions," in International Conference on Language Resources and Evaluation (LREC), 2018.

[3] F. Eyben, K. R. Scherer, B. W. Schuller, J. Sundberg, E. André, C. Busso, L. Y. Devillers, J. Epps, P. Laukka, S. S. Narayanan, and K. P. Truong, "The Geneva Minimalistic Acoustic Parameter Set (GeMAPS) for Voice Research and Affective Computing," IEEE Transactions on Affective Computing, vol. 7, no. 2, pp. 190–202, 2016.