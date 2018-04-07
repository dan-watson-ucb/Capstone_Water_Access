import pandas as pd
import numpy as np
import sklearn as sk
import datetime as dt
from sklearn import model_selection
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics
from sklearn import ensemble
from sklearn.metrics import confusion_matrix, mean_squared_error, auc, accuracy_score, log_loss
from sklearn.ensemble.partial_dependence import plot_partial_dependence
import os
import matplotlib.pyplot as plt
import itertools
from itertools import product

def permutation_importances(model, X_train, y_train, metric):
    baseline = metric( y_train.values,model.predict_proba(X_train))
    imp = []
    for col in X_train.columns:
        save = X_train[col].copy() #store the original
        X_train[col] = np.random.permutation(X_train[col]) #shuffle each column
        m = metric( y_train.values,model.predict_proba(X_train)) #make predictions
        X_train[col] = save # return it back to normal
        imp.append(baseline - m) # if
    return np.array(imp)

#function to plot_perm_importance
# ex: imp = permutation_importances(model_outer, X_test, y_test, metrics.log_loss)
def plot_perm_importance(perm_importance, X_test):
    #takes a permutatino importance and the input data from it and plots
    df = pd.DataFrame(data=abs(perm_importance), index=X_test.columns).sort_values(by=0)
    df.rename(columns={0:'Feature Importance'},inplace=True)
    df.sort_values(by='Feature Importance').plot(kind='barh',
                    title='Feature Importance', legend=None)
    return df.idxmax()[0] #the top feature column name

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def prob_dist_plot(holdout_predprob, y_holdout, country):
     #plots the probability distributions for the positive and negative class
    x1 = holdout_predprob[y_holdout==0]
    x2 = holdout_predprob[y_holdout==1]
    kwargs = dict(histtype='stepfilled', alpha=0.3, normed=True, bins=40)

    plt.title('probability distribution for true negatives and true positives')
    plt.hist(x1, **kwargs)
    plt.hist(x2, **kwargs)
    plt.savefig('{}_holdout_pred_prob_dist.pdf'.format(country), bbox_inches='tight')

def save_model(model, country):
    filename = '{}_pickle.sav'.format(country)
    pickle.dump(model, open(filename, 'wb'))
    print('saved as', filename)


def get_nested_cv_preds(model, X, Y):
    """args: classification model object, fully numeric/ encoded X, target columns
       returns: array of 1) binary classification predictions, 2) probabilities of class membership"""
    #shuffle is necessary. Define same stratified k-fold as before
    #ToDo - fix hard coding of random state, splits,
    skf= model_selection.StratifiedKFold(n_splits=5, random_state=7, shuffle=True)

    print('full data AUC- CV score', sk.model_selection.cross_val_score(model, X, y=Y, scoring='roc_auc',cv=skf))
    cv_results_preds = sk.model_selection.cross_val_predict(model, X, y=Y, cv=skf )
    cv_results_probs = sk.model_selection.cross_val_predict(model, X, y=Y, cv=skf, method ='predict_proba')

    print("Accuracy full-data : %.4g" % metrics.accuracy_score(Y, cv_results_preds))
    print("AUC Score full-data: %f" % metrics.roc_auc_score(Y, cv_results_probs[:,1]))

    return cv_results_preds, cv_results_probs

def evaluate_prediction_thresholds(y_true, y_pred_probs, recall_val):
    import numpy as np
    d = dict()
    for i in np.linspace(0,0.5, num=20):
        best = 0
        test = np.where(y_pred_probs > i, 1,0)
        recall = metrics.recall_score(y_true, test)
        precision = metrics.precision_score(y_true, test)
        f_score = metrics.f1_score(y_true, test, average='binary')
        d[i]=recall, precision, f_score

    frame = pd.DataFrame.from_dict(d, orient='index')#.columns=(['recall', 'f1_score'])
    frame.columns=(['recall','precision', 'f1_score'])
    frame = frame[frame.recall>recall_val]
    return frame


