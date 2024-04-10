import utils
import os
import time
import pandas as pd
import objects

# Globals
YEAR = 2016
MONTH = 'Enero'
tribunals = objects.TRIBUNALS
file_cases = '../Outputs/metadata_'+str(YEAR)+'_'+MONTH+'.csv'
file_details = '../Outputs/metadata_details_'+str(YEAR)+'_'+MONTH+'.csv'
file_historia = '../Outputs/historia_'+str(YEAR)+'_'+MONTH+'.csv'
file_litigantes = '../Outputs/litigantes_'+str(YEAR)+'_'+MONTH+'.csv'
download_path = objects.DOWNLOAD_PATH+str(YEAR)+'/'+MONTH+'/'

# Start time
start = time.time()

# Deleting all files in downloads folder
utils.reset_directory(download_path)

try:
    # Navigation
    driver = utils.get_driver(YEAR, MONTH)
    utils.start(driver)
    utils.query_page(driver)
    utils.query_by_date(driver)

    # Completed progress
    if os.path.exists(file_cases):
        df = pd.read_csv(file_cases, encoding='latin1')
        completed_tribunals = list(df['Tribunal'].unique())[:-1]
    else:
        completed_tribunals = []

    for tribunal in tribunals:

        if tribunal in completed_tribunals:
            print('Data from tribunal '+tribunal+' already completed. Moving on...')
            continue

        # Query parameters
        print('Getting data from tribunal '+tribunal)
        utils.define_date_parameters(driver, YEAR, MONTH, 1)
        utils.define_competencia(driver, objects.COMPETENCIA)
        utils.define_corte(driver, objects.CORTE)
        utils.define_tribunal(driver, tribunal)

        # Execute search
        utils.execute_search(driver)

        # Number of cases and pages
        total_cases = utils.get_total_cases(driver)
        total_pages = utils.get_total_pages(total_cases)

        # Getting data
        utils.get_data(driver,
                       total_pages,
                       objects.COMPETENCIA,
                       objects.CORTE,
                       tribunal,
                       file_cases,
                       file_details,
                       file_historia,
                       file_litigantes)
except:
    driver.quit()
    raise

driver.quit()
end = time.time()
print('Finished!')
print('This took ' + str(round(end-start)) + ' seconds')
