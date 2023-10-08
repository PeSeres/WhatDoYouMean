import logging


def remove_merge_commits(commits):
    mask = commits['message'].str.contains('Merge')
    cleaned_commits = commits[~mask]
    logging.info(f'Removed {len(commits) - len(cleaned_commits)} merge commits')

    return cleaned_commits
