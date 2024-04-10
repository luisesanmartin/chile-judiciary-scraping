# Libraries
import objects
import pandas as pd
import time
import math
import json
import os
import shutil
import csv
import zipfile
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import \
    StaleElementReferenceException, \
    ElementClickInterceptedException, \
    ElementNotInteractableException, \
    NoSuchElementException, \
    UnexpectedAlertPresentException, \
    NoSuchWindowException


# Functions
def get_driver(year, month):

    settings = {
       "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": "",
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }
    prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
    prefs2 = {'savefile.default_directory' : objects.DOWNLOAD_PATH+str(year)+'/'+month+'/'}
    prefs.update(prefs2)

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--kiosk-printing')

    driver = webdriver.Chrome(options=options, executable_path=objects.CHROMEDRIVER_PATH)

    return driver

def reset_directory(path):

    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

    return True

def start(driver):

    driver.get(objects.BASE_URL)
    driver.maximize_window()
    time.sleep(5)

    return True

def query_page(driver):

    button = find_by_visible_text(driver, 'Consulta causas')[0]
    click_element(button)
    time.sleep(8)

    return True

def query_by_date(driver):

    button = find_by_xpath(driver, objects.DATE_XPATH)
    click_element(button)
    time.sleep(1)

    return True

def define_date_parameters(driver, year, month, day):

    # Path for PDFs
    global PDF_PATH
    PDF_PATH = objects.PDF_PATH+str(year)+'/'+month+'/'
    os.makedirs(PDF_PATH, exist_ok=True)
    global DOWNLOADS_PATH
    DOWNLOADS_PATH = objects.DOWNLOAD_PATH+str(year)+'/'+month+'/'
    os.makedirs(DOWNLOADS_PATH, exist_ok=True)

    # Open date box - "Desde"
    button = find_by_xpath(driver, objects.DATE_FROM_XPATH)
    click_element(button)
    time.sleep(1)

    # Select month
    current_month = driver.find_element_by_class_name('ui-datepicker-month').text
    while current_month != month:
        button = find_by_xpath(driver, objects.PREVIOUS_MONTH_XPATH)
        click_element(button)
        current_month = driver.find_element_by_class_name('ui-datepicker-month').text

    # Select year
    select_year = Select(driver.find_element_by_class_name('ui-datepicker-year'))
    select_year.select_by_visible_text(str(year))
    time.sleep(1)

    # Day selection
    for item in driver.find_elements_by_tag_name('a'):
        text = get_text(item)
        if text == str(day):
            click_element(item)
            break
    time.sleep(1)

    # Open date box - "Hasta"
    button = find_by_xpath(driver, objects.DATE_TO_XPATH)
    click_element(button)
    time.sleep(1)

    # Select month
    current_month = driver.find_element_by_class_name('ui-datepicker-month').text
    while current_month != month:
        button = find_by_xpath(driver, objects.PREVIOUS_MONTH_XPATH)
        click_element(button)
        current_month = driver.find_element_by_class_name('ui-datepicker-month').text

    # Select year
    select_year = Select(driver.find_element_by_class_name('ui-datepicker-year'))
    select_year.select_by_visible_text(str(year))
    time.sleep(1)

    # Day selection
    for item in driver.find_elements_by_tag_name('a'):
        text = get_text(item)
        if text == str(day+objects.DAYS_BY_MONTH[year][month]):
            click_element(item)
    time.sleep(1)

    return True

def define_competencia(driver, competencia):

    select_competencia = Select(driver.find_element_by_id('fecCompetencia'))
    select_competencia.select_by_visible_text(competencia)
    time.sleep(1)

    return True

def define_corte(driver, corte):

    select_corte = Select(driver.find_element_by_id('corteFec'))
    select_corte.select_by_visible_text(corte)
    time.sleep(1)

    return True

def define_tribunal(driver, tribunal):

    try:
        select_tribunal = Select(driver.find_element_by_id('fecTribunal'))
        select_tribunal.select_by_visible_text(tribunal)
        time.sleep(1)
    except NoSuchElementException:
        time.sleep(3)
        select_tribunal = Select(driver.find_element_by_id('fecTribunal'))
        select_tribunal.select_by_visible_text(tribunal)
        time.sleep(1)

    return True

