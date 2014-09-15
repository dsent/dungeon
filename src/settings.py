from sys import argv

__author__ = 'dsent'

if len(argv) > 1:
    if argv[1] == 'en':
        _enc = 'en_US'
    elif argv[1] == 'ru':
        _enc = 'ru_RU'
else:
    _enc = None

SETTINGS = {
    'locale': _enc,  # Set to None for system default
    'encoding': 'UTF-8',  # Set to None for system default
}