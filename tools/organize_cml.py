#!/usr/bin/python

import sys
import os
from os.path import join
from subprocess import check_output

def fmt(msg, reset=True):
    """Replaces color annotations with ansi escape sequences"""
    global _ansi
    msg = msg.replace('@!', '@{boldon}')
    msg = msg.replace('@/', '@{italicson}')
    msg = msg.replace('@_', '@{ulon}')
    msg = msg.replace('@|', '@{reset}')
    t = ColorTemplate(msg)
    return t.substitute(_ansi) + (ansi('reset') if reset else '')


def test_colors():
    def cprint(msg):
        print(fmt(msg))

    cprint("| @{kf}Black      @|| @!@{kf}Black Bold")
    cprint("| @{rf}Red        @|| @!@{rf}Red Bold")
    cprint("| @{gf}Green      @|| @!@{gf}Green Bold")
    cprint("| @{yf}Yellow     @|| @!@{yf}Yellow Bold")
    cprint("| @{bf}Blue       @|| @!@{bf}Blue Bold")
    cprint("| @{pf}Purple     @|| @!@{pf}Purple Bold")
    cprint("| @{cf}Cyan       @|| @!@{cf}Cyan Bold")
	cprint("| White      | @!White Bold")