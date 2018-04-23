Mc Nemar's test of statistical differences between voice degradations
================
Laura Fernández Gallardo
April 2018

``` r
# Libraries needed:

library(knitr) # for kable
```

Objectives
----------

To assess the effects of speech degradations on the perfromance of Random Forest classification and Support Vector Machine classification of WAAT.

Classification was performed in [this notebook](https://github.com/laufergall/ML_Speaker_Characteristics/blob/master/classification/04_classification_degraded_speech.ipynb), from where true class 'yt\_spk' classification predictions 'yt\_spk\_pred' were genderated for each classifier.

Binomial tests to test for statistically significant differences in classification accuracy across different channel degradations.

\[1\] Noirhomme, Q., Lesenfants, D., Gomez, F., Soddu, A., Schrouff, J., Garraux, G., Luxen, A., Phillips, C., Laureys, S. "Biased binomial assessment of cross-validated estimation of classification accuracies illustrated in diagnosis predictions," NeuroImage: Clinical 4, 687-694, 2014.

Variables:

``` r
siglevel = 0.01 # p-value
```

Load predictions for each classifier
------------------------------------

NA predictions generated when transmission simulations were unsuccessfull (around 7%).

Speakers:

``` r
n_spk <- nrow(classes)
summary(classes)
```

    ##      spkID       gender   class    
    ##  Min.   :  1.0   m: 80   high:104  
    ##  1st Qu.: 81.5   w:103   low : 79  
    ##  Median :152.0                     
    ##  Mean   :151.3                     
    ##  3rd Qu.:218.5                     
    ##  Max.   :300.0

Channel distortions:

``` r
levels(res$distortion)
```

    ## [1] "pl00ji00" "pl01ji00" "pl01ji10" "pl03ji00" "pl03ji10" "pl05ji00"
    ## [7] "pl05ji10" "pl10ji00" "pl10ji10"

Channel degradations:

``` r
levels(res$degradation)
```

    ##  [1] "Clean"          "NB_AMRNB_10_2"  "NB_AMRNB_12_2"  "NB_AMRNB_4_75" 
    ##  [5] "NB_AMRNB_5_15"  "NB_AMRNB_5_9"   "NB_AMRNB_6_7"   "NB_AMRNB_7_4"  
    ##  [9] "NB_AMRNB_7_95"  "NB_G711_A_64"   "NB_G711_u_64"   "NB_G7231_5_3"  
    ## [13] "NB_G7231_6_3"   "NB_GSMEFR_12_2" "NB_Speex_11"    "NB_Speex_2_15" 
    ## [17] "NB_Speex_24_6"  "SWB_EVS_128"    "SWB_EVS_24_4"   "SWB_EVS_32"    
    ## [21] "SWB_EVS_48"     "SWB_EVS_64"     "SWB_EVS_7_2"    "SWB_EVS_96"    
    ## [25] "SWB_G7221C_24"  "SWB_G7221C_32"  "SWB_G7221C_48"  "SWB_Opus_128"  
    ## [29] "SWB_Opus_160"   "SWB_Opus_24"    "SWB_Opus_32"    "SWB_Opus_48"   
    ## [33] "SWB_Opus_64"    "WB_AMRWB_12_65" "WB_AMRWB_14_25" "WB_AMRWB_15_85"
    ## [37] "WB_AMRWB_18_25" "WB_AMRWB_19_85" "WB_AMRWB_23_05" "WB_AMRWB_23_85"
    ## [41] "WB_AMRWB_6_6"   "WB_AMRWB_8_85"  "WB_AMRWB+_10_4" "WB_AMRWB+_12"  
    ## [45] "WB_AMRWB+_13_6" "WB_AMRWB+_15_2" "WB_AMRWB+_16_8" "WB_AMRWB+_19_2"
    ## [49] "WB_AMRWB+_20_8" "WB_AMRWB+_24"   "WB_G722_64"     "WB_Speex_23_8" 
    ## [53] "WB_Speex_3_95"  "WB_Speex_42_2"

Classifiers:

``` r
unique(res$cls)
```

    ## [1] "DummyClassifier"        "KNeighborsClassifier"  
    ## [3] "LogisticRegression"     "RandomForestClassifier"
    ## [5] "SVCrbf"

Load true classes
-----------------

Load true classes of only high/low WAAT: 183 speakers

``` r
classes = read.csv('../data/generated_data/speakerIDs_cls_WAAT_all.csv') 

# predictions as 'high' class coded as 0 and 'low' class coded as 1
classes$class_num <- as.numeric(as.factor(classes$class))-1

# sort according to spkID, since predictions are sorted
classes <- classes[order(classes$spkID),]
```

Binomial tests
--------------

Run Binomial Test for each pair of codecs.

The null hypothesis is that the probability of success (accuracy - not per-class averaged) is the same for the classification with two different speech degradations.

As stated in \[1\]: "With a limited number of trials, the results of a classifier are seen as the results of tossing a coin, an unfair coin, which can be modeled as a Bernoulli trial".

### Performance over chance level

For each classifier: \* Perform Binomial Test over chance level (0.5) for each degradation \* Considering constant packet loss rate = 0 and jitter = 0

``` r
tests_all <- data.frame()

# for each classifier
for (cl in unique(res$cls)){
  
  # subset for classifier and for distortion condition
  res_cls <- res[res$cls == cl,]
  res_cls <- res_cls[res_cls$distortion == 'pl00ji00',]
  
  # tests for this cls
  tests_cls <- data.frame(res_cls$degradation, pval_greater=0, cls=cl)
  
  # for each degradation, perform Binomial Test
  for (i in 1:nrow(tests_cls)){

    # predictions of each degradation
    preds <- as.matrix(res_cls[res_cls$degradation==toString(res_cls$degradation[i]),c(5:(5+n_spk-1))])

    # number of successes 
    n_succ <- sum(preds==classes$class_num)
    
    
    # binom.test and store p.value
    bt <- binom.test(n_succ, n_spk, 0.5, alternative="greater")
    tests_cls$pval_greater[i] <- bt$p.value 
    
  }
  
  tests_all <- rbind(tests_all, tests_cls)
}
```

Looking only at significant differences at 'siglevel' level found in RF and SVC classification.

``` r
# subset for classifiers 
tests_RF_SVC <- tests_all[tests_all$cls %in% c('RandomForestClassifier','SVCrbf'),]
 
# subset for significant differences 
tests_RF_SVC_sig_greater <- tests_RF_SVC[tests_RF_SVC$pval_greater < siglevel,]
```

Performance significantly over chance level:

For RF classification: Clean, WB\_AMRWB+ (all bitrates), and SWB\_Opus (at 32 and 64 kbit/s).

For SVC classification: Clean, WB\_AMRWB (all bitrates except for 23.85 kbit/s), and WB\_AMRWB+ (all bitrates).

### Each pair of degradations

For each classifier: \* Perform Binomial Test with each pair of degradations \* Considering constant packet loss rate = 0 and jitter = 0

Generating combinations of conditions to compare: For each codec, choose the bitrate offering the highest performance. In case of ties, choose the lowest bitrate.

``` r
combs_all <- data.frame()

# for each classifier
for (cl in unique(res$cls)){
  
  # subset for classifier and for distortion condition
  res_cls <- res[res$cls == cl,]
  res_cls <- res_cls[res_cls$distortion == 'pl00ji00',]
  
  # generate combinations
  chosen <- c()
  for (co in unique(res_cls$codec)){
    res_cls_co <- res_cls[res_cls$codec == co,]
    posmax <- which.max(res_cls_co$average.per.class.accuracy)
    chosen <- append(chosen, toString(res_cls_co$degradation[posmax]))
  }
  
  combs_cls <- data.frame(t(combn(chosen, 2)), pval_greater=0, pval_less=0, cls=cl)
  
  # for each pair of degradations, perform Binomial Test
  for (i in 1:nrow(combs_cls )){
    pair <- combs_cls[i,]
    
    # predictions of each degradation
    preds1 <- as.matrix(res_cls[res_cls$degradation==toString(pair[1,1]),c(5:(5+n_spk-1))])
    preds2 <- as.matrix(res_cls[res_cls$degradation==toString(pair[1,2]),c(5:(5+n_spk-1))])

    # number of successes for preds1 and preds2
    n_succ1 <- sum(preds1==classes$class_num)
    n_succ2 <- sum(preds2==classes$class_num)
    
    
    # binom.test for "greater" and store p.value
    bt <- binom.test(n_succ1, n_spk, n_succ2/n_spk, alternative="greater")
    combs_cls$pval_greater[i] <- bt$p.value 
    
    # binom.test for "less" and store p.value
    bt <- binom.test(n_succ1, n_spk, n_succ2/n_spk, alternative="less")
    combs_cls$pval_less[i] <- bt$p.value 
    
  }
  
  combs_all <- rbind(combs_all, combs_cls)
}
```

Looking only at significant differences at 'siglevel' level found in RF and SVC classification.

``` r
# subset for classifiers 
combs_RF_SVC <- combs_all[combs_all$cls %in% c('RandomForestClassifier','SVCrbf'),]
 
# subset for significant differences 
combs_RF_SVC_sig_greater <- combs_RF_SVC[combs_RF_SVC$pval_greater < siglevel,]

combs_RF_SVC_sig_less <- combs_RF_SVC[combs_RF_SVC$pval_less < siglevel,]
```

``` r
print('Codec on the left offers significantly higher performance than the codec on the right')
```

    ## [1] "Codec on the left offers significantly higher performance than the codec on the right"

``` r
print('Significant differences for RF classification:')
```

    ## [1] "Significant differences for RF classification:"

``` r
cbind( as.character(combs_RF_SVC_sig_less[combs_RF_SVC_sig_less$cls=='RandomForestClassifier',2]), as.character(combs_RF_SVC_sig_less[combs_RF_SVC_sig_less$cls=='RandomForestClassifier',1]))
```

    ##       [,1]            [,2]            
    ##  [1,] "NB_G7231_5_3"  "NB_G711_A_64"  
    ##  [2,] "WB_AMRWB_6_6"  "NB_G711_A_64"  
    ##  [3,] "WB_AMRWB+_12"  "NB_G711_A_64"  
    ##  [4,] "SWB_G7221C_32" "NB_G711_A_64"  
    ##  [5,] "SWB_EVS_24_4"  "NB_G711_A_64"  
    ##  [6,] "SWB_Opus_32"   "NB_G711_A_64"  
    ##  [7,] "WB_AMRWB+_12"  "NB_G7231_5_3"  
    ##  [8,] "WB_AMRWB+_12"  "NB_GSMEFR_12_2"
    ##  [9,] "SWB_Opus_32"   "NB_GSMEFR_12_2"
    ## [10,] "WB_AMRWB+_12"  "NB_AMRNB_5_15" 
    ## [11,] "WB_AMRWB+_12"  "NB_Speex_11"   
    ## [12,] "SWB_Opus_32"   "NB_Speex_11"   
    ## [13,] "WB_AMRWB+_12"  "WB_G722_64"    
    ## [14,] "WB_AMRWB+_12"  "WB_AMRWB_6_6"  
    ## [15,] "WB_AMRWB+_12"  "WB_Speex_23_8" 
    ## [16,] "SWB_Opus_32"   "WB_Speex_23_8"

``` r
cbind( as.character(combs_RF_SVC_sig_less[combs_RF_SVC_sig_less$cls=='RandomForestClassifier',2]), as.character(combs_RF_SVC_sig_less[combs_RF_SVC_sig_less$cls=='RandomForestClassifier',1]))
```

    ##       [,1]            [,2]            
    ##  [1,] "NB_G7231_5_3"  "NB_G711_A_64"  
    ##  [2,] "WB_AMRWB_6_6"  "NB_G711_A_64"  
    ##  [3,] "WB_AMRWB+_12"  "NB_G711_A_64"  
    ##  [4,] "SWB_G7221C_32" "NB_G711_A_64"  
    ##  [5,] "SWB_EVS_24_4"  "NB_G711_A_64"  
    ##  [6,] "SWB_Opus_32"   "NB_G711_A_64"  
    ##  [7,] "WB_AMRWB+_12"  "NB_G7231_5_3"  
    ##  [8,] "WB_AMRWB+_12"  "NB_GSMEFR_12_2"
    ##  [9,] "SWB_Opus_32"   "NB_GSMEFR_12_2"
    ## [10,] "WB_AMRWB+_12"  "NB_AMRNB_5_15" 
    ## [11,] "WB_AMRWB+_12"  "NB_Speex_11"   
    ## [12,] "SWB_Opus_32"   "NB_Speex_11"   
    ## [13,] "WB_AMRWB+_12"  "WB_G722_64"    
    ## [14,] "WB_AMRWB+_12"  "WB_AMRWB_6_6"  
    ## [15,] "WB_AMRWB+_12"  "WB_Speex_23_8" 
    ## [16,] "SWB_Opus_32"   "WB_Speex_23_8"

``` r
print(' ')
```

    ## [1] " "

``` r
print('Significant differences for SVC classification:')
```

    ## [1] "Significant differences for SVC classification:"

``` r
cbind( as.character(combs_RF_SVC_sig_less[combs_RF_SVC_sig_less$cls=='SVCrbf',2]), as.character(combs_RF_SVC_sig_less[combs_RF_SVC_sig_less$cls=='SVCrbf',1]))
```

    ##       [,1]             [,2]            
    ##  [1,] "WB_AMRWB_14_25" "NB_G711_A_64"  
    ##  [2,] "WB_Speex_23_8"  "NB_G711_A_64"  
    ##  [3,] "WB_AMRWB+_24"   "NB_G711_A_64"  
    ##  [4,] "SWB_G7221C_48"  "NB_G711_A_64"  
    ##  [5,] "SWB_EVS_64"     "NB_G711_A_64"  
    ##  [6,] "SWB_Opus_32"    "NB_G711_A_64"  
    ##  [7,] "WB_AMRWB_14_25" "NB_G7231_5_3"  
    ##  [8,] "WB_Speex_23_8"  "NB_G7231_5_3"  
    ##  [9,] "WB_AMRWB+_24"   "NB_G7231_5_3"  
    ## [10,] "SWB_G7221C_48"  "NB_G7231_5_3"  
    ## [11,] "SWB_EVS_64"     "NB_G7231_5_3"  
    ## [12,] "SWB_Opus_32"    "NB_G7231_5_3"  
    ## [13,] "WB_AMRWB_14_25" "NB_GSMEFR_12_2"
    ## [14,] "WB_Speex_23_8"  "NB_GSMEFR_12_2"
    ## [15,] "WB_AMRWB+_24"   "NB_GSMEFR_12_2"
    ## [16,] "SWB_G7221C_48"  "NB_GSMEFR_12_2"
    ## [17,] "SWB_EVS_64"     "NB_GSMEFR_12_2"
    ## [18,] "SWB_Opus_32"    "NB_GSMEFR_12_2"
    ## [19,] "WB_AMRWB_14_25" "NB_AMRNB_4_75" 
    ## [20,] "WB_Speex_23_8"  "NB_AMRNB_4_75" 
    ## [21,] "WB_AMRWB+_24"   "NB_AMRNB_4_75" 
    ## [22,] "SWB_G7221C_48"  "NB_AMRNB_4_75" 
    ## [23,] "SWB_EVS_64"     "NB_AMRNB_4_75" 
    ## [24,] "WB_AMRWB_14_25" "NB_Speex_2_15" 
    ## [25,] "WB_Speex_23_8"  "NB_Speex_2_15" 
    ## [26,] "WB_AMRWB+_24"   "NB_Speex_2_15" 
    ## [27,] "SWB_G7221C_48"  "NB_Speex_2_15" 
    ## [28,] "SWB_EVS_64"     "NB_Speex_2_15" 
    ## [29,] "SWB_Opus_32"    "NB_Speex_2_15" 
    ## [30,] "WB_AMRWB_14_25" "WB_G722_64"    
    ## [31,] "WB_AMRWB+_24"   "WB_G722_64"    
    ## [32,] "WB_AMRWB+_24"   "WB_Speex_23_8"

``` r
cbind( as.character(combs_RF_SVC_sig_less[combs_RF_SVC_sig_less$cls=='SVCrbf',2]), as.character(combs_RF_SVC_sig_less[combs_RF_SVC_sig_less$cls=='SVCrbf',1]))
```

    ##       [,1]             [,2]            
    ##  [1,] "WB_AMRWB_14_25" "NB_G711_A_64"  
    ##  [2,] "WB_Speex_23_8"  "NB_G711_A_64"  
    ##  [3,] "WB_AMRWB+_24"   "NB_G711_A_64"  
    ##  [4,] "SWB_G7221C_48"  "NB_G711_A_64"  
    ##  [5,] "SWB_EVS_64"     "NB_G711_A_64"  
    ##  [6,] "SWB_Opus_32"    "NB_G711_A_64"  
    ##  [7,] "WB_AMRWB_14_25" "NB_G7231_5_3"  
    ##  [8,] "WB_Speex_23_8"  "NB_G7231_5_3"  
    ##  [9,] "WB_AMRWB+_24"   "NB_G7231_5_3"  
    ## [10,] "SWB_G7221C_48"  "NB_G7231_5_3"  
    ## [11,] "SWB_EVS_64"     "NB_G7231_5_3"  
    ## [12,] "SWB_Opus_32"    "NB_G7231_5_3"  
    ## [13,] "WB_AMRWB_14_25" "NB_GSMEFR_12_2"
    ## [14,] "WB_Speex_23_8"  "NB_GSMEFR_12_2"
    ## [15,] "WB_AMRWB+_24"   "NB_GSMEFR_12_2"
    ## [16,] "SWB_G7221C_48"  "NB_GSMEFR_12_2"
    ## [17,] "SWB_EVS_64"     "NB_GSMEFR_12_2"
    ## [18,] "SWB_Opus_32"    "NB_GSMEFR_12_2"
    ## [19,] "WB_AMRWB_14_25" "NB_AMRNB_4_75" 
    ## [20,] "WB_Speex_23_8"  "NB_AMRNB_4_75" 
    ## [21,] "WB_AMRWB+_24"   "NB_AMRNB_4_75" 
    ## [22,] "SWB_G7221C_48"  "NB_AMRNB_4_75" 
    ## [23,] "SWB_EVS_64"     "NB_AMRNB_4_75" 
    ## [24,] "WB_AMRWB_14_25" "NB_Speex_2_15" 
    ## [25,] "WB_Speex_23_8"  "NB_Speex_2_15" 
    ## [26,] "WB_AMRWB+_24"   "NB_Speex_2_15" 
    ## [27,] "SWB_G7221C_48"  "NB_Speex_2_15" 
    ## [28,] "SWB_EVS_64"     "NB_Speex_2_15" 
    ## [29,] "SWB_Opus_32"    "NB_Speex_2_15" 
    ## [30,] "WB_AMRWB_14_25" "WB_G722_64"    
    ## [31,] "WB_AMRWB+_24"   "WB_G722_64"    
    ## [32,] "WB_AMRWB+_24"   "WB_Speex_23_8"

Conclusions
-----------

It can therefore be concluded that:

For both classifiers:

-   Performance significantly over chance level found for Clean and WB\_AMRWB+ (all bitrates).

-   Accuracy with clean speech statistically significantly higher than that with all NB-, WB-, and SWB- coded speech, except for AMR-WB+.

For RF classification:

-   The AMRWB+ codec offers statistically significantly superior accuracy than the rest of codecs in all bandwidths.

-   No difference between the rest of WB codecs and NB codecs, except for AMRWB, which offers higher performance than G711.

-   The three SWB codecs also improve the performance of G.711 significantly.

-   In addition, SWB\_Opus provides significantly higher performance than GSMEFR\_12\_2, Speex-NB, and Speex-WB.

For SVC classification:

-   The AMRWB+ codec offers statistically significantly superior accuracy than the rest of codecs in all bandwidths, except for AMR-WB - no statistical difference in accuracy between AMRWB+ and AMRWB.

-   The AMRWB+ codec offers statistically significantly superior accuracy than the rest of codecs in all bandwidths, except for SWB\_G7221C - no statistical difference in accuracy between AMRWB and SWB\_G7221C.

-   All WB and SWB codecs offer statistically significantly superior accuracy than the NB codecs except for G.722 and Opus - no statistical difference in accuracy between G.722 (WB) and NB codecs and between Opus (SWB) and AMRNB.