def create_outyear_predictions(model_outer, X):
    #take a model, make predictions on X at current, 1 year , 3, 5
    #use the defined threshold as the cutoff
    X_today = X.copy()
    X_today['age_well_years'] = X_today.age_well_years + X_today.time_since_meas_years
    #make three other future values to predict, 1 , 3 year and 5 years
    X_1year = X_today.copy()
    X_1year['age_well_years'] = X_1year.age_well_years + 1
    X_1year['time_since_meas_years']=X_1year.time_since_meas_years + 1
    X_3year = X_1year.copy()
    X_3year['age_well_years']=X_3year.age_well_years+2
    X_3year['time_since_meas_years']=X_3year.time_since_meas_years + 2
    X_5year = X_1year.copy()
    X_5year['age_well_years']=X_5year.age_well_years+4
    X_5year['time_since_meas_years']=X_5year.time_since_meas_years + 4

    #####make create_outyear_predictions#########
    today_preds = model_outer.predict(X_today)
    today_predprob = model_outer.predict_proba(X_today)
    one_year_preds = model_outer.predict(X_1year)
    one_year_predprob = model_outer.predict_proba(X_1year)
    three_year_preds = model_outer.predict(X_3year)
    three_year_predprob = model_outer.predict_proba(X_3year)
    five_year_preds = model_outer.predict(X_5year)
    five_year_predprob = model_outer.predict_proba(X_5year)

    return today_predprob, one_year_predprob, three_year_predprob, five_year_predprob

def append_outyear_predictions(original_df, threshold, today_predprob, one_year_predprob, three_year_predprob, five_year_predprob):
    sl = original_df.copy()
    sl['today_preds']=np.where(sl.status_binary==1,1,np.where(today_predprob[:,1]>threshold,1,0))

    sl['today_predprob']= today_predprob[:,1]

    sl['one_year_preds'] = np.where(np.max(sl[['status_binary','today_preds']], axis = 1)>0,
                                    1,np.where(one_year_predprob[:,1]>threshold,1,0))
    sl['one_year_predprob'] = one_year_predprob[:,1]

    sl['three_year_preds'] = np.where(np.max(sl[['status_binary','today_preds', 'one_year_preds']], axis = 1)>0,1,
                                      np.where(three_year_predprob[:,1]>threshold,1,0))
    sl['three_year_predprob']= three_year_predprob[:,1]

    sl['five_year_preds']=np.where(np.max(sl[['status_binary','today_preds', 'one_year_preds', 'three_year_preds']], axis = 1)>0,
                                   1,np.where(five_year_predprob[:,1]>threshold,1,0))
    sl['five_year_predprob'] =five_year_predprob[:,1]

    return sl

def get_holdout_results(model,country, X2,Y, X_train, X_test, y_train, y_test, X_holdout, y_holdout):
    """
    uses pickled model to get summarized train, test and holdout scores for a model
    args: model object, label encoded X and label encoded partitions
    returns: dataframe of results, holdout probabilities and holdout predictions (default 0.5 threshold)
    """
    dtrain_predictions = model.predict(X_train)
    dtrain_predprob = model.predict_proba(X_train)[:,1]
    dtest_predprob = model.predict_proba(X_test)[:,1]
    dtest_predictions = model.predict(X_test)
    #predict on the holdout set
    dholdout_predprob = model.predict_proba(X_holdout)[:,1]
    dholdout_predictions = model.predict(X_holdout)

    #Print model report:

    train_auc = metrics.roc_auc_score(y_train, dtrain_predprob)
    test_auc= metrics.roc_auc_score(y_test, dtest_predprob)
    holdout_auc = metrics.roc_auc_score(y_holdout, dholdout_predprob)
    train_accuracy = metrics.accuracy_score(y_train.values, dtrain_predictions)
    test_accuracy = metrics.accuracy_score(y_test.values, dtest_predictions)
    holdout_accuracy = metrics.accuracy_score(y_holdout.values, dholdout_predictions)
    training_rows = int(X_train.shape[0])
    testing_rows= int(X_test.shape[0])
    holdout_rows = int(X_holdout.shape[0])

    skf= model_selection.StratifiedKFold(n_splits=5, random_state=7, shuffle=True)

    five_fold_nested_cv_auc = sk.model_selection.cross_val_score(model, X2, y=Y, scoring='roc_auc',cv=skf)
    five_fold_nested_cv_auc_mean = np.mean(five_fold_nested_cv_auc)
    five_fold_nested_cv_auc_std = np.std(five_fold_nested_cv_auc)

    df = pd.DataFrame({'country':country,'train_auc':train_auc, 'test_auc':test_auc,'holdout_auc':holdout_auc,
                    'train_accuracy':train_accuracy,'test_accuracy':test_accuracy,'holdout_accuracy':holdout_accuracy,
                     'training_rows': training_rows, 'testing_rows':testing_rows, 'holdout_rows':holdout_rows,
                      'five_fold_nested_cv_auc_mean':five_fold_nested_cv_auc_mean, 'five_fold_nested_cv_auc_std':five_fold_nested_cv_auc_std
                      }, index=['values'])

    return df, dholdout_predprob, dholdout_predictions



