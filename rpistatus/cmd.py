#!/usr/bin/python
# -*- coding: UTF-8 -*-
# created: 19.06.2018
# author:  TOS

import logging
import subprocess
import socket
import os

log = logging.getLogger(__name__)

def vcgencmd(*args):
    return subprocess.check_output(('vcgencmd',)+args)

def camera():
    txt = vcgencmd('get_camera')
    data = dict(info.split('=') for info in txt.split(' '))
    return {k:int(v.strip()) for k, v in data.items()}

def memory():
    data = dict([vcgencmd('get_mem',arg).split('=') for arg in ['arm','gpu']])
    return {k:int(v.strip().rstrip('M')) for k, v in data.items()}

def clock():
    data = {arg:vcgencmd('measure_clock',arg).split('=')[-1] for arg in 'arm, core, h264, isp, v3d, uart, pwm, emmc, pixel, vec, hdmi, dpi'.split(', ')}
    return {k:int(v.strip()) for k, v in data.items()}

def voltage():
    data = {arg:vcgencmd('measure_volts',arg).split('=')[-1].strip('\n') for arg in 'core, sdram_c, sdram_i, sdram_p'.split(', ')}
    return {k:float(v.strip('V')) for k, v in data.items()}

def temperature():
    txt = vcgencmd('measure_temp')
    return {'core': float(txt.split('=')[-1].strip().rstrip("'C"))}

def config():
    txt = vcgencmd('get_config','int')
    data = dict(info.strip('\n').split('=') for info in txt.rstrip('\n').split('\n'))
    return {k:int(v.strip(), 0) for k, v in data.items()}

def ipadress():
    with open(os.devnull, 'w') as devnull:
        ip = subprocess.check_output(['curl','https://api.ipify.org'], stderr=devnull)
    return ip

def hostname():
    return socket.gethostname()