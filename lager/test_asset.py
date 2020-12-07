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


import sys

import lager


SERVER_NAME = 'test'


def test_storage(storage_name, storage, content_type=None):
    print('[%s] delete status: %s' % (storage_name, repr(storage.delete_file(('t1',u'エグゼリカ01.jpg')))))
    print('[%s] delete status: %s' % (storage_name, repr(storage.delete_file(('t2',u'エグゼリカ02.jpg')))))
    with open('trigger_heart_exelica_wallpaper.jpg', 'rb') as fp:
        print('[%s] upload status: %s' % (storage_name, repr(storage.upload_file(('t1',u'エグゼリカ01.jpg'), fp, content_type=content_type))))
    with open('t1.jpg', 'wb') as fp:
        print('[%s] download status: %s' % (storage_name, repr(storage.download_file(('t1',u'エグゼリカ01.jpg'), fp))))
    print('[%s] copy status: %s' % (storage_name, repr(storage.copy_file(('t1',u'エグゼリカ01.jpg'), ('t2',u'エグゼリカ02.jpg')))))
    print('[%s] acl private: %s' % (storage_name, repr(storage.set_file_access_control(('t1',u'エグゼリカ01.jpg'), False))))
    print('[%s] info: %s' % (storage_name, repr(storage.get_file_info(('t1',u'エグゼリカ01.jpg')))))
    print('[%s] url: %s' % (storage_name, storage.generate_url(('t1',u'エグゼリカ01.jpg'), 60*1)))
    print('[%s] acl public: %s' % (storage_name, repr(storage.set_file_access_control(('t2',u'エグゼリカ02.jpg'), True))))
    print('[%s] info: %s' % (storage_name, repr(storage.get_file_info(('t2',u'エグゼリカ02.jpg')))))
    print('[%s] url: %s' % (storage_name, storage.generate_url(('t2',u'エグゼリカ02.jpg'), 60*1)))

    print('[%s] delete status: %s' % (storage_name, repr(storage.delete_file(['t2','takame01.jpg']))))
    print('[%s] delete status: %s' % (storage_name, repr(storage.delete_file(['t1','takame02.jpg']))))
    with open('takame.jpg', 'rb') as fp:
        print('[%s] upload status: %s' % (storage_name, repr(storage.upload_file(['t2','takame01.jpg'], fp, content_type=content_type))))
    with open('t2.jpg', 'wb') as fp:
        print('[%s] download status: %s' % (storage_name, repr(storage.download_file(['t2','takame01.jpg'], fp))))
    print('[%s] copy status: %s' % (storage_name, repr(storage.copy_file(['t2','takame01.jpg'], ['t1','takame02.jpg']))))
    print('[%s] acl private: %s' % (storage_name, repr(storage.set_file_access_control(['t2','takame01.jpg'], False))))
    print('[%s] info: %s' % (storage_name, repr(storage.get_file_info(['t2','takame01.jpg']))))
    print('[%s] url: %s' % (storage_name, storage.generate_url(['t2','takame01.jpg'], 60*1)))
    print('[%s] acl public: %s' % (storage_name, repr(storage.set_file_access_control(['t1','takame02.jpg'], True))))
    print('[%s] info: %s' % (storage_name, repr(storage.get_file_info(['t1','takame02.jpg']))))
    print('[%s] url: %s' % (storage_name, storage.generate_url(['t1','takame02.jpg'], 60*1)))

    print('[%s] invalid acl: %s' % (storage_name, repr(storage.set_file_access_control(['t3',u'エグゼリカ01.jpg'], False))))
    print('[%s] invalid info: %s' % (storage_name, repr(storage.get_file_info(['t3',u'エグゼリカ01.jpg']))))
    print('[%s] invalid url: %s' % (storage_name, str(storage.generate_url(['t3',u'エグゼリカ01.jpg'], 60*1))))

    print('[%s] list all file: %s' % (storage_name, repr(list(storage.list_file(())))))
    print('[%s] list one file: %s' % (storage_name, repr(list(storage.list_file((), max_files=1)))))
    print('[%s] list all file: %s' % (storage_name, repr(list(storage.list_file(('t1',))))))
    print('[%s] list one file: %s' % (storage_name, repr(list(storage.list_file(('t1',), max_files=1)))))
    print('[%s] list all file: %s' % (storage_name, repr(list(storage.list_file(['t2'])))))
    print('[%s] list one file: %s' % (storage_name, repr(list(storage.list_file(['t2'], max_files=1)))))
    print('')


def test_sign_url(sign_url_name, sign_url):
    print('[%s] private url: %s' % (sign_url_name, sign_url.generate_download_url(['t1',u'エグゼリカ01.jpg'], 60*1)))
    print('[%s] public url: %s' % (sign_url_name, sign_url.public_download_url(['t2',u'エグゼリカ02.jpg'])))
    print('[%s] private url: %s' % (sign_url_name, sign_url.generate_download_url(['t2','takame01.jpg'], 60*1)))
    print('[%s] public url: %s' % (sign_url_name, sign_url.public_download_url(['t1','takame02.jpg'])))
    print('[%s] invalid url: %s' % (sign_url_name, str(sign_url.generate_download_url(['t3',u'エグゼリカ01.jpg'], 60*1))))
    print('')

def test_oss():
    cf = lager.new_storage_from_config('AliYunOssStorage', 'voez_server', None)
    test_storage('oss', cf)


def main(argv=sys.argv[:]):
    test_oss()
    return 0


if __name__ == '__main__':
    sys.exit(main())

