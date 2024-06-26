from pathlib import Path


MAIN_DOC_URL = 'https://docs.python.org/3/'
BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
PEPS_DOC_URL = 'https://peps.python.org/'
EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
LOGS_DIRECTORY = 'logs'
LOG_FILENAME = 'parser.log'
RESULTS_DIRECTORY = 'results'
DEFAULT_ENCODING = 'utf-8'
PRETTY_MODE = 'pretty'
FILE_MODE = 'file'
WHATS_NEW_ENDPOINT = 'whatsnew/'
DOWNLOAD_ENDPOINT = 'download.html'
DOWNLOADS_DIR = 'downloads'
