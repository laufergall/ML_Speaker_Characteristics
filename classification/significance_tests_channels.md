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

Load predictions for each classifier.

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

Mc Nemar's tests
----------------

Run McNemar's Chi-squared test (with continuity correction). The null hypothesis is that there is no difference in the classification.

For each classifier: \* Perform Mc Nemar's test with each pair of degradations \* Considering constant packet loss rate = 0 and jitter = 0

Generating combinations of conditions to compare: For each codec, choose the bitrate offering the highest performance. In case of ties, choose the lowest bitrate.

``` r
combs <- data.frame()

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
  
  combs <- rbind(combs, data.frame(t(combn(chosen, 2)), pval=0, cls=cl) )
  
  # for each pair of degradations, perform McNemar
  for (i in 1:nrow(combs)){
    pair <- combs[i,]
    
    # predictions of each degradation
    preds1 <- as.matrix(res_cls[res_cls$degradation==toString(pair[1,1]),c(5:(5+n_spk-1))])
    preds2 <- as.matrix(res_cls[res_cls$degradation==toString(pair[1,2]),c(5:(5+n_spk-1))])
    
    preds1 <- as.factor(preds1)
    preds2 <- as.factor(preds2)
    
    levels(preds1) <- c(0,1)
    levels(preds2) <- c(0,1)
    
    # create contingency matrix
    contingm <- table(preds1, preds2)
    
    # mcnemar.test and store p.value
    mcn <- mcnemar.test(contingm)
    combs$pval[i] <- mcn$p.value # NA if identical classif (e.g. dummy)
    
    
  }
  
  
}
```

Looking only at significant differences at 0.01 level found in RF and SVC classification.

``` r
# subset for classifiers 
combs_cls <- combs[combs$cls %in% c('RandomForestClassifier','SVCrbf'),]
 
# subset for significant differences 
combs_cls_sig <- combs_cls[combs_cls$pval<0.01,]
```

TODO: why NAs?

TODO: Conclusions
