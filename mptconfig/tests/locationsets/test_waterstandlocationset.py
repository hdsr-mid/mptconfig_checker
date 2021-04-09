from mptconfig import constants
from mptconfig.tests.fixtures import patched_path_constants_1
from mptconfig.tests.fixtures import patched_path_constants_2


# silence flake8 errors
_patched_path_constants_1 = patched_path_constants_1
_patched_path_constants_2 = patched_path_constants_2

expected_idmap_section_name_1_and_2 = "WATERSTANDLOCATIES"
expected_name_1_and_2 = "waterstandlocaties"
expected_csvfile_1_and_2 = "oppvlwater_waterstanden"
expected_fews_name_1_and_2 = "OPVLWATER_WATERSTANDEN_AUTO"


expected_validation_attributes_1_and_2 = [
    "HARDMAX",
    "WIN_SMAX",
    "OV_SMAX",
    "ZOM_SMAX",
    "WIN_SMIN",
    "OV_SMIN",
    "ZOM_SMIN",
    "HARDMIN",
]

expected_validation_rules_1_and_2 = [
    {
        "parameter": "H.G.",
        "extreme_values": {
            "hmax": "HARDMAX",
            "smax": [
                {"period": 1, "attribute": "WIN_SMAX"},
                {"period": 2, "attribute": "OV_SMAX"},
                {"period": 3, "attribute": "ZOM_SMAX"},
            ],
            "smin": [
                {"period": 1, "attribute": "WIN_SMIN"},
                {"period": 2, "attribute": "OV_SMIN"},
                {"period": 3, "attribute": "ZOM_SMIN"},
            ],
            "hmin": "HARDMIN",
        },
    }
]

