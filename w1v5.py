import os
import re
import ssl
import sys
import json
import time
import random
import string
import hashlib
import httpx
import threading
import requests
from urllib.parse import urlparse
from collections import defaultdict
from datetime import datetime
from pystyle import Colorate, Colors
from colorama import init
import paho.mqtt.client as mqtt

tnghia = "dep trai hon quoc vu"
tnghia_sinh_nhat = "29/3"
tnghia_que_quan = "Gia Lai - Quy Nhon"
tnghia_nghe_nghiep = "boss king messenger"
tnghia_tinh_cach = "de thuong anime cute"
tnghia_nha = "nha giau"
tnghia_tool = "tool free khong duoc ban"
tnghia_lien_he = "ib ad de mua tool hoac ho tro"
tnghia_danh_gia = "dep trai nhat lang"
tnghia_so_fan = "rat nhieu"
tnghia_idol = "chinh la tnghia"
tnghia_skill = "code gioi, dep trai, nha giau la du roi"
tnghia_note = "ai doc duoc dong nay thi tnghia chuc ban code khong bug"
 

import warnings
import urllib3
urllib3.disable_warnings()
warnings.filterwarnings('ignore')

init(autoreset=True)

khoa_in   = threading.Lock()
khoa_mqtt = threading.Lock()


def tnghia_huongdansudung():
    lam_sach_man_hinh()
    print("1. Tool by Ng Tan Nghia - anime cute - dep trai nha giau")
    print("2. Boss anh em king messenger")
    print("3. Ban mun mua tool hay can ho tro gi thi ib ad nhe")
    print("4. Tnghia dep trai nha giau - sinh ngay 29/3")
    print("5. Tnghia o Gia Lai - Quy Nhon")
    print("6. Tnghia de thuong")
    print("")
    print("HUONG DAN SU DUNG:")
    print("1. Nhap file cookie (vd: cookie.txt) - moi dong 1 cookie")
    print("2. Nhap delay cho tung cookie (giay)")
    print("3. Nhap ID box nhan tin")
    print("4. Nhap file ngon (vd: ngon.txt)")
    print("5. Gõ done de bat dau spam")
    print("")
    print("Lenh trong khi chay:")
    print("/addck  - them cookie moi (lay id box va file ngon cu)")
    print("/xoack [so] - xoa cookie theo so thu tu")
    print("")
    nhap = ""
    while nhap.lower() != "done":
        nhap = input("Nhap done de tiep tuc: ").strip()


def tnghiacheck():
    pass


def lam_sach_man_hinh():
    os.system('cls' if os.name == 'nt' else 'clear')


def hien_banner():
    lam_sach_man_hinh()
    banner = """
                                     /\\_____/\\
                                    /  o   o  \\
                                   ( ==  ^  == )
                                    )         (
                                   (           )
                                  ( (  )   (  ) )
                                 (__(__)___(__)__)
                               /                  \\
                              /   \u256d|\u3001              \\
                             |   (\u02da\u02ce \u30027             |
                             |    |\u3001\u02dc\u3075             |
                              \\   \u3058\u3057\u02cd,)           /
                               \\                  /
                                ~~~~~~~~~~~~~~~~~~
                         TOOL MESSENGER BY NG T\u1ea4N NGH\u0128A
    """
    print(Colorate.Horizontal(Colors.rainbow, banner))


def in_log(noi_dung):
    with khoa_in:
        print(f"[{time.strftime('%H:%M:%S')}] {noi_dung}")


def tao_ssl():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode    = ssl.CERT_NONE
    return ctx


def tao_offline_threading_id():
    ret        = int(time.time() * 1000)
    value      = random.randint(0, 4294967295)
    binary_str = format(value, "022b")[-22:]
    msgs       = bin(ret)[2:] + binary_str
    return str(int(msgs, 2))


def tao_session_id():
    return random.randint(1, 2 ** 53)


def tao_client_id():
    return (
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' +
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=4)) + '-' +
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=4)) + '-' +
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=4)) + '-' +
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    )


