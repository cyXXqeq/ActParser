from os import listdir
from os.path import join as path_join
from pandas import DataFrame
from pdf2docx import Converter


def get_resource_consumption(tables: list[list[list]]) -> DataFrame:
    """
    :param tables: Таблицы в формате списка матриц, где матрицы - это список списков
    :return: DataFrame с данными о материалах, пустой DataFrame, если данные не найдутся
    """

    start = 0
    df = DataFrame()

    for i, table in enumerate(tables):
        if {'Материал (реагент)', 'Количество'}.issubset(table[0]):
            df = DataFrame(table[1:], columns=table[0])
            start = i + 1
            break

    if not df.empty:
        while start < len(tables):
            if 'Стоимость работ, руб' not in tables[start][0]:
                for row in tables[start]:
                    df.loc[len(df)] = row
                start += 1
            else:
                break

        df = df.loc[:, ['Материал (реагент)', 'Плотно сть г/см3', 'Количество']]
        df = df.replace([''], 'н/д')
        df = df.fillna(value='н/д')

        return df


def get_data_from_pdf_table(dir_path):
    """

    :param dir_path:
    :return:
    """

    paths = [path_join(dir_path, file) for file in listdir(dir_path)]
    result = []
    columns = []
    for i in range(1, 8):
        columns.append(f'Материал {i}')
        columns.append(f'Плотность материала {i}')
        columns.append(f'Количество материала {i}')
    df = DataFrame(columns=columns)

    for path in paths:
        cv = Converter(path)
        tables = cv.extract_tables()
        cv.close()

        result.append(get_resource_consumption(tables))

    for dataframe in result:
        temp_row = []

        for row in dataframe.iterrows():
            temp_row += row[1].to_list()

        while len(temp_row) < 21:
            temp_row.append(None)

        df.loc[len(df)] = temp_row

    df = df.replace([''], 'н/д')
    df = df.fillna(value='н/д')

    return df


if __name__ == '__main__':
    get_data_from_pdf_table(path_join('/', 'home', 'cyxxqeq', 'Data4ActParser', 'ВДС_Размеченные_акты'))