expected_csvfile_meta_1 = {
    "file": "oppvlwater_waterstanden",
    "geoDatum": "Rijks Driehoekstelsel",
    "id": "%LOC_ID%",
    "name": "%LOC_NAME%",
    "description": "Locaties waterstanden",
    "toolTip": '<html>\n    <table id="details">\n      <tr>\n\t<td width="50" valign="top">ID</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%ID%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Naam</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%NAME%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Type</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%DESCRIPTION%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Hymos</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%HIST_TAG%</td>\n      </tr>\n    </table>\n</html>',
    "startDateTime": "%START%",
    "endDateTime": "%EIND%",
    "x": "%X%",
    "y": "%Y%",
    "z": "%Z%",
    "relation": [
        {"relatedLocationId": "%GAFCODE%", "id": "AFVOERGEBIED"},
        {"relatedLocationId": "%GPGIDENT%", "id": "PEILGEBIED"},
        {"relatedLocationId": "%RBGID%", "id": "RBGID"},
        {"relatedLocationId": "%PEILSCHAAL%", "id": "PEILSCHAAL"},
    ],
    "attribute": [
        {"number": "%MAAIVELD%", "id": "MAAIVELD"},
        {"text": "%PEILBESLUI%", "id": "PEILBESLUIT"},
        {"text": "%HIST_TAG%", "id": "HIST_TAG"},
        {"boolean": "%GERELATEERD%", "id": "GERELATEERD"},
        {"text": "%SYSTEEM%", "id": "HOOFDSYSTEEM"},
        {"text": "%RAYON%", "id": "RAYON"},
        {"text": "%FOTO_ID%", "id": "FOTO_ID"},
        {"text": "%GPGIDENT%", "id": "PEILGEBIED"},
        {"boolean": "%SWM%", "id": "SWM"},
        {"boolean": "%NWW-MDV%", "id": "SWMGEBIED_NWW-MDV"},
    ],
    "attributeFile": [
        {
            "csvFile": "oppvlwater_langsprofielen",
            "id": "%LOC_ID%",
            "attribute": [
                {"number": "%Langsprofiel_Kromme_Rijn%", "id": "Langsprofiel_Kromme_Rijn"},
                {"number": "%Langsprofiel_Caspargouwse_Wetering%", "id": "Langsprofiel_Caspargouwse_Wetering"},
                {
                    "number": "%Langsprofiel_Stadswater_Utrecht_en_Vecht%",
                    "id": "Langsprofiel_Stadswater_Utrecht_en_Vecht",
                },
                {
                    "number": "%Langsprofiel_Doorslag-Gekanaliseerde_Hollandse_IJssel%",
                    "id": "Langsprofiel_Doorslag-Gekanaliseerde_Hollandse_IJssel",
                },
                {"number": "%Langsprofiel_Oude_Rijn_boezem_Oost%", "id": "Langsprofiel_Oude_Rijn_boezem_Oost"},
                {"number": "%Langsprofiel_Oude_Rijn_boezem_West%", "id": "Langsprofiel_Oude_Rijn_boezem_West"},
                {"number": "%Langsprofiel_Grecht%", "id": "Langsprofiel_Grecht"},
                {
                    "number": "%Langsprofiel_Lange_Linschoten_tm_Jaap_Bijzerwetering%",
                    "id": "Langsprofiel_Lange_Linschoten_tm_Jaap_Bijzerwetering",
                },
                {"number": "%Langsprofiel_Dubbele_Wiericke%", "id": "Langsprofiel_Dubbele_Wiericke"},
                {"number": "%Langsprofiel_Leidsche_Rijn%", "id": "Langsprofiel_Leidsche_Rijn"},
                {"number": "%Langsprofiel_Amsterdam-Rijnkanaal%", "id": "Langsprofiel_Amsterdam-Rijnkanaal"},
                {"number": "%Langsprofiel_Merwedekanaal%", "id": "Langsprofiel_Merwedekanaal"},
                {"number": "%Langsprofiel_Boezem_AGV%", "id": "Langsprofiel_Boezem_AGV"},
                {"number": "%Langsprofiel_Langbroekerwetering%", "id": "Langsprofiel_Langbroekerwetering"},
                {"number": "%Langsprofiel_Amerongerwetering%", "id": "Langsprofiel_Amerongerwetering"},
                {"number": "%Langsprofiel_Schalkwijkse_wetering%", "id": "Langsprofiel_Schalkwijkse_wetering"},
            ],
        },
        {
            "csvFile": "oppvlwater_waterstanden_diff.csv",
            "id": "%LOC_ID%",
            "relation": {"relatedLocationId": "%REL_DIFF%", "id": "REL_DIFF"},
        },
        {
            "csvFile": "oppvlwater_waterstanden_cacb.csv",
            "id": "%LOC_ID%",
            "relation": {"relatedLocationId": "%REL_CACB%", "id": "REL_CACB"},
            "attribute": [{"number": "%COEF_CA%", "id": "COEF_CA"}, {"number": "%COEF_CB%", "id": "COEF_CB"}],
        },
        {
            "csvFile": "oppvlwater_waterstanden_validations.csv",
            "id": "%LOC_ID%",
            "attribute": {"number": "%watervalidatie%", "id": "watervalidatie"},
        },
        {
            "csvFile": "oppvlwater_watervalidatie.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "checkForContinuousPeriod": "false",
            "attribute": [
                {"number": "%WIN_SMAX%", "id": "WIN_SMAX"},
                {"number": "%WIN_SMIN%", "id": "WIN_SMIN"},
                {"number": "%OV_SMAX%", "id": "OV_SMAX"},
                {"number": "%OV_SMIN%", "id": "OV_SMIN"},
                {"number": "%ZOM_SMAX%", "id": "ZOM_SMAX"},
                {"number": "%ZOM_SMIN%", "id": "ZOM_SMIN"},
                {"number": "%HARDMAX%", "id": "HARDMAX"},
                {"number": "%HARDMIN%", "id": "HARDMIN"},
                {"number": "%RATECHANGE%", "id": "RATECHANGE"},
                {"number": "%SR_DEV%", "id": "SR_DEV"},
                {"number": "%SR_PERIOD%", "id": "SR_PERIOD"},
                {"number": "%SR0.5_DEV%", "id": "SR0.5_DEV"},
                {"number": "%SR0.5_PERIOD%", "id": "SR0.5_PERIOD"},
                {"number": "%SR7_DEV%", "id": "SR7_DEV"},
                {"number": "%SR7_PERIOD%", "id": "SR7_PERIOD"},
                {"number": "%TS_RATE%", "id": "TS_RATE"},
                {"number": "%TS_PERIOD%", "id": "TS_PERIOD"},
            ],
        },
    ],
}
expected_csvfile_meta_2 = {
    "file": "oppvlwater_waterstanden",
    "geoDatum": "Rijks Driehoekstelsel",
    "id": "%LOC_ID%",
    "name": "%LOC_NAME%",
    "description": "Locaties waterstanden",
    "toolTip": '<html>\n    <table id="details">\n      <tr>\n\t<td width="50" valign="top">ID</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%ID%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Naam</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%NAME%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Type</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%DESCRIPTION%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Hymos</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%HIST_TAG%</td>\n      </tr>\n    </table>\n</html>',  # noqa
    "startDateTime": "%START%",
    "endDateTime": "%EIND%",
    "x": "%X%",
    "y": "%Y%",
    "z": "%Z%",
    "relation": [
        {"relatedLocationId": "%GAFCODE%", "id": "AFVOERGEBIED"},
        {"relatedLocationId": "%GPGIDENT%", "id": "PEILGEBIED"},
        {"relatedLocationId": "%RBGID%", "id": "RBGID"},
        {"relatedLocationId": "%PEILSCHAAL%", "id": "PEILSCHAAL"},
    ],
    "attribute": [
        {"number": "%MAAIVELD%", "id": "MAAIVELD"},
        {"text": "%PEILBESLUI%", "id": "PEILBESLUIT"},
        {"text": "%HIST_TAG%", "id": "HIST_TAG"},
        {"boolean": "%GERELATEERD%", "id": "GERELATEERD"},
        {"text": "%SYSTEEM%", "id": "HOOFDSYSTEEM"},
        {"text": "%RAYON%", "id": "RAYON"},
        {"text": "%FOTO_ID%", "id": "FOTO_ID"},
        {"text": "%GPGIDENT%", "id": "PEILGEBIED"},
        {"boolean": "%SWM%", "id": "SWM"},
        {"boolean": "%NWW-MDV%", "id": "SWMGEBIED_NWW-MDV"},
    ],
    "attributeFile": [
        {
            "csvFile": "oppvlwater_langsprofielen",
            "id": "%LOC_ID%",
            "attribute": [
                {"number": "%Langsprofiel_Kromme_Rijn%", "id": "Langsprofiel_Kromme_Rijn"},
                {"number": "%Langsprofiel_Caspargouwse_Wetering%", "id": "Langsprofiel_Caspargouwse_Wetering"},
                {
                    "number": "%Langsprofiel_Stadswater_Utrecht_en_Vecht%",
                    "id": "Langsprofiel_Stadswater_Utrecht_en_Vecht",
                },
                {
                    "number": "%Langsprofiel_Doorslag-Gekanaliseerde_Hollandse_IJssel%",
                    "id": "Langsprofiel_Doorslag-Gekanaliseerde_Hollandse_IJssel",
                },
                {"number": "%Langsprofiel_Oude_Rijn_boezem_Oost%", "id": "Langsprofiel_Oude_Rijn_boezem_Oost"},
                {"number": "%Langsprofiel_Oude_Rijn_boezem_West%", "id": "Langsprofiel_Oude_Rijn_boezem_West"},
                {"number": "%Langsprofiel_Grecht%", "id": "Langsprofiel_Grecht"},
                {
                    "number": "%Langsprofiel_Lange_Linschoten_tm_Jaap_Bijzerwetering%",
                    "id": "Langsprofiel_Lange_Linschoten_tm_Jaap_Bijzerwetering",
                },
                {"number": "%Langsprofiel_Dubbele_Wiericke%", "id": "Langsprofiel_Dubbele_Wiericke"},
                {"number": "%Langsprofiel_Leidsche_Rijn%", "id": "Langsprofiel_Leidsche_Rijn"},
                {"number": "%Langsprofiel_Amsterdam-Rijnkanaal%", "id": "Langsprofiel_Amsterdam-Rijnkanaal"},
                {"number": "%Langsprofiel_Merwedekanaal%", "id": "Langsprofiel_Merwedekanaal"},
                {"number": "%Langsprofiel_Boezem_AGV%", "id": "Langsprofiel_Boezem_AGV"},
                {"number": "%Langsprofiel_Langbroekerwetering%", "id": "Langsprofiel_Langbroekerwetering"},
                {"number": "%Langsprofiel_Amerongerwetering%", "id": "Langsprofiel_Amerongerwetering"},
                {"number": "%Langsprofiel_Schalkwijkse_wetering%", "id": "Langsprofiel_Schalkwijkse_wetering"},
            ],
        },
        {
            "csvFile": "oppvlwater_waterstanden_diff.csv",
            "id": "%LOC_ID%",
            "relation": {"relatedLocationId": "%REL_DIFF%", "id": "REL_DIFF"},
        },
        {
            "csvFile": "oppvlwater_waterstanden_cacb.csv",
            "id": "%LOC_ID%",
            "relation": {"relatedLocationId": "%REL_CACB%", "id": "REL_CACB"},
            "attribute": [{"number": "%COEF_CA%", "id": "COEF_CA"}, {"number": "%COEF_CB%", "id": "COEF_CB"}],
        },
        {
            "csvFile": "oppvlwater_waterstanden_validations.csv",
            "id": "%LOC_ID%",
            "attribute": {"number": "%watervalidatie%", "id": "watervalidatie"},
        },
        {
            "csvFile": "oppvlwater_watervalidatie.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "checkForContinuousPeriod": "false",
            "attribute": [
                {"number": "%WIN_SMAX%", "id": "WIN_SMAX"},
                {"number": "%WIN_SMIN%", "id": "WIN_SMIN"},
                {"number": "%OV_SMAX%", "id": "OV_SMAX"},
                {"number": "%OV_SMIN%", "id": "OV_SMIN"},
                {"number": "%ZOM_SMAX%", "id": "ZOM_SMAX"},
                {"number": "%ZOM_SMIN%", "id": "ZOM_SMIN"},
                {"number": "%HARDMAX%", "id": "HARDMAX"},
                {"number": "%HARDMIN%", "id": "HARDMIN"},
                {"number": "%RATECHANGE%", "id": "RATECHANGE"},
                {"number": "%SR_DEV%", "id": "SR_DEV"},
                {"number": "%SR_PERIOD%", "id": "SR_PERIOD"},
                {"number": "%SR0.5_DEV%", "id": "SR0.5_DEV"},
                {"number": "%SR0.5_PERIOD%", "id": "SR0.5_PERIOD"},
                {"number": "%SR7_DEV%", "id": "SR7_DEV"},
                {"number": "%SR7_PERIOD%", "id": "SR7_PERIOD"},
                {"number": "%TS_RATE%", "id": "TS_RATE"},
                {"number": "%TS_PERIOD%", "id": "TS_PERIOD"},
            ],
        },
        {
            "csvFile": "oppvlwater_herhalingstijden.csv",
            "id": "%LOC_ID%",
            "attribute": [
                {"text": "Annual Exceedance", "id": "Selection"},
                {"number": "%H_Threshold%", "id": "H_Threshold"},
                {"number": "7", "id": "Viewperiod"},
                {"text": "Exponential", "id": "Function"},
                {"text": "Maximum Likelyhood", "id": "Fit"},
                {"text": "No", "id": "SelectComputationPeriod"},
                {"text": "%RekenPeriode_Start%", "id": "ComputationPeriodStart"},
                {"text": "%RekenPeriode_Eind%", "id": "ComputationPeriodEnd"},
                {"text": "YES", "id": "GraphConfidence"},
                {"number": "95", "id": "Confidence"},
                {"text": "Yes", "id": "GraphLegend"},
                {"number": "100", "id": "XasMax"},
                {"text": "01-01-2000", "id": "DayHourDate"},
                {"number": "%H_T1%", "id": "H_T1"},
                {"number": "%H_T2%", "id": "H_T2"},
                {"number": "%H_T5%", "id": "H_T5"},
                {"number": "%H_T10%", "id": "H_T10"},
                {"number": "%H_T25%", "id": "H_T25"},
                {"number": "%H_T50%", "id": "H_T50"},
                {"number": "%H_T100%", "id": "H_T100"},
            ],
        },
    ],
}
expected_attrib_files_1 = [
    {
        "csvFile": "oppvlwater_langsprofielen",
        "id": "%LOC_ID%",
        "attribute": [
            {"number": "%Langsprofiel_Kromme_Rijn%", "id": "Langsprofiel_Kromme_Rijn"},
            {"number": "%Langsprofiel_Caspargouwse_Wetering%", "id": "Langsprofiel_Caspargouwse_Wetering"},
            {"number": "%Langsprofiel_Stadswater_Utrecht_en_Vecht%", "id": "Langsprofiel_Stadswater_Utrecht_en_Vecht"},
            {
                "number": "%Langsprofiel_Doorslag-Gekanaliseerde_Hollandse_IJssel%",
                "id": "Langsprofiel_Doorslag-Gekanaliseerde_Hollandse_IJssel",
            },
            {"number": "%Langsprofiel_Oude_Rijn_boezem_Oost%", "id": "Langsprofiel_Oude_Rijn_boezem_Oost"},
            {"number": "%Langsprofiel_Oude_Rijn_boezem_West%", "id": "Langsprofiel_Oude_Rijn_boezem_West"},
            {"number": "%Langsprofiel_Grecht%", "id": "Langsprofiel_Grecht"},
            {
                "number": "%Langsprofiel_Lange_Linschoten_tm_Jaap_Bijzerwetering%",
                "id": "Langsprofiel_Lange_Linschoten_tm_Jaap_Bijzerwetering",
            },
            {"number": "%Langsprofiel_Dubbele_Wiericke%", "id": "Langsprofiel_Dubbele_Wiericke"},
            {"number": "%Langsprofiel_Leidsche_Rijn%", "id": "Langsprofiel_Leidsche_Rijn"},
            {"number": "%Langsprofiel_Amsterdam-Rijnkanaal%", "id": "Langsprofiel_Amsterdam-Rijnkanaal"},
            {"number": "%Langsprofiel_Merwedekanaal%", "id": "Langsprofiel_Merwedekanaal"},
            {"number": "%Langsprofiel_Boezem_AGV%", "id": "Langsprofiel_Boezem_AGV"},
            {"number": "%Langsprofiel_Langbroekerwetering%", "id": "Langsprofiel_Langbroekerwetering"},
            {"number": "%Langsprofiel_Amerongerwetering%", "id": "Langsprofiel_Amerongerwetering"},
            {"number": "%Langsprofiel_Schalkwijkse_wetering%", "id": "Langsprofiel_Schalkwijkse_wetering"},
        ],
    },
    {
        "csvFile": "oppvlwater_waterstanden_cacb.csv",
        "id": "%LOC_ID%",
        "relation": {"relatedLocationId": "%REL_CACB%", "id": "REL_CACB"},
        "attribute": [{"number": "%COEF_CA%", "id": "COEF_CA"}, {"number": "%COEF_CB%", "id": "COEF_CB"}],
    },
    {
        "csvFile": "oppvlwater_waterstanden_validations.csv",
        "id": "%LOC_ID%",
        "attribute": {"number": "%watervalidatie%", "id": "watervalidatie"},
    },
    {
        "csvFile": "oppvlwater_watervalidatie.csv",
        "id": "%LOC_ID%",
        "startDateTime": "%STARTDATE%",
        "endDateTime": "%ENDDATE%",
        "checkForContinuousPeriod": "false",
        "attribute": [
            {"number": "%WIN_SMAX%", "id": "WIN_SMAX"},
            {"number": "%WIN_SMIN%", "id": "WIN_SMIN"},
            {"number": "%OV_SMAX%", "id": "OV_SMAX"},
            {"number": "%OV_SMIN%", "id": "OV_SMIN"},
            {"number": "%ZOM_SMAX%", "id": "ZOM_SMAX"},
            {"number": "%ZOM_SMIN%", "id": "ZOM_SMIN"},
            {"number": "%HARDMAX%", "id": "HARDMAX"},
            {"number": "%HARDMIN%", "id": "HARDMIN"},
            {"number": "%RATECHANGE%", "id": "RATECHANGE"},
            {"number": "%SR_DEV%", "id": "SR_DEV"},
            {"number": "%SR_PERIOD%", "id": "SR_PERIOD"},
            {"number": "%SR0.5_DEV%", "id": "SR0.5_DEV"},
            {"number": "%SR0.5_PERIOD%", "id": "SR0.5_PERIOD"},
            {"number": "%SR7_DEV%", "id": "SR7_DEV"},
            {"number": "%SR7_PERIOD%", "id": "SR7_PERIOD"},
            {"number": "%TS_RATE%", "id": "TS_RATE"},
            {"number": "%TS_PERIOD%", "id": "TS_PERIOD"},
        ],
    },
]

