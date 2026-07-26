import pandas as pd
df = pd.read_csv('vgsales.csv')
df.shape # (rows, columns)
df.describe() # count, mean, std, min, max, IQR etc.
df.values # sorted in arrays of lists within tuples

