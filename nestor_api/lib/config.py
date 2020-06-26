"""Configuration library"""

import errno
import os
from typing import Optional

from nestor_api.lib.errors import ConfigurationNotFoundError

import nestor_api.lib.io as io
from nestor_api.config.config import Configuration


def change_environment(environment, config_path=Configuration.config_path):
    """Changes the environment (branch) of the configuration"""
    io.execute('git stash', config_path)
    io.execute('git fetch origin', config_path)
    io.execute(f'git checkout {environment}', config_path)
    io.execute(f'git reset --hard origin/{environment}', config_path)


def for_app(app_name, config_path=Configuration.config_path):
    """Retrieves the configuration of an application"""
    yaml_path = os.path.join(config_path, "apps", f"{app_name}.yaml")

    if not io.exists(yaml_path):
        raise ConfigurationNotFoundError(app_name)

    project = for_project(config_path)
    app = io.yaml(yaml_path)

    configuration = {**project, **app}

    # TODO awaiting for implementation
    # 1. Check for duplicates variables
    # 2. Add validation of config here
    # 3. mapValuesDeep

    return configuration


def list_apps_config(config_path=Configuration.config_path) -> dict:
    """Retrieves all of the application names."""
    apps_path = os.path.join(config_path, "apps")

    if not os.path.isdir(apps_path):
        raise ValueError(apps_path)
    apps_files = [f for f in os.listdir(apps_path) if os.path.isfile(os.path.join(apps_path, f))]
    apps_config = [io.from_yaml(file) for file in apps_files]
    return {app_config['name']: app_config for app_config in apps_config}


def for_project(config_path=Configuration.config_path):
    """Retrieves the configuration of the project"""
    yaml_path = os.path.join(config_path, "project.yaml")
    if not io.exists(yaml_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), yaml_path)

    configuration = io.from_yaml(yaml_path)

    # TODO awaiting for implementation
    # mapValuesDeep

    return configuration


def get_configuration_copy_path(config_path=Configuration.config_path):
    """Copy the configuration in a temporary directory and returns its path"""
    return io.get_temporary_copy(config_path, "config")


def get_previous_step(config_object: object, target: str) -> Optional[str]:
    """ Returns the previous step in the defined workflow """
    index = config_object['workflow'].index(target)
    if index > 0:
        return config_object['workflow'][index - 1]
    else:
        return None
