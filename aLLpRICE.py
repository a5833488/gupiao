import pandas as pd
if __name__ == '__main__':

    dataset = pd.read_csv('C:\\Users\\qinxin\\PycharmProjects\\gupiao\\baiduocpc0.csv',index_col=0)
    dataset_total = pd.concat((["sum"][:'2020/5/3'], ["sum"]['2020/5/4':]), axis=0)
    print(dataset_total)