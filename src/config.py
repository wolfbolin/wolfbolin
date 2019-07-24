# coding=utf-8


class Config:
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
    pass


class ProductionConfig(Config):
    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
