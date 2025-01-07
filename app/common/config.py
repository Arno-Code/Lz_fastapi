import os

import yaml
from loguru import logger

from app import APP_DIR

""" 全局配置 """


class Config:
    """全局配置类"""

    def __init__(self, config_file_name: str = 'config'):
        self.config_file_name = config_file_name
        self.config = self.load_config()

    """加载配置文件"""
    def load_config(self):
        """加载配置文件，选择激活的环境配置"""
        config_file_suffixes = ['.yaml', '.yml']  # 配置文件后缀
        config_files = [f'{self.config_file_name}{suffix}' for suffix in config_file_suffixes]
        config_file = None
        env_config_file = None

        # 查找哪个配置文件存在
        for config_file_name in config_files:
            potential_config_file = APP_DIR.joinpath(config_file_name)
            if potential_config_file.exists():
                config_file = potential_config_file
                break

        # 如果没有找到配置文件，抛出异常
        if config_file is None:
            raise FileNotFoundError(f"No config file found ({config_files[0]} or {config_files[1]}).")

        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        env = os.getenv("ENV")
        if env:
            active_profile = env
        else:
            active_profile = config['profiles']['active']
        # 加载与活动环境对应的配置文件
        env_config_files = [f'{self.config_file_name}_{active_profile}{suffix}' for suffix in config_file_suffixes]
        for config_file_name in env_config_files:
            potential_config_file = APP_DIR.joinpath(config_file_name)
            if potential_config_file.exists():
                env_config_file = potential_config_file
                break

        if env_config_file is None:
            raise FileNotFoundError(f"No config file found ({env_config_files[0]} or {env_config_files[1]}).")

        with open(env_config_file, 'r', encoding='utf-8') as f:
            env_config = yaml.safe_load(f)

        # 打印配置文件内容
        logger.info(f'配置文件加载完成,已激活环境：{active_profile}')
        return config
