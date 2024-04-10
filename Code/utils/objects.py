# Globals
ATTEMPTS = 5
URL_FAILED_MESSAGE = 'URL could not be retrieved'
NO_EBOOK = ['1º Juzgado Civil de Santiago_C-30167-2015 P_ebook.pdf']
COMPETENCIA = 'Civil'
CORTE = 'C.A. de Santiago'
ENCODING = 'latin1'

# Paths
CHROMEDRIVER_PATH = 'C:/WBG/chromedriver/chromedriver.exe'
DOWNLOAD_PATH = 'C:/WBG/Temp downloads/'
PDF_PATH = '../Outputs/pdf/'

# URL and XPaths
BASE_URL = 'https://oficinajudicialvirtual.pjud.cl/home/index.php'
QUERY_XPATH = '//*[@id="myDropdown3"]/a[1]'
DATE_XPATH = '//*[@id="nuevocolapsador"]/li[3]'
DATE_FROM_XPATH = '//*[@id="fecDesde"]'
PREVIOUS_MONTH_XPATH = '//*[@id="ui-datepicker-div"]/div/a[1]'
DATE_TO_XPATH = '//*[@id="fecHasta"]'
YEAR_XPATH = '//*[@id="ui-datepicker-div"]/div/div/select'
COMPETENCIA_XPATH = '//*[@id="fecCompetencia"]'
SEARCH_XPATH = '//*[@id="btnConConsultaFec"]'
TOTAL_XPATH = '//*[@id="verDetalleFecha"]/tr[101]/td/nav/div'
CLOSE_BUTTON_XPATH = '//*[@id="modalDetalleCivil"]/div/div/div[3]/button'
DETAILS_TABLE_XPATH = '//*[@id="modalDetalleCivil"]/div/div/div[2]/div/div[1]'
HISTORIA_TABLE_XPATH = '//*[@id="historiaCiv"]/div/div/table/tbody'
LITIGANTES_TABLE_XPATH = '//*[@id="litigantesCiv"]/div/div/table/tbody'
LITIGANTES_XPATH = '//*[@id="modalDetalleCivil"]/div/div/div[2]/div/div[3]/ul/li[2]/a'
EBOOK_XPATH = '//*[@id="boton"]/form/a'
ACEPTAR_BUTTON_XPATH = '/html/body/div[12]/div[7]/div/button'
INVISIBLE_LAYER_XPATH = '//*[@id="modalDetalleCivil"]'

# Categories to iterate through:
YEARS = [2016, 2017]
MONTHS = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
          'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
DAYS_BY_MONTH = {
    2016: {
        'Enero': 30,
        'Febrero': 28,
        'Marzo': 30,
        'Abril': 29,
        'Mayo': 30,
        'Junio': 29,
        'Julio': 30,
        'Agosto': 30,
        'Septiembre': 29,
        'Octubre': 30,
        'Noviembre': 29,
        'Diciembre': 30
    },
    2017: {
        'Enero': 30,
        'Febrero': 27,
        'Marzo': 30,
        'Abril': 29,
        'Mayo': 30,
        'Junio': 29,
        'Julio': 30,
        'Agosto': 30,
        'Septiembre': 29,
        'Octubre': 30,
        'Noviembre': 29,
        'Diciembre': 30
    }

}

TRIBUNALS = [
    '1º Juzgado Civil de Santiago',
    '2º Juzgado Civil de Santiago',
    '3º Juzgado Civil de Santiago',
    '4º Juzgado Civil de Santiago',
    '5º Juzgado Civil de Santiago',
    '6º Juzgado Civil de Santiago',
    '7º Juzgado Civil de Santiago',
    '8º Juzgado Civil de Santiago',
    '9º Juzgado Civil de Santiago',
    '10º Juzgado Civil de Santiago',
    '11º Juzgado Civil de Santiago',
    '12º Juzgado Civil de Santiago',
    '13º Juzgado Civil de Santiago',
    '14º Juzgado Civil de Santiago',
    '15º Juzgado Civil de Santiago',
    '16º Juzgado Civil de Santiago',
    '17º Juzgado Civil de Santiago',
    '18º Juzgado Civil de Santiago',
    '19º Juzgado Civil de Santiago',
    '20º Juzgado Civil de Santiago',
    '21º Juzgado Civil de Santiago',
    '22º Juzgado Civil de Santiago',
    '23º Juzgado Civil de Santiago',
    '24º Juzgado Civil de Santiago',
    '25º Juzgado Civil de Santiago',
    '26º Juzgado Civil de Santiago',
    '27º Juzgado Civil de Santiago',
    '28º Juzgado Civil de Santiago',
    '29º Juzgado Civil de Santiago',
    '30º Juzgado Civil de Santiago',
    'Juzgado de Letras de Colina'
]

# Column names
METADATA_COLS = [
    'Competencia',
    'Corte',
    'Tribunal',
    'Page',
    'Rol',
    'Fecha',
    'Caratulado'
]
DETAILS_COLS = [
    'Historia Causa Cuaderno',
    'ROL',
    'F. Ing',
    'unlabeled_text',
    'Est. Adm.',
    'Proc.',
    'Ubicacion',
    'Estado Proc.',
    'Etapa',
    'Tribunal',
    'Texto Demanda',
    'Anexos de la causa',
    'Certificado de envio',
    'Ebook',
    'Causa Origen',
    'Tribunal Origen'
]
HISTORIA_COLS = [
    'Tribunal',
    'ROL',
    'Folio',
    'Doc.',
    'Anexo',
    'Etapa',
    'Tramite',
    'Desc. Tramite',
    'Fec. Tramite',
    'Foja',
    'Georref.'
]
LITIGANTES_COLS = [
    'Tribunal',
    'ROL',
    'Participante',
    'Rut',
    'Persona',
    'Nombre o Razon Social'
]
TOTAL_CASES_COLS = [
    'Year',
    'Month',
    'Tribunal',
    'Total cases',
    'Number of pages'
]