def code_and_split(df,features):
    """
    #Splits data in 60% train, 20% test and 20% holdout, and label encodes
    non-numeric features
    #args: dataframe and feature list
    #returns: full label encoded X and all encoded folds
    """

    df2 = df.copy()
    df2 = df2[features]

    #eliminate null target values
    df2 = df2[pd.notnull(df['status_binary'])]

    X = df2[df2.columns[:-1]]
    Y= df2.status_binary

    X2 = X.copy()

    #convert all fields to int labels for XGBoost
    lb=LabelEncoder() #instantiate label encoder
    cols = X2.select_dtypes(include=['object']).columns #pick non-numeric cols
    # Encoding each variable
    for col in cols:
        X2[col]= lb.fit_transform(X[col].fillna('__MISSING__'))
    #60/20/20 Train/Test/Holdout Split
    SEED=7
    X_train, X_test_and_holdout, y_train, y_test_and_holdout = sk.model_selection.train_test_split(X2, Y,
                                                                                            test_size=.4,
                                                                                            stratify=Y,
                                                                                            random_state=SEED)
    X_test, X_holdout, y_test, y_holdout = sk.model_selection.train_test_split(X_test_and_holdout,
                                                                        y_test_and_holdout,
                                                                        test_size=.5,
                                                                        stratify= y_test_and_holdout,
                                                                        random_state=SEED)
    return X2,Y, X_train, X_test, y_train, y_test, X_holdout, y_holdout

def top_feat_table(df,feat):
    """
    returns functioning and non-functioning wells by the most important
    (or any) feature
    args: un-label encoded data frame; top feature (string)
    returns: dataframe
    """
    #shows what of the top features failed in the training data
    gp = df.groupby([feat, 'status_binary']).size().unstack()
    gp['percentage_broken'] = round(gp[1]/gp.sum(axis=1)*100,2)
    gp.reset_index(inplace=True)
    gp.rename(columns={0:'# functioning', 1:'# not functioning'},index={'status_binary':'index'},  inplace=True)
    gp.sort_values(by='# not functioning', ascending =False, inplace=True)
    gp.rename_axis('index', axis='columns').fillna(0, inplace=True)
    return gp

def summarize_country(country, df, features, model):
    frame = df.loc[df.country_name==country]
    X2,Y, X_train, X_test, y_train, y_test, X_holdout, y_holdout = code_and_split(frame, features)

    results, probs, preds = get_holdout_results(model, country ,X2, Y, X_train,
                                         X_test, y_train, y_test, X_holdout, y_holdout)

    results = results.T #tall format
    results.to_csv('{}_summary.csv'.format(country))
    plt.subplots()
    prob_dist_plot(probs, y_holdout, country)
    plt.show()

    #compute feature importance
    imp = permutation_importances(model, X_test, y_test, metrics.log_loss)
    #grab the top feature
    top_feat = plot_perm_importance(imp, X_test)
    plt.show()
    #check out summary stats by top feature, water source, water tech, and save
    top_feat_table(frame, top_feat).to_csv('{}_waterpoint_function_by_{}.csv'.format(country,top_feat))
    top_feat_table(frame, 'fuzzy_water_source').to_csv('{}_waterpoint_function_by_{}.csv'.format(country,'fuzzy_water_source'))
    top_feat_table(frame, 'fuzzy_water_tech').to_csv('{}_waterpoint_function_by_{}.csv'.format(country,'fuzzy_water_tech'))

    plt.savefig('{}_feature_importance.pdf'.format(country), bbox_inches='tight')
    plt.savefig('{}_feature_importance.png'.format(country), bbox_inches='tight')

    #plot the probability distribution for functioning and non-functioning wells

    #plot the confusion matrix
    cm=confusion_matrix(y_holdout, preds)
    names = ['functioning', 'not_functioning']

    plot_confusion_matrix(cm, names, title = 'confusion matrix on holdout data, without normalization', normalize=False)
    plt.savefig('{}_confusion_matrix_by_count.pdf'.format(country, bbox_inches='tight'))
    plt.show()
    plot_confusion_matrix(cm, names, title = 'confusion matrix on holdout data, with normalization', normalize=True)
    plt.savefig('{}_confusion_matrix_normalized.pdf'.format(country, bbox_inches='tight'))

    return y_holdout, probs, preds
