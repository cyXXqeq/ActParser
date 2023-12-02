import time
from os.path import join as path_join

from act_variables import COLUMNS_VDS, DATA_FIELDS_VDS, DATA_GET_FUNCTIONS_VDS, COLUMNS_HES, DATA_FIELDS_HES, \
    DATA_GET_FUNCTIONS_HES
from data_from_pdf import get_data_from_pdf
from data_from_pdf_table import get_data_from_pdf_table


def data_to_excel(
        dir_path: str,
        table_path: str,
        act_kind: str,
        log: bool = False,
        is_docx: bool = False
) -> None:
    """

    :param dir_path: путь к директории с актами
    :param table_path: путь к итоговой таблице (результату)
    :param act_kind: VDS or HES
    :param log: вывод логов
    :param is_docx: docx file if True else pdf file
    """

    if act_kind == 'VDS':
        columns = COLUMNS_VDS
        data_fields = DATA_FIELDS_VDS
        data_get_functions = DATA_GET_FUNCTIONS_VDS

    elif act_kind == 'HES':
        columns = COLUMNS_HES
        data_fields = DATA_FIELDS_HES
        data_get_functions = DATA_GET_FUNCTIONS_HES

    else:
        raise AttributeError("act_kind must be 'VDS' or 'HES'")

    text_data = get_data_from_pdf(
        dir_path,
        columns,
        data_fields,
        data_get_functions,
        act_kind,
        log=log,
        is_docx=is_docx
    )
    if not is_docx:
        table_data = get_data_from_pdf_table(dir_path, log=log)
        text_data = text_data.join(table_data)

    text_data.to_excel(table_path)


if __name__ == '__main__':
    # start1 = time.time()
    # data_to_excel(
    #     path_join('/', 'home', 'cyxxqeq', 'Data4ActParser', 'ВДС_Размеченные_акты'),
    #     path_join('/', 'home', 'cyxxqeq', 'PycharmProjects', 'ActParser', 'results', 'labeled_result.xlsx')
    # )
    # end1 = time.time()

    # start2 = time.time()
    # data_to_excel(
    #     path_join('/', 'home', 'cyxxqeq', 'Data4ActParser', 'test'),
    #     path_join('/', 'home', 'cyxxqeq', 'PycharmProjects', 'ActParser', 'results', 'result.xlsx'),
    #     COLUMNS_VDS,
    #     DATA_FIELDS_VDS,
    #     DATA_GET_FUNCTIONS_VDS,
    #     'VDS',
    #     log=True
    # )
    # end2 = time.time()

    data_to_excel(
        path_join('documents', 'single_test'),
        path_join('/', 'home', 'cyxxqeq', 'PycharmProjects', 'ActParser', 'results', 'single_test.xlsx'),
        COLUMNS_HES,
        DATA_FIELDS_HES,
        DATA_GET_FUNCTIONS_HES,
        'HES',
        log=True
    )

    # test zone
    # start_test = time.time()
    # data_to_excel(
    #     path_join('/', 'home', 'cyxxqeq', 'Data4ActParser', 'test'),
    #     path_join('/', 'home', 'cyxxqeq', 'PycharmProjects', 'ActParser', 'results', 'test_result.xlsx'),
    #     log=True
    # )
    # print(time.time() - start_test)

    # print(f'Время выполнения на размеченных актах: {int(end1 - start1)} секунд')
    # print(f'Время выполнения на всех актах: {int(end2 - start2)} секунд')
