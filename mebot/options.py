import argparse

parser = argparse.ArgumentParser(description='Runs mebot :-). Message yourself!')

parser.add_argument('--log-level',
    help="Sets the logging level",
    choices=["INFO", "DEBUG", "WARNING", "ERROR"],
    default="INFO")

cli_args = parser.parse_args()