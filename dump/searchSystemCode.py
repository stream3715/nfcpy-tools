import binascii
import time
import nfc
import datetime

#   Suica待ち受けの1サイクル秒
TIME_cycle = 1.0
#   Suica待ち受けの反応インターバル秒
TIME_interval = 0.2
#   タッチされてから次の待ち受けを開始するまで無効化する秒
TIME_wait = 3
target_req_pass = nfc.clf.RemoteTarget("212F")
#   0003(Suica)
target_req_pass.sensf_req = bytearray.fromhex("008AC30000")


def check_services(tag, start, n):
    services = [nfc.tag.tt3.ServiceCode(i >> 6, i & 0x3f)
                for i in range(start, start+n)]
    versions = tag.request_service(services)
    for i in range(n):
        if versions[i] == 0xffff:
            continue
        print((services[i], versions[i]))


def check_system(tag, system_code):
    idm, pmm = tag.polling(system_code=system_code)
    tag.idm, tag.pmm, tag.sys = idm, pmm, system_code
    print(tag)
    n = 32
    for i in range(0, 0x10000, n):
        check_services(tag, i, n)


def on_connect(tag):
    system_codes = tag.request_system_code()
    print(system_codes)
    for s in system_codes:
        check_system(tag, s)


def main():
    with nfc.ContactlessFrontend('usb') as clf:
        while(True):
            target_res = clf.sense(target_req_pass, iterations=int(
                TIME_cycle//TIME_interval)+1, interval=TIME_interval)

            if target_res:

                now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

                tag = nfc.tag.activate(clf, target_res)
                tag.sys = 3

                # IDmを取り出す
                idm = binascii.hexlify(tag.idm)
                pmm = binascii.hexlify(tag.pmm)

                print('Suica detected.')
                print('now        = ' + now)
                print('idm        = ' + idm.decode())
                print('pmm        = ' + pmm.decode())

                print('sleep ' + str(TIME_wait) + ' seconds')
                time.sleep(TIME_wait)
                print('Suica waiting...')


if __name__ == '__main__':
    main()
