import multiprocessing
import random
import os
import sys
import pandas as pd

sys.path.insert(0,'./utils')
import objects

# Locals
MONTHS = objects.MONTHS
YEARS = objects.YEARS
TRIBUNALS = []
for tribunal in objects.TRIBUNALS:
    TRIBUNALS.append(tribunal.replace(' ', '-'))
script = 'details_data_table.py'

# Checking that scripts are not finalized
df = pd.read_csv('../Progress reports/progress_details data tables.csv', encoding=objects.ENCODING)
df = df[df['finished']==1]
finished = list(df['year'].astype(str)+df['month']+df['Tribunal'])
print('Tribunals completed:', len(finished))

# Combinations of locals values
combinations = []
for month in MONTHS:
    for year in YEARS:
        for tribunal in TRIBUNALS:

            instance = str(year)+month+tribunal.replace('-', ' ')
            if instance not in finished:
                combinations.append(' '.join([script, month, str(year), tribunal]))

# Randomly sorting
random.shuffle(combinations)
print('Number of tribunals to obtain data from:', len(combinations))

# Execution functions
def execute(process):
    os.system(f'python {process}')

def main():
    process_pool = multiprocessing.Pool(processes=6)
    process_pool.map(execute, combinations)

if __name__ == '__main__':
    main()
