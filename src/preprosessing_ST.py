import pandas as pd

dataset = "../dataset"
amino_Cap = ['G','A','V','L','I','C','M','S','T','D','E','N','Q','R','K','H','F','Y','W','P']
adj_amino_Cap = []
all_amino_Cap = []
for Cap1 in amino_Cap:
    for Cap2 in amino_Cap:
        adj_amino_Cap.append(Cap1+Cap2)
all_amino_Cap = adj_amino_Cap
all_amino_Cap.extend(amino_Cap)

train_data = pd.read_csv(dataset+"/train.csv", index_col='seq_id')
train_update = pd.read_csv(dataset+"/train_updates_20220929.csv", index_col='seq_id')
train_update = train_update.fillna(0)
train_data.update(train_update)
x_train = train_data.drop(['data_source','tm'], axis=1)
y_train = train_data['tm']

#for Cap in all_amino_Cap:
#    feature = train_data.drop(['protein_sequence','pH','data_source','tm'], axis=1)
#    rev_Cap = Cap[::-1]
#    for i in range(31389):
#        txt = str(x_train.at[i,'protein_sequence'])
#        if Cap == rev_Cap:
#            feature.at[i,Cap] = txt.count(Cap)
#        else:
#            feature.at[i,Cap] = txt.count(Cap) + txt.count(rev_Cap)
#    print(Cap)
#    x_train = pd.concat([x_train,feature],axis=1)
    
for i in range(31389):
    txt = str(x_train.at[i,'protein_sequence'])
    for Cap in all_amino_Cap:
        rev_Cap = Cap[::-1]
        if Cap == rev_Cap:
            x_train.at[i,Cap] = txt.count(Cap)
        else:
            x_train.at[i,Cap] = txt.count(Cap) + txt.count(rev_Cap)
    x_train.at[i,'len'] = len(txt)
    print(i*100/31388)

x_train = x_train[x_train['len'] != 1.0]
x_train = x_train.drop(['protein_sequence'], axis=1)
y_train = y_train[y_train['tm'] != 0.0]
x_train.to_csv(dataset+'xtrain.csv')
y_train.to_csv(dataset+'ytrain.csv')
