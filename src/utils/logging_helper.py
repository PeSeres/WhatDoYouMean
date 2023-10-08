import logging
from datetime import datetime


def configure_logging(folder_name: str):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = f'{folder_name}/what_do_you_mean_{timestamp}.log'
    logging.basicConfig(level=logging.INFO,
                        filename=log_filename,
                        format="%(asctime)s %(levelname)s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S"
                        )


def log_arguments(args):
    for argument in vars(args):
        logging.info(f"Argparse: {argument}: {getattr(args, argument)}")


def log_players(players):
    for player in players:
        logging.info(f"{player['player_id']}, {player['role']}, {player['score']}")
