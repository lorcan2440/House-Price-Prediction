from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import pandas as pd


def transform_and_predict(df_sample: pd.DataFrame) -> float:
    '''
    Takes an input containing the 9 numeric variables, preprocesses them and predicts the output.
    '''

    # generate polynomial features
    poly = PolynomialFeatures(degree=3, include_bias=False)
    df_sample_poly = poly.fit_transform(df_sample)

    # standardise wrt dataset means and variances
    means, std_devs = np.load('static/mean_std_arr.npy')
    df_sample_std = (df_sample_poly - means) / std_devs

    # transform to PC space
    pca_mat = np.load('static/pca_components.npy')
    df_sample_pc = df_sample_std @ pca_mat

    # make prediction
    intercept, coeff = np.load('static/lin_reg_int_coef.npy', allow_pickle=True)
    pred = intercept + coeff @ df_sample_pc.T
    return float(pred)
