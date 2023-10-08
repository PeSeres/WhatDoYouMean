import datetime
import logging
import pandas

from utils.get_commits_data_from_git import get_git_commit_log
from utils.helper import strip_dataframe, create_data_frame_from_git_log
from utils.commits_cleaner import remove_merge_commits


def read_players_data(players_csv, player_id_colum_name, player_name_column_name):
    players_read = pandas.read_csv(players_csv, encoding='utf-8', header=0, delimiter=',')
    players = strip_dataframe(players_read)
    players = pandas.concat([players, pandas.Series([0] * len(players), name='score')], axis=1)
    players = pandas.concat([players, pandas.Series(["spectator"] * len(players), name='role')], axis=1)
    players.rename(columns={player_id_colum_name: 'player_id'}, inplace=True)
    if player_name_column_name:
        players.rename(columns={player_name_column_name: 'player_name'}, inplace=True)
    return players


def read_commit_data_from_txt(commit_data_txt):
    column_names = ["hash", "author", "message", "repository"]
    commit_data = pandas.read_csv(commit_data_txt, sep=';', header=None, names=column_names)
    commit_data = strip_dataframe(commit_data)
    return commit_data


def read_inputs(players_csv, commit_data_txt, player_id_colum_name, player_name_column_name, repo_path, folder_name,
                remove_merge_commits_from_commits):

    players = read_players_data(players_csv, player_id_colum_name, player_name_column_name)

    players = players.rename(columns={player_id_colum_name: 'player_id'})

    logging.info('Read data from file: {}'.format(players_csv))
    for index, player in players.iterrows():
        logging.info("Player_ID:" + player["player_id"])

    if commit_data_txt:
        commit_data = read_commit_data_from_txt(commit_data_txt)
    else:
        git_commit_log = get_git_commit_log(repo_path)
        commit_data = create_data_frame_from_git_log(git_commit_log)

    if remove_merge_commits_from_commits:
        commit_data = remove_merge_commits(commit_data)

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    commit_data.to_csv(f"{folder_name}/commits_log_{timestamp}.csv", encoding='utf-8')
    logging.info(f'Log commit_data to commits_log_{timestamp}.csv')

    return players, commit_data