def execute_search(driver):

    button = find_by_xpath(driver, objects.SEARCH_XPATH)
    click_element(button)
    time.sleep(5)

    return True

def get_total_cases(driver):

    total_registros = find_by_xpath(driver, objects.TOTAL_XPATH)
    text = get_text(total_registros)
    total_cases = text.split(':')[1]

    return int(total_cases)

def get_total_pages(total_cases):

    total_pages = math.ceil(total_cases / 100)

    return total_pages

def add_rows_to_csv(file, columns, rows):

    if not os.path.exists(file):
        with open(file, 'w', newline='', encoding=objects.ENCODING) as f:
            wr = csv.writer(f, dialect='excel')
            wr.writerows([columns])

    with open(file, 'a', newline='', encoding=objects.ENCODING) as f:
        wr = csv.writer(f, dialect='excel')
        wr.writerows(rows)

    return True

def create_compressed_file(folders, years, months):

    for folder in folders:
        files = os.listdir('../Outputs/'+folder)
        zip_file = '../Outputs/'+folder+'.zip'

        counter = 0
        for filename in files:

            if filename == 'placeholder.md':
                continue

            _, year, month, _ = filename.split('_')

            if int(year) in years and month in months:

                if counter == 0:
                    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        zipf.write('../Outputs/'+folder+'/'+filename, filename)
                else:
                    with zipfile.ZipFile(zip_file, 'a', zipfile.ZIP_DEFLATED) as zipf:
                        zipf.write('../Outputs/'+folder+'/'+filename, filename)
                counter += 1

    return True

def get_metadata_from_table(driver,
                            competencia,
                            corte,
                            tribunal,
                            page,
                            file):

    cases = driver.find_element_by_id('verDetalleFecha').find_elements_by_tag_name('tr')
    cases = cases[:-1] # the last row is not a case
    rows = []
    for case in cases:
        data = case.find_elements_by_tag_name('td')
        data = data[1:4] # keeping only non-repeated info
        row = [competencia, corte, tribunal, page]
        for data_point in data:
            text = get_text(data_point)
            row.append(text)
        rows.append(row)

    add_rows_to_csv(file, objects.METADATA_COLS, rows)

    return True

def get_master_data(driver,
                    total_pages,
                    competencia,
                    corte,
                    tribunal,
                    file_master):

    # Completed data:
    if os.path.exists(file_master):
        df = pd.read_csv(file_master, encoding=objects.ENCODING)
        pages_in_metadata = list(df[df['Tribunal']==tribunal]['Page'].unique())
    else:
        pages_in_metadata = []

    # Iterating through the rest of pages
    for i in range(1, total_pages+1):

        if i > 1:
            pages = driver.find_elements_by_class_name('page-link')
            for page in pages:
                text = get_text(page)
                if text == str(i):
                    click_element(page)
                    time.sleep(5)
                    break

        if i in pages_in_metadata:
            print('Page '+str(i)+' already completed. Moving on...')
            continue
        else:
            print("Getting data from page", i)
            get_metadata_from_table(driver,
                                    competencia,
                                    corte,
                                    tribunal,
                                    i,
                                    file_master)

    return True

def get_details_data(driver,
                     total_pages,
                     competencia,
                     corte,
                     tribunal,
                     file_master,
                     file_details,
                     file_historia,
                     file_litigantes
                     ):

    # Iterating through every page:
    for i in range(1, total_pages+1):

        if i > 1:
            pages = driver.find_elements_by_class_name('page-link')
            for page in pages:
                text = get_text(page)
                if text == str(i):
                    click_element(page)
                    time.sleep(8)
                    break

        print("\tGetting data from page", i)
        get_details(driver,
                    file_master,
                    file_details,
                    file_historia,
                    file_litigantes,
                    tribunal)

    return True

