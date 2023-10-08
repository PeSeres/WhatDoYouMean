import logging

import pandas


def set_roles_to_spectators(players):
    players["role"] = "spectator"
    for index, player in players.iterrows():
        logging.info(f"Updated role: {player['player_id']}, {player['role']}, {player['score']}")


def keep_authors_and_coworkers_and_add_spectators(combined_df):
    combined_df = combined_df.drop_duplicates()

    filtered_df = combined_df[combined_df["role"].isin(["author", "coworker"])]

    return filtered_df


class Memento:
    def __init__(self, messages, players):
        self.original_messages = messages.copy()
        self.for_games_messages = messages.copy()
        self.original_players = players.copy()
        self.for_game_players = players.copy()

    def set_saved_scores(self, save_original_players_for_score):
        for index, player in self.original_players.iterrows():
            self.original_players.loc[index, 'score'] = save_original_players_for_score.loc[index, 'score']

    def update_original_players(self):
        save_original_players_for_score = self.original_players.copy()
        set_roles_to_spectators(self.original_players)

        concatenated_players = pandas.concat([self.for_game_players, self.original_players])

        filtered_players = concatenated_players.drop_duplicates(keep='first', subset=['player_id'])

        self.original_players = filtered_players
        self.original_players = self.original_players.reset_index(drop=True).copy()
        self.for_game_players = self.for_game_players.reset_index(drop=True).copy()

        set_roles_to_spectators(save_original_players_for_score)
        for index, row in save_original_players_for_score.iterrows():
            player_id = row['player_id']
            score = row['score']
            self.original_players.loc[self.original_players['player_id'] == player_id, 'score'] = score

    def delete_message(self, message):
        """
        Delete used message from the list of messages.
        """
        self.for_games_messages = self.for_games_messages[self.for_games_messages.message != message]
        if len(self.for_games_messages) == 0:
            self.for_games_messages = self.original_messages

    def remove_recent_players_from(self, players):
        self.for_game_players = players[players['role'] != 'author']
        self.for_game_players = self.for_game_players[self.for_game_players['role'] != 'coworker']
        set_roles_to_spectators(self.for_game_players)
        return self.for_game_players

    def choose_when_have_coworkers(self, original_coworkers_count):
        counter = 0

        for index, player in self.for_game_players.iterrows():
            if player['role'] == 'author' or player['role'] == 'coworker':
                counter += 1
                continue

            if player['role'] != 'author' and player['role'] != 'coworker':
                self.for_game_players.loc[index, 'role'] = 'coworker'
                counter += 1

            if counter == original_coworkers_count:
                break

    def choose_coworkers_if_not_enough(self, coworkers_count):
        save_already_authors_and_coworkers = self.for_game_players.copy()
        save_already_authors_and_coworkers.loc[save_already_authors_and_coworkers['role'] != 'author', 'role'] \
            = 'coworker'

        self.update_original_players()
        self.for_game_players = self.original_players.copy()
        for index, player in save_already_authors_and_coworkers.iterrows():
            if player['role'] == 'author' or player['role'] == 'coworker':
                self.for_game_players.loc[index, 'role'] = player['role']

        self.choose_when_have_coworkers(coworkers_count)
        self.update_original_players()

        for index, player in self.for_game_players.iterrows():
            logging.info(f"Player status: {player['player_id']}, {player['score']}, {player['role']}")
