from unittest.mock import patch

import nestor_api.lib.git as git


class TestGit:
    @patch('nestor_api.lib.git.io', autospec=True)
    def test_clone(self, io_mock):
        """Should send the right command to io lib."""
        git.clone('some/path', 'ssh://some-external-address/project.git', 'step-1')
        io_mock.execute.assert_called_once_with('git clone ssh://some-external-address/project.git -b step-1',
                                                'some/path')

    @patch('nestor_api.lib.git.io', autospec=True)
    def test_clone_with_default_branch(self, io_mock):
        """Should send the right command to io lib using master as default branch."""
        git.clone('some/path', 'ssh://some-external-address/project.git')
        io_mock.execute.assert_called_once_with('git clone ssh://some-external-address/project.git -b master',
                                                'some/path')

    @patch('nestor_api.lib.git.io', autospec=True)
    def test_get_branch_hash(self, io_mock):
        """Should send the right command to io lib."""
        git.get_branch_hash('ssh://some-external-address/project.git', 'master')
        io_mock.execute.assert_called_once_with('git ls-remote ssh://some-external-address/project.git master')
