# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 20:58:17 2018

@author: 叶哥哥
"""

import numpy as np
from pandas import Series,DataFrame
import scipy.stats.stats as stats
import matplotlib.pyplot as plt
import statsmodels.api as sm

import pandas as pd 

from scipy import stats



def mono_bin(Y, X):
    r = 0
    bad=sum(Y)      #坏客户数(假设因变量列为1的是坏客户)
    good=len(Y)-bad  #好客户数
    n=5
    X = np.array(X)
    Y = np.array(Y)
    while np.abs(r) < 1:
        d1 = pd.DataFrame({"X": X, "Y": Y, "Bucket": pd.qcut(X, n,duplicates='drop')})
        d2 = d1.groupby('Bucket', as_index = False)
        r, p = stats.spearmanr(d2.mean().X, d2.mean().Y)
        n = n - 1
    d3 = pd.DataFrame(d2.X.min(), columns = ['min'])
    d3['min']=d2.min().X    
    d3['max'] = d2.max().X
    d3['sum'] = d2.sum().Y
    d3['total'] = d2.count().Y
    d3['bad_rate'] = d2.mean().Y
    d3['group_rate']=d3['total']/(bad+good)
    d3['woe']=np.log((d3['bad_rate']/(1-d3['bad_rate']))/(bad/good))
    d3['iv']=(d3['sum']/bad-((d3['total']-d3['sum'])/good))*d3['woe']
    iv=d3['iv'].sum()
    d3['iv_sum']=iv
    woe=list(d3['woe'].round(6))   #返回woe可以看到每组对应的woe值
    cut=list(d3['min'].round(6))
    cut1=list(d3['max'].round(6))
    cut.append(cut1[-1]+1)   #返回cut可以看到分箱切割点
    x_woe=pd.cut(X,cut,right=False,labels=woe)
    return  d3


def main(data,tag):
    column_data = {}
    for n in data:
        d3 = mono_bin(tag, list(map(eval,data[n])))
        column_data[n] = d3.to_dict()
    return column_data