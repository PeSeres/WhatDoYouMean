import datetime

import pandas

from src.html_generator.game_page_html_parts import game_page_head_part, game_page_players_table_close_part, \
    game_page_right_panel_head_part, game_page_questions_head_part, game_page_questions_close_part, game_page_close_part
from src.html_generator.score_table_html_parts import score_table_head_part, score_table_tail_part

translation_map = {
    'author': 'szerző',
    'coworker': 'kolléga',
    'spectator': 'megfigyelő',
}


def generate_html_filename(supplement=""):
    if supplement != "":
        supplement = "_" + supplement
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"what_do_you_mean{supplement}_{timestamp}.html"


def generate_player_list(players):
    player_list = []
    for index, player in players.iterrows():
        player_list.append((player["player_id"], player["role"], player["score"]))
    return player_list


def separate_the_players(players):
    authors_coworkers_players = players[players['role'].isin(['author', 'coworker'])]
    spectator_players = players[players['role'] == 'spectator']
    return authors_coworkers_players, spectator_players


def make_ranks_for_the_players(players_data):
    players_data_copy = players_data.copy()
    players_data_copy.loc[:, 'rank'] = players_data_copy.loc[:, 'score'].rank(method='dense', ascending=False).astype(
        int)

    ranked_and_sorted_players = players_data_copy.sort_values(by='rank')
    return ranked_and_sorted_players


def save_score_table_to_html_file(original_players, folder_name, players_path):
    players = add_name_column_to_players(original_players, players_path)
    players = make_ranks_for_the_players(players)

    html = score_table_head_part + generate_score_table(players) + score_table_tail_part

    file_name = generate_html_filename("score_table")
    with open(folder_name + "/" + file_name, "w", encoding='utf-8') as f:
        f.write(html)


def generate_score_table(players):
    name_column = set_name_column(players)
    if name_column == "player_name":
        html = f"""
        <table>
            <tr>
                <th>Helyezés</th>
                <th>Játékos név</th>
                <th>Játékos ID</th>
            </tr>
        """
        for index, player in players.iterrows():
            html += f"""
            <tr>
                <td>{player["rank"]}</td>
                <td>{player["player_name"]}</td>
                <td>{player["player_id"]}</td>
            </tr>
            """
        html += """
        </table>
        """
    else:
        html = f"""
        <table>
            <tr>
                <th>Helyezés</th>
                <th>Játékos</th>
            </tr>
        """
        for index, player in players.iterrows():
            html += f"""
            <tr>
                <td>{player["rank"]}</td>
                <td>{player["player_id"]}</td>
            </tr>
            """
        html += """
        </table>
        """
    return html


def read_players_csv(players_csv_path):
    players = pandas.read_csv(players_csv_path, sep=';')
    return players


def add_name_column_to_players(players, players_csv_path):
    players_with_name = read_players_csv(players_csv_path)
    if 'player_name' in players_with_name.columns and 'player_name' not in players.columns:
        merged_players = players.merge(players_with_name, on='player_id')
    else:
        merged_players = players
    return merged_players


def set_name_column(players):
    name_column = 'player_id'
    if 'player_name' in players.columns:
        name_column = 'player_name'
    return name_column


def generate_html_page(memento, message, folder_name, question_about_the_similarity, question_about_the_summary_list,
                       players_csv_path):
    if "player_name" not in memento.original_players.columns:
        players = add_name_column_to_players(memento.original_players, players_csv_path)
        players = make_ranks_for_the_players(players)
    else:
        players = make_ranks_for_the_players(memento.original_players)

    authors_coworkers_players_sorted, spectator_players_sorted = separate_the_players(players)

    name_column = set_name_column(players)

    html = game_page_head_part

    for index, row in players.iterrows():
        if row['role'] == "author" or row['role'] == "coworker":
            html += f"""
                    <tr class="coworker">
                        <td>{row['rank']}</td>
                        <td>{row[name_column]}</td>
                        <td>{translation_map[row['role']]}</td>
                    </tr>
        """
        else:
            html += f"""
                        <tr>
                            <td>{row['rank']}</td>
                            <td>{row[name_column]}</td>
                            <td>{translation_map[row['role']]}</td>
                        </tr>
            """

    html += game_page_players_table_close_part + game_page_right_panel_head_part

    players_str = ""
    for index, row in authors_coworkers_players_sorted.iterrows():
        players_str += f"{row[name_column]}, "

    html += f"""
                <p>{players_str[:-2]}</p>
            </details>
    """
    html += game_page_questions_head_part
    for question in question_about_the_summary_list:
        html += f"""
                   <div class="question-container">
                       <p>{question}</p>
                   </div>
           """

    html += game_page_questions_close_part

    if message.repository:
        html += f"""
                   <div class="message-box">
                       <p id="commit-title">Üzenet:</p>
                       <p id="commit-message">{message.message}</p>
                       <p id="commit-repository">Projekt: {message.repository}</p>
                   </div>

                   """
    else:
        html += f"""
           <div class="message-box">
               <p id="commit-title">Üzenet:</p>
               <p id="commit-message">{message.message}</p>
           </div>

           """

    html += f"""
           <details>
               <summary>Kérdés a pontozáshoz</summary>
               <div class="question-container">
               <p>{question_about_the_similarity}</p>
               </div>
           </details>
       </div>
       """
    html += game_page_close_part

    file_name = generate_html_filename()
    with open(folder_name + "/" + file_name, "w", encoding='utf-8') as f:
        f.write(html)

    return folder_name + "/" + file_name
