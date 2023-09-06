from configparser import ConfigParser
import os


def get(filename='app.config', section='DATABASE'):
    base_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(base_dir + filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db