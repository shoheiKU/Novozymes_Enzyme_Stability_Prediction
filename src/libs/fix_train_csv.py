import pandas as pd

dataset_path = "./dataset"


def fix_train_csv():
    train_data = pd.read_csv(dataset_path+"/train.csv", index_col='seq_id')
    train_update = pd.read_csv(
        dataset_path+"/train_updates_20220929.csv", index_col='seq_id')
    train_update = train_update.fillna(0)
    train_data.update(train_update)

    train_updated = train_data[train_data['tm'] != 0.0]
    train_updated.to_csv(dataset_path+'/train_fixed.csv')