def get_details(driver,
                file_master,
                file_details,
                file_historia,
                file_litigantes,
                tribunal):

    # Getting the cases in this page
    cases = driver.find_element_by_id('verDetalleFecha').find_elements_by_tag_name('tr')
    cases = cases[:-1] # the last row is not a case

    # List of completed cases
    if os.path.exists(file_details):
        df = pd.read_csv(file_details, encoding=objects.ENCODING)
        df['Tribunal'] = df['Tribunal'].astype(str).apply(lambda x: x.replace('Âº', 'º'))
        rols = df[df['Tribunal']==tribunal]['ROL'].apply(lambda x: x.split()[0])
        tribunals = df[df['Tribunal']==tribunal]['Tribunal']
        completed_cases = list(zip(tribunals, rols))
    else:
        completed_cases = []

    # Cases in master data
    df_master = pd.read_csv(file_master, encoding=objects.ENCODING)
    master_rols = list(df_master['Rol'])

    # Getting the data for every case
    for i, case in enumerate(cases):

        # Checking that the case is not already finalized
        case_id = get_tribunal_rol(case)

        if case_id in completed_cases:
            print('\t\tCase: '+case_id[1]+' from '+case_id[0]+' already finished. Moving on...')
            continue

        # Checking that the case is indeed part of the master data
        elif case_id[1] not in master_rols:
            print('\t\tCase: '+case_id[1]+' from '+case_id[0]+' is not in the master table. Moving on...')
            continue

        # Opening details popup and getting the details data
        got_details = open_popup_and_get_data(driver,
                                              case,
                                              file_details,
                                              file_historia,
                                              file_litigantes)

        if got_details is False: # we try again

                # Opening details popup
                print("\t\tOoops! Getting the metadata details didn't work...")
                print('\t\ttrying again...')
                got_details = open_popup_and_get_data(driver,
                                                      case,
                                                      file_details,
                                                      file_historia,
                                                      file_litigantes)

        if got_details is False:

            raise ValueError('\t\tGetting the metadata details did not work')

    return True

def open_popup_and_get_data(driver, case, file_details, file_historia, file_litigantes):

    # Opening details popup
    magnifying_glass = case.find_elements_by_tag_name('td')[0].\
        find_element_by_class_name('toggle-modal')
    click_element(magnifying_glass)
    time.sleep(2)

    # Checking that case is not reserved
    if is_reserved(driver):
        case_id = get_tribunal_rol(case)
        row = ['CAUSA RESERVADA', case_id[1], '', '', '', '', '', '', '', case_id[0], '', '', '', '', '', '']
        add_rows_to_csv(file_details, objects.DETAILS_COLS, [row])

        button = find_by_xpath(driver, objects.ACEPTAR_BUTTON_XPATH)
        click_element(button)
        time.sleep(2)

        # Remove invisible layer
        layer = driver.find_element_by_xpath(objects.INVISIBLE_LAYER_XPATH)
        layer.click()

        return 'Case is reserved'

    else: # regular cases

        # Getting details
        got_details = get_case_details2(driver, file_details, file_historia, file_litigantes)

        # Closing popup
        close_button = find_by_xpath(driver, objects.CLOSE_BUTTON_XPATH)
        click_element(close_button)
        time.sleep(2)

        return got_details

def is_reserved(driver):

    elements = find_by_visible_text(driver, 'Causa Reservada.', n_tries=1)

    if len(elements) == 2:
        return True
    elif len(elements) == 1:
        return False
    else:
        '\tCheck what happened inside is_reserved()'
        return False

def get_case_details2(driver,
                      file_details,
                      file_historia,
                      file_litigantes,
                      all_cuadernos=False):

    cuadernos = get_cuadernos(driver)

    # Details of the first cuaderno
    row = get_case_metadata_details(driver, cuadernos[0], get_ebook=False)
    if row == False or row == ['']: # we will reload the details page
        return False

    # Historia and litigantes
    tribunal = row[9]
    rol = row[1]
    got_historia = get_historia(driver, file_historia, tribunal, rol, get_pdf=False)
    got_litigantes = get_litigantes(driver, file_litigantes, tribunal, rol)

    # Saving case details
    add_rows_to_csv(file_details, objects.DETAILS_COLS, [row])

    return True

