#!/usr/bin/python
# -*- coding: UTF-8 -*-
# created: 20.06.2018
# author:  TOS

import logging
import os

log = logging.getLogger(__name__)

def get_secret(name):
    if name not in os.environ:
        secret = open('run/secrets/{}'.format(name.lower()), 'r').read()
    else:
        secret = os.environ[name]
    return secret
