import time
from os.path import join as path_join

from data_from_pdf import get_data_from_pdf
from data_from_pdf_table import get_data_from_pdf_table


def data_to_excel(dir_path: str, table_path: str) -> None:
    """

    :param dir_path: путь к директории с актами
    :param table_path: путь к итоговой таблице (результату)
    """

    table_data = get_data_from_pdf_table(dir_path)
    text_data = get_data_from_pdf(dir_path)
    df = text_data.join(table_data)

    df.to_excel(table_path)


if __name__ == '__main__':
    start = time.time()
    data_to_excel(
        path_join('/', 'home', 'cyxxqeq', 'Data4ActParser', 'ВДС_Размеченные_акты'),
        path_join('/', 'home', 'cyxxqeq', 'PycharmProjects', 'ActParser', 'results', 'result.xlsx')
    )
    print(f'Время выполнения: {int(time.time() - start)} секунд')
