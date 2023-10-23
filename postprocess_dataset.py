import pandas as pd

dataset = pd.read_csv('dataset.csv')
print(len(dataset))
dataset.replace(' ', pd.NA, inplace=True)
dataset = dataset.dropna(subset=['topic'])
dataset['topic'] = dataset['topic'].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
dataset = dataset[dataset['topic'].str.len() >= 1]
dataset = dataset.drop_duplicates()
dataset.reset_index(drop=True, inplace=True)
dataset.to_csv('dataset.csv', index=False)
print(len(dataset))