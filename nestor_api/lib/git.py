import nestor_api.lib.io as io


def clone(repository: str, remote_repository_url: str, branch: str = 'master'):
    return io.execute(f'git clone {remote_repository_url} -b {branch}', repository)


def get_branch_hash(remote_repository_url: str, branch: str):
    return io.execute(f'git ls-remote {remote_repository_url} {branch}')
