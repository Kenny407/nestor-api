from unittest.mock import patch, call

import nestor_api.lib.workflow as workflow


class TestWorkflow:
    @patch('nestor_api.lib.workflow.git')
    def test_compare_unequal_step_hashes(self, git_mock):
        """Should return False when step hashes are unequal."""
        git_mock.get_branch_hash.side_effect = ['hash-1', 'hash-2']
        result = workflow.compare_step_hashes('repository_url', 'step-1', 'step-2')
        assert git_mock.get_branch_hash.call_count == 2
        git_mock.get_branch_hash.assert_has_calls([
            call('repository_url', 'step-1'),
            call('repository_url', 'step-2')
        ])
        assert result is False

    @patch('nestor_api.lib.workflow.git')
    def test_compare_equal_step_hashes(self, git_mock):
        """Should return True when step hashes are equal."""
        git_mock.get_branch_hash.side_effect = ['hash-1', 'hash-1']
        result = workflow.compare_step_hashes('repository_url', 'step-1', 'step-2')
        assert git_mock.get_branch_hash.call_count == 2
        git_mock.get_branch_hash.assert_has_calls([
            call('repository_url', 'step-1'),
            call('repository_url', 'step-2')
        ])
        assert result is True

    @patch('nestor_api.lib.workflow.compare_step_hashes')
    def test_is_app_ready_to_progress(self, compare_step_hashes_mock):
        """Should forward to compare_step_hashes."""
        compare_step_hashes_mock.return_value = True
        workflow.is_app_ready_to_progress('repository-url', 'step-1', 'step-2')
        compare_step_hashes_mock.assert_called_once_with('repository-url', 'step-1', 'step-2')

    @patch('nestor_api.lib.workflow.is_app_ready_to_progress')
    @patch('nestor_api.lib.workflow.config', autospec=True)
    def test_get_ready_to_progress_apps(self, config_mock, is_app_ready_to_progress_mock):
        """Should return a dict with app name as key and
        boolean for ability to progress as value."""
        # Mocks
        config_mock.get_configuration_copy_path.return_value = 'config-path'
        config_mock.get_previous_step.return_value = 'step-1'
        config_mock.for_project.return_value = {'some': 'config'}
        config_mock.list_apps_config.return_value = {
            'app1': {'name': 'app1', 'git': {'origin': 'fake-remote-url-1'}},
            'app2': {'name': 'app2', 'git': {'origin': 'fake-remote-url-2'}},
            'app3': {'name': 'app2', 'git': {'origin': 'fake-remote-url-3'}},
        }
        is_app_ready_to_progress_mock.return_value = True

        result = workflow.get_ready_to_progress_apps('step-2')

        # Assertions
        config_mock.change_environment.assert_called_once_with('step-2', 'config-path')
        config_mock.for_project.assert_called_once_with('config-path')
        config_mock.get_previous_step.assert_called_once_with({'some': 'config'}, 'step-2')
        assert result == {'app1': True, 'app2': True, 'app3': True}
