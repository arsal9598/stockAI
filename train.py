from data import create_csv, get_toordinal

import pandas as pd
import numpy as np
from sklearn import linear_model

# create stock data
create_csv("aapl")

# loading and separating our stock dataset into labels and features
df = pd.read_csv('aapl.csv')
label = df['open']
features = df.drop('open', axis=1)

# defining our linear regression estimator and training it with our stock data
regr = linear_model.LinearRegression()
regr.fit(features, label)

# using it to predict an open price, all data thats entered should be from date
# previous to one you're trying to predict
print(regr.predict([[get_toordinal("2019-02-01"), 151.7, 155.14, 153.92, 23046560, 0.96, 0.616, 166.9123, 1.368863964914]]))
