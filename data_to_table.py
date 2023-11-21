import time
from os.path import join as path_join

from data_from_pdf import get_data_from_pdf
from data_from_pdf_table import get_data_from_pdf_table


def data_to_excel(dir_path: str, table_path: str, log: bool = False, is_docx: bool = False) -> None:
    """

    :param dir_path: путь к директории с актами
    :param table_path: путь к итоговой таблице (результату)
    :param log: вывод логов
    :param is_docx: docx file if True else pdf file
    """
    text_data = get_data_from_pdf(dir_path, log=log, is_docx=is_docx)
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

    start2 = time.time()
    data_to_excel(
        path_join('/', 'home', 'cyxxqeq', 'Data4ActParser', 'ВДС'),
        path_join('/', 'home', 'cyxxqeq', 'PycharmProjects', 'ActParser', 'results', 'result.xlsx'),
        log=True
    )
    end2 = time.time()

    # test zone
    # start_test = time.time()
    # data_to_excel(
    #     path_join('/', 'home', 'cyxxqeq', 'Data4ActParser', 'test'),
    #     path_join('/', 'home', 'cyxxqeq', 'PycharmProjects', 'ActParser', 'results', 'test_result.xlsx'),
    #     log=True
    # )
    # print(time.time() - start_test)

    # print(f'Время выполнения на размеченных актах: {int(end1 - start1)} секунд')
    print(f'Время выполнения на всех актах: {int(end2 - start2)} секунд')
