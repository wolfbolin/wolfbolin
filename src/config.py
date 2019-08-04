# coding=utf-8
import os


class Config:
    # 设置运行路径
    BASE_PATH = os.path.split(os.path.abspath(__file__))[0]
    # 定时任务相关
    JOBS = []
    SCHEDULER_API_ENABLED = True
    # 出网网络代理
    PROXY = {}
    # RSS数据地址
    RSS = "https://blog.wolfbolin.com/feed"
    # 模版页面信息
    COPYRIGHT = "CopyRight © 2017-2020 WolfBolin. All Rights Reserved."
    NAV_ITEM = [
        {
            "id": "index",
            "href": "/",
            "name": "主页",
        },
        {
            "id": "blog",
            "href": "http://blog.wolfbolin.com",
            "name": "博客",
        },
        {
            "id": "project",
            "href": "/project",
            "name": "项目",
        },
    ]


class DevelopmentConfig(Config):
    DEBUG = True
    JOBS = [
        {
            'id': 'job_1h_data',
            'func': 'func:update_blog_feed',
            'args': [Config.RSS, Config.BASE_PATH],
            'trigger': 'interval',
            'hours': 1
        }
    ]


class IntranetConfig(DevelopmentConfig):
    HTTP_PROXY = "http://127.0.0.1:12639"
    HTTPS_PROXY = "http://127.0.0.1:12639"
    PROXY = {
        'http': HTTP_PROXY,
        'https': HTTPS_PROXY
    }


class ProductionConfig(Config):
    DEBUG = False
    JOBS = [
        {
            'id': 'job_1h_data',
            'func': 'func:update_blog_feed',
            'args': [Config.RSS, Config.BASE_PATH],
            'trigger': 'interval',
            'hours': 1
        }
    ]


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'intranet': IntranetConfig
}
