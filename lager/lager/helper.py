#!/usr/bin/env python
# -*- coding: utf-8 -*-


################################################################################
#
# lager - an easy tool to access cloud storage service,
#         and also, abstract and simplify corresponding API
# Copyright (C) 2015-present Himawari Tachibana <fieliapm@gmail.com>
#
# This file is part of lager
#
# lager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################


import time
import base64
import binascii
import json

def get_key_name(server_name, name_tuple):
    return '/'.join(type(name_tuple)((server_name,))+name_tuple).encode('utf-8')

def get_key_name_origin(server_name, name_tuple):
    return '/'.join(type(name_tuple)((server_name,))+name_tuple)

def get_name_tuple(server_name, key_name):
    internal_name_tuple = tuple(key_name.split('/'))
    if internal_name_tuple[0] == server_name:
        return internal_name_tuple[1:]
    else:
        raise ValueError('key name is not belong to server name')


def expire_time(duration):
    return int(time.time())+duration


def base64_to_hex(base64data):
    return binascii.hexlify(base64.standard_b64decode(base64data)).decode('utf-8')


class KeyNameMixin(object):
    def _get_key_name(self, name_tuple):
        return get_key_name(self.server_name, name_tuple)
    def _get_key_name_origin(self, name_tuple):
        return get_key_name_origin(self.server_name, name_tuple)
    def __init__(self, server_name):
        self.server_name = server_name


