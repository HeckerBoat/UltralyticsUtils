import pandas as pd


def get_csv_values(models, y_column):
    for model in models:
        df = pd.read_csv(fr'runs\train\{model}\results.csv')
        df.columns = df.columns.str.strip()

        # 设置Pandas显示选项，以显示所有的行和列
        pd.set_option('display.max_rows', None)  # 显示所有的行
        pd.set_option('display.max_columns', None)  # 显示所有的列

        # 将DataFrame转换为字符串并打印出来
        print(df[y_column].to_string(index=False))
        print(y_column)
