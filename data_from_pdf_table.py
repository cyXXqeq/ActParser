from os.path import join as path_join

from pandas import DataFrame
from pdf2docx import Converter


def is_mismatched(row):
    for i in row:
        if not i:
            return True
    return False


def get_resource_consumption(tables: list[list[list]]) -> DataFrame:
    """
    :param tables: Таблицы в формате списка матриц, где матрицы - это список списков
    :return: DataFrame с данными о материалах, пустой DataFrame, если данные не найдутся
    """

    start = 0
    df = DataFrame()

    # for table in tables:
    #     for row in table:
    #         print(row)
    #     print('\n')

    for i, table in enumerate(tables):
        if {'Материал (реагент)', 'Количество'}.issubset(table[0]):
            df = DataFrame(table, columns=table[0])
            start = i + 1
            break

    if not df.empty:
        df = df.drop(index=0)

        while start < len(tables):
            if len(tables[start][0]) == 9:
                for row in tables[start]:
                    if not is_mismatched(row):
                        df.loc[len(df)] = row
                start += 1
            else:
                break

        if not df.empty:
            df.columns = [column.replace(' ', '') for column in df.columns]
            # df = df.rename(columns={'Плотнос': 'Плотностьг/см3'})
            df = df.loc[:, ['Материал(реагент)', 'Плотностьг/см3', 'Количество']]
            df = df.replace([''], 'н/д')
            df = df.fillna(value='н/д')

    return df


def get_data_from_pdf_table(paths: list[str], log: bool = False):
    """

    :param paths: список путей к документам
    :param log: вывод логов
    :return: датафрейм с данными о материалах
    """

    result = []
    columns = []
    for i in range(1, 8):
        columns.append(f'Материал {i}')
        columns.append(f'Плотность материала {i}')
        columns.append(f'Количество материала {i}')
    df = DataFrame(columns=columns)

    for path in paths:
        print(f'[INFO] path: {path}')
        cv = Converter(path)
        tables = cv.extract_tables()
        cv.close()
        result.append(get_resource_consumption(tables))

    fails: list[str] = []

    for i, dataframe in enumerate(result):
        temp_row = []

        if not dataframe.empty:
            for row in dataframe.iterrows():
                temp_row += row[1].to_list()

            while len(temp_row) < 21:
                temp_row.append(None)

            df.loc[len(df)] = temp_row
        else:
            fails.append(paths[i])
            df.loc[len(df)] = ['н/д или п/д'] * 21

    if log:
        for fail in fails:
            print(f'[FAIL] {fail}')

    df = df.replace([''], 'н/д')
    df = df.fillna(value='н/д')

    return df


if __name__ == '__main__':
    get_data_from_pdf_table(path_join('documents', 'single_test'), log=True)
