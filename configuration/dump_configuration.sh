#! /bin/bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

../../manage.py dumpdata superlachaise_api.AdminCommand superlachaise_api.Language superlachaise_api.Setting superlachaise_api.SuperLachaiseCategory superlachaise_api.SuperLachaiseLocalizedCategory superlachaise_api.SuperLachaiseOccupation > configuration.json
