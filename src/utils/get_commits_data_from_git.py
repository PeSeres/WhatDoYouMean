import subprocess
import os


def get_project_name(repo_path):
    project_name = os.path.basename(repo_path)
    return project_name


def get_git_commit_log(repo_path):
    try:
        project_name = get_project_name(repo_path)
        git_command = f'git log --all --pretty=format:"%h;; %al;; %s;; {project_name}" '
        git_commit_log = subprocess.run(git_command, capture_output=True, cwd=repo_path)
        commit_log = git_commit_log.stdout.decode('utf-8')
        return commit_log
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error running Git command: {e}") from e
