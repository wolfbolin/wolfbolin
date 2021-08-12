# coding=utf-8
import json
import yaml
import Kit
import base64
import Network
import requests
from urllib import parse
from flask import request
from Network import database as db
from flask import current_app as app

remove_keyword = ["Sakura", "KDDI", "IDCF", "Netflix", "HKT", "TVB", "HBO", "CN2", "GIA", "hulu",
                  "AbemaTV", "happyon", "GMO", "HKBN", "HGC", "WTT", "PCCW", "Hinet", "BBC", "ITV",
                  "C4", "F4", "Azure", " - 基础VIP节点", "(广)"]

replace_keyword = {
    "(广SS)": "SS",
    "IEPL": "专线"
}


@Network.network_blue.route('/proxy/rule', methods=["GET"])
@Kit.verify_passwd("proxy_acl")
def get_proxy_rule():
    username = request.args.get("user", "none")
    # 读取代理规则列表
    conn = app.mysql_pool.connection()
    rule_list = db.read_proxy_rule(conn, username)

    return Kit.common_rsp(rule_list)


@Network.network_blue.route('/proxy/rule', methods=["PUT"])
@Kit.verify_passwd("proxy_acl")
def set_proxy_rule():
    username = request.args.get("user", "none")

    # 解析列表数据
    rule_list = request.get_data(as_text=True)
    rule_list = json.loads(rule_list)

    # 更新代理规则
    conn = app.mysql_pool.connection()
    db.update_proxy_rule(conn, username, rule_list)
    rule_list = db.read_proxy_rule(conn, username)

    return Kit.common_rsp(rule_list)


@Network.network_blue.route('/proxy/node', methods=["GET"])
@Kit.verify_token()
def proxy_node_list():
    method = request.args.get("refresh", "false")
    echo = request.args.get("echo", "false")

    req_result = {"count": 0}
    conn = app.mysql_pool.connection()

    if method == "true":
        # 读取节点源
        service_source = app.config["AGENT"]['service'].split(";")

        # 更新源信息
        node_list = []
        flow_data = [0, 0, 0, 0]
        for source in service_source:
            api_url = app.config["AGENT"][source]

            try:
                api_result = requests.get(api_url, timeout=10)
            except requests.exceptions.RequestException:
                continue

            # 处理节点数据
            api_data = yaml.safe_load(api_result.text)
            if "Proxy" in api_data.keys():
                api_data["proxies"] = api_data["Proxy"]

            for node in api_data["proxies"]:
                node["source"] = source
                node_list.append(node)

            # 处理流量信息
            flow_res = api_result.headers["Subscription-Userinfo"].split(";")
            flow_data[0] += int(flow_res[0].split("=")[1])
            flow_data[1] += int(flow_res[1].split("=")[1])
            flow_data[2] += int(flow_res[2].split("=")[1])
            flow_data[3] += int(flow_res[3].split("=")[1])

        # 写入节点更新数据
        if len(node_list) != 0:
            Kit.set_app_pair(conn, "proxy", "node_list", json.dumps(node_list))
            Kit.set_app_pair(conn, "proxy", "flow_data", json.dumps(flow_data))
            Kit.set_app_pair(conn, "proxy", "timestamp", Kit.unix_time())
            req_result["count"] = len(node_list)

    if echo == "true":
        req_result["node_list"] = json.loads(Kit.get_app_pair(conn, "proxy", "node_list"))
        req_result["flow_data"] = json.loads(Kit.get_app_pair(conn, "proxy", "flow_data"))
        req_result["timestamp"] = json.loads(Kit.get_app_pair(conn, "proxy", "timestamp"))
        req_result["count"] = len(req_result["node_list"])

    return Kit.common_rsp(req_result)


