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

from . import helper
import oss2


# sign url offline
class SignUrl(helper.KeyNameMixin):
    def generate_download_url(self, name_tuple, duration):
        raise NotImplementedError('generate_download_url() is not implemented')

    def public_download_url(self, name_tuple):
        raise NotImplementedError('public_download_url() is not implemented')

class AliYunOssStorageSignUrl(SignUrl):
    def __init__(self, server_name, bucket_name, endpoint, oss_access_key_id, oss_secret_access_key):
        super(AliYunOssStorageSignUrl, self).__init__(server_name)

        self.auth = oss2.Auth(oss_access_key_id,oss_secret_access_key)
        self.bucket = oss2.Bucket(self.auth, endpoint, bucket_name)
        self.bucket_name = bucket_name
        self.endpoint = endpoint

    def generate_download_url(self, name_tuple, duration):
        path = self._get_key_name_origin(name_tuple)
        return self.bucket.sign_url('GET',path,600)

    def public_download_url(self, name_tuple):
        path = self._get_key_name_origin(name_tuple)
        return 'https://'+self.bucket_name+'.'+self.endpoint.replace('https://','')+'/'+path


def new_sign_url(sign_url_class_name, *args, **kwargs):
    sign_url_class = eval(sign_url_class_name)
    if issubclass(sign_url_class, SignUrl):
        return sign_url_class(*args, **kwargs)
    else:
        raise TypeError('must be name of subclass of SignUrl')
