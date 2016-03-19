import configparser
from os.path import expanduser

def parse_file ():
    config = configparser.ConfigParser()
    confFile = expanduser ("~") + '/.kpd.conf'
    try:
        config.readfp (open (confFile))
    except:
        print ('Create a config file kpd.conf')
        exit (1)

    values = config.items ('main')
    for tupl in values:
        if 'database' in tupl:
            dbLocation = tupl[1]
        elif 'use_compression' in tupl:
            compressionBool = tupl[1]

    yield dbLocation
    yield compressionBool
