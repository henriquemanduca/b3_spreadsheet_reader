import pandas as pd
import logging
import sys

from src.exceptions.exceptions import DataFrameError

from src.utils.utils import get_logger
from src.service.calculate import read_operations
from src.service.printer import print_assets_csv


def import_spreadsheet(**kwargs):
    if kwargs.get('verbose'):
        get_logger().setLevel(logging.DEBUG)

    try:
        input_file = kwargs.get('input')
        sheet = kwargs.get('sheet')
        data_frame = pd.read_excel(input_file, sheet_name=sheet)
    except Exception as e:
        get_logger().error(f"Error on load data from file!\n{e}")
        sys.exit()

    try:
        filter_type = kwargs.get('filter')
        wallet = read_operations(data_frame, filter_type)
    except DataFrameError as e:
        get_logger().error(f"{e}")
        sys.exit()
    except Exception as e:
        get_logger().error(f"Error on read operations from dataframe!\n{e}")
        sys.exit()

    try:
        output_file = kwargs.get('output')
        print_assets_csv(output_file, wallet)
    except IOError as e:
        get_logger().error(f"Error on printing to csv!\n{e}")
        sys.exit()

    get_logger().info(f"Report saved on {output_file}")
