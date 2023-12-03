import os.path
import time

from data_to_table import data_to_excel

if __name__ == '__main__':
    root_path = os.path.join('/', 'home', 'cyxxqeq', 'PycharmProjects', 'ActParser')
    paths = ['АЗН', 'АН', 'ДЖ']
    pdf_paths = [os.path.join('documents', path) for path in paths]
    docx_paths = [os.path.join('documents', path, '2015_ворд') for path in paths]
    start = time.time()

    data_to_excel(
        os.path.join('documents', 'single_test'),
        os.path.join('results', 'single_test.xlsx'),
        'VDS',
        log=True,
        is_docx=False
    )

    # data_to_excel(
    #     os.path.join('documents', 'ВДС'),
    #     os.path.join('results', 'vds_result.xlsx'),
    #     'VDS',
    #     log=True,
    #     is_docx=False
    # )

    # data_to_excel(
    #     os.path.join('documents', 'fix_vds'),
    #     os.path.join('results', 'fix_vds.xlsx'),
    #     'VDS',
    #     log=True,
    #     is_docx=False
    # )

    # for path, name in zip(pdf_paths, paths):
    #     data_to_excel(
    #         path,
    #         os.path.join('results', f'{name}.xlsx'),
    #         'HES',
    #         log=True,
    #         is_docx=False
    #     )
    # for path, name in zip(docx_paths, paths):
    #     data_to_excel(
    #         path,
    #         os.path.join('results', f'{name}_docx.xlsx'),
    #         'HES',
    #         log=True,
    #         is_docx=True
    #     )
    end = time.time()
    print('execute time: ', end - start)
