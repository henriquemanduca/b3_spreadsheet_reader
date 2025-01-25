import argparse
import sys
import logging

from src.utils.utils import get_logger
from src.main import import_spreadsheet


def main():
    help = """
    Usage: python b3_shpeadsheet_reader.py -i sample.xlsx -t Movimentação -f STOCK/REIT/OTHER -o b3_sheet_report.csv
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

    parser.add_argument(
        "--no-cache",
        help="Force new data",
        action="store_true"
    )

    try:
        args = parser.parse_args()
    except SystemExit:
        get_logger().info(help)
        sys.exit()

    if args.verbose:
        get_logger().setLevel(logging.DEBUG)

    sheet = args.sheet if args.sheet else 'Movimentação'
    input_file = args.input if args.input else 'sample.xlsx'
    output_file = args.output if args.output else 'b3_sheet_report.csv'
    filter_type = args.filter if args.filter else None
    no_cache = args.no_cache

    import_spreadsheet(input=input_file, output=output_file, sheet=sheet, filter=filter_type, no_cache=no_cache)


if __name__ == "__main__":
    main()
