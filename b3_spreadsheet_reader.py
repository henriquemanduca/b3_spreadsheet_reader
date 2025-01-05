import argparse
import sys

from src.calculate import calculate_spreadsheet


def main():
    help = """
    Usage: python b3_shpeadsheet_reader.py -i sample.xlsx -t Movimentação -f STOCK/REIT/OTHER -o report.csv
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
        help='Filter by type asset',
        required=False
    )

    parser.add_argument(
        "-v", "--verbose",
        help="Add debugging output",
        action="store_true"
    )

    try:
        args = parser.parse_args()
    except SystemExit:
        LOGGER.info(help)
        sys.exit()

    calculate_spreadsheet(args)


if __name__ == "__main__":
    main()
