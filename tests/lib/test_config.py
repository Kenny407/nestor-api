# pylint: disable=missing-function-docstring disable=missing-module-docstring

import nestor_api.lib.config as config


def test_for_app():
    configuration = config.for_app("my-app")
    assert configuration == dict({"app_name": "my-app"})
