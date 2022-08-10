import blazingMatch as bm
import numpy as np
import pandas as pd
from time import time

ctr_score = np.array([
    np.arange(20),
    sorted(np.random.normal(size=20))
]).T

trt_score = np.array([
    np.arange(5),
    sorted(np.random.normal(size=5))
]).T

bm.nearestScore(ctr_score, trt_score)

lalonde = bm.load_lalonde()

tic = time()
result = bm.blazingMatch(data=lalonde, treatment_var='treat',
                confounding_vars=['age', 'educ', 'married', 'nodegree', 're74', 're75', 're78'],
                treatment_group=1)
print(time() - tic)

lalonde[lalonde['treat']==0].describe()
lalonde[lalonde['treat']==1].describe()

result['control'].describe()
result['treatment'].describe()

# data = pd.concat([lalonde for i in range(1000)])
# tic = time()
# result = bm.blazingMatch(data=data, treatment_var='treat',
#                 confounding_vars=['age', 'educ', 'married', 'nodegree', 're74', 're75', 're78'],
#                 treatment_group=1)
# print(time() - tic)
