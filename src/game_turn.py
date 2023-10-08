import logging
from enum import Enum

from html_generator.html_generator import generate_html_page
from utils.helper import get_valid_integer_input


class Role(Enum):
    AUTHOR = "author"
    SPECTATOR = "spectator"
    COWORKER = "coworker"


def reward_punish_players(*, players, role, limit, point, good_votes_percentage):
    if (1 - limit) < good_votes_percentage:
        players.loc[players['role'] == role.value, 'score'] += int(point)
    elif limit > good_votes_percentage:
        players.loc[players['role'] == role.value, 'score'] -= int(point)

    logging.info(f"{role.value} good_votes_percentage {good_votes_percentage}")
    for _, player in players.iterrows():
        logging.info(f"Point after updating {role.value} points: {player['player_id']}, {player['role']}, {player['score']}")


def agreement_scoring_spectators(*, players, good_votes_percentage, limit, point):
    bad_votes_percentage = 1 - good_votes_percentage

    agreement_percentage = max(good_votes_percentage, bad_votes_percentage)
    agreement_percentage_normalized = (agreement_percentage - 0.5) * 2
    logging.info(f"Spectators agreements: {agreement_percentage}")

    # calculate_agreement
    if agreement_percentage_normalized == 1:
        logging.info("Spectators agreement was 100%")
        return  # in this case spectators don't get points

    reward_punish_players(players=players, role=Role.SPECTATOR, limit=limit, point=point,
                          good_votes_percentage=agreement_percentage_normalized)


def set_roles_to_spectators(players):
    players.loc[:, "role"] = "spectator"
    for index, player in players.iterrows():
        logging.info(f"Updated role: {player['player_id']}, {player['role']}, {player['score']}")


def calculate_spectator_percentage(players, good_votes):
    number_of_spectators = players["role"].value_counts()["spectator"]
    good_votes_percentage = good_votes / number_of_spectators

    logging.info(f"good_votes_percentage? {good_votes_percentage}")

    return good_votes_percentage


def game_turn(*, commit_for_the_game, question_about_the_summary, question_about_the_similarity,
              coworkers_limit, coworkers_point, author_limit, players_csv_path,
              author_point, spectators_limit, spectators_point, output_folder_name, memento):

    question_about_the_summary_list = question_about_the_summary.split("| ")
    html_path = generate_html_page(memento,
                                   commit_for_the_game,
                                   output_folder_name,
                                   question_about_the_similarity,
                                   question_about_the_summary_list,
                                   players_csv_path
                                   )

    print(f"Open the new HTML file: {html_path}")
    input("Ask the questions from the summary. (You can find the questions in the HTML file, \nunder the What do you "
          "mean? and above the commit message.) \nAfter you asked the questions press an enter. ")

    print("Ask the similarity question (under the commit message) from the spectators.\nAfter that count how many "
          "spectator votes with 'yes' and type it. ")

    good_answers_from_spectators = get_valid_integer_input("How many spectators raised their hands? ")
    logging.info(f"How many spectators raised their hands? {good_answers_from_spectators}")

    good_votes_percentage = calculate_spectator_percentage(memento.original_players, int(good_answers_from_spectators))

    reward_punish_players(players=memento.original_players, role=Role.COWORKER, limit=coworkers_limit,
                          point=coworkers_point,
                          good_votes_percentage=good_votes_percentage)

    reward_punish_players(players=memento.original_players, role=Role.AUTHOR, limit=coworkers_limit,
                          point=coworkers_point,
                          good_votes_percentage=good_votes_percentage)

    reward_punish_players(players=memento.original_players, role=Role.AUTHOR, limit=author_limit, point=author_point,
                          good_votes_percentage=good_votes_percentage)

    agreement_scoring_spectators(players=memento.original_players, good_votes_percentage=good_votes_percentage,
                                 limit=spectators_limit,
                                 point=spectators_point)