expected_attrib_files_2 = [
    {
        "csvFile": "oppvlwater_langsprofielen",
        "id": "%LOC_ID%",
        "attribute": [
            {"number": "%Langsprofiel_Kromme_Rijn%", "id": "Langsprofiel_Kromme_Rijn"},
            {"number": "%Langsprofiel_Caspargouwse_Wetering%", "id": "Langsprofiel_Caspargouwse_Wetering"},
            {
                "number": "%Langsprofiel_Stadswater_Utrecht_en_Vecht%",
                "id": "Langsprofiel_Stadswater_Utrecht_en_Vecht",
            },
            {
                "number": "%Langsprofiel_Doorslag-Gekanaliseerde_Hollandse_IJssel%",
                "id": "Langsprofiel_Doorslag-Gekanaliseerde_Hollandse_IJssel",
            },
            {"number": "%Langsprofiel_Oude_Rijn_boezem_Oost%", "id": "Langsprofiel_Oude_Rijn_boezem_Oost"},
            {"number": "%Langsprofiel_Oude_Rijn_boezem_West%", "id": "Langsprofiel_Oude_Rijn_boezem_West"},
            {"number": "%Langsprofiel_Grecht%", "id": "Langsprofiel_Grecht"},
            {
                "number": "%Langsprofiel_Lange_Linschoten_tm_Jaap_Bijzerwetering%",
                "id": "Langsprofiel_Lange_Linschoten_tm_Jaap_Bijzerwetering",
            },
            {"number": "%Langsprofiel_Dubbele_Wiericke%", "id": "Langsprofiel_Dubbele_Wiericke"},
            {"number": "%Langsprofiel_Leidsche_Rijn%", "id": "Langsprofiel_Leidsche_Rijn"},
            {"number": "%Langsprofiel_Amsterdam-Rijnkanaal%", "id": "Langsprofiel_Amsterdam-Rijnkanaal"},
            {"number": "%Langsprofiel_Merwedekanaal%", "id": "Langsprofiel_Merwedekanaal"},
            {"number": "%Langsprofiel_Boezem_AGV%", "id": "Langsprofiel_Boezem_AGV"},
            {"number": "%Langsprofiel_Langbroekerwetering%", "id": "Langsprofiel_Langbroekerwetering"},
            {"number": "%Langsprofiel_Amerongerwetering%", "id": "Langsprofiel_Amerongerwetering"},
            {"number": "%Langsprofiel_Schalkwijkse_wetering%", "id": "Langsprofiel_Schalkwijkse_wetering"},
        ],
    },
    {
        "csvFile": "oppvlwater_waterstanden_cacb.csv",
        "id": "%LOC_ID%",
        "relation": {"relatedLocationId": "%REL_CACB%", "id": "REL_CACB"},
        "attribute": [{"number": "%COEF_CA%", "id": "COEF_CA"}, {"number": "%COEF_CB%", "id": "COEF_CB"}],
    },
    {
        "csvFile": "oppvlwater_waterstanden_validations.csv",
        "id": "%LOC_ID%",
        "attribute": {"number": "%watervalidatie%", "id": "watervalidatie"},
    },
    {
        "csvFile": "oppvlwater_watervalidatie.csv",
        "id": "%LOC_ID%",
        "startDateTime": "%STARTDATE%",
        "endDateTime": "%ENDDATE%",
        "checkForContinuousPeriod": "false",
        "attribute": [
            {"number": "%WIN_SMAX%", "id": "WIN_SMAX"},
            {"number": "%WIN_SMIN%", "id": "WIN_SMIN"},
            {"number": "%OV_SMAX%", "id": "OV_SMAX"},
            {"number": "%OV_SMIN%", "id": "OV_SMIN"},
            {"number": "%ZOM_SMAX%", "id": "ZOM_SMAX"},
            {"number": "%ZOM_SMIN%", "id": "ZOM_SMIN"},
            {"number": "%HARDMAX%", "id": "HARDMAX"},
            {"number": "%HARDMIN%", "id": "HARDMIN"},
            {"number": "%RATECHANGE%", "id": "RATECHANGE"},
            {"number": "%SR_DEV%", "id": "SR_DEV"},
            {"number": "%SR_PERIOD%", "id": "SR_PERIOD"},
            {"number": "%SR0.5_DEV%", "id": "SR0.5_DEV"},
            {"number": "%SR0.5_PERIOD%", "id": "SR0.5_PERIOD"},
            {"number": "%SR7_DEV%", "id": "SR7_DEV"},
            {"number": "%SR7_PERIOD%", "id": "SR7_PERIOD"},
            {"number": "%TS_RATE%", "id": "TS_RATE"},
            {"number": "%TS_PERIOD%", "id": "TS_PERIOD"},
        ],
    },
    {
        "csvFile": "oppvlwater_herhalingstijden.csv",
        "id": "%LOC_ID%",
        "attribute": [
            {"text": "Annual Exceedance", "id": "Selection"},
            {"number": "%H_Threshold%", "id": "H_Threshold"},
            {"number": "7", "id": "Viewperiod"},
            {"text": "Exponential", "id": "Function"},
            {"text": "Maximum Likelyhood", "id": "Fit"},
            {"text": "No", "id": "SelectComputationPeriod"},
            {"text": "%RekenPeriode_Start%", "id": "ComputationPeriodStart"},
            {"text": "%RekenPeriode_Eind%", "id": "ComputationPeriodEnd"},
            {"text": "YES", "id": "GraphConfidence"},
            {"number": "95", "id": "Confidence"},
            {"text": "Yes", "id": "GraphLegend"},
            {"number": "100", "id": "XasMax"},
            {"text": "01-01-2000", "id": "DayHourDate"},
            {"number": "%H_T1%", "id": "H_T1"},
            {"number": "%H_T2%", "id": "H_T2"},
            {"number": "%H_T5%", "id": "H_T5"},
            {"number": "%H_T10%", "id": "H_T10"},
            {"number": "%H_T25%", "id": "H_T25"},
            {"number": "%H_T50%", "id": "H_T50"},
            {"number": "%H_T100%", "id": "H_T100"},
        ],
    },
]


