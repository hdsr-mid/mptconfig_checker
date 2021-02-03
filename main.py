from meetpuntconfig.config import MeetpuntConfig

import logging
import sys


def check_python_version():
    major = sys.version_info.major
    minor = sys.version_info.minor
    minor_min = 6
    minor_max = 9
    if major == 3 and minor_min <= minor <= minor_max:
        return
    raise AssertionError(f"your python version = {major}.{minor}. Please use python 3.{minor_min} to 3.{minor_max}")


def setup_logging() -> None:
    """Adds a configured strearm handler to the root logger."""
    log_level = logging.INFO
    log_date_format = "%H:%M:%S"
    log_format = "%(asctime)s %(filename)s %(levelname)s %(message)s"

    _logger = logging.getLogger()
    _logger.setLevel(log_level)
    formatter = logging.Formatter(fmt=log_format, datefmt=log_date_format)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)
    _logger.addHandler(stream_handler)


if __name__ == "__main__":
    check_python_version()
    setup_logging()

    # run checks
    meetpunt_config = MeetpuntConfig()
    meetpunt_config.check_idmap_sections()
    meetpunt_config.check_ignored_hist_tags()
    meetpunt_config.check_missing_hist_tags()
    meetpunt_config.check_double_idmaps()
    meetpunt_config.hist_tags_to_mpt()
    meetpunt_config.check_missing_pars()
    meetpunt_config.check_hloc_consistency()
    meetpunt_config.check_expar_errors_intloc_missing()
    meetpunt_config.check_expar_missing()
    meetpunt_config.check_exloc_intloc_consistency()
    meetpunt_config.check_timeseries_logic()
    meetpunt_config.check_validation_rules()
    meetpunt_config.check_intpar_expar_consistency()
    meetpunt_config.check_location_set_errors()

    # write excel file
    meetpunt_config.write_excel()

    # write csv files
    meetpunt_config.write_csvs()