def get_case_metadata_details(driver, cuaderno, get_ebook=True):

    table = find_by_xpath(driver, objects.DETAILS_TABLE_XPATH)
    data_points = find_by_tag_name(table, 'td')

    row = [cuaderno]
    for i, data_point in enumerate(data_points):

        text = get_text(data_point)
        if text == '':
            continue
        elif i == 2: # unlabeled_text is here
            row.append(text)

        elif i == 12 and get_ebook: # Ebook is here
            tribunal = row[9]
            rol = row[1]
            name = tribunal + '_' + \
                   rol + '_ebook.pdf'

            filename = PDF_PATH + name
            if not os.path.exists(filename):
                button = find_by_xpath(data_point, objects.EBOOK_XPATH)
                downloaded = print_pdf_from_button(driver, button, filename)

                if downloaded is False:
                    pdf_url = retrieve_url_from_attributes(data_point)
                    downloaded = open_new_tab_and_print(driver, pdf_url, filename)

                if downloaded is True:
                    row.append(name)
                else:
                    text = 'PDF file could not be downloaded'
                    print('\t'+text+': '+name)
                    row.append(text)

            else:
                print('\t'+'File '+name+' already downloaded')
                row.append(name)

        else:
            row.append(text.split(':')[1].strip())

    return row

def get_litigantes(driver, file_litigantes, tribunal, rol):

    # click on litigantes
    button = find_by_xpath(driver, objects.LITIGANTES_XPATH)
    click_element(button)
    time.sleep(1)

    # Get data in table
    table = find_by_xpath(driver, objects.LITIGANTES_TABLE_XPATH)
    table_rows = find_by_tag_name(table, 'tr')

    rows = []
    for table_row in table_rows:
        row = [tribunal, rol]
        data_points = find_by_tag_name(table_row, 'td')
        for data_point in data_points:
            text = get_text(data_point)
            row.append(text)
        rows.append(row)

    # Saving litigantes
    add_rows_to_csv(file_litigantes, objects.LITIGANTES_COLS, rows)

    return True

def get_historia(driver, file_historia, tribunal, rol, get_pdf=True):

    table = find_by_xpath(driver, objects.HISTORIA_TABLE_XPATH)
    table_rows = find_by_tag_name(table, 'tr')

    rows = []
    for table_row in table_rows:
        row = [tribunal, rol]
        data_points = find_by_tag_name(table_row, 'td')
        for i, data_point in enumerate(data_points):

            text = get_text(data_point)
            if i == 1 and text != '' and get_pdf:

                # Getting PDF URL
                folio = row[-1]
                name = tribunal + '_' + \
                       rol + '_' + \
                       folio + '.pdf'
                filename = PDF_PATH + name
                downloaded = print_pdf_from_button(driver, data_point, filename)

                if not downloaded:
                    pdf_url = retrieve_url_from_attributes(data_point)
                    downloaded = open_new_tab_and_print(driver, pdf_url, filename)

                if downloaded:
                    text = name
                else:
                    text = 'PDF file could not be downloaded'
                    print('\t'+text+': '+name)

            row.append(text)

        rows.append(row)

    # Saving case history
    add_rows_to_csv(file_historia, objects.HISTORIA_COLS, rows)

    return True

def get_data(driver,
             total_pages,
             competencia,
             corte,
             tribunal,
             file_master,
             file_details,
             file_historia,
             file_litigantes):

    # Completed data:
    if os.path.exists(file_cases):
        df = pd.read_csv(file_cases, encoding=objects.ENCODING)
        pages_in_metadata = list(df[df['Tribunal']==tribunal]['Page'].unique())
        completed_pages = pages_in_metadata[:-1]
    else:
        completed_pages = []
        pages_in_metadata = []

    # Getting metadata in page 1
    if 1 not in completed_pages:
        print("Getting data from page 1")
        if 1 not in pages_in_metadata:
            get_metadata_from_table(driver, competencia, corte, tribunal, 1, file_cases)
        get_details(driver, file_details, file_historia, file_litigantes, tribunal)
    else:
        print('Page 1 already completed. Moving on...')

    # Iterating through the rest of pages
    for i in range(2, total_pages+1):

        pages = driver.find_elements_by_class_name('page-link')
        for page in pages:
            text = get_text(page)
            if text == str(i):
                click_element(page)
                time.sleep(5)
                break
        if i in completed_pages:
            print('Page '+str(i)+' already completed. Moving on...')
            continue
        else:
            print("Getting data from page", i)
            if i not in pages_in_metadata:
                get_metadata_from_table(driver, competencia, corte, tribunal, i, file_cases)
            get_details(driver, file_details, file_historia, file_litigantes, tribunal)

    return True

