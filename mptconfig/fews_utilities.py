from collections import defaultdict
from lxml import etree as ET  # noqa
from pathlib import Path
from shapely.geometry import Point  # noqa shapely comes with geopandas
from typing import Dict
from typing import Optional
from typing import Union

import geopandas as gpd
import os


# TODO: move to constants
GEO_DATUM = {"Rijks Driehoekstelsel": "epsg:28992"}


def xml_to_etree(xml_file: str) -> ET._Element:
    """ parses an xml-file to an etree. ETree can be used in function etree_to_dict """
    # TODO: xml_file is a path, so make it type Path
    etree = ET.parse(xml_file).getroot()
    return etree


def etree_to_dict(etree: Union[ET._Element, ET._Comment], section_start: str = None, section_end: str = None,) -> Dict:
    """ converts an etree to a dictionary """
    # TODO: kan t alleen een ET._Element of ET._Comment zijn?
    if isinstance(etree, ET._Comment):
        # TODO: return of toch return {} ??
        return
    _dict = {etree.tag.rpartition("}")[-1]: {} if etree.attrib else None}
    children = list(etree)

    # get a section only
    if section_start or section_end:
        if section_start:
            start = [
                idx
                for idx, child in enumerate(children)
                if isinstance(child, ET._Comment)
                if ET.tostring(child).decode("utf-8").strip() == section_start
            ][0]
        else:
            start = 0
        if section_end:
            end = [
                idx
                for idx, child in enumerate(children)
                if isinstance(child, ET._Comment)
                if ET.tostring(child).decode("utf-8").strip() == section_end
            ][0]
            if start < end:
                children = children[start:end]
        else:
            children = children[start:]

    children = [child for child in children if not isinstance(child, ET._Comment)]

    if children:
        dd = defaultdict(list)
        # for dc in map(etree_to_dict, children):
        for dc in [etree_to_dict(child) for child in children]:
            for k, v in dc.items():
                dd[k].append(v)

        _dict = {etree.tag.rpartition("}")[-1]: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if etree.attrib:
        _dict[etree.tag.rpartition("}")[-1]].update((k, v) for k, v in etree.attrib.items())
    if etree.text:
        text = etree.text.strip()
        if children or etree.attrib:
            if text:
                _dict[etree.tag.rpartition("}")[-1]]["#text"] = text
        else:
            _dict[etree.tag.rpartition("}")[-1]] = text
    return _dict


def xml_to_dict(xml_file: str, section_start: str = None, section_end: str = None) -> Dict:
    """ converts an xml-file to a dictionary """
    # TODO: xml_file type is a path
    etree = xml_to_etree(xml_file)
    return etree_to_dict(etree, section_start=section_start, section_end=section_end)


class FewsConfig:
    def __init__(self, path):
        self.path = path

        # FEWS config dir-structure
        self.CoefficientSetsFiles = dict()
        self.DisplayConfigFiles = dict()
        self.FlagConversionsFiles = dict()
        self.IconFiles = dict()
        self.IdMapFiles = dict()
        self.MapLayerFiles = dict()
        self.ModuleConfigFiles = dict()
        self.ModuleDatasetFiles = dict()
        self.PiClientConfigFiles = dict()
        self.RegionConfigFiles = dict()
        self.ReportTemplateFiles = dict()
        self.RootConfigFiles = dict()
        self.SystemConfigFiles = dict()
        self.UnitConversionsFiles = dict()
        self.WorkflowFiles = dict()

        # populate config dir-structure
        self._populate_files()

        # get locationSets
        # TODO: no camelcase. But leave it for now as a lot of location_sets exists
        self.locationSets = self._get_location_sets()

    def _populate_files(self) -> None:
        """ Set all fews config filepaths (.xml, .shx, etc) on self.

        Example result:
            self.IdMapFiles = {
                'IdAHN': 'D:\\WIS_6.0_ONTWIKKEL_201902\\FEWS_SA\\config\\IdMapFiles\\IdAHN.xml',
                'IdArtDiver': 'D:\\WIS_6.0_ONTWIKKEL_201902\\FEWS_SA\\config\\IdMapFiles\\IdArtDiver.xml',
                ..
                },
            self.MapLayerFiles = {
                'afvoergebieden': 'D:\\WIS_6.0_ONTWIKKEL_201902\\FEWS_SA\\config\\MapLayerFiles\\afvoergebieden.shx',  # noqa
                'begroeiingsgraad_trajecten': 'D:\\WIS_6.0_ONTWIKKEL_201902\\FEWS_SA\\config\\MapLayerFiles\\begroeiingsgraad_trajecten.shx',  # noqa
                },
            etc

        TODO: work with pathlib.Path
        """
        for dirpath, dirnames, filenames in os.walk(self.path):
            if dirpath == self.path:
                continue
            prop = next((key for key in self.__dict__.keys() if key in dirpath), None)
            if not prop:
                continue
            self.__dict__[prop].update(
                {os.path.splitext(file_name)[0]: os.path.join(dirpath, file_name) for file_name in filenames}
            )

    def _get_location_sets(self) -> Dict:
        """build-in method to extract a dict of locationsets"""
        location_sets = xml_to_dict(self.RegionConfigFiles["LocationSets"])["locationSets"]["locationSet"]
        return {
            location_set["id"]: {key: value for key, value in location_set.items() if key != "id"}
            for location_set in location_sets
        }

    def get_parameters(self, dict_keys: str = "groups") -> Dict:
        """method to extract a dictionary of parameter(groups) from a FEWS-config"""
        # TODO: include parameters from CSV-files (support parametersCsvFile)
        assert dict_keys in ("groups", "parameters")
        parameters = xml_to_dict(self.RegionConfigFiles["Parameters"])["parameters"]
        if dict_keys == "groups":
            return {
                group["id"]: {key: value for key, value in group.items() if key != "id"}
                for group in parameters["parameterGroups"]["parameterGroup"]
            }
        result = {}
        for group in parameters["parameterGroups"]["parameterGroup"]:
            if type(group["parameter"]) == dict:
                group["parameter"] = [group["parameter"]]
            for parameter in group["parameter"]:
                result.update({parameter["id"]: {}})
                result[parameter["id"]] = {key: value for key, value in parameter.items() if not key == "id"}
                result[parameter["id"]].update({key: value for key, value in group.items() if not key == "parameter"})
                result[parameter["id"]]["groupId"] = result[parameter["id"]].pop("id")
        return result

    def get_locations(self, location_set_key: str) -> Optional[gpd.GeoDataFrame]:
        """Convert fews locationSet locations into geopandas df
        args 'location_set_key' (str) is e.g. 'OPVLWATER_HOOFDLOC'
        """
        # TODO: support other than csvFile type locationSets
        # TODO: concatenate attribute-files
        # TODO: rename to internal attribute names
        location_set = self.locationSets.get(location_set_key, None)
        if not location_set:
            return
        file = location_set.get("csvFile", {}).get("file", None)
        if not file:
            return

        file = Path(file)
        if not file.suffix:
            file = file.parent / (file.name + ".csv")
        filepath = self.path / "MapLayerFiles" / file
        assert filepath.is_file(), f"file {filepath} does not exist"

        x_attrib = location_set["csvFile"]["x"].replace("%", "")
        y_attrib = location_set["csvFile"]["y"].replace("%", "")
        z_attrib = None
        if "z" in location_set["csvFile"].keys():
            # use key 'y' for z_attrib
            z_attrib = location_set["csvFile"]["y"].replace("%", "")

        gdf = gpd.read_file(filepath)

        if z_attrib:
            gdf["geometry"] = gdf.apply(
                (lambda x: Point(float(x[x_attrib]), float(x[y_attrib]), float(x[z_attrib]),)), axis=1,
            )
        else:
            gdf["geometry"] = gdf.apply((lambda x: Point(float(x[x_attrib]), float(x[y_attrib]))), axis=1,)

        crs = None
        if location_set["csvFile"]["geoDatum"] in GEO_DATUM.keys():
            crs = GEO_DATUM[location_set["csvFile"]["geoDatum"]]
        if crs:
            gdf.crs = crs
        return gdf
