from os import listdir
from os.path import join as path_join, isdir

from data_from_pdf_table import get_data_from_pdf_table
from data_from_text import get_data_from_text
from utils.clean_null_acts import clean_df
from utils.get_text_variables import get_variables
from utils.split_vds import split_vds_by_rbm


def data_to_excel(
        dir_path: str | list[str],
        table_path: str,
        act_kind: str,
        log: bool = False,
        is_docx: bool = False,
        check_rbm: bool = True
) -> None:
    """

    :param dir_path: путь к директории с актами
    :param table_path: путь к итоговой таблице (результату)
    :param act_kind: VDS or HES
    :param log: вывод логов
    :param is_docx: docx file if True else pdf file
    :param check_rbm: проверка наличия РБМ в ВДС
    """

    if isinstance(dir_path, str):
        paths = [path_join(dir_path, file) for file in listdir(dir_path)]
        paths = list(filter(lambda x: not isdir(x), paths))
    else:
        paths = dir_path

    if act_kind == 'VDS':
        if check_rbm:
            rbm, not_rbm = split_vds_by_rbm(paths)
            if rbm:
                data_to_excel(
                    rbm,
                    table_path.replace('.xlsx', '_rbm.xlsx'),
                    'RBM',
                    log,
                    is_docx,
                    False
                )
                if not_rbm:
                    data_to_excel(
                        not_rbm,
                        table_path.replace('.xlsx', '_not_rbm.xlsx'),
                        'VDS',
                        log,
                        is_docx,
                        False
                    )
                return

    columns, data_fields, data_get_functions = get_variables(act_kind, is_docx)

    print('[INFO] get data from text')
    text_data = get_data_from_text(
        paths,
        columns,
        data_fields,
        data_get_functions,
        act_kind,
        is_docx=is_docx
    )
    if not is_docx:
        print('[INFO] get data from pdf tables')
        table_data = get_data_from_pdf_table(paths, log=log)
        text_data = text_data.join(table_data)

    text_data = clean_df(text_data)
    text_data.to_excel(table_path)


if __name__ == '__main__':
    data_to_excel(
        path_join('documents', 'single_test'),
        path_join('/', 'home', 'cyxxqeq', 'PycharmProjects', 'ActParser', 'results', 'single_test.xlsx'),
        'HES',
        log=True
    )
