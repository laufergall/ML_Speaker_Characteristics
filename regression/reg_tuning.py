import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.multioutput import MultiOutputRegressor
import pickle # save models

def summary_tuning(cname, search_result, filename):
    """
    Summarize results of cross-validation on set A for hyperparameter tuning

    Inputs:
    - cname: regressor name
    - search_result: RandomizedSearchCV results for this regressor, output of search.fit(AX, Ay)
    - filename: filename with path to write the summary to
    """
    means = search_result.cv_results_['mean_test_score']
    stds = search_result.cv_results_['std_test_score']
    params = search_result.cv_results_['params']

    # print best result and append to our lists
    print("%r -> Best cross-val score on A set: %f using %s" % (cname, search_result.best_score_, search_result.best_params_))

    # dataframe with summary
    d = {
        'model': cname,
        'mean_acc_A': means,
        'stdev_acc_A': stds,
        'params': params,
    }
    df = pd.DataFrame(data = d)
    df.to_csv(filename, index=False)


def hp_tuner(AX, BX, Ay, By, get_reg_functions, label, feats_names, k_array, mode, n_iter=10):
    """
    Perform nested hyperparameter tuning with RandomizedSearchCV.
    Given training data splitted into A, B sets and for each regressor type:
    Stratified cross-validation for feature selection and hyperparameter tuning using set A
    Generates csv file with summary of hp tuning (set A)
    Evaluate the performance on set B and return accs

    Input:
    - AX and BX: features of the train set, splitted
    - Ay and By: labels of the train set, splitted
    - get_reg_functions: list of functions tho get regressor and dict of hp to tune
    - label: str to keep track of the different runs in the filename
    - feats_names: list of feature names, only needed for output
    - k_array: numpy array with values to try for SelectKBest features
    - mode: str indicating type of hyperparameter search: 'random' or 'grid'
    - n_iter: number of iterations for random search (optional, default = 10, ignored if grid search)

    Output:
    - reg_acc_hps: pandas dataframe with:
        - regressors names
        - regressors hyperparameters
        - selected features
        - accuracies on B set
        of each tuned regressor corresponding to get_reg_functions
    - trained_reg_list: list of regressors tuned and trained on (AX+BX)
    """

    # init lists (there will be one element per regressor in get_reg_functions)

    regressors_names = []
    regressors = []
    hparam_searchs = []
    best_accs = [] # on the B set
    best_hps = [] # determined with CV on A
    sel_feats_i = [] # indexes of selected features
    sel_feats = [] # names of selected features
    trained_reg_list = [] # tuned regressor trained on X,y

    # iterate over list of functions
    # to get regressors and parameters and append to our lists

    for fn in get_reg_functions:
        regname, reg, hp = fn()
        regressors_names.append(regname)
        regressors.append(reg)
        hparam_searchs.append(hp)

    # tune hyperparameters with RandomizedSearchCV for each regressor

    for i in np.arange(len(regressors)):

        if Ay.ndim > 1: # multioutput (SelectKBest not supported)

            # create pipeline
            pipe = Pipeline([
                ('regressor', MultiOutputRegressor(regressors[i]))
            ])

            # feature selection params and regressor's params for param_gridsearch:
            all_params = hparam_searchs[i]

        else:

            # create pipeline
            pipe = Pipeline([
                ('selecter', SelectKBest(f_regression, k=4)),
                ('regressor', regressors[i])
            ])

            # feature selection params: given as input to this function
            fsel_params = dict(
                selecter__k = k_array
            )

            # feature selection params and regressor's params for param_gridsearch:
            all_params = {**fsel_params, **hparam_searchs[i]}

        # perform randomized search or grid search on hyper parameters
        if mode == 'random':
            search = RandomizedSearchCV(estimator=pipe,
                                param_distributions=all_params,
                                n_iter=n_iter,
                                scoring='neg_mean_squared_error', # metrics.mean_squared_error
                                n_jobs=1,
                                cv=10)

        elif mode == 'grid':
            search = GridSearchCV(estimator=pipe,
                                param_grid=all_params,
                                scoring='neg_mean_squared_error', # metrics.mean_squared_error
                                n_jobs=1,
                                cv=10)

        # This might take a while:
        search_result = search.fit(AX, Ay)

        # summary of hp tuning on set A
        # generate one csv file per regressor
        summary_tuning(regressors_names[i],
                       search_result,
                       r'.\data_while_tuning\%s_%s_tuning.csv' % (regressors_names[i], label))

        # get selected features on set A (not if multioutput
        if Ay.ndim > 1: # multioutput (SelectKBest not supported)
            sel_i = np.ones(AX.shape[1], dtype=bool)
        else:
            sel_i = search_result.best_estimator_.named_steps['selecter'].get_support()

        selected = [i for indx, i in enumerate(feats_names) if sel_i[indx]]
        #print("%r -> Selected features:" % regressors_names[i])
        #print(selected)
        sel_feats_i.append(sel_i)
        sel_feats.append(selected)

        # evaluate regressor on set B
        By_pred = search_result.best_estimator_.predict(BX)
        score_on_B = np.sqrt(mean_squared_error(By, By_pred))
        print("%r -> root mean_squared_error on B set: %f\n" % (regressors_names[i], score_on_B))

        # add score on B and hyperparams for output
        best_accs.append(score_on_B)
        best_hps.append(search_result.best_params_)

        # train regressor using all training data with this regressor
        X = np.concatenate((AX, BX), axis=0)
        y = np.concatenate((Ay, By), axis=0)
        trained_reg = search_result.best_estimator_.fit(X,y)
        trained_reg_list.append(trained_reg)

    # create the output dataframe
    d = {
        'regressors_names': regressors_names,
        'best_accs': best_accs,
        'best_hps': best_hps,
        'sel_feats': sel_feats,
        'sel_feats_i': sel_feats_i
    }
    reg_acc_hps = pd.DataFrame(data = d)

    return reg_acc_hps, trained_reg_list


def save_tuning(tuning_all, trained_all, label):
    """
    Saving outpus of hp tuning to disk
    Called after tuning each regressor

    Input:
    - tuning_all: pandas df with tuning results
    - trained_all: list of all regressors trained on training data
    - label: str to keep track of the different runs in the filename
    """

    # save tuning_all
    tuning_all.to_csv(r'.\data_while_tuning\tuning_all_'+ label +'.csv', index=False)

    # save trained_all
    for i in np.arange(len(trained_all)):
        filename = r'.\data_while_tuning\trained_' + tuning_all.loc[i, 'regressors_names'] + '_' + label + '.sav'
        pickle.dump(trained_all[i], open(filename, 'wb'))


def load_tuning(label):
    """
    Loading outpus of hp tuning from disk
    Called to recover what was tuned and trained in previous sessions

    Input:
    - label: str to keep track of the different runs in the filename

    Output:
    - tuning_all: pandas df with tuning results
    - trained_all: list of all regressors trained on training data
    """

    # load tuning_all
    tuning_all = pd.read_csv(r'.\data_while_tuning\tuning_all_'+ label +'.csv')

    # load trained_all
    trained_all=[]
    for i in np.arange(len(tuning_all)):
        filename = r'.\data_while_tuning\trained_' + tuning_all.loc[i, 'regressors_names'] + '_'+ label +'.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
        trained_all.append(loaded_model)

    return tuning_all, trained_all
