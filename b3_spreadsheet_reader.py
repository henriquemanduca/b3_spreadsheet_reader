import argparse
import logging
import sys

from src.calculate import calculate_spreadsheet

logging.basicConfig()
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def main():
    help = """
    Usage: python b3_shpeadsheet_reader.py -i sample.xlsx -t Movimentação -o report.txt
    or python b3_shpeadsheet_reader.py -t Movimentação
    """

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-i', '--input',
        type=str,
        help='Input spreadsheet file (xlsx)',
        required=False
    )

    parser.add_argument(
        '-t', '--sheet',
        type=str,
        help='Inside tab sheet',
        required=True
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output file',
        required=False
    )

    parser.add_argument(
        '-f', '--filter',
        type=str,
        help='Filter by code asset',
        required=False
    )

    try:
        args = parser.parse_args()
    except SystemExit:
        LOGGER.info(help)
        sys.exit()

    calculate_spreadsheet(args)


if __name__ == "__main__":
    main()
