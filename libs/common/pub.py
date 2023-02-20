import datetime
import hashlib
import json
import socket
import uuid


def make_token():
    a = uuid.uuid1()
    return str(a)


# md5 hash
def md5_str(data):
    md = hashlib.md5()
    # 获取一个md5加密算法对象
    md.update(data.encode('utf-8'))
    # 制定需要加密的字符串
    hash_str = md.hexdigest()
    return hash_str


def is_json(my_json):
    try:
        json.loads(my_json)
    except ValueError:
        return False
    except TypeError:
        return False
    return True


def get_ip_addr(request):
    ip = request.headers.get('X-Forwarded-For') or request.headers.get('X-Real-IP') or request.remote_addr
    return ip


def get_hostname():
    return socket.gethostname()


def merge_log_info(info):
    info['hostname'] = get_hostname()
    info['@timestamp'] = datetime.datetime.now().isoformat()
    return info

