from enum import Enum
from mptconfig.constants import PathConstants
from openpyxl import worksheet as openpyxl_worksheet
from pandas.api.types import is_datetime64_any_dtype as is_datetime  # noqa pandas comes with geopandas
from pandas.io.excel._xlsxwriter import XlsxWriter  # noqa used for type-hinting
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import logging
import pandas as pd  # noqa pandas comes with geopandas


logger = logging.getLogger(__name__)


class ExcelTabColorChoices(Enum):
    red = "00FF0000"
    green = "0000FF00"
    blue = "000000FF"
    black = "00000000"
    white = "FFFFFFFF"


class ExcelSheetTypeChoices(Enum):
    input = "input"
    output_check = "output_check"
    output_no_check = "output_no_check"
    content = "content"

    def tab_color(self, empty_sheet: bool) -> ExcelTabColorChoices:
        mapping = {
            self.input: ExcelTabColorChoices.blue,
            self.output_check: ExcelTabColorChoices.green if empty_sheet else ExcelTabColorChoices.red,
            self.output_no_check: ExcelTabColorChoices.white,
            self.content: ExcelTabColorChoices.white,
        }
        return mapping[self]

    @classmethod
    def tab_color_description(cls) -> List[Tuple]:
        """
        Example: [
                    ('sheet_type=input and empty_sheet=True', 'white'),
                    ('sheet_type=input and empty_sheet=False', 'white'),
                    ('sheet_type=output_check and empty_sheet=True', 'green'),
                    ('sheet_type=output_check and empty_sheet=False', 'red')
                    etc..
                ]
        """
        description = []
        for sheet_type in cls.__members__.values():
            for empty_sheet in True, False:
                tab_color = cls.tab_color(sheet_type, empty_sheet=empty_sheet)
                assert isinstance(tab_color, ExcelTabColorChoices)
                description.append((f"sheet_type={sheet_type.name} and empty_sheet={empty_sheet}", tab_color.name))
        return description


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
        tab_color = self.sheet_type.tab_color(empty_sheet=self.nr_rows == 0)
        assert isinstance(tab_color, ExcelTabColorChoices), f"tab_color {tab_color} must be a ExcelTabColorChoices"
        return tab_color

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
        self.df.reset_index(drop=True, inplace=True)

    def to_content_dict(self) -> Dict:
        return {
            "name": self.name,
            "type": self.sheet_type.value,
            "color": self.tab_color.name,
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
        logger.info("auto-generating excel content sheet")
        content_columns = self.output_check_sheets[0].to_content_dict().keys()
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
        return [self.content_sheet] + self.output_no_check_sheets + self.input_sheets + self.output_check_sheets


class ExcelWriter:
    def __init__(self, results: ExcelSheetCollector):
        self.results = results
        assert isinstance(self.results, ExcelSheetCollector), "results is not a ExcelSheetCollector"
        assert self.results.has_sheets, "cannot create excel file if no sheets exists"

    def _set_sheet_style(
        self, df: pd.DataFrame, worksheet: openpyxl_worksheet, tab_color: ExcelTabColorChoices = None
    ) -> None:
        if tab_color:
            assert isinstance(tab_color, ExcelTabColorChoices), f"tab_color {tab_color} must be a ExcelTabColorChoices"
            worksheet.tab_color = tab_color.value
        # Apply the auto filter based on the dimensions of the dataframe
        worksheet.autofilter(first_row=0, first_col=0, last_row=df.shape[0], last_col=df.shape[1])
        self.__auto_fit_column_size(worksheet=worksheet, df=df)
        # freeze first row and first two columns
        worksheet.freeze_panes(row=1, col=2)

    @staticmethod
    def __as_text(value):
        if value is None:
            return ""
        return str(value)

    @staticmethod
    def get_df_column_widths(df: pd.DataFrame) -> List[int]:
        # find the maximum length of the index column
        index_column_width = max([len(str(s)) for s in df.index.values] + [len(str(df.index.name))])
        # find max of the lengths of column name and its values for each column, left to right
        other_column_widths = [max([len(str(s)) for s in df[col].values] + [len(col)]) for col in df.columns]
        return [index_column_width] + other_column_widths

    def __auto_fit_column_size(self, worksheet: openpyxl_worksheet, df: pd.DataFrame) -> None:
        minimal_cell_width = 13
        df_column_widths = self.get_df_column_widths(df=df)
        # index column is not included (counted) in worksheet.dim_colmax
        assert worksheet.dim_colmax == len(df_column_widths) - 1
        for index, width in enumerate(df_column_widths):
            new_width = float(max(minimal_cell_width, width))
            worksheet.set_column(first_col=index, last_col=index, width=new_width)

    @staticmethod
    def _create_excel_writer(path: Path) -> XlsxWriter:
        options = {"strings_to_formulas": False, "strings_to_urls": False}
        writer = pd.ExcelWriter(path=path.as_posix(), mode="w", engine="xlsxwriter", options=options)
        return writer

    def write(self):
        """Write each ExcelSheet object in ExcelSheetCollector to a separate sheet in one excel file."""
        # TODO: added jinja2 as dependency, but it does not work on excel, so remove it from env
        # TODO: add xlsxwriter ass dependency: we now use pd.ExcelWriter(engine="xlsxwriter") instead of engine=openpyxl

        # create and load xlsx file
        result_xlsx_path = PathConstants.result_xlsx.value.path
        logger.info(f"creating result file {PathConstants.result_xlsx.value.path}")
        # TODO: activate this assert
        # assert not result_xlsx_path.exists(), f"result file should not already exist {result_xlsx_path}"
        writer = self._create_excel_writer(path=result_xlsx_path)
        if not self.results.has_content_sheet:
            self.results.create_content_sheet()
        for sheet in self.results.ordered_sheets:
            assert isinstance(sheet, ExcelSheet)
            sheet.df.to_excel(excel_writer=writer, sheet_name=sheet.name, index=True)
            worksheet = writer.sheets[sheet.name]
            self._set_sheet_style(df=sheet.df, worksheet=worksheet, tab_color=sheet.tab_color)

        writer.save()
        if writer.engine != "xlsxwriter":
            assert writer.engine == "openpyxl"
            writer.close()
        logger.info(f"created result file {PathConstants.result_xlsx.value.path}")
