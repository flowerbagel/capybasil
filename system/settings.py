#!/usr/bin/python3

### capybasil settings ###

CB_VERSION = '1.3.1'
CB_DEVMODE = True

if CB_DEVMODE == True:
    CB_PREFIX = 'capu '
    # dev token
    CB_TOKEN = 'TOKEN GOES HERE'
else:
    CB_PREFIX = 'capy '
    # normal token
    CB_TOKEN = 'TOKEN GOES HERE'


# people allowed to use admin commands
CB_OPERATORS = []

# servers trusted to use the "zabloing" command
CB_ZABLOING_TRUSTED = []

