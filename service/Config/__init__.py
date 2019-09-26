# coding=utf-8
import os
import logging


def get_config():
    # 读取配置文件
    run_env = 'production'
    if 'SERVICE_ENV' in os.environ:
        run_env = os.environ['SERVICE_ENV']

    config_path = '{}/{}.py'.format(os.path.split(os.path.abspath(__file__))[0], run_env)
    if os.path.isfile(config_path):

        logging.info('===========ENVIRONMENT===========')
        logging.info('Running environment: %s' % run_env)
        logging.info('=================================')

        return config_path
    else:
        logging.error("Config not exist")
        exit()
