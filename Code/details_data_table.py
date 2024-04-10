import sys
import os

sys.path.insert(0,'../utils')
sys.path.insert(0,'./utils')
import utils
import objects

# Locals
MONTH = sys.argv[1]
YEAR = int(sys.argv[2])
TRIBUNAL = sys.argv[3].replace('-', ' ')
file_master = '../Outputs/master/master_'+str(YEAR)+'_'+MONTH+'_'+TRIBUNAL+'.csv'
file_details = '../Outputs/details/details_'+str(YEAR)+'_'+MONTH+'_'+TRIBUNAL+'.csv'
file_historia = '../Outputs/historia/historia_'+str(YEAR)+'_'+MONTH+'_'+TRIBUNAL+'.csv'
file_litigantes = '../Outputs/litigantes/litigantes_'+str(YEAR)+'_'+MONTH+'_'+TRIBUNAL+'.csv'

try:
    # Navigation
    print('Getting data for: '+str(YEAR)+' '+MONTH+' '+TRIBUNAL)
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

    # Data
    utils.get_details_data(driver,
                           total_pages,
                           objects.COMPETENCIA,
                           objects.CORTE,
                           TRIBUNAL,
                           file_master,
                           file_details,
                           file_historia,
                           file_litigantes)

except:
    driver.quit()
    raise

driver.quit()
print("Finished getting data for: "+str(YEAR)+' '+MONTH+' '+TRIBUNAL)
