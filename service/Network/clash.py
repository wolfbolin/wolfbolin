# coding=utf-8
import json
import yaml
import Util
import base64
import pymysql
import Network
import requests
from urllib import parse
from flask import current_app as app

remove_keyword = ["Sakura", "KDDI", "IDCF", "Netflix", "HKT", "TVB", "HBO", "CN2", "GIA", "hulu",
                  "AbemaTV", "happyon", "GMO", "HKBN", "HGC", "WTT", "PCCW", "Hinet", "BBC", "ITV",
                  "C4", "F4"]


@Network.network_blue.route('/proxy/clash', methods=["GET"])
@Util.verify_token
def proxy_clash():
    # 下载网络接口
    api_url = app.config["CLASH"]['api']
    http_result = requests.get(api_url)
    api_data = yaml.safe_load(http_result.text)

    # 预处理通用规则
    conn = app.mysql_pool.connection()
    gfw_list = Util.get_app_pair(conn, "proxy", "gfwlist")
    gfw_data = base64.b64decode(gfw_list).decode()
    gfw_rule = parse_gfw_rule(gfw_data)

    rule_list = gfw_rule + read_proxy_rule(conn)

    rule_list.append("IP-CIDR,10.0.0.0/8,DIRECT")
    rule_list.append("IP-CIDR,127.0.0.0/8,DIRECT")
    rule_list.append("IP-CIDR,172.16.0.0/12,DIRECT")
    rule_list.append("IP-CIDR,192.168.0.0/16,DIRECT")
    rule_list.append("GEOIP,CN,LAN")
    rule_list.append("MATCH,LAN")

    # 组装新的配置文件
    foreign_list = []
    transfer_list = []
    domestic_list = []
    for api in api_data["Proxy"]:
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

    clash_config = {
        "Proxy": foreign_list + transfer_list + domestic_list,
        "Proxy Group": [
            proxy_group(foreign_list + transfer_list, "Foreign"),
            proxy_group(domestic_list, "Domestic"),
            {"name": "VAC", "type": "select", "proxies": ["DIRECT", "Foreign", "Domestic"]},
            {"name": "ACC", "type": "select", "proxies": ["DIRECT", "Foreign", "Domestic"]},
            {"name": "LAN", "type": "select", "proxies": ["DIRECT", "Foreign", "Domestic"]},
        ],
        "Rule": rule_list
    }

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


def read_proxy_rule(conn):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM `proxy_rule`"
    cursor.execute(sql)
    rule_list = []
    for rule in cursor.fetchall():
        rule_list.append("{},{},{}".format(rule["type"], rule["content"], rule["group"]))
    return rule_list


def proxy_group(api_list, group_name):
    group_info = {
        "name": group_name,
        "type": "select",
        "proxies": [api["name"] for api in api_list]
    }
    return group_info
