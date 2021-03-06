#!/usr/bin/python

# MIT License
#
# Copyright (c) 2016 Daily Actie
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Author: Quan Pan <quanpan302@hotmail.com>
# License: MIT License
# Create: 2016-12-02

# 0 --py:Success::
# 1 --py:Warning::
# 2 --py:Error::
# --py:Start::['+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+']::
# --py:End::  ['+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+']::
# --py:Test:: 'test'

"""
Description, delft3d_waq

:param arg:
:return:
"""


import numpy as np


def delft3dWAQ(variable, numObj):
    """delft3d WAQ return zeros.
    """
    # estimator/delft3d_waq.py
    # if _Nobj==1:
    #     f1 = 0.0
    #     return np.array([f1]).tolist()
    # if _Nobj==2:
    #     f1 = 0.0
    #     f2 = 0.0
    #     return np.array([f1, f2]).tolist()
    # if _Nobj>=3:
    #     f1 = 0.0
    #     f2 = 0.0
    #     return np.array([f1, f2]).tolist()
    rtnarray = [f/10.0 for f in range(numObj)]
    return np.array(rtnarray).tolist()
