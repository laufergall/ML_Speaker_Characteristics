## Details about simulated speech transmissions

The channel degradations have been systematically applied to the clean speech via software simulation of channel transmissions. Different versions of the speech data have been created, and used for the speaker characterization tasks.

### Procedure

1. First, the speech signals were downsampled to 8, 16, or 32 kHz for NB, WB, and SWB transmissions, respectively, using anti-aliasing low-pass FIR filters. 


2. The speech was then level-equalized to -26 dBov, a characteristic level of telephone channels, using the voltmeter algorithm of the International Telecommunication Union - Telecommunication Standardization Sector (ITU-T) Recommendation [P.56](https://www.itu.int/rec/T-REC-P.56/_page.print). 
3. Afterwards, the signals were processed with a pass-band filter simulating typical terminals' sending characteristics, as specified in this [ETSI document](http://www.etsi.org/deliver/etsi_tr/103100_103199/103138/01.03.01_60/tr_103138v010301p.pdf) , which are different for each bandwidth. 
4. Then, pass-band filters with the channel bandwidth-limiting characteristic were applied, following ITU-T recommendations:
  - For NB transmissions: The 8-kHz [P.48](https://www.itu.int/rec/T-REC-P.48-198811-I/en) Intermediate Reference System (IRS) weighting filter was applied as pre-processing. This filter is referred to as *IRS8* in ITU-T Rec. [G.191](https://www.itu.int/rec/T-REC-G.191/en). The bandwith filter applied was the ITU-T Rec. [G.712](https://www.itu.int/rec/T-REC-G.712/en) filter (300-3,400~Hz). 
  - For WB transmissions: A *modified P.341* band-pass filter with cut-off frequencies of 135-7000 Hz was applied as pre-processing to simulate the terminal and the bandwidth limitation. The low cut-off frequency of 135 Hz roughly represents a real WB terminal (mobile phone of reasonable quality or a good quality hand-held or hands-free device). Such a filter was also employed [in this study](http://www.etsi.org/deliver/etsi_eg/202300_202399/20239602/01.01.01_50/eg_20239602v010101m.pdf) (Chapter 7.4). 
  - For SWB transmissions: The flat 50-14000~Hz filter was applied to simulate a good SWB-capable device and the SWB channel bandwidth. This filter can be found in [G.191](https://www.itu.int/rec/T-REC-G.191/en) named as *14KBP*. 
5. After band-filtering the signals, codecs were applied employing standard ITU or European Telecommunications Standards Institute (ETSI) tools or the open-source Speex codec. 
6. Finally, the speech was again level-equalized to \-26 dBov.




### Conditions studied

The degradations involved: 

- a bandwidth filter, which limits the range of speech frequencies transmitted. Narrowband (NB, 300 - 3400 Hz), Wideband (WB, 50 - 7000 Hz), and SWB (50 - 14000 Hz) standard telephony bandwidths were considered. 
- a transmission codec to compress/decompress the speech signals for transmission. Each codec implements a compression algorithm of different characteristics with certain levels of information loss and introduced non-linear distortions. They can operate at different bitrates (kbit/s). 
- Narrowband codecs:  
  - G.711(A-law)@64 and G.711(u-law)@64 
  - G.723.1@5.3 and @6.3
  - GSM-EFR@12.2 
  - AMR-NB@4.75, @5.15, @5.9, @6.7, @7.4, @7.95, @10.2, and @12.2
  - Speex-NB@2.15, @11, and @24.6 
- Wideband codecs:  
  - G.722@64 
  - AMR-WB@6.6, @8.85, @12.65, @14.25, @15.85, @18.25, @19.85, @23.05, and @23.85 
  - Speex-WB@3.95, @23.8, and @42.2 
  - AMR-WB+@10.4, @12, @13.6, @15.2, @16.8, @19.2, @20.8, and @24 
- Super-wideband codecs: 
  - G.722.1C@24, @32, and @48 
  - EVS@7.2, @24.4, @32, @48, @64, @96, and @128 
  - Opus@24, @32, @48, @64, @128, and @160 
- for each of the codecs a random packet loss rate was applied, indicating how frequently packets are lost in the transmission: 0%, 1%, 3%, 5%, and 10% were considered. 
- jitter conditions (no jitter and 10ms jitter) were also considered for each packet loss condition. 

My many thanks to Dr. Ramón Sánchez Iborra (University of Murcia, Spain) for the application of packet loss and jitter conditions using the [FFmpeg](https://www.ffmpeg.org/) library.



### Details about the test-bench for jitter and packet loss

By: Dr. Ramón Sánchez Iborra (University of Murcia, Spain)

An emulation-based test-bench has been deployed for processing the clean audio samples, with the aim of introducing typical impairments suffered during the transmission of the audio signal through a packet-switched network. This emulation strategy permitted us to maintain this network-related negative effects under control for its subsequent analysis. 

Concretely, we employed three different Linux-based virtual machines that assumed the role of i) transmitter, ii) receiver, and iii) intermediate network. The first elements (transmitter and receiver) made use of the *ffmpeg* tool in order to establish and UDP/RTP connection between them. In the transmitter side, the *ffmpeg* tool permitted to encode the original audio sources by using different codecs and configurations. At the other end, the receiver just stored the streamed flow without employing neither reordering techniques nor error-correction algorithms. 

As aforementioned, the network impairments have been emulated by means of a third Linux-based virtual machine; in this case, the *traffic control* (tc) tool processed the crossing traffic introducing specific packet loss and jitter to the audio stream. 

The use of virtual machines permitted us to keep the system under perfect control, avoiding undesirable extra latencies or packet loss in addition to those intentionally introduced by the network-emulation node.

Figure "distortions_test-bench.png" depicts the test-bench configuration.