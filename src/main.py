import pandas as pd
import sys

from src.exceptions.exceptions import DataFrameError

from src.utils.utils import get_logger
from src.service.config_service import ConfigService
from src.service.calculate_service import CalculateService
from src.service.printer_service import PrinterService


def import_spreadsheet(**kwargs):
    config = ConfigService()
    service = CalculateService(config=config)
    printer = PrinterService(config=config)

    try:
        input_file = kwargs.get('input')
        sheet = kwargs.get('sheet')
        data_frame = pd.read_excel(input_file, sheet_name=sheet)
    except Exception as e:
        get_logger().error(f"Error on load data from file!\n{e}")
        sys.exit()

    try:
        filter_type = kwargs.get('filter')
        wallet = service.read_operations(data_frame, filter_type)
    except DataFrameError as e:
        get_logger().error(f"{e}")
        sys.exit()
    except Exception as e:
        get_logger().error(f"Error on read operations from dataframe!\n{e}")
        sys.exit()

    try:
        output_file = kwargs.get('output')
        printer.print_assets_csv(output_file, wallet)
    except IOError as e:
        get_logger().error(f"Error on printing to csv!\n{e}")
        sys.exit()

    get_logger().info(f"Report saved on {output_file}")
