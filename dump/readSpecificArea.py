#!/usr/bin/env python
# -*- coding: utf-8 -*-

import binascii
import nfc
import time

# 学生証のサービスコード
service_code = 0x100B


def on_startup(targets):
    for target in targets:
        # nanaco
        # target.sensf_req = bytearray.fromhex("0004c70000")
        # pasmo
        target.sensf_req = bytearray.fromhex("008AC30000")
    return targets


def on_connect_nfc(tag):
    # タグのIDなどを出力する
    # print tag

    if isinstance(tag, nfc.tag.tt3.Type3Tag):
        try:
            print(binascii.hexlify(tag.idm).decode())
            sc = nfc.tag.tt3.ServiceCode(
                service_code >> 6, service_code & 0x3f)
            bc = [
                nfc.tag.tt3.BlockCode(0, service=0),
                nfc.tag.tt3.BlockCode(7, service=0),
                nfc.tag.tt3.BlockCode(8, service=0),
                nfc.tag.tt3.BlockCode(9, service=0)]
            data = tag.read_without_encryption([sc], bc)
            print(data)
        except Exception as e:
            print("error: %s" % e)
    else:
        print("error: tag isn't Type3Tag")


def main():
    clf = nfc.ContactlessFrontend('usb')
    while True:
        clf.connect(
            rdwr={
                'targets': ['212F'],
                'on-startup': on_startup,
                'on-connect': on_connect_nfc
            })
        time.sleep(3)


if __name__ == "__main__":
    main()
