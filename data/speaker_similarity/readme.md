## Similarity matrices

These similarity matrices were built as part of Renzo Verastegui's master thesis. 

### Speaker recognition systems

Voice similarity among the speakers of the [NSC corpus](http://www.qu.tu-berlin.de/?id=nsc-corpus)  was computed from the scores of two speaker recognition systems: 

* **ivCDS**: considers i-vectors and cosine distance scoring (CDS)
    * Best performance, male speakers: 128 Gaussian mixtures (GMM) of the UBM and 100 i-vector components (ivdim) (EER = 0.258, DCF 2008 = 0.0003)
    * Best performance, female speakers: 128 GMM, 100 ivdim (EER = 0.010, DCF 2008 = 9.9e-5)
* **ivFFNN**: inputs i-vectors to a fully connected Feedforward Neural Network (FFNN) and computes the probability of each speaker having the identity of every other in the database
    * Best performance, male speakers: 128 GMM and 200 ivdim (EER = 0.793, DCF 2008 = 0.0031)
    * Best performance, female speakers: 128 GMM, 200 ivdim (EER = 0, DCF 2008 = 0)

The i-vectors corresponding to the NSC semi-spontaneous dialogs can be seen in the \data\ivectors folder.