import os.path
import time

from data_to_table import data_to_excel

if __name__ == '__main__':
    root_path = os.path.join('/', 'home', 'cyxxqeq', 'PycharmProjects', 'ActParser')
    start = time.time()
    data_to_excel(
        os.path.join('documents', 'single_test'),
        os.path.join('results', 'single_test_result.xlsx'),
        log=True
    )
    end = time.time()
    print('execute time: ', end - start)
