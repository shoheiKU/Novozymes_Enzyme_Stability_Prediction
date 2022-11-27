from libs import save_dataset as sd
import pandas as pd
def main():
    print("main")
    test = pd.read_csv('../dataset/train_fixed.csv')
    test = sd.add_classified_num_dataset(test)
    test.to_csv('tameshi.csv')


if __name__ == "__main__":
    main()