def json_gon(obj):
    return json.dumps(obj, separators=(',', ':'))


def trich_xuat_user(cookie):
    try:
        m = re.search(r'c_user=(\d+)', cookie)
        if m:
            return m.group(1)
    except Exception:
        pass
    return None


def trich_xuat_i_user(cookie):
    try:
        m = re.search(r'i_user=(\d+)', cookie)
        if m:
            return m.group(1)
    except Exception:
        pass
    return None


def lay_fb_dtsg(cookie):
    try:
        ssl_ctx = tao_ssl()
        headers = {
            'accept':                    'text/html,application/xhtml+xml,*/*;q=0.8',
            'accept-language':           'en-US,en;q=0.9,vi;q=0.8',
            'cookie':                    cookie,
            'user-agent':                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'sec-fetch-dest':            'document',
            'sec-fetch-mode':            'navigate',
            'sec-fetch-site':            'none',
            'sec-fetch-user':            '?1',
            'upgrade-insecure-requests': '1'
        }
        with httpx.Client(verify=ssl_ctx, timeout=30.0, http2=True, follow_redirects=True) as client:
            for url in ['https://www.facebook.com/', 'https://mbasic.facebook.com/', 'https://m.facebook.com/', 'https://touch.facebook.com/']:
                try:
                    r = client.get(url, headers=headers)
                    if r.status_code == 200:
                        for pat in [
                            r'"DTSGInitialData",\[\],{"token":"([^"]+)"',
                            r'"token":"([^"]+)"',
                            r'name="fb_dtsg"\s+value="([^"]+)"',
                            r'name="fb_dtsg" value="([^"]+)"',
                            r'{"name":"fb_dtsg","value":"([^"]+)"',
                        ]:
                            m = re.search(pat, r.text)
                            if m:
                                return m.group(1)
                except Exception:
                    continue
    except Exception:
        pass
    return None


