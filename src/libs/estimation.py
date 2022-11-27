import os
import pickle
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor


# input:
#   X: (pd.DataFrame) input dataset,
#   Y: (array) target values
#   path: (str) save path for cv_results_
# output:
#   best_estimator_: (RandomForestRegressor) the best randomforest estimator
# about:
#   rf_grid_search saves cv_results_ as binary file (.pkl) and returns best_estimator_
def rf_grid_search(X, Y, path):
    SEARCH_PARAMS = {
        'max_features': [1, 2, 3, 10, "sqrt", 1.0],
        'min_samples_split': [2, 3, 5, 10],
        'min_samples_leaf': [1, 2, 3, 5, 10],
        'max_depth': [2, 5, 10, 12, 15, 17, 20, None],
        'n_estimators': [5, 10, 25, 50, 75, 100]
    }
    gsr = GridSearchCV(
        RandomForestRegressor(random_state=50),
        SEARCH_PARAMS,
        cv=5,
        n_jobs=-1,
        verbose=True,
        return_train_score=True
    )
    gsr.fit(X, Y)
    with open(path, "rb") as f:
        pickle.dump(gsr.cv_results_, f)
    return gsr.best_estimator_


# input:
#   path: (str) the path to the cv_result binary file (.pkl)
# output:
#   dic: (dict) dict of cv_result
def load_hyper_tuning_result(path):
    with open(path, "rb") as f:
        dic = pickle.load(f)
    return dic


# input:
#   y: (array) predicted values
# output:
#   None
def save_result(y):
    # make result directory
    os.makedirs("./result", exist_ok=True)
    seq_id_test = pd.read_csv("./dataset/test.csv").iloc[:, 0]
    result = pd.concat([seq_id_test, pd.Series(y, name="tm")], axis=1)
    # get save path
    save_path = "./result/result_{:02d}.csv"
    save_index = 0
    while os.path.isfile(save_path.format(save_index)):
        save_index += 1
    # save
    result.to_csv(save_path.format(save_index), index=False)
