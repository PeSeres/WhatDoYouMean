import logging
import datetime
import configargparse

from game_turn import game_turn
from html_generator.html_generator import save_score_table_to_html_file
from src.classes.memento import Memento

from utils.helper import (
    get_random_commit,
    get_attending_players_messages,
    check_authors_percentage_in_commit_messages,
    choose_active_coworkers,
    get_next_message, set_selected_message, get_output_folder,
)
from utils.logging_helper import log_arguments, configure_logging
from utils.readers import read_inputs


def save_info(players, folder_name):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    players.to_csv(f"{folder_name}/save_players_{timestamp}.csv", encoding='utf-8')
    logging.info(f'Log players to save_players_{timestamp}.csv')


def main():
    parser = configargparse.ArgParser(default_config_files=['./myconfig.ini'])
    parser.add_argument('--config-file', required=True, is_config_file=True, help='Config file path')

    # input data
    commit_from = parser.add_mutually_exclusive_group(required=True)
    commit_from.add_argument('--repository-path', help='Path to the GitLab repository (for the commit messages)')
    commit_from.add_argument('--commit-data-txt', help='Path to the txt file what contains the commit messages and '
                                                       'authors.')

    parser.add_argument('--players-csv', help='Path to the csv file what contains the players data.')

    parser.add_argument('--player-name-column-name', help='Name of the column what stores the player names in players '
                                                          'CSV.')
    parser.add_argument('--player-commit-author-id-column-name',
                        help='Name of the column what stores the player commit IDs (username of the email address) in'
                             ' players csv.', required=True)

    # game settings
    parser.add_argument('--choose-random-commit', help='Choose random commit from the commits.', default=True)
    parser.add_argument('--remove-merge-commits-from-commits', help='Remove merge commits from the commit messages.',
                        default=False)

    parser.add_argument('--question-about-the-summary', help='Question about the summary', required=True)
    parser.add_argument('--question-about-the-similarity', help='Question about the similarity', required=True)

    parser.add_argument('--coworkers-count', help='Number of coworkers in the game.', required=True)
    parser.add_argument('--author-percent', help='Percentage in float. How many author should be here?',
                        required=True)

    parser.add_argument('--coworkers-limit', help='Limits for coworkers', required=True)
    parser.add_argument('--coworkers-point', help='Points for coworkers', required=True)

    parser.add_argument('--author-limit', help='Limits for authors', required=True)
    parser.add_argument('--author-point', help='Points for authors', required=True)

    parser.add_argument('--spectators-limit', help='Limits for spectators', required=True)
    parser.add_argument('--spectators-point', help='Points for spectators.', required=True)

    args = parser.parse_args()
    output_folder_name = get_output_folder()

    configure_logging(output_folder_name)

    log_arguments(args)

    players, commit_data = read_inputs(args.players_csv, args.commit_data_txt, args.player_commit_author_id_column_name,
                                       args.player_name_column_name, args.repository_path, output_folder_name,
                                       args.remove_merge_commits_from_commits)

    if check_authors_percentage_in_commit_messages(players, commit_data, float(args.author_percent)):
        commits_for_the_game = get_attending_players_messages(players, commit_data)

    else:
        commits_for_the_game = commit_data

    # log
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    commits_for_the_game.to_csv(f"{output_folder_name}/commits_for_the_game{timestamp}.csv", encoding='utf-8')
    logging.info(f'Log commits_for_the_game to commits_for_the_game{timestamp}.csv')

    memento = Memento(players=players, messages=commits_for_the_game)

    flag = True

    while flag:
        if args.choose_random_commit:
            selected_message = get_random_commit(memento.for_games_messages)
        else:
            selected_message = get_next_message(memento.for_games_messages)

        memento.delete_message(selected_message["message"].values[0])

        commit_for_the_game = set_selected_message(selected_message)
        memento.for_game_players = choose_active_coworkers(memento, commit_for_the_game, int(args.coworkers_count))

        game_turn(commit_for_the_game=commit_for_the_game,
                  question_about_the_summary=args.question_about_the_summary,
                  question_about_the_similarity=args.question_about_the_similarity,
                  author_point=int(args.author_point),
                  author_limit=float(args.author_limit),
                  coworkers_point=int(args.coworkers_point),
                  coworkers_limit=float(args.coworkers_limit),
                  spectators_point=int(args.spectators_point),
                  spectators_limit=float(args.spectators_limit),
                  output_folder_name=output_folder_name,
                  memento=memento,
                  players_csv_path=args.players_csv
                  )
        memento.for_game_players = memento.remove_recent_players_from(memento.for_game_players)

        is_exit = input("If you would like to finish the game type 'exit' in other case type something else:")
        save_info(memento.original_players, output_folder_name)
        if is_exit == "exit":
            save_score_table_to_html_file(memento.original_players, output_folder_name, args.players_csv)
            logging.info("The game is ended: exit")
            flag = False


if __name__ == '__main__':
    main()
