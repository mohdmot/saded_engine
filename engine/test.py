import preprocessing, layer_a, layer_b, fusion
import pandas as pd

df = pd.read_csv('..\\surveys\\survey_1\\data.csv')

# New Data
nr = pd.DataFrame([{
    'name':'John', 
    'age': 23,
    'job': 'Engineer', 
    'salary': 5000,
    'status': 'Single'
}])
df = pd.concat( [df,nr] , ignore_index=True)


config = {
  "numerical_columns": ["age", "salary"],
  "categorical_columns": ["job", "status"],
  "columns_ignored": ["name"],
  "correlation_top_k": 3,
  "suspicion_threshold": 2.0,
  "min_training_samples": 20,
  "ignore_suspicion_below": 0.4
}


df=df.drop('name',axis=1)

preprocessor = preprocessing.Preprocessor(config)
X = preprocessor.fit_transform(df)

#print(X)

layer_a = layer_a.LayerA(config)
layer_a.fit(X)
local_score, local_info = layer_a.evaluate(X)

print(f'''
LayerA
      local_score : {local_score}
      local_info  : {local_info}
''')


layer_b = layer_b.LayerB(config)
layer_b.fit(X)
global_score, global_info = layer_b.evaluate(X)

print(f'''
LayerB
      global_score : {global_score}
      global_info  : {global_info}
''')


fusion = fusion.FusionEngine(config)
final_score = fusion.combine(local_score, global_score)

print('Final Score:',final_score)

if final_score > config["suspicion_threshold"]:
    print('Suspicious !')