def lay_thong_tin(cookie, user_id, fb_dtsg, session=None):
    try:
        if not session:
            session = requests.Session()
        headers = {
            'Accept':           '*/*',
            'Accept-Language':  'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection':       'keep-alive',
            'Content-Type':     'application/x-www-form-urlencoded',
            'Cookie':           cookie,
            'Origin':           'https://www.facebook.com',
            'Referer':          'https://www.facebook.com/',
            'User-Agent':       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        try:
            r = session.post(
                'https://www.facebook.com/chat/user_info/',
                headers=headers,
                data={"ids[0]": user_id, "fb_dtsg": fb_dtsg, "__a": "1", "__req": "1", "__rev": "1006793597"},
                timeout=15, verify=False
            )
            if r.status_code == 200:
                txt = r.text[9:] if r.text.startswith('for (;;);') else r.text
                js  = json.loads(txt)
                if 'payload' in js and 'profiles' in js['payload']:
                    profiles = js['payload']['profiles']
                    if profiles:
                        return profiles[next(iter(profiles))].get('name', f'User_{user_id[:8]}')
        except Exception:
            pass
        try:
            r = session.get(
                f'https://mbasic.facebook.com/profile.php?id={user_id}',
                headers={'Cookie': cookie, 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15'},
                timeout=15, verify=False
            )
            if r.status_code == 200:
                m = re.search(r'<title>([^<]+)</title>', r.text)
                if m and m.group(1).strip() != 'Facebook':
                    return m.group(1).strip()
        except Exception:
            pass
        try:
            r = session.post(
                'https://www.facebook.com/api/graphql/',
                headers=headers,
                data={'fb_dtsg': fb_dtsg, 'q': f'node({user_id}){{name}}', '__a': '1'},
                timeout=15, verify=False
            )
            if r.status_code == 200:
                txt  = r.text[9:] if r.text.startswith('for (;;);') else r.text
                data = json.loads(txt)
                if isinstance(data, dict) and 'data' in data:
                    name = data['data'].get('name')
                    if name:
                        return name
        except Exception:
            pass
    except Exception:
        pass
    return f'User_{user_id[:8]}'


def lay_last_seq_id(cookie, user_id):
    try:
        ssl_ctx = tao_ssl()
        headers = {
            'accept':         '*/*',
            'accept-language':'en-US,en;q=0.9',
            'cookie':          cookie,
            'user-agent':      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        with httpx.Client(verify=ssl_ctx, timeout=30.0, http2=True) as client:
            r = client.get('https://www.facebook.com/', headers=headers)
            if r.status_code == 200:
                for pat in [r'"sync_sequence_id":"?(\d+)"?', r'"lastSeqId":"?(\d+)"?']:
                    m = re.search(pat, r.text)
                    if m:
                        return m.group(1)
    except Exception:
        pass
    return str(int(time.time() * 1000))


class KetNoiMQTT:
    def __init__(self, fb_data):
        self.fb_data       = fb_data
        self.mqtt          = None
        self.ws_req_number = 0
        self.sync_token    = None
        self.last_seq_id   = fb_data.get('last_seq_id', '0')
        self.req_callbacks = {}
        self.cookie_hash   = hashlib.md5(fb_data['cookie'].encode()).hexdigest()
        self.last_cleanup  = time.time()
        self.so_thanh_cong = 0
        self.da_ket_noi    = False
        self.so_lan_thu    = 0
        self.last_attempt  = 0
        self._lock         = threading.Lock()

    def don_ram(self):
        now = time.time()
        if now - self.last_cleanup > 3600:
            with self._lock:
                self.req_callbacks.clear()
                self.last_cleanup = now

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.da_ket_noi = True
            self.so_lan_thu = 0
            client.subscribe([('/t_ms', 0)])
            queue = {
                'sync_api_version':           10,
                'max_deltas_able_to_process':  1000,
                'delta_batch_size':            500,
                'encoding':                    'JSON',
                'entity_fbid':                 self.fb_data['user_id'],
            }
            if self.sync_token is None:
                topic                              = '/messenger_sync_create_queue'
                queue['initial_titan_sequence_id'] = self.last_seq_id
                queue['device_params']             = None
            else:
                topic                  = '/messenger_sync_get_diffs'
                queue['last_seq_id']   = self.last_seq_id
                queue['sync_token']    = self.sync_token
            client.publish(topic, json_gon(queue), qos=1, retain=False)
        else:
            self.da_ket_noi = False

    def on_disconnect(self, client, userdata, rc):
        self.da_ket_noi = False
        if rc != 0:
            time.sleep(5)
            try:
                client.reconnect()
            except Exception:
                pass

    def ket_noi(self):
        if self.so_lan_thu >= 3:
            return False
        now = time.time()
        if now - self.last_attempt < 10:
            time.sleep(10 - (now - self.last_attempt))
        self.last_attempt = time.time()
        self.so_lan_thu  += 1
        try:
            session_id = tao_session_id()
            user = {
                'u':          self.fb_data['user_id'],
                's':          session_id,
                'chat_on':    json_gon(True),
                'fg':         False,
                'd':          tao_client_id(),
                'ct':         'websocket',
                'aid':        219994525426954,
                'mqtt_sid':   '',
                'cp':         3,
                'ecp':        10,
                'st':         ['/t_ms', '/messenger_sync_get_diffs', '/messenger_sync_create_queue'],
                'pm':         [],
                'dc':         '',
                'no_auto_fg': True,
                'gas':        None,
                'pack':       [],
            }
            host   = f"wss://edge-chat.messenger.com/chat?region=eag&sid={session_id}"
            parsed = urlparse(host)
            try:
                self.mqtt = mqtt.Client(
                    mqtt.CallbackAPIVersion.VERSION1,
                    client_id='mqttwsclient',
                    clean_session=True,
                    protocol=mqtt.MQTTv31,
                    transport='websockets',
                )
            except Exception:
                self.mqtt = mqtt.Client(
                    client_id='mqttwsclient',
                    clean_session=True,
                    protocol=mqtt.MQTTv31,
                    transport='websockets',
                )
            self.mqtt.tls_set(
                certfile=None, keyfile=None,
                cert_reqs=ssl.CERT_NONE,
                tls_version=ssl.PROTOCOL_TLSv1_2
            )
            self.mqtt.on_connect    = self.on_connect
            self.mqtt.on_disconnect = self.on_disconnect
            self.mqtt.username_pw_set(username=json_gon(user))
            self.mqtt.ws_set_options(
                path=f"{parsed.path}?{parsed.query}",
                headers={
                    'Cookie':     self.fb_data['cookie'],
                    'Origin':     'https://www.messenger.com',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 9; SM-G973U Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
                    'Referer':    'https://www.messenger.com/',
                    'Host':       'edge-chat.messenger.com',
                },
            )
            self.mqtt.connect(host='edge-chat.messenger.com', port=443, keepalive=10)
            self.mqtt.loop_start()
            for _ in range(20):
                if self.da_ket_noi:
                    return True
                time.sleep(0.5)
            return False
        except Exception:
            return False

    def gui_tin_nhan(self, thread_id, message):
        if not self.da_ket_noi:
            if not self.ket_noi():
                return False
        self.don_ram()
        with self._lock:
            self.ws_req_number += 1
            req_num = self.ws_req_number

        task_payload = {
            'initiating_source':    0,
            'multitab_env':         0,
            'otid':                 tao_offline_threading_id(),
            'send_type':            1,
            'skip_url_preview_gen': 0,
            'source':               0,
            'sync_group':           1,
            'text':                 message,
            'text_has_links':       0,
            'thread_id':            int(thread_id),
        }
        task = {
            'failure_count': None,
            'label':         '46',
            'payload':       json.dumps(task_payload, separators=(',', ':')),
            'queue_name':    str(thread_id),
            'task_id':       req_num,
        }
        task_mark = {
            'failure_count': None,
            'label':         '21',
            'payload':       json.dumps({
                'last_read_watermark_ts': int(time.time() * 1000),
                'sync_group':             1,
                'thread_id':              int(thread_id),
            }, separators=(',', ':')),
            'queue_name': str(thread_id),
            'task_id':    req_num + 1,
        }
        content = {
            'app_id':     '2220391788200892',
            'payload':    json.dumps({
                'data_trace_id': None,
                'epoch_id':      int(tao_offline_threading_id()),
                'tasks':         [task, task_mark],
                'version_id':    '7545284305482586',
            }, separators=(',', ':')),
            'request_id': req_num,
            'type':       3,
        }
        try:
            with khoa_mqtt:
                self.mqtt.publish(
                    topic='/ls_req',
                    payload=json.dumps(content, separators=(',', ':')),
                    qos=1,
                    retain=False,
                )
            self.so_thanh_cong += 1
            return True
        except Exception:
            self.da_ket_noi = False
            return False

    def ngat_ket_noi(self):
        if self.mqtt:
            try:
                self.mqtt.disconnect()
                self.mqtt.loop_stop()
            except Exception:
                pass
        self.da_ket_noi = False
        self.don_ram()


class TaiKhoanThuong:
    def __init__(self, cookie, so_thu_tu):
        self.cookie      = cookie
        self.so_thu_tu   = so_thu_tu
        self.user_id     = trich_xuat_user(cookie)
        self.fb_dtsg     = None
        self.ten         = f'ACC{so_thu_tu}'
        self.mqtt_sender = None
        self.hoat_dong   = True
        self.so_gui      = 0
        self.so_ok       = 0
        self.so_loi      = 0

    def khoi_tao(self):
        if not self.user_id:
            return False
        self.fb_dtsg = lay_fb_dtsg(self.cookie)
        if self.fb_dtsg:
            self.ten = lay_thong_tin(self.cookie, self.user_id, self.fb_dtsg)
        return True

    def khoi_tao_mqtt(self):
        seq_id  = lay_last_seq_id(self.cookie, self.user_id)
        fb_data = {
            'user_id':      self.user_id,
            'display_name': self.ten,
            'cookie':       self.cookie,
            'last_seq_id':  seq_id,
        }
        self.mqtt_sender = KetNoiMQTT(fb_data)
        return self.mqtt_sender.ket_noi()

    def tai_ket_noi(self):
        if self.mqtt_sender:
            self.mqtt_sender.ngat_ket_noi()
        return self.khoi_tao_mqtt()

    def gui(self, thread_id, message):
        if not self.hoat_dong:
            return False
        self.so_gui += 1
        if self.mqtt_sender is None:
            self.khoi_tao_mqtt()
        if not self.mqtt_sender.da_ket_noi:
            self.tai_ket_noi()
            time.sleep(2)
        ok = self.mqtt_sender.gui_tin_nhan(thread_id, message)
        if ok:
            self.so_ok += 1
        else:
            self.so_loi += 1
        return ok

    def ngat_ket_noi(self):
        if self.mqtt_sender:
            self.mqtt_sender.ngat_ket_noi()
        self.hoat_dong = False


class AccTitik:
    def __init__(self, cookie, so_thu_tu):
        self.cookie      = cookie
        self.so_thu_tu   = so_thu_tu
        self.user_id     = trich_xuat_i_user(cookie)
        self.fb_dtsg     = None
        self.ten         = f'TITIK_{so_thu_tu}'
        self.mqtt_sender = None
        self.hoat_dong   = True
        self.so_gui      = 0
        self.so_ok       = 0
        self.so_loi      = 0
        self._session    = requests.Session()

    def khoi_tao(self):
        if not self.user_id:
            return False
        self.fb_dtsg = self._lay_dtsg_titik()
        if not self.fb_dtsg:
            self.fb_dtsg = lay_fb_dtsg(self.cookie)
        if self.fb_dtsg:
            self.ten = lay_thong_tin(self.cookie, self.user_id, self.fb_dtsg, self._session)
        return True

    def _lay_dtsg_titik(self):
        try:
            headers = {
                'cookie':     self.cookie,
                'user-agent': 'Mozilla/5.0 (Linux; Android 9; SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
                'accept':     'text/html,application/xhtml+xml,*/*;q=0.8',
            }
            r = self._session.get('https://m.facebook.com/', headers=headers, timeout=15, verify=False)
            if r.status_code == 200:
                for pat in [
                    r'"DTSGInitialData",\[\],{"token":"([^"]+)"',
                    r'name="fb_dtsg" value="([^"]+)"',
                    r'"token":"([^"]+)"',
                ]:
                    m = re.search(pat, r.text)
                    if m:
                        return m.group(1)
        except Exception:
            pass
        return None

    def khoi_tao_mqtt(self):
        seq_id  = lay_last_seq_id(self.cookie, self.user_id)
        fb_data = {
            'user_id':      self.user_id,
            'display_name': self.ten,
            'cookie':       self.cookie,
            'last_seq_id':  seq_id,
        }
        self.mqtt_sender = KetNoiMQTT(fb_data)
        return self.mqtt_sender.ket_noi()

    def tai_ket_noi(self):
        if self.mqtt_sender:
            self.mqtt_sender.ngat_ket_noi()
        return self.khoi_tao_mqtt()

    def gui(self, thread_id, message):
        if not self.hoat_dong:
            return False
        self.so_gui += 1
        if self.mqtt_sender is None:
            self.khoi_tao_mqtt()
        if not self.mqtt_sender.da_ket_noi:
            self.tai_ket_noi()
            time.sleep(2)
        ok = self.mqtt_sender.gui_tin_nhan(thread_id, message)
        if ok:
            self.so_ok += 1
        else:
            self.so_loi += 1
        return ok

    def ngat_ket_noi(self):
        if self.mqtt_sender:
            self.mqtt_sender.ngat_ket_noi()
        self.hoat_dong = False


class QuanLySpam:
    def __init__(self):
        self.accounts      = []
        self.threads       = []
        self.dang_chay     = True
        self.recipient_ids = []
        self.message       = ''
        self.delay_map     = {}
        self.tong_acc      = 0
        self._file_ngon    = 'ngon.txt'

    def doc_file_ngon(self, ten_file):
        try:
            with open(ten_file, 'r', encoding='utf-8') as f:
                noi_dung = f.read()
            if noi_dung.strip():
                self.message    = noi_dung
                self._file_ngon = ten_file
                print(f"OK doc file ngon: {ten_file} ({len(noi_dung)} ky tu)")
                return True
            print("File ngon rong")
            return False
        except Exception as e:
            print(f"Loi doc file ngon: {e}")
            return False

    def doc_file_cookie(self, ten_file):
        try:
            with open(ten_file, 'r', encoding='utf-8') as f:
                dong = [d.strip() for d in f if d.strip()]
            return dong
        except Exception as e:
            print(f"Loi doc file cookie: {e}")
            return []

    def them_acc_tu_cookie(self, cookie, delay):
        self.tong_acc += 1
        loai = getattr(self, '_loai_cookie_mac_dinh', '1')
        if loai == '2':
            acc = AccTitik(cookie, self.tong_acc)
        else:
            acc = TaiKhoanThuong(cookie, self.tong_acc)
        ok = acc.khoi_tao()
        if not ok:
            self.tong_acc -= 1
            print(f"Cookie {self.tong_acc+1} khong hop le hoac da die")
            return None
        self.delay_map[id(acc)] = delay
        self.accounts.append(acc)
        loai = 'Titik' if isinstance(acc, AccTitik) else 'Thuong'
        print(f"OK: {acc.ten} | {acc.user_id} | Loai: {loai} | Delay: {delay}s")
        ok_mqtt = acc.khoi_tao_mqtt()
        if not ok_mqtt:
            print(f"Loi ket noi MQTT: {acc.ten}")
        return acc

    def _worker(self, acc):
        delay = self.delay_map.get(id(acc), 0)
        while self.dang_chay and acc.hoat_dong:
            for rid in list(self.recipient_ids):
                try:
                    ok = acc.gui(rid, self.message)
                    if ok:
                        in_log(f"CK{acc.so_thu_tu} > {acc.ten} > {rid} > Success")
                    else:
                        in_log(f"CK{acc.so_thu_tu} > {acc.ten} > {rid} > Failed")
                except Exception:
                    pass
            time.sleep(delay if delay > 0 else 0.1)

    def bat_dau_spam(self):
        self.dang_chay = True
        for acc in self.accounts:
            if acc.hoat_dong:
                t = threading.Thread(target=self._worker, args=(acc,), daemon=True)
                self.threads.append(t)
                t.start()

    def cmd_addck(self):
        print("")
        print("/addck - them cookie moi")
        print("ID box va file ngon lay tu cau hinh hien tai")
        print("")
        try:
            delay = int(input("Delay cho cookie moi (giay): ").strip())
        except Exception:
            delay = 0
        ck = input("Nhap cookie: ").strip()
        if not ck:
            print("Cookie rong")
            return
        acc = self.them_acc_tu_cookie(ck, delay)
        if acc and self.dang_chay and self.recipient_ids:
            t = threading.Thread(target=self._worker, args=(acc,), daemon=True)
            self.threads.append(t)
            t.start()
            print(f"Da them va bat dau spam: {acc.ten}")

    def cmd_xoack(self, so_tt=None):
        if not self.accounts:
            print("Khong co tai khoan nao")
            return
        for i, acc in enumerate(self.accounts, 1):
            loai = 'Titik' if isinstance(acc, AccTitik) else 'Thuong'
            print(f"{i}. {acc.ten} | {acc.user_id} | Loai: {loai}")
        if so_tt is None:
            try:
                so_tt = int(input("So thu tu can xoa (0 = huy): ").strip())
            except Exception:
                return
        if so_tt == 0:
            return
        if 1 <= so_tt <= len(self.accounts):
            removed = self.accounts.pop(so_tt - 1)
            removed.ngat_ket_noi()
            print(f"Da xoa: {removed.ten}")
        else:
            print("So thu tu khong hop le")

    def dung_tat_ca(self):
        self.dang_chay = False
        for acc in self.accounts:
            acc.ngat_ket_noi()
        for t in self.threads:
            if t.is_alive():
                t.join(timeout=1)
        self.threads = []

    def vong_lenh(self):
        print("")
        print("Dang spam... Lenh: /addck | /xoack [so] | exit")
        while True:
            try:
                lenh = input("> ").strip()
                if not lenh:
                    continue
                if lenh.lower() == '/addck':
                    self.cmd_addck()
                elif lenh.lower().startswith('/xoack'):
                    phan  = lenh.split()
                    so_tt = None
                    if len(phan) >= 2:
                        try:
                            so_tt = int(phan[1])
                        except Exception:
                            pass
                    self.cmd_xoack(so_tt)
                elif lenh.lower() in ['exit', 'quit', 'thoat']:
                    self.dung_tat_ca()
                    break
                else:
                    print("Lenh khong hop le. Dung /addck hoac /xoack [so]")
            except KeyboardInterrupt:
                self.dung_tat_ca()
                break
            except Exception:
                pass

    def chay(self):
        tnghia_huongdansudung()
        hien_banner()

        print("Chon loai cookie:")
        print("1. Cookie thuong (c_user)")
        print("2. Cookie Titik (i_user)")
        loai_chon = input("Chon (1/2): ").strip()
        if loai_chon not in ['1', '2']:
            loai_chon = '1'
        self._loai_cookie_mac_dinh = loai_chon

        file_ck = input("File cookie (vd: cookie.txt): ").strip()
        if not file_ck:
            file_ck = 'cookie.txt'
        cookies = self.doc_file_cookie(file_ck)
        if not cookies:
            print("Khong doc duoc cookie tu file")
            input("Enter de thoat...")
            return

        print(f"Doc duoc {len(cookies)} cookie tu {file_ck}")
        print("")

        delays = []
        for i, ck in enumerate(cookies, 1):
            try:
                d = int(input(f"Delay cho cookie #{i} (giay): ").strip())
            except Exception:
                d = 0
            delays.append(d)

        print("")
        print("Nhap ID box nhan tin (moi dong 1 ID, gõ done de xong):")
        while True:
            rid = input(f"ID #{len(self.recipient_ids)+1}: ").strip()
            if rid.lower() == 'done':
                break
            if rid:
                self.recipient_ids.append(rid)
                print(f"Da them: {rid}")
        if not self.recipient_ids:
            print("Phai co it nhat 1 ID box")
            input("Enter de thoat...")
            return

        print("")
        file_ngon = input("File ngon (vd: ngon.txt): ").strip()
        if not file_ngon:
            file_ngon = 'ngon.txt'
        if not self.doc_file_ngon(file_ngon):
            print("Khong doc duoc file ngon")
            input("Enter de thoat...")
            return

        print("")
        print("Dang kiem tra va ket noi cookie...")
        for i, ck in enumerate(cookies):
            self.them_acc_tu_cookie(ck, delays[i])

        if not self.accounts:
            print("Khong co cookie hop le")
            input("Enter de thoat...")
            return

        print("")
        print(f"Bat dau spam: {len(self.accounts)} acc | {len(self.recipient_ids)} ID box | file: {file_ngon}")
        self.bat_dau_spam()
        time.sleep(1)
        lam_sach_man_hinh()
        hien_banner()
        self.vong_lenh()


def main():
    quan_ly = QuanLySpam()
    try:
        quan_ly.chay()
    except KeyboardInterrupt:
        print("\nThoat...")
        quan_ly.dung_tat_ca()
    except Exception as e:
        print(f"Loi: {e}")
        input("Enter de thoat...")


if __name__ == '__main__':
    main()
