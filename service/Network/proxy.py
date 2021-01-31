# coding=utf-8
import json
import yaml
import Kit
import base64
import Network
import requests
import operator
from urllib import parse
from flask import request
from functools import reduce
from Network import database as db
from flask import current_app as app

remove_keyword = ["Sakura", "KDDI", "IDCF", "Netflix", "HKT", "TVB", "HBO", "CN2", "GIA", "hulu",
                  "AbemaTV", "happyon", "GMO", "HKBN", "HGC", "WTT", "PCCW", "Hinet", "BBC", "ITV",
                  "C4", "F4", "Azure"]


@Network.network_blue.route('/proxy/rule', methods=["GET"])
@Kit.verify_token()
def get_proxy_rule():
    # 读取代理规则列表
    conn = app.mysql_pool.connection()
    rule_list = db.read_proxy_rule(conn)

    return Kit.common_rsp(rule_list)


@Network.network_blue.route('/proxy/rule', methods=["PUT"])
@Kit.verify_token()
def set_proxy_rule():
    # 解析列表数据
    rule_list = request.get_data(as_text=True)
    rule_list = json.loads(rule_list)

    # 更新代理规则
    conn = app.mysql_pool.connection()
    db.update_proxy_rule(conn, rule_list)
    rule_list = db.read_proxy_rule(conn)

    return Kit.common_rsp(rule_list)


@Network.network_blue.route('/proxy/clash', methods=["GET"])
@Kit.verify_token()
def proxy_clash():
    # 下载网络接口
    api_url = app.config["CLASH"]['api']
    http_result = requests.get(api_url)
    api_data = yaml.safe_load(http_result.text)

    # 预处理通用规则
    conn = app.mysql_pool.connection()
    gfw_list = Kit.get_app_pair(conn, "proxy", "gfwlist")
    gfw_data = base64.b64decode(gfw_list).decode()
    gfw_rule = parse_gfw_rule(gfw_data)

    rule_list = []
    for rule in db.read_proxy_rule(conn):
        rule_list.append("{},{},{}".format(rule["type"], rule["content"], rule["group"]))
    rule_list = rule_list + gfw_rule

    rule_list.append("IP-CIDR,10.0.0.0/8,DIRECT")
    rule_list.append("IP-CIDR,127.0.0.0/8,DIRECT")
    rule_list.append("IP-CIDR,172.16.0.0/12,DIRECT")
    rule_list.append("IP-CIDR,192.168.0.0/16,DIRECT")
    rule_list.append("GEOIP,CN,LAN")
    rule_list.append("MATCH,LAN")

    # 代理配置分类归档
    foreign_list = []
    transfer_list = []
    domestic_list = []

    if "Proxy" in api_data.keys():
        api_data["proxies"] = api_data["Proxy"]
    if "Proxy Group" in api_data.keys():
        api_data["proxy-groups"] = api_data["Proxy Group"]
    if "Rule" in api_data.keys():
        api_data["rules"] = api_data["Rule"]

    for api in api_data["proxies"]:
        for keyword in remove_keyword:
            api["name"] = api["name"].replace(keyword, "")
        api["name"] = api["name"].strip()
        if api["name"].find("回国") >= 0:
            api["name"] = api["name"].replace("回国-", "")
            api["name"] = "【国内】" + api["name"]
            domestic_list.append(api)
        elif api["name"].find("中转") >= 0:
            transfer_list.append(api)
        else:
            api["name"] = "【海外】" + api["name"]
            foreign_list.append(api)

    # 初始化配置信息
    clash_config = {
        "proxies": foreign_list + transfer_list + domestic_list,
        "proxy-groups": [
            {
                "name": "VAC", "type": "select",
                "proxies": ["DIRECT", "CHK", "CTW", "USA", "SEA"]
            },
            {
                "name": "ACC", "type": "select",
                "proxies": ["DIRECT", "CHK", "CTW", "USA", "SEA"]
            },
            {
                "name": "DEV", "type": "select",
                "proxies": ["DIRECT", "CHK", "CTW", "USA", "SEA"]
            },
            {
                "name": "LAN", "type": "select",
                "proxies": ["DIRECT", "CHK", "CTW", "USA", "SEA"]
            }
        ],
        "rules": rule_list
    }

    # 私有节点列表
    private_data = Kit.get_app_pair(conn, "proxy", "private_node")
    private_data = json.loads(private_data)
    for group in private_data:
        clash_config["proxies"] += group["node"]
        clash_config["proxy-groups"] += proxy_group(group["name"], group["node"], **group["config"]),

    # 基础节点列表
    clash_config["proxy-groups"] += [
        proxy_group("CHK", pick_api(foreign_list + transfer_list, ["香港"])),
        proxy_group("CTW", pick_api(foreign_list + transfer_list, ["台湾"])),
        proxy_group("JPN", pick_api(foreign_list + transfer_list, ["日本"])),
        proxy_group("USA", pick_api(foreign_list + transfer_list, ["美国"])),
        proxy_group("SEA", foreign_list + transfer_list),
    ]

    return str(yaml.dump(clash_config, indent=4, allow_unicode=True, line_break="\r\n"))


def parse_gfw_rule(rule_data):
    proxy_rule = []
    lines = rule_data.splitlines(False)
    for line in lines:
        # 逐行识别
        proxy_status = True
        if line.find('.*') >= 0:
            continue
        elif line.find('*.') >= 0:
            line = line.replace('*.', '')
        elif line.startswith('@@'):
            line = line.replace('@@', '')
            proxy_status = False

        if line.startswith('['):
            continue
        elif line.startswith('!'):
            continue
        elif line.startswith('||'):
            add_domain(proxy_status, proxy_rule, line.lstrip("||"), "DOMAIN-SUFFIX")
        elif line.startswith('|'):
            add_domain(proxy_status, proxy_rule, line.lstrip("|"), "DOMAIN-SUFFIX")
        elif line.startswith('.'):
            add_domain(proxy_status, proxy_rule, line.lstrip("."), "DOMAIN-SUFFIX")
        else:
            add_domain(proxy_status, proxy_rule, line, "DOMAIN")
    return list(set(proxy_rule))


def add_domain(proxy_status, proxy_rule, domain, rule):
    # 提取域名信息
    if not domain.startswith('http'):
        domain = 'http://' + domain
    domain = parse.urlparse(domain).hostname
    if domain is None:
        return

    if proxy_status:
        proxy_rule.append("{},{},VAC".format(rule, domain))
    else:
        proxy_rule.append("{},{},LAN".format(rule, domain))


def pick_api(api_list, keywords):
    api_group = []
    for api in api_list:
        for keyword in keywords:
            if keyword in api["name"]:
                api_group.append(api)
    return api_group


def proxy_group(group_name, api_list, mode="url-test", test_url="https://www.gstatic.com/generate_204"):
    if mode == "url-test":
        group_info = {
            "name": group_name, "type": "url-test", "interval": 300, "url": test_url, "tolerance": 200,
            "proxies": ["DIRECT"] + [api["name"] for api in api_list]
        }
    elif mode == "fallback":
        group_info = {
            "name": group_name, "type": "fallback", "interval": 300, "url": test_url,
            "proxies": [api["name"] for api in api_list] + ["DIRECT"]
        }
    else:
        group_info = {
            "name": group_name, "type": "select",
            "proxies": ["DIRECT"] + [api["name"] for api in api_list]
        }
    return group_info
