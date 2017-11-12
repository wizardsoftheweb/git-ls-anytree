from mock import patch

def test_main():
    with patch('git_ls_anytree.cli_file.cli') as mock_cli:
        import git_ls_anytree.__main__
        mock_cli.assert_called_once_with()
