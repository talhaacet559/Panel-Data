import pandas as pd
#Variables
json_file = "example.json"
out_file = "Data.xlsx"
row_cond = '"type'

#Useful with transforming rows to columns
def str_to_dict(string):
    # remove the curly braces from the string
    string = string.strip(',')
    string = string.strip("}")
 
    # split the string into key-value pairs
    pairs = string.split(',')
    pair_list = [pair.split(':') for pair in pairs]
    pair_list = [key for key in pair_list if len(key) == 2]
    # use a dictionary comprehension to create
    # the dictionary, converting the values to
    # integers and removing the quotes from the keys
    return {key[1:-2]: value for key, value in pair_list}

df = pd.read_json(json_file)
df = df[df[0].str.startswith(row_cond)]  

count = 0
for i in df.values:
    dict1 = str_to_dict(i[0])
    df_i = pd.DataFrame(dict1,index=[count])
    if count == 0:
        df1 = df_i
        count += 1
    else:
        df1 = pd.concat([df1,df_i])
        count += 1
del df_i
del df

#Transposing
df1 = df1[[df1.columns[3],df1.columns[8],df1.columns[10],df1.columns[-4]]]
df1.set_index([df1.columns[0], df1.columns[1]], append=True, inplace=True)
df1 = df1.pivot(columns=df1.columns[0], values=df1.columns[1])
df1.reset_index(inplace=True)
df1.drop(columns=["level_0"],inplace=True)

#pd.numeric before aggregation
for col in df1.columns[2:]:
    df1[col] = df1[col].apply(pd.to_numeric)
  
#check types
print(df1.dtypes)
    

count = 0
for country in df1[df1.columns[1]].unique():
    for year in df1[df1.columns[0]].unique():
        partial = df1[(df1[df1.columns[0]] == year)&(df1[df1.columns[1]] == country)]
        partial = partial.agg('max').reset_index().T
        partial.columns = partial.loc[df1.columns[1],:]
        partial.drop(index=df1.columns[1],inplace=True)
        if count ==0:
            excel_df1 = partial
            count += 1
        else:
            excel_df1 = pd.concat([excel_df1,partial],axis=0)
del df1
del partial

excel_df1.to_excel(outfile)