def get_tribunal_rol(case):

    row = case.find_elements_by_tag_name('td')
    tribunal, rol = row[4].text, row[1].text

    return tribunal, rol

def get_case_details(driver,
                     file_details,
                     file_historia,
                     file_litigantes,
                     all_cuadernos=False):

    cuadernos = get_cuadernos(driver)

    # Details of the first cuaderno
    row = get_case_metadata_details(driver, cuadernos[0], get_ebook=True)
    if row == False or row == ['']: # we will reload the details page
        return False

    # Historia and litigantes
    tribunal = row[9]
    rol = row[1]
    got_historia = get_historia(driver, file_historia, tribunal, rol, get_pdf=False)
    got_litigantes = get_litigantes(driver, file_litigantes, tribunal, rol)

    # Saving case details
    if not os.path.exists(file_details):
        with open(file_details, 'w', newline='') as f:
            wr = csv.writer(f, dialect='excel')
            wr.writerows([objects.DETAILS_COLS])
    with open(file_details, 'a', newline='') as f:
        wr = csv.writer(f, dialect='excel')
        wr.writerows([row])

    # Rest of cuadernos
    if len(cuadernos) > 1 and all_cuadernos:
        for cuaderno in cuadernos[1:]:

            dropdown = Select(driver.find_element_by_id('selCuaderno'))
            try:
                dropdown.select_by_visible_text(cuaderno)
            except NoSuchElementException as e:
                print("\tSelecting a cuaderno didn't work...")
                print('\tText in cuadernos:')
                for cuaderno in cuadernos:
                    print('\t\t'+cuaderno.text)
                raise e
            time.sleep(1)

            row = get_case_metadata_details(driver, cuaderno)
            if row == False: # we'll try again
                return False
            #if len(row) == len(df.columns) - 1:
                #row += ['']

            with open(file_details, 'a', newline='') as f:
                wr = csv.writer(f, dialect='excel')
                wr.writerows([row])

            # note that we're not getting historia nor litigantes
            # in the rest of cuadernos

    return True

def open_new_tab_and_print(driver, url, filename):

    # Opening new tab
    driver.execute_script('''window.open("'''+url+'''","_blank");''')
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[1])

    # Printing
    printed = print_download(driver, filename)
    if printed:
        driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return True

def print_download(driver, filename, n_tries=objects.ATTEMPTS):

    '''
    Downloads a pdf file by printing it from Chrome's pdf viewer
    Note that this only works if the driver is set to print and
    download automatically, otherwise it will ask to manually indicate
    the pdf path in a new prompt.
    Reference: https://stackoverflow.com/a/52486757/11214568
    '''

    name = filename.split('/')[-1]

    try:
        driver.execute_script('window.print();')
        time.sleep(1)
    except UnexpectedAlertPresentException:
        #print('\tFile: '+name+' could not be downloaded')
        return False

    downloaded_files = os.listdir(DOWNLOADS_PATH)
    attempts = 0

    while downloaded_files == [] and attempts <= n_tries:
        time.sleep(3)
        downloaded_files = os.listdir(DOWNLOADS_PATH)
        attempts += 1

    if downloaded_files == []:
        print('\tFile: '+name+' could not be downloaded')
        return False

    filename_download = max([DOWNLOADS_PATH + f for f in downloaded_files],
                        key=os.path.getctime)
    shutil.move(filename_download, filename)
    print('\tSaved file: '+name)

    return True

