import multiprocessing
import os

ALL_PROCESSES = [
    'main_2016_01.py',
    'main_2016_02.py',
    'main_2016_03.py',
    'main_2016_04.py',
    'main_2016_05.py',
    'main_2016_06.py',
    'main_2016_07.py',
    'main_2016_08.py',
    'main_2016_09.py',
    'main_2016_10.py',
    'main_2016_11.py',
    'main_2016_12.py',
    'main_2017_01.py',
    'main_2017_02.py',
    'main_2017_03.py',
    'main_2017_04.py',
    'main_2017_05.py',
    'main_2017_06.py',
    'main_2017_07.py',
    'main_2017_08.py',
    'main_2017_09.py',
    'main_2017_10.py',
    'main_2017_11.py',
    'main_2017_12.py',
]
ALL_PROCESSES = ALL_PROCESSES * 400

def execute(process):
    os.system(f'python {process}')

def main():

    process_pool = multiprocessing.Pool(processes = 5)
    process_pool.map(execute, ALL_PROCESSES)

if __name__ == '__main__':
    main()
