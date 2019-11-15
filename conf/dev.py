from conf.base import *

LOG_PATH = os.path.join('/tmp', PROJECT_NAME)
DATA_PATH = os.path.join('/data', PROJECT_NAME)
LOGGING['handlers']['file']['filename'] = os.path.join(LOG_PATH, 'dylan-daily.log')

HDFS = {

}

DATABASES = {

}