def print_pdf_from_button(driver, button, filename):

    '''
    Uses Chrome's print function to downloads a pdf from the pdf viewer
    button is the html link/button that opens the pdf in a new tab.
    '''

    click = click_element(button)

    if click:
        time.sleep(1)

        try:

            driver.switch_to.window(driver.window_handles[1])
            print_download(driver, filename)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            return True

        except IndexError:
            driver.switch_to.window(driver.window_handles[0])
            return False

        except (NoSuchWindowException, UnexpectedAlertPresentException):
            driver.switch_to.window(driver.window_handles[0])
            return "PDF couldn't be obtained"

    else:
        return False

def retrieve_url_from_attributes(button):

    '''
    Retrieves the URL of a PDF button by getting it from the
    HTML attributes.
    Note: this is a less accurate method than getting it from
    the new tab.
    '''

    prefix = find_by_tag_name(button, 'form')[0].get_attribute('action')
    suffix1 = find_by_tag_name(button, 'input')[0].get_attribute('name')
    suffix2 = find_by_tag_name(button, 'input')[0].get_attribute('value')

    url = prefix + '?' + suffix1 + '=' + suffix2

    return url

def retrieve_url_from_new_tab(driver, button):

    '''
    Retrieves the URL of a new tab that opens
    after clicking on a button
    Ref: https://paveltashev.medium.com/python-and-selenium-open-focus-and-close-a-new-tab-4cc606b73388
    '''

    click_element(button)
    time.sleep(1)

    try:
        driver.switch_to.window(driver.window_handles[1])
        url = driver.current_url
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except IndexError:
        url = objects.URL_FAILED_MESSAGE

    return url

def get_cuadernos(driver):

    cuadernos = []
    dropdown = driver.find_element_by_id('selCuaderno')
    options = dropdown.find_elements_by_tag_name('option')
    for option in options:
        text = get_text(option)
        cuadernos.append(text)

    return cuadernos

def get_text(element, n_tries=objects.ATTEMPTS):

    '''
    Attempts to get the text of an element at most n_tries times
    '''

    attempts = 0
    while attempts <= n_tries:

        try:
            text = element.text
            return text
        except StaleElementReferenceException:
            attempts += 1
            time.sleep(3)

    print('\tCould not get text in element')
    return 'Data point not retrieved'

def click_element(element, n_tries=objects.ATTEMPTS):

    '''
    Attempts to click on an element at most n_tries times
    '''

    attempts = 0
    while attempts <= n_tries:

        try:
            element.click()
            return True
        except ElementClickInterceptedException:
            attempts += 1
            time.sleep(3)
        except ElementNotInteractableException:
            attempts += 1
            time.sleep(3)
        except StaleElementReferenceException:
            attempts += 1
            time.sleep(3)

    raise ValueError('Could not click element')
    print('\tCould not click element')
    return False

def find_by_visible_text(driver, text, n_tries=objects.ATTEMPTS):

    attempts = 0
    while attempts <= n_tries:

        try:
            elements = driver.find_elements_by_xpath("//*[contains(text(), '"+text+"')]")
            return elements
        except NoSuchElementException:
            attempts += 1
            time.sleep(3)

    if n_tries > 1:
        print('\tCould not find the element with text: '+text)

    return False

def find_by_xpath(driver, xpath, n_tries=objects.ATTEMPTS):

    attempts = 0
    while attempts <= n_tries:

        try:
            element = driver.find_element_by_xpath(xpath)
            return element
        except NoSuchElementException:
            attempts += 1
            time.sleep(3)

    print('\tCould not find the element in '+xpath)
    return False

def find_by_tag_name(root_element, tag, n_tries=objects.ATTEMPTS):

    attempts = 0
    while attempts <= n_tries:

        try:
            element = root_element.find_elements_by_tag_name(tag)
            return element
        except StaleElementReferenceException:
            attempts += 1
            time.sleep(3)

    print('\tCould not find tag: '+tag)
    return False

def add_row(df, row):

    i = len(df)
    try:
        df.loc[i] = row
        return df
    except ValueError:
        print('\tColumns in df: '+str(len(df.columns)))
        print('\tValues in row: '+str(len(row)))
        print('\tValues:')
        for i, item in enumerate(row):
            print('\t\tItem '+str(i)+':'+item)
        #raise ValueError

    return False
