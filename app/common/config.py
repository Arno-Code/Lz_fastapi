import os

import yaml
from loguru import logger

from app import APP_DIR


def load_config(config_file_prefix: str = 'config'):
    """加载配置文件，选择激活的环境配置"""
    config_file_suffixes = ['.yaml', '.yml']  # 配置文件后缀
    config_files = [f'{config_file_prefix}{suffix}' for suffix in config_file_suffixes]
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

    # 选择环境配置
    env = os.getenv("ENV")  # 从环境变量获取环境
    if env:
        active_profile = env
    else:
        # 如果没有环境变量，选择默认配置文件中的配置
        active_profile = config.get('profiles', {}).get('active', 'default')  # 添加默认值处理

    # 加载与活动环境对应的配置文件
    env_config_files = [f'{config_file_prefix}_{active_profile}{suffix}' for suffix in config_file_suffixes]
    for config_file_name in env_config_files:
        potential_config_file = APP_DIR.joinpath(config_file_name)
        if potential_config_file.exists():
            env_config_file = potential_config_file
            break

    if env_config_file is None:
        raise FileNotFoundError(
            f"No config file found for active profile ({env_config_files[0]} or {env_config_files[1]}).")

    # 加载环境配置文件
    with open(env_config_file, 'r', encoding='utf-8') as f:
        env_config = yaml.safe_load(f)

    # 合并配置
    config.update(env_config)

    # 打印配置文件内容
    logger.info(f'配置文件加载完成,已激活环境：{active_profile}')
    return config


# 全局配置变量，存储加载的配置字典
# 通过调用 load_config() 函数，加载并返回配置文件的内容
GLOBAL_CONFIG: dict = load_config()

# 配置文件上传路径
UPLOAD_FOLDER = GLOBAL_CONFIG.get('file', {}).get('upload_path', APP_DIR.parent.joinpath('uploads'))