def test_waterstandlocationset_1(patched_path_constants_1):
    wsloc = constants.WaterstandLocationSet(fews_config_path=constants.PathConstants.fews_config.value.path)
    assert wsloc.fews_config.path == constants.D_WIS_60_REFERENTIE_201902
    assert wsloc.idmap_section_name == expected_idmap_section_name_1_and_2
    assert wsloc.name == expected_name_1_and_2
    assert wsloc.csv_filename == expected_csvfile_1_and_2
    assert wsloc.fews_name == expected_fews_name_1_and_2
    assert wsloc.get_validation_attributes(int_pars=None) == expected_validation_attributes_1_and_2
    assert wsloc.validation_rules == expected_validation_rules_1_and_2
    assert wsloc.csv_file_meta == expected_csvfile_meta_1
    assert wsloc.attrib_files == expected_attrib_files_1


def test_waterstandlocationset_2(patched_path_constants_2):
    wsloc = constants.WaterstandLocationSet(fews_config_path=constants.PathConstants.fews_config.value.path)
    assert wsloc.fews_config.path == constants.D_WIS_60_REFERENTIE_202002
    assert wsloc.idmap_section_name == expected_idmap_section_name_1_and_2
    assert wsloc.name == expected_name_1_and_2
    assert wsloc.csv_filename == expected_csvfile_1_and_2
    assert wsloc.fews_name == expected_fews_name_1_and_2
    assert wsloc.get_validation_attributes(int_pars=None) == expected_validation_attributes_1_and_2
    assert wsloc.validation_rules == expected_validation_rules_1_and_2
    assert wsloc.csv_file_meta == expected_csvfile_meta_2
    assert wsloc.attrib_files == expected_attrib_files_2
