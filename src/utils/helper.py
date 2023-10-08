import os
import numpy
import pandas
import random
import logging

from datetime import datetime
from pandas import DataFrame

from src.classes.commit_for_the_game import CommitForTheGame


def create_data_frame_from_git_log(git_log):
    rows = git_log.strip().split("\n")

    data = [row.split(";; ") for row in rows]

    column_names = ["hash", "author", "message", "repository"]
    commit_data = pandas.DataFrame(data, columns=column_names)
    commit_data_stripped = strip_dataframe(commit_data)

    return commit_data_stripped


def strip_dataframe(dataframe):
    stripped_df = dataframe.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    return stripped_df


def get_list_of_player_ids(players):
    return list(players['player_id'])


def get_random_commit(commit_data):
    """
    This function takes a pandas DataFrame as input and returns a random row from the DataFrame.
    """
    num_rows = commit_data.shape[0]
    random_index = numpy.random.randint(low=0, high=num_rows)
    random_row = commit_data.sample(n=1, random_state=random_index)

    return random_row


def get_next_message(commit_data):
    """
    This function takes a pandas DataFrame as input and returns the first row from the DataFrame.
    """
    first_row = commit_data.iloc[0]
    return first_row.to_frame().transpose()


def get_attending_players_messages(players, commit_data):
    player_id = get_list_of_player_ids(players)
    selected_rows = []

    for index, row in commit_data.iterrows():
        if row["author"] in player_id:
            selected_rows.append(row)

    selected_commits = pandas.DataFrame(selected_rows)
    return selected_commits


def get_output_folder():
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    folder_name = f"output_{timestamp}"
    os.makedirs(folder_name)

    return folder_name


def get_valid_integer_input(prompt):
    while True:
        try:
            user_input = input(prompt)
            integer_input = int(user_input)
            return integer_input
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def get_random_coworkers(memento, count: int, commit_author: str = None):
    indices_list = memento.for_game_players.index.tolist()

    if commit_author is not None:
        indices_list.remove(find_commit_author_index(memento.for_game_players, commit_author))

    random_indices = []
    while len(random_indices) < count:
        index = numpy.random.choice(indices_list)
        if index not in random_indices:
            random_indices.append(index)

    memento.for_game_players.loc[random_indices, 'role'] = 'coworker'

    if commit_author is not None:
        memento.for_game_players.loc[memento.for_game_players["player_id"] == commit_author, 'role'] = 'author'

    memento.update_original_players()

    return memento.for_game_players


def original_get_random_coworkers(players: DataFrame, count: int, commit_author: str = None):
    if commit_author:
        ids = players.loc[:, "player_id"].to_list()
        ids = [item for item in ids if item != commit_author]
        selected_coworkers = random.sample(ids, k=count)

    else:
        ids = players.loc[:, "player_id"].to_list()
        selected_coworkers = random.sample(ids, k=count)

    players.loc[players['player_id'].isin(selected_coworkers), 'role'] = 'coworker'


def find_commit_author_index(players: DataFrame, commit_author: str):
    return players[players['player_id'] == commit_author].index[0]


def choose_active_coworkers(memento, game_commit, coworkers_count):
    set_role_to_spectator(memento.for_game_players)
    set_role_to_spectator(memento.original_players)

    commit_author = game_commit.author

    original_players_ids = get_list_of_player_ids(memento.original_players)
    for_games_players_ids = get_list_of_player_ids(memento.for_game_players)

    if commit_author in original_players_ids and commit_author not in for_games_players_ids:
        for index, row in memento.original_players.iterrows():
            if row['player_id'] == commit_author:
                row['role'] = 'spectator'
                memento.for_game_players = pandas.concat([memento.for_game_players, row.to_frame().T], axis=0)
                break

    if commit_author in get_list_of_player_ids(memento.for_game_players):
        memento.for_game_players.loc[memento.for_game_players["player_id"] == commit_author, 'role'] = 'author'
        if len(memento.for_game_players) < coworkers_count:
            memento.choose_coworkers_if_not_enough(coworkers_count)
        else:
            memento.for_game_players = get_random_coworkers(memento, coworkers_count - 1, commit_author)
    else:
        if len(memento.for_game_players) < coworkers_count:
            memento.choose_coworkers_if_not_enough(coworkers_count)
        else:
            memento.for_game_players = get_random_coworkers(memento, coworkers_count)

    for _, player in memento.for_game_players.iterrows():
        logging.info(f"Player status: {player['player_id']}, {player['score']}, {player['role']}")

    check_players(memento, coworkers_count)
    return memento.for_game_players


def check_players(memento, arg_count):
    check_players_counter = 0
    for index, row in memento.for_game_players.iterrows():
        if row["role"] != 'spectator':
            check_players_counter += 1
    if check_players_counter != arg_count:
        set_role_to_spectator(memento.for_game_players)
        set_role_to_spectator(memento.original_players)
        have_enough_coworkers = 0
        for index, row in memento.for_game_players.iterrows():
            if have_enough_coworkers < arg_count:
                memento.for_game_players.at[index, 'role'] = 'coworker'
                have_enough_coworkers += 1
        memento.update_original_players()


def check_authors_percentage_in_commit_messages(players, commit_data, authors_percentage):
    all_authors_in_commits = set(commit_data['author'])

    attending_authors_mask = players['player_id'].isin(commit_data['author'])
    attending_authors = attending_authors_mask.sum()

    percentage = attending_authors / len(all_authors_in_commits)
    authors_percentage_in_commit_messages_is_bigger_than_limit = percentage >= authors_percentage
    logging.info("Authors percentage in commit message is bigger than limit:" +
                 str(authors_percentage_in_commit_messages_is_bigger_than_limit))
    return authors_percentage_in_commit_messages_is_bigger_than_limit


def set_role_to_spectator(df):
    for index, row in df.iterrows():
        df.at[index, 'role'] = 'spectator'


def set_selected_message(selected_message):
    if "repository" in selected_message.columns:
        logging.info(f"selected_message: "
                     f"{selected_message['hash'].iloc[0]}, "
                     f"{selected_message['author'].iloc[0]}, "
                     f"{selected_message['message'].iloc[0]}"
                     f"{selected_message['repository'].iloc[0]}"
                     )
        commit_for_the_game = CommitForTheGame(message=selected_message["message"].iloc[0],
                                               author=selected_message["author"].iloc[0],
                                               repository=selected_message["repository"].iloc[0]
                                               )
    else:
        logging.info(f"selected_message: "
                     f"{selected_message['hash'].iloc[0]}, "
                     f"{selected_message['author'].iloc[0]}, "
                     f"{selected_message['message'].iloc[0]}"
                     )
        commit_for_the_game = CommitForTheGame(message=selected_message["message"].iloc[0],
                                               author=selected_message["author"].iloc[0])

    return commit_for_the_game
