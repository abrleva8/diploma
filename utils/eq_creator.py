from itertools import combinations_with_replacement

import pandas as pd


def get_linear(size: int, add_y: bool = False) -> str:
    li_res = [f'a{i + 1}*x{i + 1}' for i in range(size)]
    return add_y * 'y = ' + 'a0+' + '+'.join(li_res)


def get_quad(size: int, add_y: bool = False) -> str:
    li_params = [f'x{i + 1}' for i in range(size)]
    pairs = map(lambda x: f'a{x[0] + size + 1}*{x[1][0]}*{x[1][1]}',
                enumerate((combinations_with_replacement(li_params, 2))))
    return add_y * 'y = ' + get_linear(size) + '+' + '+'.join(pairs)


def pars_eq(text: str) -> tuple[bool, list[str]]:
    text = text.replace(' ', '')
    eq = text.split('=')[-1]
    params = eq.split('+')
    fit_intercept = 'a0' in params
    params = [el for el in params if 'x' in el]
    params = list(map(lambda x: '*'.join(x.split('*')[1:]), params))
    return fit_intercept, params


def drop_a(mult: str) -> str:
    ind = mult.find('*')
    if ind != -1:
        mult = mult[ind + 1:]
    else:
        mult = ''
    return mult


def get_new_x(df: pd.DataFrame, text: str) -> pd.DataFrame:
    # df.to_csv('fragment.csv', index=False)
    new_columns = df.columns[2:].str.split(', ')
    d = {}
    for column in new_columns:
        d[column[1]] = column[0] + ', ' + column[1]

    new_keys = list(map(drop_a, text.split('+')))
    new_keys = list(filter(lambda x: True if x else False, new_keys))

    new_X = pd.DataFrame()
    for key in new_keys:
        if d.get(key, None) in df.columns:
            new_X[key] = df[d[key]]
        else:
            x = key.split('*')
            # new_X[key] = new_X[x[0]] * new_X[x[1]]
            new_X[key] = df[d[x[1].strip()]] * df[d[x[1].strip()]]

    return new_X
