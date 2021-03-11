from enum import Enum
from mptconfig import constants
from openpyxl import worksheet as openpyxl_worksheet
from openpyxl.utils import get_column_letter
from pandas.api.types import is_datetime64_any_dtype as is_datetime  # noqa pandas comes with geopandas
from typing import Dict
from typing import List
from typing import Optional

import logging
import pandas as pd  # noqa pandas comes with geopandas


logger = logging.getLogger(__name__)


class ExcelSheetTypeChoices(Enum):
    input = "input"
    output_check = "output_check"
    output_no_check = "output_no_check"
    content = "content"


class ExcelTabColorChoices(Enum):
    red = "00FF0000"
    green = "0000FF00"
    blue = "000000FF"
    black = "00000000"
    white = "FFFFFFFF"


class ExcelSheet:
    def __init__(self, name: str, description: str, df: pd.DataFrame, sheet_type: ExcelSheetTypeChoices):
        self.name = name
        self.description = description
        self.df = df
        self.sheet_type = sheet_type
        self.validate_constructor()
        self.ensure_uniform_df_index()

    def validate_constructor(self) -> None:
        assert isinstance(self.name, str), f"sheet name {self.name} must be a str"
        assert (
            2 < len(self.name) < 25
        ), f"sheet name '{self.name}' with length {len(self.name)} must be between 2 and 25 chars"
        assert isinstance(self.description, str), f"sheet description {self.description} must be a str"
        assert (
            10 < len(self.description) < 200
        ), f"sheet description with length {len(self.description)} must be between 10 and 200 chars"
        assert isinstance(
            self.df, pd.DataFrame
        ), f"sheet name {self.name} data must be a pd.DataFrame and not a {type(self.df)}"
        assert isinstance(
            self.sheet_type, ExcelSheetTypeChoices
        ), f"sheet name {self.name} type must be a ExcelSheetTypeChoices and not a {type(self.sheet_type)}"

    @property
    def tab_color(self) -> ExcelTabColorChoices:
        if self.sheet_type == ExcelSheetTypeChoices.content:
            return ExcelTabColorChoices.white
        elif self.sheet_type == ExcelSheetTypeChoices.input:
            return ExcelTabColorChoices.blue
        elif self.sheet_type == ExcelSheetTypeChoices.output_no_check:
            return ExcelTabColorChoices.white
        assert (
            self.sheet_type == ExcelSheetTypeChoices.output_check
        ), "we expected sheet type to be SheetType.output_check"
        # red if at least one error was found
        return ExcelTabColorChoices.red if len(self.df) > 0 else ExcelTabColorChoices.green

    @property
    def nr_rows(self) -> int:
        return len(self.df)

    def ensure_uniform_df_index(self) -> None:
        """Enforce uniform index type on all sheets, so that when creating excel we
        can do pd.to_excel(index=True) resulting in same first column"""
        if self.nr_rows == 0:
            return
        if not (isinstance(self.df.index, pd.Int64Index) or isinstance(self.df.index, pd.RangeIndex)):
            raise AssertionError(
                f"sheet {self.name} index must be a Int64Index or RangeIndex, not type {type(self.df.index)}"
            )

    def to_content_dict(self) -> Dict:
        return {
            "name": self.name,
            "type": self.sheet_type.value,
            # "color": self.tab_color.,
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
        assert key == value.name, "key must equal value.name. We advise you to use public method 'add_sheet()'"
        assert key not in self, f"can not add sheet with name '{key}' as it already exists and name must be unique"
        if value.sheet_type == ExcelSheetTypeChoices.content:
            already_exists = [sheet for sheet in self.values() if sheet.sheet_type == ExcelSheetTypeChoices.content]
            assert not already_exists, "content sheet already exist, can only have one content sheet"
        super().__setitem__(key, value)

    def __delitem__(self, key: str) -> None:
        if key not in self:
            raise AttributeError(f"No sheet with name '{key}'. Delete is not possible")
        super().__delitem__(key)

    def add_sheet(self, excelsheet: ExcelSheet) -> None:
        assert isinstance(excelsheet, ExcelSheet), "excelsheet is not an instance of ExcelSheet"
        self.__setitem__(key=excelsheet.name, value=excelsheet)

    def create_content_sheet(self) -> None:
        """Create panda dataframe based on all ExcelSheet objects included in ExcelSheetCollector (self.results).
        This content df has columns (ExcelSheet objects): "name", "type", "nr_rows", "description"."""
        assert self.has_sheets and not self.has_content_sheet, "can not create content sheet"
        content_columns = self.input_sheets[0].to_content_dict().keys()
        data = []
        for sheet in self.content_sheet_input:
            assert isinstance(sheet, ExcelSheet)
            data.append(sheet.to_content_dict())
        content_df = pd.DataFrame(columns=content_columns, data=data)
        content_sheet = ExcelSheet(
            name="content",
            description="content sheet, an overview of all sheets",
            df=content_df,
            sheet_type=ExcelSheetTypeChoices.content,
        )
        self.add_sheet(excelsheet=content_sheet)

    @property
    def has_sheets(self) -> bool:
        return True if self.keys() else False

    @property
    def has_content_sheet(self) -> bool:
        return True if self.content_sheet else False

    @property
    def content_sheet(self) -> Optional[pd.DataFrame]:
        content_sheet = [sheet for sheet in self.values() if sheet.sheet_type == ExcelSheetTypeChoices.content]
        if content_sheet:
            return content_sheet[0]
        logger.debug("no content sheet exists")
        return None

    @property
    def content_sheet_input(self) -> List[pd.DataFrame]:
        """Defines which sheet types should be included in the content sheet."""
        return self.input_sheets + self.output_no_check_sheets + self.output_check_sheets

    @property
    def input_sheets(self) -> List[pd.DataFrame]:
        """A input sheet has a dataframe that served as input for the MptConfigChecker."""
        if not self.has_sheets:
            return []
        return [sheet for sheet in self.values() if sheet.sheet_type == ExcelSheetTypeChoices.input]

    @property
    def output_check_sheets(self) -> List[pd.DataFrame]:
        """A output_check sheet has a dataframes which holds result from 1 MptConfigChecker check."""
        if not self.has_sheets:
            return []
        return [sheet for sheet in self.values() if sheet.sheet_type == ExcelSheetTypeChoices.output_check]

    @property
    def output_no_check_sheets(self) -> List[pd.DataFrame]:
        """A output_no_check sheet has a dataframe that contoins data that was produced during the checks but is not
        a result of 1 or more checks. An example is sheet 'mpt_histtags_new'."""
        if not self.has_sheets:
            return []
        return [sheet for sheet in self.values() if sheet.sheet_type == ExcelSheetTypeChoices.output_no_check]

    @property
    def ordered_sheets(self) -> List[pd.DataFrame]:
        """This is the tab order in the excel file"""
        assert self.has_content_sheet
        return [self.content_sheet] + self.input_sheets + self.output_no_check_sheets + self.output_check_sheets


class ExcelWriter:
    def __init__(self, results: ExcelSheetCollector):
        self.results = results
        assert isinstance(self.results, ExcelSheetCollector), "results is not a ExcelSheetCollector"
        assert self.results.has_sheets, "cannot create excel file if no sheets exists"

    def _set_sheet_style(self, worksheet: openpyxl_worksheet, tab_color: ExcelTabColorChoices = None) -> None:
        if tab_color:
            worksheet.sheet_properties.tabColor = tab_color.value
        worksheet.auto_filter.ref = worksheet.dimensions
        self.__auto_fit_column_size(worksheet=worksheet)
        # freeze first row and first two columns
        worksheet.freeze_panes = worksheet["C2"]

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
        # TODO: activate this check
        # assert not result_xlsx_path.exists(), f"result file should not already exist {result_xlsx_path}"
        writer = pd.ExcelWriter(path=result_xlsx_path.as_posix(), mode="w", engine="openpyxl")

        if not self.results.has_content_sheet:
            self.results.create_content_sheet()
        for sheet in self.results.ordered_sheets:
            assert isinstance(sheet, ExcelSheet)
            sheet.df.to_excel(excel_writer=writer, sheet_name=sheet.name, index=True)
            worksheet = writer.sheets[sheet.name]
            self._set_sheet_style(worksheet=worksheet, tab_color=sheet.tab_color)

        writer.save()
        writer.close()
        logger.info(f"created result file {result_xlsx_path}")
