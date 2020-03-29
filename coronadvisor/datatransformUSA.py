from sklearn import preprocessing
import pandas as pd

df = pd.read_csv("us_counties.csv", parse_dates=['Date'])

df["area"] = df["CountryName"] + df["Region"] + df["County"]

df.drop(['County', 'CountryName', 'Region'], axis=1, inplace=True)

le = preprocessing.LabelEncoder()
le.fit(df['area'])
le.transform(df['area']) 

#transform
df["areaCode"] = le.transform(df['area'])
df.drop('area', axis=1, inplace=True)

##inverse function
df["area"] = le.inverse_transform(df['areaCode'])

