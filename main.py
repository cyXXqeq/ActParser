import os.path
import time

from act_variables import DATA_FIELDS_HES, COLUMNS_HES, DATA_GET_FUNCTIONS_HES
from data_to_table import data_to_excel

if __name__ == '__main__':
    root_path = os.path.join('/', 'home', 'cyxxqeq', 'PycharmProjects', 'ActParser')
    paths = ['АЗН', 'АН', 'ДЖ']
    pdf_paths = [os.path.join('documents', path) for path in paths]
    docx_paths = [os.path.join('documents', path, '2015_ворд') for path in paths]
    start = time.time()
    for path, name in zip(pdf_paths, paths):
        data_to_excel(
            path,
            os.path.join('results', f'{name}.xlsx'),
            COLUMNS_HES,
            DATA_FIELDS_HES,
            DATA_GET_FUNCTIONS_HES,
            'HES',
            log=True,
            is_docx=False
        )
    for path, name in zip(docx_paths, paths):
        data_to_excel(
            path,
            os.path.join('results', f'{name}_docx.xlsx'),
            COLUMNS_HES,
            DATA_FIELDS_HES,
            DATA_GET_FUNCTIONS_HES,
            'HES',
            log=True,
            is_docx=True
        )
    end = time.time()
    print('execute time: ', end - start)
