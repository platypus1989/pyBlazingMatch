import pandas as pd
import numpy as np
from cppmodule import nearestScore
import statsmodels.api as sm
from statsmodels.genmod.generalized_linear_model import GLM

def closestIndex(ctr_score, trt_score):
    ctr_score = ctr_score.sort_values().reset_index().values
    trt_score = trt_score.sort_values().reset_index().values

    matched_index = nearestScore(ctr_score, trt_score).reshape([trt_score.shape[0], 2], order='F')

    return matched_index


def blazingMatch(data, treatment_var, confounding_vars, treatment_group=1):
    index_dict = dict(zip(np.arange(data.shape[0]), data.index))
    data.index = np.arange(data.shape[0]) # temporary fix

    group_labels = data[treatment_var].unique()
    if 'score' in data.columns:
        raise ValueError("data can not have column named as score")
    if len(group_labels) != 2:
        raise ValueError("currently only support binary treatment variable")
    if treatment_group not in group_labels:
        raise ValueError("treatment_group has to be one of the two groups in treatment variable")

    y = np.where(data[treatment_var]==treatment_group, 1, 0)
    X = data[confounding_vars].values

    model = GLM(y, X, family = sm.families.Binomial())
    result = model.fit()

    scores = pd.Series(result.predict(X), index=data.index)

    ctr_score = scores[y == 0]
    trt_score = scores[y == 1]

    matched_index = closestIndex(ctr_score, trt_score)

    matched_control = data.loc[matched_index[:, 0]]
    treatment = data.loc[matched_index[:, 1]]

    matched_control.index = matched_control.index.map(index_dict)
    treatment.index = treatment.index.map(index_dict)

    result = {'control': matched_control,
              'treatment': treatment}

    data.index = data.index.map(index_dict)

    return result
