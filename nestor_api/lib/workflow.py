import nestor_api.lib.config as config
import nestor_api.lib.git as git


def get_ready_to_progress_apps(next_step: str) -> dict:
    # Copy the configuration to ensure strict isolation
    config_dir = config.get_configuration_copy_path()
    config.change_environment(next_step, config_dir)
    project_config = config.for_project(config_dir)
    previous_step = config.get_previous_step(project_config, next_step)
    apps = config.list_apps_config()

    return {
        app_name: is_app_ready_to_progress(app_config['git']['origin'], previous_step, next_step)
        for (app_name, app_config) in apps.items()
    }


def is_app_ready_to_progress(repository_url: str, current_step: str, next_step: str) -> bool:
    """Determines if an app can be advanced to the next step."""
    return compare_step_hashes(repository_url, current_step, next_step)


def compare_step_hashes(repository_url: str, branch1: str, branch2: str) -> bool:
    """Compare branches hashes and return True if they are the sames, False otherwise."""
    branch1_hash = git.get_branch_hash(repository_url, branch1)
    branch2_hash = git.get_branch_hash(repository_url, branch2)
    return branch1_hash == branch2_hash
