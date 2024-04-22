from itertools import combinations_with_replacement


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
