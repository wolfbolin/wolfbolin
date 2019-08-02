# coding=utf-8


class Config:
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
               ],


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
