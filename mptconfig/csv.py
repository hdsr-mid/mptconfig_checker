# from mptconfig.excel import ExcelSheetCollector
# from mptconfig.fews_utilities import FewsConfig
# from typing import List
# import pandas as pd
#
# class CsvWriter:
#
#     def __init__(self, csvs: List[pd.DataFrame]
#         self.csvs = csvs
#
#         assert isinstance(self.csvs, ExcelSheetCollector), "results is not a ExcelSheetCollector"
#         assert self.results.output_no_check_sheets, "cannot create excel file if no sheets exists"
#
#     def validate_constructor(self):
#         for csv in self.csv:
#             assert isinstance(csv, pd.DataFrame)
#
#     def write(self):
#         csv_file = self.paths["csv_out"].joinpath(
#             self.fews_config.locationSets[value["id"]]["csvFile"]["file"]
#         )
#         if csv_file.suffix == "":
#             csv_file = Path(f"{csv_file}.csv")
#         df.to_csv(csv_file, index=False)
