from enum import Enum
from mptconfig import constants
from openpyxl import worksheet as openpyxl_worksheet
from openpyxl.utils import get_column_letter
from pandas.api.types import is_datetime64_any_dtype as is_datetime  # noqa pandas comes with geopandas
from typing import Dict
from typing import List

import logging
import pandas as pd  # noqa pandas comes with geopandas


logger = logging.getLogger(__name__)


class ExcelSheetTypeChoices(Enum):
    input = "input"
    output = "output"


class ExcelTabColorChoices(Enum):
    red = "00FF0000"
    blue = "000000FF"
    green = "0000FF00"
    white = "00000000"


class ExcelSheet:
    def __init__(self, name: str, description: str, data: pd.DataFrame, sheet_type: ExcelSheetTypeChoices):
        self.name = name
        self.description = description
        self.data = data
        self.sheet_type = sheet_type
        self.validate_constructor()
        self.set_sheet_index()

    @property
    def column_names(self) -> pd.Index:
        return self.data.columns

    @property
    def tab_color(self) -> ExcelTabColorChoices:
        if self.sheet_type == ExcelSheetTypeChoices.input:
            return ExcelTabColorChoices.blue
        assert self.sheet_type == ExcelSheetTypeChoices.output, "we expected sheet type to be SheetType.output "
        if len(self.data) > 0:
            # at least one row means at least one error found
            return ExcelTabColorChoices.red
        return ExcelTabColorChoices.green

    @property
    def nr_rows(self) -> int:
        return len(self.data)

    def validate_constructor(self) -> None:
        assert isinstance(self.name, str)
        assert (
            2 < len(self.name) < 25
        ), f"sheet name '{self.name}' with length {len(self.name)} must be between 2 and 25 chars"
        assert isinstance(self.description, str)
        assert (
            10 < len(self.description) < 200
        ), f"sheet description with length {len(self.description)} must be between 10 and 200 chars"
        assert isinstance(
            self.data, pd.DataFrame
        ), f"sheet name {self.name} data is no pd.DataFrame bu {type(self.data)}"
        assert isinstance(self.sheet_type, ExcelSheetTypeChoices)

    def set_sheet_index(self) -> None:
        """Enforce uniform index type on all sheets, so that when creating excel we
        can do pd.to_excel(index=False) resulting in same first column"""
        if self.nr_rows == 0:
            return
        # TODO: fix (reset_index()) index of new_mpt
        if self.name == "new_mpt":
            return
        if not isinstance(self.data.index, pd.Int64Index):
            raise AssertionError(f"sheet {self.name} index must be a Int64Index, not type {type(self.data.index)}")
        self.data.reset_index(inplace=True, drop=True)

    def to_content_dict(self) -> Dict:
        return {
            "name": self.name,
            "type": self.sheet_type.value,
            "nr_rows": self.nr_rows,
            "description": self.description,
        }


class ExcelSheetCollector(dict):
    def __init__(self):
        super().__init__()

    def __getitem__(self, key: str) -> ExcelSheet:
        if key not in self:
            raise AttributeError(f"No sheet with name: {key}")
        return super().__getitem__(key)

    def __setitem__(self, key: str, value: ExcelSheet) -> None:
        assert isinstance(value, ExcelSheet), "value must be an instance of ExcelSheet"
        assert key == value.name, f"key must equal value.name. We advise you to use public method 'add_sheet()'"
        assert key not in self, f"sheet with name '{key}' already exists. Must be unique"
        super().__setitem__(key, value)

    def __delitem__(self, key: str) -> None:
        if key not in self:
            raise AttributeError(f"No sheet with name '{key}'. Delete is not possible")
        super().__delitem__(key)

    def add_sheet(self, excelsheet: ExcelSheet) -> None:
        assert isinstance(excelsheet, ExcelSheet), "excelsheet is not an instance of ExcelSheet"
        self.__setitem__(key=excelsheet.name, value=excelsheet)

    @property
    def sheet_names(self) -> List[str]:
        return list(self.keys())

    @property
    def has_sheets(self) -> bool:
        return True if self.keys() else False

    @property
    def input_sheets(self) -> List[pd.DataFrame]:
        if not self.has_sheets:
            return []
        return [sheet for sheet in self.values() if sheet.sheet_type == ExcelSheetTypeChoices.output]

    @property
    def output_sheets(self) -> List[pd.DataFrame]:
        if not self.has_sheets:
            return []
        return [sheet for sheet in self.values() if sheet.sheet_type == ExcelSheetTypeChoices.output]


class ExcelWriter:
    def __init__(self, results: ExcelSheetCollector):
        self.results = results
        assert isinstance(self.results, ExcelSheetCollector), f"results is not a ExcelSheetCollector"
        assert self.results.has_sheets, f"cannot create excel file if no sheets exists"

    def _get_content_df(self) -> pd.DataFrame:
        """Create panda dataframe based on all ExcelSheet objects included in ExcelSheetCollector (self.results).
        This content df has columns (ExcelSheet objects): "name", "type", "nr_rows", "description"."""
        assert self.results.has_sheets
        columns = self.results.input_sheets[0].to_content_dict().keys()
        data = []
        for sheet in self.results.input_sheets + self.results.output_sheets:
            assert isinstance(sheet, ExcelSheet)
            data.append(sheet.to_content_dict())
        return pd.DataFrame(columns=columns, data=data)

    def _set_sheet_style(self, worksheet: openpyxl_worksheet, tab_color: ExcelTabColorChoices = None) -> None:
        if tab_color:
            worksheet.sheet_properties.tabColor = tab_color.value
        worksheet.auto_filter.ref = worksheet.dimensions
        self.__auto_fit_column_size(worksheet=worksheet)

    @staticmethod
    def __as_text(value):
        if value is None:
            return ""
        return str(value)

    def __auto_fit_column_size(self, worksheet: openpyxl_worksheet) -> None:
        minimal_cell_width = 13
        for column_cells in worksheet.columns:
            len_longest_str = max(len(self.__as_text(value=cell.value)) for cell in column_cells)
            new_width = max(minimal_cell_width, len_longest_str)
            column_letter = get_column_letter(column_cells[0].column)
            worksheet.column_dimensions[column_letter].width = float(new_width)

    def write(self):
        """Write each ExcelSheet object in ExcelSheetCollector to a separate sheet in one excel file."""
        # TODO: added jinja2 as dependency, but it does not work on excel, so remove it from env

        # create and load xlsx file
        result_xlsx_path = constants.PathConstants.result_xlsx.path
        logger.info(f"creating result file {result_xlsx_path}")
        # TODO: activate this assert
        # assert not result_xlsx_path.exists(), f"result file should not already exist {result_xlsx_path}"

        # add first sheet 'content'
        writer = pd.ExcelWriter(path=result_xlsx_path.as_posix(), mode="w", engine="openpyxl")
        content_sheet_name = "content"
        content_df = self._get_content_df()
        content_df.to_excel(excel_writer=writer, sheet_name=content_sheet_name, index=True)
        worksheet = writer.sheets[content_sheet_name]
        self._set_sheet_style(worksheet=worksheet, tab_color=None)

        # add rest of sheets starting with input_sheets, then output_sheets
        for index, sheet in enumerate(self.results.input_sheets + self.results.output_sheets):
            assert isinstance(sheet, ExcelSheet)
            sheet.data.to_excel(excel_writer=writer, sheet_name=sheet.name, index=True)
            worksheet = writer.sheets[sheet.name]
            self._set_sheet_style(worksheet=worksheet, tab_color=sheet.tab_color)

        logger.info(f"saving result file {result_xlsx_path}")
        writer.save()
        writer.close()
