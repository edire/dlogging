
import os
import logging
import socket
import datetime as dt


directory = os.path.join(os.getcwd(), 'logs')
log_level = 20
clear_files = True


class HostnameFilter(logging.Filter):
    hostname = socket.gethostname()
    def filter(self, record):
        record.hostname = HostnameFilter.hostname
        return True


def LogDirectory(directory_new):
    global directory
    global clear_files
    directory = os.path.join(directory_new, 'logs')
    clear_files = True


def LogLevel(level_new):
    global log_level
    log_level = level_new


def NewLogger(logger_name, use_cd=False, file_name='python.log', backup_count=45):
    global clear_files
    if use_cd:
        LogDirectory(os.path.dirname(logger_name))
    if not os.path.exists(directory):
        os.makedirs(directory)

    logger_name = os.path.basename(logger_name)
    logger = logging.getLogger(logger_name)

    if backup_count != 'inf':
        dte_format = '%Y%m%d'
        backup_dte = dt.date.today() - dt.timedelta(days=backup_count)
        if clear_files == True:
            for file in (os.listdir(directory)):
                if file[-len(file_name):] == file_name:
                    dte, nme = file.split('_', 1)
                    dte = dt.datetime.strptime(dte, dte_format).date()
                    if dte < backup_dte:
                        os.remove(os.path.join(directory, file))
            clear_files = False
        file_date = dt.date.today().strftime(dte_format)
        file_name = f'{file_date}_{file_name}'

    log_file =  os.path.join(directory, file_name)
    logger.setLevel(log_level)

    file_handler = logging.FileHandler(log_file)
    file_handler.addFilter(HostnameFilter())
    file_formatter = logging.Formatter('%(asctime)s: %(hostname)s: %(name)s: %(levelname)s: %(message)s')
    file_handler.setFormatter(file_formatter)

    stream_handler = logging.StreamHandler()
    stream_formatter = logging.Formatter('%(asctime)s: %(name)s: %(levelname)s: %(message)s')
    stream_handler.setFormatter(stream_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


def SetLoggingLevel(log_level):
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        logger.setLevel(log_level)




#NOTSET 0
#DEBUG 10
#INFO 20
#WARNING 30
#ERROR 40
#CRITICAL 50
