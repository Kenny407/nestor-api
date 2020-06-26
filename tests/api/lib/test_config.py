import unittest
from unittest.mock import patch

import nestor_api.lib.config as config


class TestConfig(unittest.TestCase):
    def test_get_previous_step_with_previous_step(self):
        """Should answer with the previous step."""
        previous_step = config.get_previous_step({'workflow': ['step1', 'step2', 'step3']}, 'step2')
        assert previous_step == 'step1'

    def test_get_previous_step_without_previous_step(self):
        """Should answer with None as the previous step does not exist."""
        previous_step = config.get_previous_step({'workflow': ['step1', 'step2', 'step3']}, 'step1')
        assert previous_step is None

    def test_get_previous_step_raises_error_with_incorrect_config(self):
        """Should raise an error if config is malformed."""
        with self.assertRaises(KeyError):
            config.get_previous_step({}, 'step1')

    @patch('nestor_api.lib.config.io', autospec=True)
    @patch('nestor_api.lib.config.os', autospec=True)
    def test_list_apps_config(self, os_mock, io_mock):
        """Should return an dictionary of apps config."""
        os_mock.path.isdir.return_value = True
        os_mock.listdir.return_value = ['path/to/app-1', 'path/to/app-2', 'path/to/app-3']
        os_mock.path.isfile.return_value = True

        def yaml_side_effect(arg):
            if arg == 'path/to/app-1':
                return {'name': 'app-1', 'config_key': 'value for app-1'}
            elif arg == 'path/to/app-2':
                return {'name': 'app-2', 'config_key': 'value for app-2'}
            elif arg == 'path/to/app-3':
                return {'name': 'app-3', 'config_key': 'value for app-3'}

        io_mock.from_yaml.side_effect = yaml_side_effect

        result = config.list_apps_config()
        assert result == {
            'app-1': {'name': 'app-1', 'config_key': 'value for app-1'},
            'app-2': {'name': 'app-2', 'config_key': 'value for app-2'},
            'app-3': {'name': 'app-3', 'config_key': 'value for app-3'}
        }
