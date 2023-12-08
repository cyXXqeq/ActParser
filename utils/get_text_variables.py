from copy import copy

from act_variables import *


def get_variables(act_kind: str, is_docx: bool = False):
    if act_kind == 'VDS':
        column, data_fields, data_get_functions = copy(COLUMNS_VDS), copy(DATA_FIELDS_VDS), copy(DATA_GET_FUNCTIONS_VDS)
    elif act_kind == 'RBM':
        column, data_fields, data_get_functions = copy(COLUMNS_VDS_RBM), copy(DATA_FIELDS_VDS_RBM), copy(DATA_GET_FUNCTIONS_VDS_RBM)
    elif act_kind == 'HES':
        column, data_fields, data_get_functions = copy(COLUMNS_HES), copy(DATA_FIELDS_HES), copy(DATA_GET_FUNCTIONS_HES)
    else:
        raise AttributeError('act_kind must be "VDS" or "RBM" or "HES"')

    if is_docx:
        for _ in range(2):
            column.pop(1)
            data_fields.pop(1)
            data_get_functions.pop(1)

    return column, data_fields, data_get_functions
