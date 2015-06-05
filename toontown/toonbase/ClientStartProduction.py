#!/usr/bin/env python2
import json
import os
import requests
from pandac.PandaModules import *


username = os.environ['ttiUsername']
password = os.environ['ttiPassword']
distribution = ConfigVariableString('distribution', 'dev').getValue()

accountServerEndpoint = ConfigVariableString(
    'account-server-endpoint',
    'https://toontowninfinite.com/api/').getValue()
request = requests.post(
    accountServerEndpoint + 'login/',
    data={'username': username, 'password': password, 'distribution': distribution})

try:
    response = json.loads(request.text)
except ValueError:
    print "Couldn't verify account credentials."
else:
    if not response['success']:
        print response['result']
    else:
        os.environ['TTI_PLAYCOOKIE'] = response['cookie']

        # Start the game:
        import toontown.toonbase.ClientStart