@Network.network_blue.route('/proxy/clash', methods=["GET"])
@Kit.verify_passwd("proxy_acl")
def proxy_clash():
    username = request.args.get("user", "none")
    gfw = request.args.get("gfw", "false")
    x_headers = {}

    # 获取节点数据
    conn = app.mysql_pool.connection()
    node_list = json.loads(Kit.get_app_pair(conn, "proxy", "node_list"))
    flow_data = json.loads(Kit.get_app_pair(conn, "proxy", "flow_data"))
    timestamp = Kit.get_app_pair(conn, "proxy", "timestamp")

    tx_info = {"name": "TX={}".format(Kit.byte2all(flow_data[0])),
               "type": "http", "server": "0.0.0.0", "port": 0}
    rx_info = {"name": "RX={}".format(Kit.byte2all(flow_data[1])),
               "type": "http", "server": "0.0.0.0", "port": 0}
    all_info = {"name": "ALL={}".format(Kit.byte2all(flow_data[2])),
                "type": "http", "server": "0.0.0.0", "port": 0}
    time_info = {"name": Kit.unix2timestamp(timestamp),
                 "type": "http", "server": "0.0.0.0", "port": 0}
    expire_info = {"name": Kit.unix2timestamp(flow_data[3]),
                   "type": "http", "server": "0.0.0.0", "port": 0}

    x_headers["Subscription-Userinfo"] = "upload={}; download={}; total={}; expire={}" \
        .format(flow_data[0], flow_data[1], flow_data[2], flow_data[3])

    traffic_info = [tx_info, rx_info, all_info, time_info, expire_info]
    flow_data = {"name": "TX/RX/ALL", "type": "select",
                 "proxies": ["DIRECT"] + [it["name"] for it in traffic_info]}

    # 预处理通用规则
    rule_list = []
    if gfw == "true":
        gfw_list = Kit.get_app_pair(conn, "proxy", "gfwlist")
        gfw_data = base64.b64decode(gfw_list).decode()
        gfw_rule = parse_gfw_rule(gfw_data)
        rule_list = gfw_rule

    # 读取用户流量规则
    temp_list = []
    for rule in db.read_proxy_rule(conn, username):
        temp_list.append("{},{},{}".format(rule["type"], rule["content"], rule["group"]))
    rule_list = temp_list + rule_list

    rule_list.append("IP-CIDR,10.0.0.0/8,DIRECT")
    rule_list.append("IP-CIDR,127.0.0.0/8,DIRECT")
    rule_list.append("IP-CIDR,172.16.0.0/12,DIRECT")
    rule_list.append("IP-CIDR,192.168.0.0/16,DIRECT")
    rule_list.append("GEOIP,CN,ALL")
    rule_list.append("MATCH,ALL")

    # 代理配置分类归档
    foreign_list = []
    transfer_list = []
    domestic_list = []

    for api in node_list:
        for keyword in remove_keyword:
            api["name"] = api["name"].replace(keyword, "")
        for key, val in replace_keyword.items():
            api["name"] = api["name"].replace(key, val)
        api["name"] = api["name"].strip()
        api["name"] = api["name"].replace("(SS)", "[SS]")
        if api["name"].find("特殊") >= 0:
            continue
        if api["name"].find("仅海外") >= 0:
            continue
        if api["name"].find("回国") >= 0:
            api["name"] = api["name"].replace("回国-", "")
            api["name"] = "【国内】" + api["name"]
            domestic_list.append(api)
        elif api["name"].find("->") >= 0:
            api["name"] = "【中转】" + api["name"]
            transfer_list.append(api)
        elif api["name"].find("中转") >= 0:
            api["name"] = "【中转】" + api["name"]
            transfer_list.append(api)
        else:
            api["name"] = "【海外】" + api["name"]
            foreign_list.append(api)
        api["name"] = "{}@{}".format(api["name"], api["source"])

    # 初始化配置信息
    clash_config = {
        "proxies": foreign_list + transfer_list + domestic_list + traffic_info,
        "proxy-groups": [
            flow_data,
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
                "name": "ALL", "type": "select",
                "proxies": ["DIRECT", "CHK", "CTW", "USA", "SEA"]
            }
        ],
        "rules": rule_list
    }

    # 私有节点列表
    # TODO Remove hard code
    if username == "wolfbolin":
        private_data = Kit.get_app_pair(conn, "proxy", "private_node")
        private_data = json.loads(private_data)
        for group in private_data:
            clash_config["proxies"] += group["node"]
            clash_config["proxy-groups"] += proxy_group(group["name"], group["node"], **group["params"]),

    # 基础节点列表
    node_group_config = {"url": "https://www.gstatic.com/generate_204", "tolerance": 200}
    clash_config["proxy-groups"] += [
        proxy_group("CHK", pick_api(foreign_list + transfer_list, ["香港"]), config=node_group_config),
        proxy_group("CTW", pick_api(foreign_list + transfer_list, ["台湾"]), config=node_group_config),
        proxy_group("JPN", pick_api(foreign_list + transfer_list, ["日本"]), config=node_group_config),
        proxy_group("USA", pick_api(foreign_list + transfer_list, ["美国"]), config=node_group_config),
        proxy_group("SEA", foreign_list + transfer_list, config=node_group_config),
    ]

    return str(yaml.dump(clash_config, indent=4, allow_unicode=True, line_break="\r\n")), 200, x_headers


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
        proxy_rule.append("{},{},ALL".format(rule, domain))


def pick_api(api_list, keywords):
    api_group = []
    for api in api_list:
        for keyword in keywords:
            if "仅海外" in api["name"]:
                continue
            if keyword in api["name"]:
                api_group.append(api)
    return api_group


def proxy_group(group_name, api_list, mode="url-test", base_proxies=None, config=None):
    if config is None:
        config = dict()

    if base_proxies is None:
        base_proxies = []

    if mode == "url-test":
        group_info = {
            "name": group_name, "type": "url-test", "interval": 300,
            "proxies": base_proxies + [api["name"] for api in api_list]
        }
    elif mode == "fallback":
        group_info = {
            "name": group_name, "type": "fallback", "interval": 300,
            "proxies": base_proxies + [api["name"] for api in api_list]
        }
    else:
        group_info = {
            "name": group_name, "type": "select",
            "proxies": base_proxies + [api["name"] for api in api_list]
        }

    group_info.update(config)
    return group_info
