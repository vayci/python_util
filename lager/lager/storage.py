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


import oss2
from itertools import islice
from . import helper


# In AWS CloudFront Distribution:
# Origin Settings: Restrict Bucket Access: Yes
#                  Grant Read Permissions on Bucket: Yes
# Default Cache Behavior Settings: Restrict Viewer Access (Use Signed URLs or Signed Cookies): Yes


MAX_FILES = int(2**31-1)


class Storage(helper.KeyNameMixin):
    def _get_key_prefix(self, name_tuple_prefix):
        return helper.get_key_name(self.server_name, name_tuple_prefix+type(name_tuple_prefix)(('',)))

    def _get_name_tuple(self, key_name):
        return helper.get_name_tuple(self.server_name, key_name)

    def list_file(self, name_tuple_prefix, max_files=None):
        raise NotImplementedError('list() is not implemented')

    def delete_file(self, name_tuple):
        raise NotImplementedError('delete_file() is not implemented')

    def copy_file(self, src_name_tuple, dst_name_tuple):
        raise NotImplementedError('copy_file() is not implemented')

    def upload_file(self, name_tuple, fp, content_type=None, size=None):
        raise NotImplementedError('upload_file() is not implemented')

    def download_file(self, name_tuple, fp):
        raise NotImplementedError('download_file() is not implemented')

    def set_file_access_control(self, name_tuple, is_public):
        raise NotImplementedError('set_file_access_control() is not implemented')

    def get_file_info(self, name_tuple):
        raise NotImplementedError('get_file_info() is not implemented')

    def generate_url(self, name_tuple, duration, method='GET'):
        raise NotImplementedError('generate_url() is not implemented')

class AliYunOssStorage(Storage):
    def __init__(self, server_name, bucket_name, endpoint, oss_access_key_id=None, oss_secret_access_key=None):
            super(AliYunOssStorage, self).__init__(server_name)
            self.auth = oss2.Auth(oss_access_key_id,oss_secret_access_key)
            self.bucket = oss2.Bucket(self.auth, endpoint, bucket_name)

    def list_file(self, name_tuple_prefix, max_files=None):
        path_prefix = self._get_key_prefix(name_tuple_prefix)
        for obj in islice(oss2.ObjectIteratorV2(self.bucket), 1):
            print(obj.key)
        if max_files is None:
            iter = oss2.ObjectIteratorV2(self.bucket, prefix=path_prefix)
        else:
            iter = islice(oss2.ObjectIteratorV2(self.bucket, prefix=path_prefix), max_files)
        return map(lambda obj: self._get_name_tuple(obj.key), iter)
        

    def delete_file(self, name_tuple):
        path = self._get_key_name_origin(name_tuple)
        exist = self.bucket.object_exists(path)
        if exist:
            self.bucket.delete_object(path)
            return True
        else:
            return False                  

    def copy_file(self, src_name_tuple, dst_name_tuple):
        src_path = self._get_key_name_origin(src_name_tuple)
        dst_path = self._get_key_name_origin(dst_name_tuple)
        exist = self.bucket.object_exists(src_path)
        if exist:
            self.bucket.copy_object(self.bucket.bucket_name,src_path,dst_path)
            return True
        else:
            return False      

    def upload_file(self, name_tuple, fp, content_type=None, size=None):
        path = self._get_key_name_origin(name_tuple)
        print(path)
        exist = self.bucket.object_exists(path)
        if exist:
            return False
        else:
            self.bucket.put_object(path,fp)
            return True      

    def download_file(self, name_tuple, fp):
        path = self._get_key_name_origin(name_tuple)
        exist = self.bucket.object_exists(path)
        if exist:
            fp = self.bucket.get_object(path).read()
            return True
        else:
            return False

    def set_file_access_control(self, name_tuple, is_public):
        path = self._get_key_name_origin(name_tuple)
        exist = self.bucket.object_exists(path)
        if exist:
            if bool(is_public):
                self.bucket.put_object_acl(path, oss2.OBJECT_ACL_PUBLIC_READ)
            else:
                self.bucket.put_object_acl(path, oss2.OBJECT_ACL_PRIVATE)
            return True
        else:
            return False

    def get_file_info(self, name_tuple):
        path = self._get_key_name_origin(name_tuple)
        exist = self.bucket.object_exists(path)
        if exist:
            meta = self.bucket.head_object(path)
            info = {
                'content_type': meta.headers['Content-Type'],
                'size': meta.headers['Content-Length'],
                'checksum': {
                    'md5': meta.headers['ETag'],
                },
            }
        else:
            info = None
        return info

    def generate_url(self, name_tuple, duration, method='GET'):
        if method == 'GET':
            path = self._get_key_name_origin(name_tuple)
            return self.bucket.sign_url('GET',path,600)
        else:
            raise ValueError('cloudfront support GET method only')

def new_storage(storage_class_name, *args, **kwargs):
    storage_class = eval(storage_class_name)
    if issubclass(storage_class, Storage):
        return storage_class(*args, **kwargs)
    else:
        raise TypeError('must be name of subclass of Storage')

