import sys
import os
import pandas as pd

sys.path.insert(0,'../utils')
sys.path.insert(0,'./utils')
import utils
import objects

# Locals
MONTH = sys.argv[1]
YEAR = int(sys.argv[2])
TRIBUNAL = sys.argv[3].replace('-', ' ')
file_master = '../Outputs/master/master_'+str(YEAR)+'_'+MONTH+'_'+TRIBUNAL+'.csv'
file_total_cases = '../Outputs/master/total_cases.csv'

try:
    # Navigation
    driver = utils.get_driver(YEAR, MONTH)
    utils.start(driver)
    utils.query_page(driver)
    utils.query_by_date(driver)

    # Query
    utils.define_date_parameters(driver, YEAR, MONTH, 1)
    utils.define_competencia(driver, objects.COMPETENCIA)
    utils.define_corte(driver, objects.CORTE)
    utils.define_tribunal(driver, TRIBUNAL)

    # Execute search
    utils.execute_search(driver)

    # Number of cases and pages
    total_cases = utils.get_total_cases(driver)
    total_pages = utils.get_total_pages(total_cases)
    if os.path.exists(file_total_cases):
        total_cases_df = pd.read_csv(file_total_cases, encoding='latin1')
        row = total_cases_df[(total_cases_df['Year']==YEAR) & \
                             (total_cases_df['Month']==MONTH) & \
                             (total_cases_df['Tribunal']==TRIBUNAL)]
        if len(row) == 0:
            not_in_total_cases = True
        else:
            not_in_total_cases = False
    else:
        not_in_total_cases = True

    if not_in_total_cases:
        rows = [[YEAR, MONTH, TRIBUNAL, total_cases, total_pages]]
        utils.add_rows_to_csv(file=file_total_cases,
                              columns=objects.TOTAL_CASES_COLS,
                              rows=rows)

    # Data
    utils.get_master_data(driver,
                          total_pages,
                          objects.COMPETENCIA,
                          objects.CORTE,
                          TRIBUNAL,
                          file_master)

except:
    driver.quit()
    raise

driver.quit()
