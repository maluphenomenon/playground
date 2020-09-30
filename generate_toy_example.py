import pandas as pd
import numpy as np


def display_best_match_designer(designer_name):
    df_designer, df_customer = _generate_top_matches()
    df = df_designer.loc[df_designer['designer_name'] == designer_name.lower()]
    print(f'Hi {designer_name.capitalize()}! Here are your top three suggestions for customers:')
    for x in range(len(df)) :
        df_cust = df.iloc[[x]]
        criteria = df_cust.columns[df_cust.isin([1]).any()].to_list()
        cleaned_criteria = []
        for i in criteria:
            cleaned_criteria.append(i[:-6])
        print('Customer ' + str(df_cust['customer_name'].iloc[0]).capitalize() + f'is your number {x + 1} match, based on:')
        print(*cleaned_criteria, sep=', ')


def _generate_top_matches():
    df = _match_customers_and_designers()
    cols_to_keep = ['designer_name', 'customer_name']
    df['rank'] = df.drop(cols_to_keep, axis=1).sum(axis=1)
    df_designer = df.groupby("designer_name").apply(lambda x: x.sort_values(["rank"], ascending=False).head(3)).reset_index(drop=True)
    df_customer = df.groupby("customer_name").apply(lambda x: x.sort_values(["rank"], ascending=False).head(3)).reset_index(drop=True)
    return df_designer, df_customer


def _match_customers_and_designers():
    df = _read_in_data()
    qual_cols = ['theme', 'color', 'cut', 'fabric']
    quant_cols = ['time', 'price']
    for qual_col in qual_cols:
        df[f'{qual_col}_match'] = np.where(df[f'designer_{qual_col}'] ==
            df[f'customer_{qual_col}'], 1, 0)
    for quant_col in quant_cols:
        if quant_col == 'time':
            df[f'{quant_col}_match'] = np.where((df[f'designer_{quant_col}'] <=
                df[f'customer_{quant_col}']) | (df[f'designer_{quant_col}'] ==
                df[f'customer_{quant_col}'] + 1), 1, 0)
        else:
            df[f'{quant_col}_match'] = np.where((df[f'designer_{quant_col}'] <=
                df[f'customer_{quant_col}']) | (df[f'designer_{quant_col}'] ==
                df[f'customer_{quant_col}'] + 100), 1, 0)
    match_cols = ['designer_name', 'customer_name'] + [col for col in df.columns if 'match' in col]
    df_out = df[match_cols]
    return df_out


def _read_in_data():
    df_designers = pd.read_csv('data/designer_features.csv')
    df_customers = pd.read_csv('data/customer_features.csv')
    df_designers['key'] = 0
    df_customers['key'] = 0
    df = df_designers.merge(df_customers, how='outer')
    return df


if __name__ == '__main__':
    #display_best_match_designer('alf')
    df_designers = pd.read_csv('data/designer_features.csv')
    list = df_designers['designer_name'].to_list()
    for i in list:
        display_best_match_designer(f'{i}')
        print('\n')
