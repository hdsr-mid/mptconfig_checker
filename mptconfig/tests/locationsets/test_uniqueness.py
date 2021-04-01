from mptconfig import constants
from mptconfig.tests.fixtures import patched_path_constants_1
from mptconfig.tests.fixtures import patched_path_constants_2


# silence flake8 errors
_patched_path_constants_1 = patched_path_constants_1
_patched_path_constants_2 = patched_path_constants_2


expected_sub_loc_meta_1 = {
    "file": "oppvlwater_subloc",
    "geoDatum": "Rijks Driehoekstelsel",
    "id": "%LOC_ID%",
    "name": "%LOC_NAME%",
    "description": "Sublocaties oppervlaktewater",
    "parentLocationId": "%PAR_ID%",
    "startDateTime": "%START%",
    "endDateTime": "%EIND%",
    "x": "%X%",
    "y": "%Y%",
    "relation": [
        {"relatedLocationId": "%HBOV%", "id": "HBOV"},
        {"relatedLocationId": "%HBEN%", "id": "HBEN"},
        {"relatedLocationId": "%HBOVPS%", "id": "HBOVPS"},
        {"relatedLocationId": "%HBENPS%", "id": "HBENPS"},
        {"relatedLocationId": "%GAFCODE%", "id": "AFVOERGEBIED"},
        {"relatedLocationId": "%GPGIDENT%", "id": "PEILGEBIED"},
        {"relatedLocationId": "%RBGID%", "id": "RBGID"},
        {"relatedLocationId": "%B_VAN%", "id": "B_VAN"},
        {"relatedLocationId": "%B_NAAR%", "id": "B_NAAR"},
        {"relatedLocationId": "%AFGB_VAN%", "id": "AFGB_VAN"},
        {"relatedLocationId": "%AFGB_NAAR%", "id": "AFGB_NAAR"},
    ],
    "attribute": [
        {"text": "%LOC_NAME%", "id": "LOC_NAME"},
        {"text": "%QNORM%", "id": "QNORM"},
        {"text": "%TYPE%", "id": "TYPE"},
        {"text": "%ALLE_TYPES%", "id": "ALLE_TYPES"},
        {"text": "%FUNCTIE%", "id": "FUNCTIE"},
        {"text": "%AKKOORD%", "id": "WATERAKKOORD"},
        {"text": "%BALANS%", "id": "WATERBALANS"},
        {"text": "%SYSTEEM%", "id": "HOOFDSYSTEEM"},
        {"text": "%RAYON%", "id": "RAYON"},
        {"text": "%KOMPAS%", "id": "KOMPAS"},
        {"text": "%HBOV%", "id": "HBOV"},
        {"text": "%HBEN%", "id": "HBEN"},
        {"text": "%AFGB_NAAR%", "id": "AFGB_NAAR"},
        {"text": "%AFGB_VAN%", "id": "AFGB_VAN"},
        {"description": "Dit attribuut wordt in de filters gebruikt", "boolean": "%SWM%", "id": "SWM"},
        {"boolean": "%NWW-MDV%", "id": "SWMGEBIED_NWW-MDV"},
    ],
    "attributeFile": [
        {
            "csvFile": "oppvlwater_subloc_parameters.csv",
            "id": "%LOC_ID%",
            "attribute": {"text": "%PARAMETERS%", "id": "PARAMETERS"},
        },
        {
            "csvFile": "oppvlwater_subloc_validations.csv",
            "id": "%LOC_ID%",
            "attribute": [
                {"text": "%kunstvalidatie_freq%", "id": "kunstvalidatie_freq"},
                {"text": "%kunstvalidatie_kroos%", "id": "kunstvalidatie_kroos"},
                {"text": "%kunstvalidatie_kruinh%", "id": "kunstvalidatie_kruinh"},
                {"text": "%kunstvalidatie_schuifp%", "id": "kunstvalidatie_schuifp"},
                {"text": "%kunstvalidatie_schuifp2%", "id": "kunstvalidatie_schuifp2"},
                {"text": "%kunstvalidatie_stuur1%", "id": "kunstvalidatie_stuur1"},
                {"text": "%kunstvalidatie_stuur2%", "id": "kunstvalidatie_stuur2"},
                {"text": "%kunstvalidatie_stuur3%", "id": "kunstvalidatie_stuur3"},
            ],
        },
        {
            "csvFile": "oppvlwater_subloc_relatie_swm_arknzk.csv",
            "id": "%LOC_ID%",
            "checkForContinuousPeriod": "false",
            "relation": {"relatedLocationId": "%ACTUEEL%", "id": "SWMGEBIED"},
            "attribute": {"text": "%ACTUEEL%", "id": "SWMGEBIED_NZK-ARK"},
        },
        {
            "description": "GEEN TIJDSAFHANKELIJKHEID GEBRUIKEN HIER VOORLOPIG",
            "csvFile": "oppvlwater_subloc_relatie_debietmeter.csv",
            "id": "%LOC_ID%",
            "relation": {"relatedLocationId": "%DEBIETMETER%", "id": "DEBIETMETER"},
            "attribute": {"text": "DEBIETMETER", "id": "DEBIETMETER"},
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_debiet.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [
                {"number": "%Q_SMAX%", "id": "Q_SMAX"},
                {"number": "%Q_SMIN%", "id": "Q_SMIN"},
                {"number": "%Q_HMAX%", "id": "Q_HMAX"},
                {"number": "%Q_HMIN%", "id": "Q_HMIN"},
            ],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_freq.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [
                {"number": "%FRQ_HMAX%", "id": "FRQ_HMAX"},
                {"number": "%FRQ_HMIN%", "id": "FRQ_HMIN"},
                {"number": "%FRQ_RRRF%", "id": "FRQ_RRRF"},
                {"number": "%FRQ_RTS%", "id": "FRQ_RTS"},
                {"number": "%FRQ_TPS%", "id": "FRQ_TPS"},
            ],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_hefh.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [
                {"number": "%HEF_HMAX%", "id": "HEF_HMAX"},
                {"number": "%HEF_HMIN%", "id": "HEF_HMIN"},
                {"number": "%HEF_RRRF%", "id": "HEF_RRRF"},
                {"number": "%HEF_SARE%", "id": "HEF_SARE"},
                {"number": "%HEF_SAPE%", "id": "HEF_SAPE"},
                {"number": "%HEF_RTS%", "id": "HEF_RTS"},
                {"number": "%HEF_TPS%", "id": "HEF_TPS"},
            ],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_kruinh.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [
                {"number": "%KR_SMAX%", "id": "KR_SMAX"},
                {"number": "%KR_SMIN%", "id": "KR_SMIN"},
                {"number": "%KR_HMAX%", "id": "KR_HMAX"},
                {"number": "%KR_HMIN%", "id": "KR_HMIN"},
                {"number": "%KR_RRRF%", "id": "KR_RRRF"},
                {"number": "%KR_SARE%", "id": "KR_SARE"},
                {"number": "%KR_SAPE%", "id": "KR_SAPE"},
            ],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_schuifp.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [
                {"number": "%PERC_HMAX%", "id": "PERC_HMAX"},
                {"number": "%PERC_HMIN%", "id": "PERC_HMIN"},
                {"number": "%PERC_SMAX%", "id": "PERC_SMAX"},
                {"number": "%PERC_SMIN%", "id": "PERC_SMIN"},
            ],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_schuifp2.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [
                {"number": "%PERC2_HMAX%", "id": "PERC2_HMAX"},
                {"number": "%PERC2_HMIN%", "id": "PERC2_HMIN"},
                {"number": "%PERC2_SMAX%", "id": "PERC2_SMAX"},
                {"number": "%PERC2_SMIN%", "id": "PERC2_SMIN"},
            ],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_toert.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [
                {"number": "%TT_HMAX%", "id": "TT_HMAX"},
                {"number": "%TT_HMIN%", "id": "TT_HMIN"},
                {"number": "%TT_RRRF%", "id": "TT_RRRF"},
                {"number": "%TT_SARE%", "id": "TT_SARE"},
                {"number": "%TT_SAPE%", "id": "TT_SAPE"},
                {"number": "%TT_RTS%", "id": "TT_RTS"},
                {"number": "%TT_TPS%", "id": "TT_TPS"},
            ],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_kroos.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [
                {"number": "%HW_SMAX%", "id": "HW_SMAX"},
                {"number": "%HW_SMIN%", "id": "HW_SMIN"},
                {"number": "%HO_SMAX%", "id": "HO_SMAX"},
                {"number": "%HO_SMIN%", "id": "HO_SMIN"},
                {"number": "%HZ_SMAX%", "id": "HZ_SMAX"},
                {"number": "%HZ_SMIN%", "id": "HZ_SMIN"},
                {"number": "%H_HMAX%", "id": "H_HMAX"},
                {"number": "%H_HMIN%", "id": "H_HMIN"},
                {"number": "%H_RRRF%", "id": "H_RRRF"},
                {"number": "%H_SARE%", "id": "H_SARE"},
                {"number": "%H_SAPE%", "id": "H_SAPE"},
                {"number": "%H_RTS%", "id": "H_RTS"},
                {"number": "%H_TPS%", "id": "H_TPS"},
            ],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_stuur1.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [{"number": "%HR1_HMAX%", "id": "HR1_HMAX"}, {"number": "%HR1_HMIN%", "id": "HR1_HMIN"}],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_stuur2.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [{"number": "%HR2_HMAX%", "id": "HR2_HMAX"}, {"number": "%HR2_HMIN%", "id": "HR2_HMIN"}],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_stuur3.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [{"number": "%HR3_HMAX%", "id": "HR3_HMAX"}, {"number": "%HR3_HMIN%", "id": "HR3_HMIN"}],
        },
        {
            "csvFile": "herberekeningDebietenLocsets.csv",
            "id": "%locid%",
            "relation": [
                {"relatedLocationId": "%totaal_plus%", "id": "totaal_plus"},
                {"relatedLocationId": "%totaal_min%", "id": "totaal_min"},
            ],
            "attribute": [{"text": "%formule%", "id": "formule"}, {"text": "%keuze_formule%", "id": "keuze_formule"}],
        },
        {
            "csvFile": "herberekeningDebieten.csv",
            "id": "%locid%",
            "dateTimePattern": "yyyy-MM-dd",
            "startDateTime": "%startdate%",
            "endDateTime": "%enddate%",
            "attribute": [
                {"number": "%breedte%", "id": "breedte"},
                {"number": "%cc%", "id": "cc"},
                {"number": "%cd%", "id": "cd"},
                {"number": "%coefficient_a%", "id": "coefficient_a"},
                {"number": "%coefficient_b%", "id": "coefficient_b"},
                {"number": "%coefficient_c%", "id": "coefficient_c"},
                {"number": "%cv%", "id": "cv"},
                {"number": "%diameter%", "id": "diameter"},
                {"number": "%drempelhoogte%", "id": "drempelhoogte"},
                {"number": "%keuze_afsluitertype%", "id": "keuze_afsluitertype"},
                {"number": "%lengte%", "id": "lengte"},
                {"number": "%max_frequentie%", "id": "max_frequentie"},
                {"number": "%max_schuif%", "id": "max_schuif"},
                {"number": "%ontwerp_capaciteit%", "id": "ontwerp_capaciteit"},
                {"number": "%sw%", "id": "sw"},
                {"number": "%tastpunt%", "id": "tastpunt"},
                {"number": "%vulpunt%", "id": "vulpunt"},
                {"number": "%wandruwheid%", "id": "wandruwheid"},
                {"number": "%xi_extra%", "id": "xi_extra"},
                {"number": "%xi_intree%", "id": "xi_intree"},
                {"number": "%xi_uittree%", "id": "xi_uittree"},
                {"number": "%vaste_frequentie%", "id": "vaste_frequentie"},
            ],
        },
        {
            "csvFile": "herberekeningDebieten_h.csv",
            "id": "%locid%",
            "attribute": [
                {"number": "%bovenpeil%", "id": "bovenpeil"},
                {"number": "%benedenpeil%", "id": "benedenpeil"},
            ],
        },
    ],
}
expected_sub_loc_meta_2 = {}
expected_hoofd_loc_meta_1 = {
    "file": "oppvlwater_hoofdloc",
    "geoDatum": "Rijks Driehoekstelsel",
    "id": "%LOC_ID%",
    "name": "%LOC_NAME%",
    "description": "Hoofdlocaties oppervlaktewater",
    "toolTip": '<html>\n    <table id="details">\n      <tr>\n\t<td width="50" valign="top">ID</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%ID%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Naam</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%NAME%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Type</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%DESCRIPTION%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Foto</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top"><img src="file:$PHOTO_DIR$/Kunstwerkfoto/%FOTO_ID%" border="0" width="300" height="300"/></td>\n    </tr>\n    </table>\n</html>',
    "startDateTime": "%START%",
    "endDateTime": "%EIND%",
    "x": "%X%",
    "y": "%Y%",
    "z": "%Z%",
    "attribute": [
        {"text": "%ALLE_TYPES%", "id": "ALLE_TYPES"},
        {"text": "%SYSTEEM%", "id": "HOOFDSYSTEEM"},
        {"text": "%RAYON%", "id": "RAYON"},
        {"text": "%KOMPAS%", "id": "KOMPAS"},
        {"text": "%FOTO_ID%", "id": "FOTO_ID"},
        {"text": "%SCHEMA%", "id": "SCHEMA"},
    ],
    "attributeFile": [
        {
            "csvFile": "oppvlwater_hoofdloc_parameters.csv",
            "id": "%LOC_ID%",
            "attribute": {"text": "%PARAMETERS%", "id": "PARAMETERS"},
        },
        {
            "csvFile": "oppvlwater_hoofdloc_validations.csv",
            "id": "%LOC_ID%",
            "attribute": [
                {"text": "%kunstvalidatie_streef1%", "id": "kunstvalidatie_streef1"},
                {"text": "%kunstvalidatie_streef2%", "id": "kunstvalidatie_streef2"},
                {"text": "%kunstvalidatie_streef3%", "id": "kunstvalidatie_streef3"},
            ],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_streef1.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [{"number": "%HS1_HMAX%", "id": "HS1_HMAX"}, {"number": "%HS1_HMIN%", "id": "HS1_HMIN"}],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_streef2.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [{"number": "%HS2_HMAX%", "id": "HS2_HMAX"}, {"number": "%HS2_HMIN%", "id": "HS2_HMIN"}],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_streef3.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [{"number": "%HS3_HMAX%", "id": "HS3_HMAX"}, {"number": "%HS3_HMIN%", "id": "HS3_HMIN"}],
        },
        {
            "csvFile": "oppvlwater_kentermeetdata.csv",
            "id": "%LOC_ID%",
            "attribute": [
                {"text": "%KENTER_EAN%", "id": "EAN"},
                {"text": "%KENTER_EAN%", "id": "KENTER_EAN"},
                {"text": "%METER_ID%", "id": "METER_ID"},
            ],
        },
    ],
}
expected_hoofd_loc_meta_2 = {}
expected_ws_loc_meta_1 = {
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
expected_ws_loc_meta_2 = {}
expected_msw_loc_meta_1 = {}
expected_msw_loc_meta_2 = {}
expected_ps_loc_meta_1 = {}
expected_ps_loc_meta_2 = {}


general_location_set_dict_1_and_2 = [
    {
        "csvFile": {
            "file": "HDSR_neerslagstations",
            "geoDatum": "Rijks Driehoekstelsel",
            "id": "%LOC_ID%",
            "name": "%LOC_NAME%",
            "description": "HDSR neerslagstations",
            "startDateTime": "%START%",
            "endDateTime": "%EIND%",
            "x": "%X%",
            "y": "%Y%",
            "relation": [
                {"relatedLocationId": "%GAFCODE%", "id": "AFVOERGEBIED"},
                {"relatedLocationId": "%GPGIDENT%", "id": "PEILGEBIED"},
                {"relatedLocationId": "%RBGID%", "id": "RBGID"},
            ],
            "attribute": {"text": "%TS%", "id": "TIMESTEP"},
        },
        "id": "HDSRNEERSLAG",
    },
    {
        "csvFile": {
            "file": "ow_rwzi",
            "geoDatum": "Rijks Driehoekstelsel",
            "id": "%LOC_ID%",
            "name": "%LOC_NAME%",
            "description": "RWZI",
            "startDateTime": "%START%",
            "endDateTime": "%EIND%",
            "x": "%XCOORD%",
            "y": "%YCOORD%",
            "relation": [
                {"relatedLocationId": "%GAFCODE%", "id": "AFVOERGEBIED"},
                {"relatedLocationId": "%GPGIDENT%", "id": "PEILGEBIED"},
                {"relatedLocationId": "%RBGID%", "id": "RBGID"},
            ],
        },
        "id": "RWZI",
    },
    {
        "csvFile": {
            "file": "rioolgemalen_2",
            "geoDatum": "Rijks Driehoekstelsel",
            "id": "%LOC_ID%",
            "name": "%LOC_NAME%",
            "description": "Rioolgemaal",
            "x": "%X_COORD%",
            "y": "%Y_COORD%",
            "relation": [
                {"relatedLocationId": "%GAFCODE%", "id": "AFVOERGEBIED"},
                {"relatedLocationId": "%GPGIDENT%", "id": "PEILGEBIED"},
                {"relatedLocationId": "%RBGID%", "id": "RBGID"},
            ],
            "attribute": {"text": "%RWZI_ID%", "id": "RWZI_ID"},
        },
        "id": "RIOOLGEMALEN",
    },
    {
        "csvFile": {
            "file": "oppvlwater_wqloc",
            "geoDatum": "Rijks Driehoekstelsel",
            "id": "%LOC_ID%",
            "name": "%LOC_NAME%",
            "description": "Waterkwaliteitlocaties oppervlaktewater",
            "startDateTime": "%START%",
            "endDateTime": "%EIND%",
            "x": "%X%",
            "y": "%Y%",
            "z": "%Z%",
            "attributeFile": {
                "csvFile": "oppvlwater_wqloc_parameters.csv",
                "id": "%LOC_ID%",
                "attribute": {"text": "%PARAMETERS%", "id": "PARAMETERS"},
            },
        },
        "id": "OPVLWATER_WQLOC",
    },
    {
        "csvFile": {
            "file": "oppvlwater_hoofdloc",
            "geoDatum": "Rijks Driehoekstelsel",
            "id": "%LOC_ID%",
            "name": "%LOC_NAME%",
            "description": "Hoofdlocaties oppervlaktewater",
            "toolTip": '<html>\n    <table id="details">\n      <tr>\n\t<td width="50" valign="top">ID</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%ID%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Naam</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%NAME%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Type</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%DESCRIPTION%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Foto</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top"><img src="file:$PHOTO_DIR$/Kunstwerkfoto/%FOTO_ID%" border="0" width="300" height="300"/></td>\n    </tr>\n    </table>\n</html>',
            "startDateTime": "%START%",
            "endDateTime": "%EIND%",
            "x": "%X%",
            "y": "%Y%",
            "z": "%Z%",
            "attribute": [
                {"text": "%ALLE_TYPES%", "id": "ALLE_TYPES"},
                {"text": "%SYSTEEM%", "id": "HOOFDSYSTEEM"},
                {"text": "%RAYON%", "id": "RAYON"},
                {"text": "%KOMPAS%", "id": "KOMPAS"},
                {"text": "%FOTO_ID%", "id": "FOTO_ID"},
                {"text": "%SCHEMA%", "id": "SCHEMA"},
            ],
            "attributeFile": [
                {
                    "csvFile": "oppvlwater_hoofdloc_parameters.csv",
                    "id": "%LOC_ID%",
                    "attribute": {"text": "%PARAMETERS%", "id": "PARAMETERS"},
                },
                {
                    "csvFile": "oppvlwater_hoofdloc_validations.csv",
                    "id": "%LOC_ID%",
                    "attribute": [
                        {"text": "%kunstvalidatie_streef1%", "id": "kunstvalidatie_streef1"},
                        {"text": "%kunstvalidatie_streef2%", "id": "kunstvalidatie_streef2"},
                        {"text": "%kunstvalidatie_streef3%", "id": "kunstvalidatie_streef3"},
                    ],
                },
                {
                    "csvFile": "oppvlwater_kunstvalidatie_streef1.csv",
                    "id": "%LOC_ID%",
                    "startDateTime": "%STARTDATE%",
                    "endDateTime": "%ENDDATE%",
                    "attribute": [
                        {"number": "%HS1_HMAX%", "id": "HS1_HMAX"},
                        {"number": "%HS1_HMIN%", "id": "HS1_HMIN"},
                    ],
                },
                {
                    "csvFile": "oppvlwater_kunstvalidatie_streef2.csv",
                    "id": "%LOC_ID%",
                    "startDateTime": "%STARTDATE%",
                    "endDateTime": "%ENDDATE%",
                    "attribute": [
                        {"number": "%HS2_HMAX%", "id": "HS2_HMAX"},
                        {"number": "%HS2_HMIN%", "id": "HS2_HMIN"},
                    ],
                },
                {
                    "csvFile": "oppvlwater_kunstvalidatie_streef3.csv",
                    "id": "%LOC_ID%",
                    "startDateTime": "%STARTDATE%",
                    "endDateTime": "%ENDDATE%",
                    "attribute": [
                        {"number": "%HS3_HMAX%", "id": "HS3_HMAX"},
                        {"number": "%HS3_HMIN%", "id": "HS3_HMIN"},
                    ],
                },
                {
                    "csvFile": "oppvlwater_kentermeetdata.csv",
                    "id": "%LOC_ID%",
                    "attribute": [
                        {"text": "%KENTER_EAN%", "id": "EAN"},
                        {"text": "%KENTER_EAN%", "id": "KENTER_EAN"},
                        {"text": "%METER_ID%", "id": "METER_ID"},
                    ],
                },
            ],
        },
        "id": "OPVLWATER_HOOFDLOC",
    },
    {
        "csvFile": {
            "file": "oppvlwater_subloc",
            "geoDatum": "Rijks Driehoekstelsel",
            "id": "%LOC_ID%",
            "name": "%LOC_NAME%",
            "description": "Sublocaties oppervlaktewater",
            "parentLocationId": "%PAR_ID%",
            "startDateTime": "%START%",
            "endDateTime": "%EIND%",
            "x": "%X%",
            "y": "%Y%",
            "relation": [
                {"relatedLocationId": "%HBOV%", "id": "HBOV"},
                {"relatedLocationId": "%HBEN%", "id": "HBEN"},
                {"relatedLocationId": "%HBOVPS%", "id": "HBOVPS"},
                {"relatedLocationId": "%HBENPS%", "id": "HBENPS"},
                {"relatedLocationId": "%GAFCODE%", "id": "AFVOERGEBIED"},
                {"relatedLocationId": "%GPGIDENT%", "id": "PEILGEBIED"},
                {"relatedLocationId": "%RBGID%", "id": "RBGID"},
                {"relatedLocationId": "%B_VAN%", "id": "B_VAN"},
                {"relatedLocationId": "%B_NAAR%", "id": "B_NAAR"},
                {"relatedLocationId": "%AFGB_VAN%", "id": "AFGB_VAN"},
                {"relatedLocationId": "%AFGB_NAAR%", "id": "AFGB_NAAR"},
            ],
            "attribute": [
                {"text": "%LOC_NAME%", "id": "LOC_NAME"},
                {"text": "%QNORM%", "id": "QNORM"},
                {"text": "%TYPE%", "id": "TYPE"},
                {"text": "%ALLE_TYPES%", "id": "ALLE_TYPES"},
                {"text": "%FUNCTIE%", "id": "FUNCTIE"},
                {"text": "%AKKOORD%", "id": "WATERAKKOORD"},
                {"text": "%BALANS%", "id": "WATERBALANS"},
                {"text": "%SYSTEEM%", "id": "HOOFDSYSTEEM"},
                {"text": "%RAYON%", "id": "RAYON"},
                {"text": "%KOMPAS%", "id": "KOMPAS"},
                {"text": "%HBOV%", "id": "HBOV"},
                {"text": "%HBEN%", "id": "HBEN"},
                {"text": "%AFGB_NAAR%", "id": "AFGB_NAAR"},
                {"text": "%AFGB_VAN%", "id": "AFGB_VAN"},
                {"description": "Dit attribuut wordt in de filters gebruikt", "boolean": "%SWM%", "id": "SWM"},
                {"boolean": "%NWW-MDV%", "id": "SWMGEBIED_NWW-MDV"},
            ],
            "attributeFile": [
                {
                    "csvFile": "oppvlwater_subloc_parameters.csv",
                    "id": "%LOC_ID%",
                    "attribute": {"text": "%PARAMETERS%", "id": "PARAMETERS"},
                },
                {
                    "csvFile": "oppvlwater_subloc_validations.csv",
                    "id": "%LOC_ID%",
                    "attribute": [
                        {"text": "%kunstvalidatie_freq%", "id": "kunstvalidatie_freq"},
                        {"text": "%kunstvalidatie_kroos%", "id": "kunstvalidatie_kroos"},
                        {"text": "%kunstvalidatie_kruinh%", "id": "kunstvalidatie_kruinh"},
                        {"text": "%kunstvalidatie_schuifp%", "id": "kunstvalidatie_schuifp"},
                        {"text": "%kunstvalidatie_schuifp2%", "id": "kunstvalidatie_schuifp2"},
                        {"text": "%kunstvalidatie_stuur1%", "id": "kunstvalidatie_stuur1"},
                        {"text": "%kunstvalidatie_stuur2%", "id": "kunstvalidatie_stuur2"},
                        {"text": "%kunstvalidatie_stuur3%", "id": "kunstvalidatie_stuur3"},
                    ],
                },
                {
                    "csvFile": "oppvlwater_subloc_relatie_swm_arknzk.csv",
                    "id": "%LOC_ID%",
                    "checkForContinuousPeriod": "false",
                    "relation": {"relatedLocationId": "%ACTUEEL%", "id": "SWMGEBIED"},
                    "attribute": {"text": "%ACTUEEL%", "id": "SWMGEBIED_NZK-ARK"},
                },
                {
                    "description": "GEEN TIJDSAFHANKELIJKHEID GEBRUIKEN HIER VOORLOPIG",
                    "csvFile": "oppvlwater_subloc_relatie_debietmeter.csv",
                    "id": "%LOC_ID%",
                    "relation": {"relatedLocationId": "%DEBIETMETER%", "id": "DEBIETMETER"},
                    "attribute": {"text": "DEBIETMETER", "id": "DEBIETMETER"},
                },
                {
                    "csvFile": "oppvlwater_kunstvalidatie_debiet.csv",
                    "id": "%LOC_ID%",
                    "startDateTime": "%STARTDATE%",
                    "endDateTime": "%ENDDATE%",
                    "attribute": [
                        {"number": "%Q_SMAX%", "id": "Q_SMAX"},
                        {"number": "%Q_SMIN%", "id": "Q_SMIN"},
                        {"number": "%Q_HMAX%", "id": "Q_HMAX"},
                        {"number": "%Q_HMIN%", "id": "Q_HMIN"},
                    ],
                },
                {
                    "csvFile": "oppvlwater_kunstvalidatie_freq.csv",
                    "id": "%LOC_ID%",
                    "startDateTime": "%STARTDATE%",
                    "endDateTime": "%ENDDATE%",
                    "attribute": [
                        {"number": "%FRQ_HMAX%", "id": "FRQ_HMAX"},
                        {"number": "%FRQ_HMIN%", "id": "FRQ_HMIN"},
                        {"number": "%FRQ_RRRF%", "id": "FRQ_RRRF"},
                        {"number": "%FRQ_RTS%", "id": "FRQ_RTS"},
                        {"number": "%FRQ_TPS%", "id": "FRQ_TPS"},
                    ],
                },
                {
                    "csvFile": "oppvlwater_kunstvalidatie_hefh.csv",
                    "id": "%LOC_ID%",
                    "startDateTime": "%STARTDATE%",
                    "endDateTime": "%ENDDATE%",
                    "attribute": [
                        {"number": "%HEF_HMAX%", "id": "HEF_HMAX"},
                        {"number": "%HEF_HMIN%", "id": "HEF_HMIN"},
                        {"number": "%HEF_RRRF%", "id": "HEF_RRRF"},
                        {"number": "%HEF_SARE%", "id": "HEF_SARE"},
                        {"number": "%HEF_SAPE%", "id": "HEF_SAPE"},
                        {"number": "%HEF_RTS%", "id": "HEF_RTS"},
                        {"number": "%HEF_TPS%", "id": "HEF_TPS"},
                    ],
                },
                {
                    "csvFile": "oppvlwater_kunstvalidatie_kruinh.csv",
                    "id": "%LOC_ID%",
                    "startDateTime": "%STARTDATE%",
                    "endDateTime": "%ENDDATE%",
                    "attribute": [
                        {"number": "%KR_SMAX%", "id": "KR_SMAX"},
                        {"number": "%KR_SMIN%", "id": "KR_SMIN"},
                        {"number": "%KR_HMAX%", "id": "KR_HMAX"},
                        {"number": "%KR_HMIN%", "id": "KR_HMIN"},
                        {"number": "%KR_RRRF%", "id": "KR_RRRF"},
                        {"number": "%KR_SARE%", "id": "KR_SARE"},
                        {"number": "%KR_SAPE%", "id": "KR_SAPE"},
                    ],
                },
                {
                    "csvFile": "oppvlwater_kunstvalidatie_schuifp.csv",
                    "id": "%LOC_ID%",
                    "startDateTime": "%STARTDATE%",
                    "endDateTime": "%ENDDATE%",
                    "attribute": [
                        {"number": "%PERC_HMAX%", "id": "PERC_HMAX"},
                        {"number": "%PERC_HMIN%", "id": "PERC_HMIN"},
                        {"number": "%PERC_SMAX%", "id": "PERC_SMAX"},
                        {"number": "%PERC_SMIN%", "id": "PERC_SMIN"},
                    ],
                },
                {
                    "csvFile": "oppvlwater_kunstvalidatie_schuifp2.csv",
                    "id": "%LOC_ID%",
                    "startDateTime": "%STARTDATE%",
                    "endDateTime": "%ENDDATE%",
                    "attribute": [
                        {"number": "%PERC2_HMAX%", "id": "PERC2_HMAX"},
                        {"number": "%PERC2_HMIN%", "id": "PERC2_HMIN"},
                        {"number": "%PERC2_SMAX%", "id": "PERC2_SMAX"},
                        {"number": "%PERC2_SMIN%", "id": "PERC2_SMIN"},
                    ],
                },
                {
                    "csvFile": "oppvlwater_kunstvalidatie_toert.csv",
                    "id": "%LOC_ID%",
                    "startDateTime": "%STARTDATE%",
                    "endDateTime": "%ENDDATE%",
                    "attribute": [
                        {"number": "%TT_HMAX%", "id": "TT_HMAX"},
                        {"number": "%TT_HMIN%", "id": "TT_HMIN"},
                        {"number": "%TT_RRRF%", "id": "TT_RRRF"},
                        {"number": "%TT_SARE%", "id": "TT_SARE"},
                        {"number": "%TT_SAPE%", "id": "TT_SAPE"},
                        {"number": "%TT_RTS%", "id": "TT_RTS"},
                        {"number": "%TT_TPS%", "id": "TT_TPS"},
                    ],
                },
                {
                    "csvFile": "oppvlwater_kunstvalidatie_kroos.csv",
                    "id": "%LOC_ID%",
                    "startDateTime": "%STARTDATE%",
                    "endDateTime": "%ENDDATE%",
                    "attribute": [
                        {"number": "%HW_SMAX%", "id": "HW_SMAX"},
                        {"number": "%HW_SMIN%", "id": "HW_SMIN"},
                        {"number": "%HO_SMAX%", "id": "HO_SMAX"},
                        {"number": "%HO_SMIN%", "id": "HO_SMIN"},
                        {"number": "%HZ_SMAX%", "id": "HZ_SMAX"},
                        {"number": "%HZ_SMIN%", "id": "HZ_SMIN"},
                        {"number": "%H_HMAX%", "id": "H_HMAX"},
                        {"number": "%H_HMIN%", "id": "H_HMIN"},
                        {"number": "%H_RRRF%", "id": "H_RRRF"},
                        {"number": "%H_SARE%", "id": "H_SARE"},
                        {"number": "%H_SAPE%", "id": "H_SAPE"},
                        {"number": "%H_RTS%", "id": "H_RTS"},
                        {"number": "%H_TPS%", "id": "H_TPS"},
                    ],
                },
                {
                    "csvFile": "oppvlwater_kunstvalidatie_stuur1.csv",
                    "id": "%LOC_ID%",
                    "startDateTime": "%STARTDATE%",
                    "endDateTime": "%ENDDATE%",
                    "attribute": [
                        {"number": "%HR1_HMAX%", "id": "HR1_HMAX"},
                        {"number": "%HR1_HMIN%", "id": "HR1_HMIN"},
                    ],
                },
                {
                    "csvFile": "oppvlwater_kunstvalidatie_stuur2.csv",
                    "id": "%LOC_ID%",
                    "startDateTime": "%STARTDATE%",
                    "endDateTime": "%ENDDATE%",
                    "attribute": [
                        {"number": "%HR2_HMAX%", "id": "HR2_HMAX"},
                        {"number": "%HR2_HMIN%", "id": "HR2_HMIN"},
                    ],
                },
                {
                    "csvFile": "oppvlwater_kunstvalidatie_stuur3.csv",
                    "id": "%LOC_ID%",
                    "startDateTime": "%STARTDATE%",
                    "endDateTime": "%ENDDATE%",
                    "attribute": [
                        {"number": "%HR3_HMAX%", "id": "HR3_HMAX"},
                        {"number": "%HR3_HMIN%", "id": "HR3_HMIN"},
                    ],
                },
                {
                    "csvFile": "herberekeningDebietenLocsets.csv",
                    "id": "%locid%",
                    "relation": [
                        {"relatedLocationId": "%totaal_plus%", "id": "totaal_plus"},
                        {"relatedLocationId": "%totaal_min%", "id": "totaal_min"},
                    ],
                    "attribute": [
                        {"text": "%formule%", "id": "formule"},
                        {"text": "%keuze_formule%", "id": "keuze_formule"},
                    ],
                },
                {
                    "csvFile": "herberekeningDebieten.csv",
                    "id": "%locid%",
                    "dateTimePattern": "yyyy-MM-dd",
                    "startDateTime": "%startdate%",
                    "endDateTime": "%enddate%",
                    "attribute": [
                        {"number": "%breedte%", "id": "breedte"},
                        {"number": "%cc%", "id": "cc"},
                        {"number": "%cd%", "id": "cd"},
                        {"number": "%coefficient_a%", "id": "coefficient_a"},
                        {"number": "%coefficient_b%", "id": "coefficient_b"},
                        {"number": "%coefficient_c%", "id": "coefficient_c"},
                        {"number": "%cv%", "id": "cv"},
                        {"number": "%diameter%", "id": "diameter"},
                        {"number": "%drempelhoogte%", "id": "drempelhoogte"},
                        {"number": "%keuze_afsluitertype%", "id": "keuze_afsluitertype"},
                        {"number": "%lengte%", "id": "lengte"},
                        {"number": "%max_frequentie%", "id": "max_frequentie"},
                        {"number": "%max_schuif%", "id": "max_schuif"},
                        {"number": "%ontwerp_capaciteit%", "id": "ontwerp_capaciteit"},
                        {"number": "%sw%", "id": "sw"},
                        {"number": "%tastpunt%", "id": "tastpunt"},
                        {"number": "%vulpunt%", "id": "vulpunt"},
                        {"number": "%wandruwheid%", "id": "wandruwheid"},
                        {"number": "%xi_extra%", "id": "xi_extra"},
                        {"number": "%xi_intree%", "id": "xi_intree"},
                        {"number": "%xi_uittree%", "id": "xi_uittree"},
                        {"number": "%vaste_frequentie%", "id": "vaste_frequentie"},
                    ],
                },
                {
                    "csvFile": "herberekeningDebieten_h.csv",
                    "id": "%locid%",
                    "attribute": [
                        {"number": "%bovenpeil%", "id": "bovenpeil"},
                        {"number": "%benedenpeil%", "id": "benedenpeil"},
                    ],
                },
            ],
        },
        "id": "OPVLWATER_SUBLOC",
    },
    {
        "csvFile": {
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
        },
        "id": "OPVLWATER_WATERSTANDEN_AUTO",
    },
    {
        "csvFile": {
            "file": "oppvlwater_peilschalen",
            "geoDatum": "Rijks Driehoekstelsel",
            "id": "%LOC_ID%",
            "name": "%LOC_NAME%",
            "description": "Locaties waterstanden",
            "toolTip": '<html>\n    <table id="details">\n      <tr>\n\t<td width="50" valign="top">ID</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%ID%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Naam</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%NAME%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Type</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%DESCRIPTION%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Foto</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">\n\t   <img src="file:$PHOTO_DIR$/Peilschaalfoto/%FOTO_ID%" border="0" width="300" height="300"/>\n\t</td>\n      </tr>\n    </table>\n</html>',
            "startDateTime": "%START%",
            "endDateTime": "%EIND%",
            "x": "%X%",
            "y": "%Y%",
            "relation": [
                {"relatedLocationId": "%GAFCODE%", "id": "AFVOERGEBIED"},
                {"relatedLocationId": "%GPGIDENT%", "id": "PEILGEBIED"},
                {"relatedLocationId": "%RBGID%", "id": "RBGID"},
            ],
            "attribute": [
                {"text": "%PEILBESLUI%", "id": "PEILBESLUIT"},
                {"text": "%RAYON%", "id": "RAYON"},
                {"text": "%FOTO_ID%", "id": "FOTO_ID"},
            ],
        },
        "id": "OPVLWATER_PEILSCHALEN",
    },
    {
        "csvFile": {
            "file": "oppvlwater_inlaten",
            "geoDatum": "Rijks Driehoekstelsel",
            "id": "%LOC_ID%",
            "name": "%LOC_NAME%",
            "toolTip": '<html>\n    <table id="details">\n      <tr>\n\t<td width="50" valign="top">ID</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%ID%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Naam</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%NAME%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Foto</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">\n\t   <img src="file:$PHOTO_DIR$/Peilschaalfoto/%FOTO_ID%" border="0" width="300" height="300"/>\n\t</td>\n      </tr>\n    </table>\n</html>',
            "startDateTime": "%START%",
            "endDateTime": "%EIND%",
            "x": "%X%",
            "y": "%Y%",
            "z": "%Z%",
            "relation": [
                {"relatedLocationId": "%GAFCODE%", "id": "AFVOERGEBIED"},
                {"relatedLocationId": "%GPGIDENT%", "id": "PEILGEBIED"},
                {"relatedLocationId": "%RBGID%", "id": "RBGID"},
            ],
            "attribute": [
                {"text": "%RAYON%", "id": "RAYON"},
                {"text": "%FOTO_ID%", "id": "FOTO_ID"},
                {"text": "%PARAMETERS%", "id": "PARAMETERS"},
            ],
        },
        "id": "OPVLWATER_INLATEN",
    },
    {
        "csvFile": {
            "file": "msw_stations",
            "geoDatum": "Rijks Driehoekstelsel",
            "id": "%LOC_ID%",
            "name": "%LOC_NAME%",
            "description": "MSW-station",
            "x": "%X%",
            "y": "%Y%",
            "relation": [
                {"relatedLocationId": "%GAFCODE%", "id": "AFVOERGEBIED"},
                {"relatedLocationId": "%GPGIDENT%", "id": "PEILGEBIED"},
                {"relatedLocationId": "%RBGID%", "id": "RBGID"},
            ],
            "attribute": {"text": "%PARS%", "id": "PARS"},
        },
        "id": "MSW_STATIONS",
    },
    {
        "csvFile": {
            "file": "KNMI_uurstations.csv",
            "geoDatum": "Rijks Driehoekstelsel",
            "id": "%KNMIUUR_ID%",
            "name": "%PLAATS%",
            "description": "KNMI uurstation",
            "x": "%X%",
            "y": "%Y%",
            "relation": [
                {"relatedLocationId": "%GAFCODE%", "id": "AFVOERGEBIED"},
                {"relatedLocationId": "%GPGIDENT%", "id": "PEILGEBIED"},
                {"relatedLocationId": "%RBGID%", "id": "RBGID"},
            ],
            "attribute": {"text": "%STATION%", "id": "KNMIUUR_STATION"},
        },
        "id": "KNMIUUR",
    },
    {
        "csvFile": {
            "file": "KNMI_dagstations",
            "geoDatum": "Rijks Driehoekstelsel",
            "id": "%KNMIDAG_ID%",
            "name": "%LOCNAME%",
            "description": "KNMI neerslagstation",
            "x": "%X%",
            "y": "%Y%",
            "relation": [
                {"relatedLocationId": "%GAFCODE%", "id": "AFVOERGEBIED"},
                {"relatedLocationId": "%GPGIDENT%", "id": "PEILGEBIED"},
                {"relatedLocationId": "%RBGID%", "id": "RBGID"},
            ],
            "attribute": [
                {"text": "%LOCNR%", "id": "ID_KNMI"},
                {"text": "%LOCNAME%", "id": "KNMIDAG_STATION"},
                {"text": "%RAYON%", "id": "RAYON"},
            ],
        },
        "id": "KNMIDAG",
    },
    {
        "esriShapeFile": {
            "file": "afvoergebieden",
            "geoDatum": "Rijks Driehoekstelsel",
            "id": "%GAFCODE%",
            "name": "%GAFNAAM%",
            "x": "%XCOORD%",
            "y": "%YCOORD%",
            "relation": [
                {"relatedLocationId": "%GAFCODE%", "id": "AFVOERGEBIED"},
                {"relatedLocationId": "%REL_HDSR%", "id": "REL_HDSR"},
            ],
            "attribute": [
                {"text": "%GAFIDENT%", "id": "GAFIDENT"},
                {"number": "%AREA%", "id": "AREA"},
                {"number": "%OWF%", "id": "OWF"},
                {"text": "%AANVOER%", "id": "AANVOER"},
                {"text": "%AFVOER%", "id": "AFVOER"},
                {"text": "%GAFCODE%", "id": "LOC_ID"},
            ],
        },
        "id": "AFVOERGEBIEDEN",
    },
    {
        "locationSetId": "AFVOERGEBIEDEN",
        "constraints": {"attributeTextEquals": {"id": "AANVOER", "equals": "Y"}},
        "id": "AFVOERGEBIEDEN_AANVOER",
    },
    {
        "locationSetId": "AFVOERGEBIEDEN",
        "constraints": {"attributeTextEquals": {"id": "AFVOER", "equals": "Y"}},
        "id": "AFVOERGEBIEDEN_AFVOER",
    },
    {
        "esriShapeFile": {
            "file": "peilgebieden",
            "geoDatum": "Rijks Driehoekstelsel",
            "id": "%GPGIDENT%",
            "name": "%GPGNAAM%",
            "x": "%X%",
            "y": "%Y%",
            "relation": {"relatedLocationId": "%GPGIDENT%", "id": "PEILGEBIED"},
            "attribute": [
                {"text": "%PEILBESLUI%", "id": "PEILBESLUIT"},
                {"text": "%GPGIDENT%", "id": "PEILGEBIED"},
                {"number": "%OWF%", "id": "OWF"},
            ],
        },
        "id": "PEILGEBIEDEN",
    },
    {
        "esriShapeFile": {
            "file": "bemalingsgebieden",
            "geoDatum": "Rijks Driehoekstelsel",
            "id": "%RBGID%",
            "name": "%RGGIDENT%",
            "x": "%XCOORD%",
            "y": "%YCOORD%",
            "relation": {"relatedLocationId": "%RBGID%", "id": "RBGID"},
            "attribute": {"text": "%OBJECTID%", "id": "RGGIDENT"},
        },
        "id": "BEMALINGSGEBIEDEN",
    },
    {
        "csvFile": {
            "file": "GrondwaterMeetpunten",
            "geoDatum": "Rijks Driehoekstelsel",
            "id": "%LOC_ID%",
            "name": "%LOC_NAME%",
            "x": "%X%",
            "y": "%Y%",
            "z": "%MAAIVLDNAP%",
            "relation": [
                {"relatedLocationId": "%GAFCODE%", "id": "AFVOERGEBIED"},
                {"relatedLocationId": "%GPGIDENT%", "id": "PEILGEBIED"},
                {"relatedLocationId": "%RBGID%", "id": "RBGID"},
            ],
            "attribute": [
                {"text": "%NITG_CODE%", "id": "NITG_CODE"},
                {"text": "%MEETNET%", "id": "MEETNET"},
                {"text": "%PAKKETCODE%", "id": "PAKKETCODE"},
                {"text": "%TELEMETRIE%", "id": "TELEMETRIE"},
                {"text": "%LOC_NAME%", "id": "LOC_NAME"},
                {"number": "%GHG%", "id": "GHG"},
                {"number": "%GLG%", "id": "GLG"},
                {"number": "%GVG%", "id": "GVG"},
            ],
        },
        "id": "GRONDWATERMEETPUNTEN",
    },
    {
        "locationSetId": "GRONDWATERMEETPUNTEN",
        "constraints": {"attributeExists": {"id": "NITG_CODE"}},
        "id": "GRONDWATERMEETPUNTEN_DINO",
    },
    {
        "esriShapeFile": {
            "file": "boezemwatersysteem",
            "geoDatum": "Rijks Driehoekstelsel",
            "id": "%AFWID%",
            "name": "%AFWNAAM%",
            "x": "%X%",
            "y": "%Y%",
        },
        "id": "BOEZEMWATERSYSTEMEN",
    },
    {
        "esriShapeFile": {
            "file": "waterschappen2008",
            "geoDatum": "Rijks Driehoekstelsel",
            "id": "%ID%",
            "name": "%NAAM%",
        },
        "id": "WATERSCHAPPEN",
    },
    {
        "esriShapeFile": {
            "file": "begroeiingsgraad_trajecten",
            "geoDatum": "Rijks Driehoekstelsel",
            "id": "%LOC_ID%",
            "name": "%LOC_NAME%",
            "startDateTime": "%STARTDATUM%",
            "endDateTime": "%EINDDATUM%",
            "x": "%XCENTROID%",
            "y": "%YCENTROID%",
            "relation": {"relatedLocationId": "%RAYON%", "id": "BEG_RAYON"},
            "attribute": [
                {"text": "%TYPE%", "id": "TYPE"},
                {"text": "%RAYON%", "id": "BEG_RAYON"},
                {"text": "%REGIOCODE%", "id": "REGIOCODE"},
                {"text": "%MEETPUNT%", "id": "MEETPUNT"},
                {"text": "%NORMKLASSE%", "id": "BEG_KLASSE"},
                {"number": "%LIMIET%", "id": "LIMIET"},
            ],
        },
        "id": "BEGROEIINGSTRAJECTEN",
    },
    {
        "csvFile": {
            "file": "begroeiingsMonitoring",
            "geoDatum": "Rijks Driehoekstelsel",
            "id": "%LOC_ID%",
            "name": "%LOC_NAME%",
            "description": "BEGROEIINGSMEETPUNT",
            "startDateTime": "%STARTDATUM%",
            "endDateTime": "%EINDDATUM%",
            "x": "%X%",
            "y": "%Y%",
            "relation": {"relatedLocationId": "%RAYON%", "id": "BEG_RAYON"},
            "attribute": [
                {"text": "%LOC_ID%", "id": "LOC_ID"},
                {"text": "%LOC_NAME%", "id": "LOC_NAME"},
                {"text": "Puntmeting", "id": "TYPE"},
                {"text": "%RAYON%", "id": "BEG_RAYON"},
                {"text": "%REGIOCODE%", "id": "REGIOCODE"},
                {"text": "%MEETPUNT%", "id": "MEETPUNT"},
                {"text": "%EXTID%", "id": "EXTID"},
                {"text": "%WATERGANG%", "id": "WATERGANG"},
                {"text": "%NORMKLASSE%", "id": "BEG_KLASSE"},
                {"number": "%LIMIET%", "id": "LIMIET"},
            ],
        },
        "id": "BEGROEIINGSMONITORING",
    },
    {
        "locationId": "hkv_dummie",
        "locationSetId": "BEGROEIINGSMONITORING",
        "constraints": {
            "anyValid": {
                "idContains": {"contains": "hkv_dummie"},
                "attributeTextEquals": {"id": "BEG_KLASSE", "equals": "ergkrap"},
            }
        },
        "id": "BEGROEIINGSMONITORING_ERGKRAP",
    },
    {
        "locationId": "hkv_dummie",
        "locationSetId": "BEGROEIINGSMONITORING",
        "constraints": {
            "anyValid": {
                "idContains": {"contains": "hkv_dummie"},
                "attributeTextEquals": {"id": "BEG_KLASSE", "equals": "krap"},
            }
        },
        "id": "BEGROEIINGSMONITORING_KRAP",
    },
    {
        "locationId": "hkv_dummie",
        "locationSetId": "BEGROEIINGSMONITORING",
        "constraints": {
            "anyValid": {
                "idContains": {"contains": "hkv_dummie"},
                "attributeTextEquals": {"id": "BEG_KLASSE", "equals": "normaal"},
            }
        },
        "id": "BEGROEIINGSMONITORING_NORMAAL",
    },
    {
        "locationId": "hkv_dummie",
        "locationSetId": "BEGROEIINGSMONITORING",
        "constraints": {
            "anyValid": {
                "idContains": {"contains": "hkv_dummie"},
                "attributeTextEquals": {"id": "BEG_KLASSE", "equals": "ruim"},
            }
        },
        "id": "BEGROEIINGSMONITORING_RUIM",
    },
    {
        "locationId": "hkv_dummie",
        "locationSetId": "BEGROEIINGSMONITORING",
        "constraints": {
            "anyValid": {
                "idContains": {"contains": "hkv_dummie"},
                "attributeTextEquals": {"id": "BEG_KLASSE", "equals": "xruim"},
            }
        },
        "id": "BEGROEIINGSMONITORING_XRUIM",
    },
    {
        "esriShapeFile": {
            "file": "HDSR_Buitendienstgebieden",
            "geoDatum": "Rijks Driehoekstelsel",
            "id": "%RAYON%",
            "name": "%RAYON%",
            "x": "%X%",
            "y": "%Y%",
            "attribute": {"text": "%RAYON%", "id": "NAAM"},
        },
        "id": "BEG_RAYON",
    },
    {
        "locationSetId": "OPVLWATER_WATERSTANDEN_AUTO",
        "constraints": {"relatedLocationExists": {"locationRelationId": "AFVOERGEBIED"}},
        "id": "OPVLWATER_WATERSTANDEN_AFVOERGEBIED",
    },
    {
        "locationSetId": "OPVLWATER_WATERSTANDEN_AUTO",
        "constraints": {"relatedLocationExists": {"locationRelationId": "PEILGEBIED"}},
        "id": "OPVLWATER_WATERSTANDEN_PEILGEBIED",
    },
    {
        "locationSetId": "OPVLWATER_WATERSTANDEN_AUTO",
        "constraints": {"relatedLocationExists": {"locationRelationId": "RBGID"}},
        "id": "OPVLWATER_WATERSTANDEN_RBG",
    },
    {
        "locationSetId": "OPVLWATER_WATERSTANDEN_AUTO",
        "constraints": {"relatedLocationExists": {"locationRelationId": "PEILSCHAAL"}},
        "id": "OPVLWATER_WATERSTANDEN_PEILSCHAAL",
    },
    {
        "locationSetId": "OPVLWATER_PEILSCHALEN",
        "constraints": {"relatedLocationExists": {"locationRelationId": "PEILGEBIED"}},
        "id": "OPVLWATER_PEILSCHALEN_PEILGEBIED",
    },
    {
        "locationSetId": "OPVLWATER_PEILSCHALEN",
        "constraints": {"relatedLocationExists": {"locationRelationId": "AFVOERGEBIED"}},
        "id": "OPVLWATER_PEILSCHALEN_AFVOERGEBIED",
    },
    {"locationSetId": ["OPVLWATER_WATERSTANDEN_AUTO", "OPVLWATER_PEILSCHALEN"], "id": "OPVLWATER_WATERSTANDEN"},
    {"locationSetId": ["OPVLWATER_WATERSTANDEN", "GRONDWATERMEETPUNTEN"], "id": "OPVL_GROND_WATER_WATERSTANDEN"},
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"relatedLocationExists": {"locationRelationId": "HBOV"}},
        "id": "OPVLWATER_SUBLOC_HBOV",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"relatedLocationExists": {"locationRelationId": "HBEN"}},
        "id": "OPVLWATER_SUBLOC_HBEN",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"relatedLocationExists": {"locationRelationId": "HBOVPS"}},
        "id": "OPVLWATER_SUBLOC_HBOVPS",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"relatedLocationExists": {"locationRelationId": "HBENPS"}},
        "id": "OPVLWATER_SUBLOC_HBENPS",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextEquals": {"id": "TYPE", "equals": "pompvijzel"}},
        "id": "OPVLWATER_SUBLOC_POMPVIJZEL",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextEquals": {"id": "TYPE", "equals": "stuw"}},
        "id": "OPVLWATER_SUBLOC_STUW",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextEquals": {"id": "TYPE", "equals": "schuif"}},
        "id": "OPVLWATER_SUBLOC_SCHUIF",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextEquals": {"id": "TYPE", "equals": "debietmeter"}},
        "id": "OPVLWATER_SUBLOC_DEBIETMETER",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextEquals": {"id": "TYPE", "equals": "krooshek"}},
        "id": "OPVLWATER_SUBLOC_KROOSHEK",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextEquals": {"id": "TYPE", "equals": "vispassage"}},
        "id": "OPVLWATER_SUBLOC_VISPASSAGE",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextEquals": {"id": "TYPE", "equals": "afsluiter"}},
        "id": "OPVLWATER_SUBLOC_AFSLUITER",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "QNORM", "contains": "qnorm"}},
        "id": "OPVLWATER_SUBLOC_Q_NORM",
    },
    {"locationId": "KW102812", "id": "OPVLWATER_SUBLOC_VISSCHUIF"},
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeExists": {"id": "Q_HMAX"}},
        "id": "OPVLWATER_SUBLOC_Q_HMAX",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"not": {"attributeExists": {"id": "Q_HMAX"}}},
        "id": "OPVLWATER_SUBLOC_NO_Q_HMAX",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {
            "anyValid": {
                "attributeTextEquals": [
                    {"id": "TYPE", "equals": "pompvijzel"},
                    {"id": "TYPE", "equals": "stuw"},
                    {"id": "TYPE", "equals": "schuif"},
                    {"id": "TYPE", "equals": "debietmeter"},
                    {"id": "TYPE", "equals": "vispassage"},
                    {"id": "TYPE", "equals": "totaal"},
                ],
                "attributeTextContains": {"id": "PARAMETERS", "contains": "Q.G.0"},
                "idContains": {"contains": "KW104313"},
            }
        },
        "id": "OPVLWATER_SUBLOC_DEBIETEN",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC_DEBIETEN",
        "constraints": {"relatedLocationExists": {"locationRelationId": "HBOV"}},
        "id": "OPVLWATER_SUBLOC_DEBIETEN_HBOV",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC_DEBIETEN",
        "constraints": {"relatedLocationExists": {"locationRelationId": "HBEN"}},
        "id": "OPVLWATER_SUBLOC_DEBIETEN_HBEN",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC_DEBIETEN",
        "constraints": {
            "anyValid": {
                "attributeTextEquals": {"id": "FUNCTIE", "equals": "aanvoer"},
                "attributeTextContains": {"id": "LOC_NAME", "contains": "-totaal_aanvoer"},
            }
        },
        "id": "OPVLWATER_SUBLOC_DEBIETEN_AANVOER",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC_DEBIETEN",
        "constraints": {
            "anyValid": {
                "attributeTextEquals": [
                    {"id": "FUNCTIE", "equals": "afvoer"},
                    {"id": "FUNCTIE", "equals": "debietmeting"},
                ],
                "attributeTextContains": {"id": "LOC_NAME", "contains": "-totaal_afvoer"},
            }
        },
        "id": "OPVLWATER_SUBLOC_DEBIETEN_AFVOER",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {
            "attributeTextEquals": {"id": "formule", "equals": "Debiet Inlaat"},
            "not": {"relatedLocationExists": {"locationRelationId": "DEBIETMETER"}},
        },
        "id": "DEBIETBEREKENING_Inlaat",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {
            "attributeTextEquals": {"id": "formule", "equals": "Debiet Kantelstuw"},
            "not": {"relatedLocationExists": {"locationRelationId": "DEBIETMETER"}},
        },
        "id": "DEBIETBEREKENING_Kantelstuw",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {
            "attributeTextEquals": {"id": "formule", "equals": "Debiet Schuif"},
            "not": {"relatedLocationExists": {"locationRelationId": "DEBIETMETER"}},
        },
        "id": "DEBIETBEREKENING_Schuif",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {
            "anyValid": {
                "attributeTextEquals": [
                    {"id": "formule", "equals": "Debiet overlaat"},
                    {"id": "formule", "equals": "Debiet ECOStuw"},
                ]
            },
            "not": {"relatedLocationExists": {"locationRelationId": "DEBIETMETER"}},
        },
        "id": "DEBIETBEREKENING_Overlaat",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {
            "attributeTextEquals": {"id": "formule", "equals": "Debiet Pomp"},
            "not": {"relatedLocationExists": {"locationRelationId": "DEBIETMETER"}},
        },
        "id": "DEBIETBEREKENING_Pomp",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {
            "attributeTextEquals": [{"id": "formule", "equals": "Debiet Pomp"}, {"id": "keuze_formule", "equals": "1"}],
            "not": [
                {"relatedLocationExists": {"locationRelationId": "DEBIETMETER"}},
                {"idContains": {"contains": "KW218221"}},
                {"idContains": {"contains": "KW218231"}},
            ],
        },
        "id": "DEBIETBEREKENING_Pomp_sF",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {
            "attributeTextEquals": {"id": "formule", "equals": "Debiet Pomp"},
            "not": [
                {"attributeTextEquals": {"id": "keuze_formule", "equals": "1"}},
                {"relatedLocationExists": {"locationRelationId": "DEBIETMETER"}},
            ],
        },
        "id": "DEBIETBEREKENING_Pomp_gF",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {
            "attributeTextEquals": {"id": "formule", "equals": "Debiet Vijzel"},
            "not": {"relatedLocationExists": {"locationRelationId": "DEBIETMETER"}},
        },
        "id": "DEBIETBEREKENING_Vijzel",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {
            "anyValid": {
                "attributeTextEquals": [
                    {"id": "formule", "equals": "Debiet SluisVispassage"},
                    {"id": "formule", "equals": "Debiet WitVispassage"},
                ]
            },
            "not": {"relatedLocationExists": {"locationRelationId": "DEBIETMETER"}},
        },
        "id": "DEBIETBEREKENING_Vispassage",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {
            "anyValid": {
                "idContains": [{"contains": "KW218221"}, {"contains": "KW218231"}],
                "attributeTextEquals": [
                    {"id": "formule", "equals": "Debiet Inlaat"},
                    {"id": "formule", "equals": "Debiet Kantelstuw"},
                    {"id": "formule", "equals": "Debiet Schuif"},
                    {"id": "formule", "equals": "Debiet overlaat"},
                    {"id": "formule", "equals": "Debiet ECOStuw"},
                    {"id": "formule", "equals": "Debiet Vijzel"},
                    {"id": "formule", "equals": "Debiet SluisVispassage"},
                    {"id": "formule", "equals": "Debiet WitVispassage"},
                ],
                "allValid": {
                    "attributeTextEquals": [
                        {"id": "formule", "equals": "Debiet Pomp"},
                        {"id": "keuze_formule", "equals": "1"},
                    ]
                },
            },
            "not": {"relatedLocationExists": {"locationRelationId": "DEBIETMETER"}},
        },
        "id": "DEBIETBEREKENING",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {
            "anyValid": {
                "attributeTextEquals": [
                    {"id": "formule", "equals": "Debiet Inlaat"},
                    {"id": "formule", "equals": "Debiet Kantelstuw"},
                    {"id": "formule", "equals": "Debiet Schuif"},
                    {"id": "formule", "equals": "Debiet overlaat"},
                    {"id": "formule", "equals": "Debiet ECOStuw"},
                    {"id": "formule", "equals": "Debiet Vijzel"},
                    {"id": "formule", "equals": "Debiet SluisVispassage"},
                    {"id": "formule", "equals": "Debiet WitVispassage"},
                ],
                "allValid": {
                    "attributeTextEquals": [
                        {"id": "formule", "equals": "Debiet Pomp"},
                        {"id": "keuze_formule", "equals": "1"},
                    ]
                },
            },
            "not": {"relatedLocationExists": {"locationRelationId": "DEBIETMETER"}},
            "relatedLocationExists": {"locationRelationId": "totaal_plus"},
        },
        "id": "DEBIETBEREKENING_TOTAAL_PLUS",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {
            "anyValid": {
                "attributeTextEquals": [
                    {"id": "formule", "equals": "Debiet Inlaat"},
                    {"id": "formule", "equals": "Debiet Kantelstuw"},
                    {"id": "formule", "equals": "Debiet Schuif"},
                    {"id": "formule", "equals": "Debiet overlaat"},
                    {"id": "formule", "equals": "Debiet ECOStuw"},
                    {"id": "formule", "equals": "Debiet Vijzel"},
                    {"id": "formule", "equals": "Debiet SluisVispassage"},
                    {"id": "formule", "equals": "Debiet WitVispassage"},
                ],
                "allValid": {
                    "attributeTextEquals": [
                        {"id": "formule", "equals": "Debiet Pomp"},
                        {"id": "keuze_formule", "equals": "1"},
                    ]
                },
            },
            "not": {"relatedLocationExists": {"locationRelationId": "DEBIETMETER"}},
            "relatedLocationExists": {"locationRelationId": "totaal_min"},
        },
        "id": "DEBIETBEREKENING_TOTAAL_MIN",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "LOC_NAME", "contains": "-totaal"}},
        "id": "DEBIETBEREKENING_TOTAAL",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {
            "anyValid": {
                "attributeTextEquals": [
                    {"id": "formule", "equals": "Debiet Inlaat"},
                    {"id": "formule", "equals": "Debiet Kantelstuw"},
                    {"id": "formule", "equals": "Debiet Schuif"},
                    {"id": "formule", "equals": "Debiet overlaat"},
                    {"id": "formule", "equals": "Debiet ECOStuw"},
                    {"id": "formule", "equals": "Debiet Vijzel"},
                ],
                "allValid": {
                    "attributeTextEquals": [
                        {"id": "formule", "equals": "Debiet Pomp"},
                        {"id": "keuze_formule", "equals": "1"},
                    ]
                },
            },
            "not": [
                {"relatedLocationExists": {"locationRelationId": "HBOV"}},
                {"relatedLocationExists": {"locationRelationId": "DEBIETMETER"}},
            ],
        },
        "id": "OPVLWATER_SUBLOC_DEBIETEN_NOHBOV",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {
            "anyValid": {
                "attributeTextEquals": [
                    {"id": "formule", "equals": "Debiet Inlaat"},
                    {"id": "formule", "equals": "Debiet Kantelstuw"},
                    {"id": "formule", "equals": "Debiet Schuif"},
                    {"id": "formule", "equals": "Debiet overlaat"},
                    {"id": "formule", "equals": "Debiet ECOStuw"},
                    {"id": "formule", "equals": "Debiet Vijzel"},
                ],
                "allValid": {
                    "attributeTextEquals": [
                        {"id": "formule", "equals": "Debiet Pomp"},
                        {"id": "keuze_formule", "equals": "1"},
                    ]
                },
            },
            "not": [
                {"relatedLocationExists": {"locationRelationId": "HBEN"}},
                {"relatedLocationExists": {"locationRelationId": "DEBIETMETER"}},
            ],
        },
        "id": "OPVLWATER_SUBLOC_DEBIETEN_NOHBEN",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"not": {"idContains": {"contains": "_totaal"}}},
        "id": "BEREKEND_DEBIET_NT",
    },
    {
        "locationSetId": "OPVLWATER_WQLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "C."}},
        "id": "OPVLWATER_WQLOC_CONDUCT_MILLI",
    },
    {
        "locationSetId": "OPVLWATER_WQLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "C2."}},
        "id": "OPVLWATER_WQLOC_CONDUCT_MICRO",
    },
    {
        "locationSetId": "OPVLWATER_WQLOC",
        "constraints": {
            "anyValid": {
                "attributeTextContains": [
                    {"id": "PARAMETERS", "contains": "C.0"},
                    {"id": "PARAMETERS", "contains": "C2.0"},
                ]
            }
        },
        "id": "OPVLWATER_WQLOC_CONDUCT",
    },
    {
        "locationSetId": "OPVLWATER_WQLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "O2ppm."}},
        "id": "OPVLWATER_WQLOC_O2",
    },
    {
        "locationSetId": "OPVLWATER_WQLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "T."}},
        "id": "OPVLWATER_WQLOC_TC",
    },
    {
        "locationSetId": "OPVLWATER_WQLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "OPAQ."}},
        "id": "OPVLWATER_WQLOC_TROEB",
    },
    {
        "locationSetId": "OPVLWATER_HOOFDLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "Q.S."}},
        "id": "OPVLWATER_HFDLOC_QS",
    },
    {
        "locationSetId": "OPVLWATER_HOOFDLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "Q2.S."}},
        "id": "OPVLWATER_HFDLOC_Q2S",
    },
    {
        "locationSetId": "OPVLWATER_HOOFDLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "Q3.S."}},
        "id": "OPVLWATER_HFDLOC_Q3S",
    },
    {
        "locationSetId": "OPVLWATER_HOOFDLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "Q.R."}},
        "id": "OPVLWATER_HFDLOC_QR",
    },
    {
        "locationSetId": "OPVLWATER_HOOFDLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "Q2.R."}},
        "id": "OPVLWATER_HFDLOC_Q2R",
    },
    {
        "locationSetId": "OPVLWATER_HOOFDLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "Q3.R."}},
        "id": "OPVLWATER_HFDLOC_Q3R",
    },
    {
        "locationSetId": "OPVLWATER_HOOFDLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "H.S."}},
        "id": "OPVLWATER_HFDLOC_HSTREEF1",
    },
    {
        "locationSetId": "OPVLWATER_HOOFDLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "H2.S."}},
        "id": "OPVLWATER_HFDLOC_HSTREEF2",
    },
    {
        "locationSetId": "OPVLWATER_HOOFDLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "H3.S."}},
        "id": "OPVLWATER_HFDLOC_HSTREEF3",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "ES."}},
        "id": "OPVLWATER_SUBLOC_ES",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "ES2."}},
        "id": "OPVLWATER_SUBLOC_ES2",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "F."}},
        "id": "OPVLWATER_SUBLOC_FR",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "Hh."}},
        "id": "OPVLWATER_SUBLOC_HH1",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "Hk."}},
        "id": "OPVLWATER_SUBLOC_HK",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "H.G."}},
        "id": "OPVLWATER_SUBLOC_HM1",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "H.R."}},
        "id": "OPVLWATER_SUBLOC_HSTUUR1",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "H2.R."}},
        "id": "OPVLWATER_SUBLOC_HSTUUR2",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "H3.R."}},
        "id": "OPVLWATER_SUBLOC_HSTUUR3",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "IB."}},
        "id": "OPVLWATER_SUBLOC_IB0",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "IBH."}},
        "id": "OPVLWATER_SUBLOC_IBH",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "IBL."}},
        "id": "OPVLWATER_SUBLOC_IBL",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "POS."}},
        "id": "OPVLWATER_SUBLOC_POS1",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "POS2."}},
        "id": "OPVLWATER_SUBLOC_POS2",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "Qipcl.G."}},
        "id": "OPVLWATER_SUBLOC_QIPCL",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "Q.G."}},
        "id": "OPVLWATER_SUBLOC_QM1",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "DD.15"}},
        "id": "OPVLWATER_SUBLOC_DD0",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "DDH.15"}},
        "id": "OPVLWATER_SUBLOC_DDH",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "DDL.15"}},
        "id": "OPVLWATER_SUBLOC_DDL",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "TT.15"}},
        "id": "OPVLWATER_SUBLOC_RPM",
    },
    {
        "locationSetId": "OPVLWATER_WQLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "C.0"}},
        "id": "OPVLWATER_WQLOC_CONDUCT_MILLI_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_WQLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "C2.0"}},
        "id": "OPVLWATER_WQLOC_CONDUCT_MICRO_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_WQLOC",
        "constraints": {
            "anyValid": {
                "attributeTextContains": [
                    {"id": "PARAMETERS", "contains": "C.0"},
                    {"id": "PARAMETERS", "contains": "C2.0"},
                ]
            }
        },
        "id": "OPVLWATER_WQLOC_CONDUCT_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_WQLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "OPAQ.0"}},
        "id": "OPVLWATER_WQLOC_TROEB_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_HOOFDLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "Q.S.0"}},
        "id": "OPVLWATER_HFDLOC_QS_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_WQLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "O2ppm.0"}},
        "id": "OPVLWATER_WQLOC_O2_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_WQLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "T.0"}},
        "id": "OPVLWATER_WQLOC_TC_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_HOOFDLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "H.S.0"}},
        "id": "OPVLWATER_HFDLOC_HSTREEF1_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_HOOFDLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "WR.0"}},
        "id": "OPVLWATER_HFDLOC_WR_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_HOOFDLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "WS.0"}},
        "id": "OPVLWATER_HFDLOC_WS_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_HOOFDLOC",
        "constraints": {"attributeExists": {"id": "KENTER_EAN"}},
        "id": "OPVLWATER_HFDLOC_KENTERMEETDATA",
    },
    {
        "locationSetId": "OPVLWATER_INLATEN",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "Hh.0"}},
        "id": "OPVLWATER_INLATEN_HH_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_INLATEN",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "POS.0"}},
        "id": "OPVLWATER_INLATEN_POS1_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "ES.0"}},
        "id": "OPVLWATER_SUBLOC_ES_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "ES2.0"}},
        "id": "OPVLWATER_SUBLOC_ES2_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "F.0"}},
        "id": "OPVLWATER_SUBLOC_FR_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "Hh.0"}},
        "id": "OPVLWATER_SUBLOC_HH1_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "Hk.0"}},
        "id": "OPVLWATER_SUBLOC_HK_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "H.G.0"}},
        "id": "OPVLWATER_SUBLOC_HM1_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "H.R.0"}},
        "id": "OPVLWATER_SUBLOC_HSTUUR1_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "H2.R.0"}},
        "id": "OPVLWATER_SUBLOC_HSTUUR2_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "H3.R.0"}},
        "id": "OPVLWATER_SUBLOC_HSTUUR3_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "IB.0"}},
        "id": "OPVLWATER_SUBLOC_IB0_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "IBH.0"}},
        "id": "OPVLWATER_SUBLOC_IBH_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "IBL.0"}},
        "id": "OPVLWATER_SUBLOC_IBL_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "POS.0"}},
        "id": "OPVLWATER_SUBLOC_POS1_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "POS2.0"}},
        "id": "OPVLWATER_SUBLOC_POS2_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "Qipcl.G.0"}},
        "id": "OPVLWATER_SUBLOC_QIPCL_NONEQ",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "PARAMETERS", "contains": "Q.G.0"}},
        "id": "OPVLWATER_SUBLOC_QM1_NONEQ",
    },
    {
        "chainageLocationAttributeId": "Langsprofiel_Kromme_Rijn",
        "id": "Langsprofiel_Kromme_Rijn",
        "name": "Set_Kromme_Rijn",
    },
    {
        "chainageLocationAttributeId": "Langsprofiel_Caspargouwse_Wetering",
        "id": "Langsprofiel_Caspargouwse_Wetering",
        "name": "Set_Caspargouwse_Wetering",
    },
    {
        "chainageLocationAttributeId": "Langsprofiel_Stadswater_Utrecht_en_Vecht",
        "id": "Langsprofiel_Stadswater_Utrecht_en_Vecht",
        "name": "Set_Stadswater_Utrecht_en_Vecht",
    },
    {
        "chainageLocationAttributeId": "Langsprofiel_Doorslag-Gekanaliseerde_Hollandse_IJssel",
        "id": "Langsprofiel_Doorslag-Gekanaliseerde_Hollandse_IJssel",
        "name": "Set_Doorslag-Gekanaliseerde_Hollandse_IJssel",
    },
    {
        "chainageLocationAttributeId": "Langsprofiel_Oude_Rijn_boezem_Oost",
        "id": "Langsprofiel_Oude_Rijn_boezem_Oost",
        "name": "Set_Oude_Rijn_boezem_Oost",
    },
    {
        "chainageLocationAttributeId": "Langsprofiel_Oude_Rijn_boezem_West",
        "id": "Langsprofiel_Oude_Rijn_boezem_West",
        "name": "Set_Oude_Rijn_boezem_West",
    },
    {"chainageLocationAttributeId": "Langsprofiel_Grecht", "id": "Langsprofiel_Grecht", "name": "Set_Grecht"},
    {
        "chainageLocationAttributeId": "Langsprofiel_Lange_Linschoten_tm_Jaap_Bijzerwetering",
        "id": "Langsprofiel_Lange_Linschoten_tm_Jaap_Bijzerwetering",
        "name": "Set_Lange_Linschoten_tm_Jaap_Bijzerwetering",
    },
    {
        "chainageLocationAttributeId": "Langsprofiel_Dubbele_Wiericke",
        "id": "Langsprofiel_Dubbele_Wiericke",
        "name": "Set_Dubbele_Wiericke",
    },
    {
        "chainageLocationAttributeId": "Langsprofiel_Leidsche_Rijn",
        "id": "Langsprofiel_Leidsche_Rijn",
        "name": "Set_Leidsche_Rijn",
    },
    {
        "chainageLocationAttributeId": "Langsprofiel_Amsterdam-Rijnkanaal",
        "id": "Langsprofiel_Amsterdam-Rijnkanaal",
        "name": "Set_Amsterdam-Rijnkanaal",
    },
    {
        "chainageLocationAttributeId": "Langsprofiel_Merwedekanaal",
        "id": "Langsprofiel_Merwedekanaal",
        "name": "Set_Merwedekanaal",
    },
    {
        "chainageLocationAttributeId": "Langsprofiel_Boezem_AGV",
        "id": "Langsprofiel_Boezem_AGV",
        "name": "Set_Boezem_AGV",
    },
    {
        "chainageLocationAttributeId": "Langsprofiel_Langbroekerwetering",
        "id": "Langsprofiel_Langbroekerwetering",
        "name": "Set_Langbroekerwetering",
    },
    {
        "chainageLocationAttributeId": "Langsprofiel_Amerongerwetering",
        "id": "Langsprofiel_Amerongerwetering",
        "name": "Set_Amerongerwetering",
    },
    {
        "chainageLocationAttributeId": "Langsprofiel_Schalkwijkse_wetering",
        "id": "Langsprofiel_Schalkwijkse_wetering",
        "name": "Set_Schalkwijkse_wetering",
    },
    {"locationSetId": ["RIOOLGEMALEN", "RWZI"], "id": "RIOOLGEMALEN_EN_RWZIS"},
    {
        "locationId": ["KW102512", "KW102812", "KW102912", "KW103012", "KW103812", "KW104313", "KW215412", "KW216225"],
        "id": "STROOMSNELHEID",
    },
    {
        "locationSetId": "HDSRNEERSLAG",
        "constraints": {"attributeTextEquals": {"id": "TIMESTEP", "equals": "900"}},
        "id": "HDSRNEERSLAG_15M",
    },
    {
        "locationSetId": "HDSRNEERSLAG",
        "constraints": {"attributeTextEquals": {"id": "TIMESTEP", "equals": "300"}},
        "id": "HDSRNEERSLAG_5M",
    },
    {
        "locationSetId": "OPVLWATER_WATERSTANDEN_AUTO",
        "constraints": {"relatedLocationExists": {"locationRelationId": "REL_DIFF"}},
        "id": "OPVLWATER_WATERSTANDEN_DIFF",
        "name": "Set gaten vullen door verschil",
    },
    {
        "locationSetId": "OPVLWATER_WATERSTANDEN_AUTO",
        "constraints": {"relatedLocationExists": {"locationRelationId": "REL_CACB"}},
        "id": "OPVLWATER_WATERSTANDEN_CACB",
        "name": "Set gaten vullen door relatie",
    },
    {
        "locationSetId": ["OPVLWATER_WATERSTANDEN_DIFF", "OPVLWATER_WATERSTANDEN_CACB"],
        "id": "OPVLWATER_WATERSTANDEN_GAPFILLING",
    },
    {
        "locationSetId": "OPVLWATER_WATERSTANDEN_AUTO",
        "constraints": {"attributeExists": {"id": "watervalidatie"}},
        "id": "OPVLWATER_WATERSTANDEN_VALID",
    },
    {
        "locationId": "hkv_dummie",
        "locationSetId": "OPVLWATER_WATERSTANDEN_AUTO",
        "constraints": {"not": {"attributeExists": {"id": "watervalidatie"}}},
        "id": "OPVLWATER_WATERSTANDEN_NOVALID",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC_HM1_NONEQ",
        "constraints": {"attributeExists": {"id": "kunstvalidatie_kroos"}},
        "id": "OPVLWATER_SUBLOC_HM1_NONEQ_VALID",
    },
    {
        "locationId": "hkv_dummie",
        "locationSetId": "OPVLWATER_SUBLOC_HM1_NONEQ",
        "constraints": {"not": {"attributeExists": {"id": "kunstvalidatie_kroos"}}},
        "id": "OPVLWATER_SUBLOC_HM1_NONEQ_NOVALID",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC_HK_NONEQ",
        "constraints": {"attributeExists": {"id": "kunstvalidatie_kruinh"}},
        "id": "OPVLWATER_SUBLOC_HK_NONEQ_VALID",
    },
    {
        "locationId": "hkv_dummie",
        "locationSetId": "OPVLWATER_SUBLOC_HK_NONEQ",
        "constraints": {"not": {"attributeExists": {"id": "kunstvalidatie_kruinh"}}},
        "id": "OPVLWATER_SUBLOC_HK_NONEQ_NOVALID",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC_FR_NONEQ",
        "constraints": {"attributeExists": {"id": "kunstvalidatie_freq"}},
        "id": "OPVLWATER_SUBLOC_FR_NONEQ_VALID",
    },
    {
        "locationId": "hkv_dummie",
        "locationSetId": "OPVLWATER_SUBLOC_FR_NONEQ",
        "constraints": {"not": {"attributeExists": {"id": "kunstvalidatie_freq"}}},
        "id": "OPVLWATER_SUBLOC_FR_NONEQ_NOVALID",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC_HH1_NONEQ",
        "constraints": {"attributeExists": {"id": "HEF_HMAX"}},
        "id": "OPVLWATER_SUBLOC_HH1_NONEQ_VALID",
    },
    {
        "locationId": "hkv_dummie",
        "locationSetId": "OPVLWATER_SUBLOC_HH1_NONEQ",
        "constraints": {"not": {"attributeExists": {"id": "HEF_HMAX"}}},
        "id": "OPVLWATER_SUBLOC_HH1_NONEQ_NOVALID",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC_POS1_NONEQ",
        "constraints": {"attributeExists": {"id": "kunstvalidatie_schuifp"}},
        "id": "OPVLWATER_SUBLOC_POS1_NONEQ_VALID",
    },
    {
        "locationId": "hkv_dummie",
        "locationSetId": "OPVLWATER_SUBLOC_POS1_NONEQ",
        "constraints": {"not": {"attributeExists": {"id": "kunstvalidatie_schuifp"}}},
        "id": "OPVLWATER_SUBLOC_POS1_NONEQ_NOVALID",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC_POS2_NONEQ",
        "constraints": {"attributeExists": {"id": "kunstvalidatie_schuifp2"}},
        "id": "OPVLWATER_SUBLOC_POS2_NONEQ_VALID",
    },
    {
        "locationId": "hkv_dummie",
        "locationSetId": "OPVLWATER_SUBLOC_POS2_NONEQ",
        "constraints": {"not": {"attributeExists": {"id": "kunstvalidatie_schuifp2"}}},
        "id": "OPVLWATER_SUBLOC_POS2_NONEQ_NOVALID",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC_RPM",
        "constraints": {"attributeExists": {"id": "TT_HMAX"}},
        "id": "OPVLWATER_SUBLOC_RPM_VALID",
    },
    {
        "locationId": "hkv_dummie",
        "locationSetId": "OPVLWATER_SUBLOC_RPM",
        "constraints": {"not": {"attributeExists": {"id": "TT_HMAX"}}},
        "id": "OPVLWATER_SUBLOC_RPM_NOVALID",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC_HSTUUR1_NONEQ",
        "constraints": {"attributeExists": {"id": "kunstvalidatie_stuur1"}},
        "id": "OPVLWATER_SUBLOC_HSTUUR1_NONEQ_VALID",
    },
    {
        "locationId": "hkv_dummie",
        "locationSetId": "OPVLWATER_SUBLOC_HSTUUR1_NONEQ",
        "constraints": {"not": {"attributeExists": {"id": "kunstvalidatie_stuur1"}}},
        "id": "OPVLWATER_SUBLOC_HSTUUR1_NONEQ_NOVALID",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC_HSTUUR2_NONEQ",
        "constraints": {"attributeExists": {"id": "kunstvalidatie_stuur2"}},
        "id": "OPVLWATER_SUBLOC_HSTUUR2_NONEQ_VALID",
    },
    {
        "locationId": "hkv_dummie",
        "locationSetId": "OPVLWATER_SUBLOC_HSTUUR2_NONEQ",
        "constraints": {"not": {"attributeExists": {"id": "kunstvalidatie_stuur2"}}},
        "id": "OPVLWATER_SUBLOC_HSTUUR2_NONEQ_NOVALID",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC_HSTUUR3_NONEQ",
        "constraints": {"attributeExists": {"id": "kunstvalidatie_stuur3"}},
        "id": "OPVLWATER_SUBLOC_HSTUUR3_NONEQ_VALID",
    },
    {
        "locationId": "hkv_dummie",
        "locationSetId": "OPVLWATER_SUBLOC_HSTUUR3_NONEQ",
        "constraints": {"not": {"attributeExists": {"id": "kunstvalidatie_stuur3"}}},
        "id": "OPVLWATER_SUBLOC_HSTUUR3_NONEQ_NOVALID",
    },
    {
        "locationSetId": "OPVLWATER_HFDLOC_HSTREEF1_NONEQ",
        "constraints": {"attributeExists": {"id": "kunstvalidatie_streef1"}},
        "id": "OPVLWATER_HFDLOC_HSTREEF1_NONEQ_VALID",
    },
    {
        "locationId": "hkv_dummie",
        "locationSetId": "OPVLWATER_HFDLOC_HSTREEF1_NONEQ",
        "constraints": {"not": {"attributeExists": {"id": "kunstvalidatie_streef1"}}},
        "id": "OPVLWATER_HFDLOC_HSTREEF1_NONEQ_NOVALID",
    },
    {
        "locationSetId": "OPVLWATER_HFDLOC_HSTREEF2",
        "constraints": {"attributeExists": {"id": "kunstvalidatie_streef2"}},
        "id": "OPVLWATER_HFDLOC_HSTREEF2_VALID",
    },
    {
        "locationId": "hkv_dummie",
        "locationSetId": "OPVLWATER_HFDLOC_HSTREEF2",
        "constraints": {"not": {"attributeExists": {"id": "kunstvalidatie_streef2"}}},
        "id": "OPVLWATER_HFDLOC_HSTREEF2_NOVALID",
    },
    {
        "locationId": "hkv_dummie",
        "locationSetId": "OPVLWATER_HFDLOC_HSTREEF3",
        "constraints": {"attributeExists": {"id": "kunstvalidatie_streef3"}},
        "id": "OPVLWATER_HFDLOC_HSTREEF3_VALID",
    },
    {
        "locationId": "hkv_dummie",
        "locationSetId": "OPVLWATER_HFDLOC_HSTREEF3",
        "constraints": {"not": {"attributeExists": {"id": "kunstvalidatie_streef3"}}},
        "id": "OPVLWATER_HFDLOC_HSTREEF3_NOVALID",
    },
    {
        "locationId": [
            "ImportAfvalwater",
            "ImportWaterwatch",
            "ImportEtHkvItc",
            "ImportEvaporation",
            "ImportGrondwater",
            "ImportNeerslag",
            "ImportNeerslagMFBS",
            "ImportOpvlWater",
            "RadarCorrectie",
            "RadarRuw",
            "WerkFilter",
            "MetingenFilter",
        ],
        "id": "MODULES",
    },
    {
        "description": "West , Oos, EvS, en heel HDSR",
        "csvFile": {
            "file": "swmgebieden",
            "geoDatum": "Rijks Driehoekstelsel",
            "id": "%LOC_ID%",
            "name": "%LOC_NAME%",
            "x": "%X%",
            "y": "%Y%",
            "relation": {"relatedLocationId": "%SUM_LOC%", "id": "SUM_LOC"},
            "attribute": [{"boolean": "%SWM%", "id": "SWM"}, {"text": "%LOC_ID%", "id": "SWM_ID"}],
        },
        "id": "SWMGEBIEDEN",
    },
    {
        "description": "West, Oos, EvS, niet heel HDSR",
        "locationSetId": "SWMGEBIEDEN",
        "constraints": {"relatedLocationExists": {"locationRelationId": "SUM_LOC"}},
        "id": "SWMSUBGEBIEDEN",
    },
    {
        "description": "Alleen heel HDSR",
        "locationSetId": "SWMGEBIEDEN",
        "constraints": {"not": {"relatedLocationExists": {"locationRelationId": "SUM_LOC"}}},
        "id": "SWMHDSRGEBIEDEN",
    },
    {
        "locationSetId": "SWMGEBIEDEN",
        "constraints": {"idContains": {"contains": "aanvoer"}},
        "id": "SWMGEBIEDEN_AANVOER",
    },
    {"locationSetId": "SWMGEBIEDEN", "constraints": {"idContains": {"contains": "afvoer"}}, "id": "SWMGEBIEDEN_AFVOER"},
    {
        "locationSetId": "SWMSUBGEBIEDEN",
        "constraints": {"not": {"idContains": {"contains": "netto"}}},
        "id": "SWMSUBGEBIEDEN_AANAFVOER",
    },
    {"locationSetId": "SWMGEBIEDEN", "constraints": {"idContains": {"contains": "netto"}}, "id": "SWMGEBIEDEN_NETTO"},
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "SWMGEBIED_NZK-ARK", "contains": "aanvoer"}},
        "id": "OPVLWATER_SUBLOC_SWM_AANVOER",
    },
    {
        "locationSetId": "OPVLWATER_SUBLOC",
        "constraints": {"attributeTextContains": {"id": "SWMGEBIED_NZK-ARK", "contains": "afvoer"}},
        "id": "OPVLWATER_SUBLOC_SWM_AFVOER",
    },
    {"locationSetId": ["OPVLWATER_SUBLOC_SWM_AANVOER", "OPVLWATER_SUBLOC_SWM_AFVOER"], "id": "OPVLWATER_SUBLOC_SWM"},
    {
        "locationSetId": "OPVLWATER_WATERSTANDEN_AUTO",
        "constraints": {"attributeExists": {"id": "H_Threshold"}},
        "id": "HERHALINGSTIJDEN.OW",
    },
]


def test_general_location_set_dict_1(patched_path_constants_1):
    hoofd = constants.hoofdlocationset.general_location_set_dict
    sub = constants.sublocationset.general_location_set_dict
    ws = constants.waterstandlocationset.general_location_set_dict
    msw = constants.mswlocationset.general_location_set_dict
    ps = constants.pslocationset.general_location_set_dict
    assert hoofd == sub == ws == msw == ps == general_location_set_dict_1_and_2


def test_general_location_set_dict_2(patched_path_constants_2):
    hoofd = constants.hoofdlocationset.general_location_set_dict
    sub = constants.sublocationset.general_location_set_dict
    ws = constants.waterstandlocationset.general_location_set_dict
    msw = constants.mswlocationset.general_location_set_dict
    ps = constants.pslocationset.general_location_set_dict
    assert hoofd == sub == ws == msw == ps == general_location_set_dict_1_and_2


def test_unique_validation_attributes1(patched_path_constants_1):
    hoofd = constants.hoofdlocationset.get_validation_attributes(int_pars=None)
    sub = constants.sublocationset.get_validation_attributes(int_pars=None)
    ws = constants.waterstandlocationset.get_validation_attributes(int_pars=None)
    msw = constants.mswlocationset.get_validation_attributes(int_pars=None)
    ps = constants.pslocationset.get_validation_attributes(int_pars=None)
    assert hoofd and sub and ws
    assert not msw and not ps
    assert hoofd != sub != ws


def test_unique_validation_attributes2(patched_path_constants_2):
    hoofd = constants.hoofdlocationset.get_validation_attributes(int_pars=None)
    sub = constants.sublocationset.get_validation_attributes(int_pars=None)
    ws = constants.waterstandlocationset.get_validation_attributes(int_pars=None)
    msw = constants.mswlocationset.get_validation_attributes(int_pars=None)
    ps = constants.pslocationset.get_validation_attributes(int_pars=None)
    assert hoofd and sub and ws
    assert not msw and not ps
    assert hoofd != sub != ws


def test_unique_csvfile_meta1(patched_path_constants_1):
    from mptconfig.tmp import dict_compare

    hoofd = constants.hoofdlocationset.csvfile_meta
    sub = constants.sublocationset.csvfile_meta
    ws = constants.waterstandlocationset.csvfile_meta
    msw = constants.mswlocationset.csvfile_meta
    ps = constants.pslocationset.csvfile_meta
    assert hoofd and sub and ws and msw and ps
    assert hoofd != sub != ws != msw != ps
    assert sub == expected_sub_loc_meta_1
    assert hoofd == expected_hoofd_loc_meta_1
    added, removed, modified, same = dict_compare(d1=ws, d2=expected_ws_loc_meta_1)
    assert not added and not removed
    assert list(modified.keys()) == ["attributeFile"]
    for index in range(0, 5):
        assert ws["attributeFile"][index] == expected_ws_loc_meta_1["attributeFile"][index]
    assert len(ws["attributeFile"]) == 6
    assert len(expected_ws_loc_meta_1["attributeFile"]) == 5

    # TODO
    renier
    # waar komt dit nou weer vandaan?
    ws["attributeFile"][5] = {
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
    }

    # assert not added and not removed
    # assert sorted(modified.keys()) == ["attributeFile"]
    # for index in range(0, 5):
    #     assert hoofd["attributeFile"][index] == expected_hoofd_loc_meta_1["attributeFile"][index]
    # assert hoofd["attributeFile"][5] == {
    #     "csvFile": "oppvlwater_kentermeetdata.csv",
    #     "id": "%LOC_ID%",
    #     "attribute": [
    #         {"text": "%KENTER_EAN%", "id": "EAN"},
    #         {"text": "%KENTER_EAN%", "id": "KENTER_EAN"},
    #         {"text": "%METER_ID%", "id": "METER_ID"},
    #     ],
    # }
    # assert expected_hoofd_loc_meta_1["attributeFile"][5] == {
    #     "csvFile": "oppvlwater_kentermeetdata.csv",
    #     "id": "%LOC_ID%",
    #     "attribute": [{"text": "%KENTER_EAN%", "id": "KENTER_EAN"}, {"text": "%METER_ID%", "id": "METER_ID"}],
    # }
    print("hoi")


def test_unique_csvfile_meta2(patched_path_constants_2):
    hoofd = constants.hoofdlocationset.csvfile_meta
    sub = constants.sublocationset.csvfile_meta
    ws = constants.waterstandlocationset.csvfile_meta
    msw = constants.mswlocationset.csvfile_meta
    ps = constants.pslocationset.csvfile_meta
    assert hoofd and sub and ws and msw and ps
    assert hoofd != sub != ws != msw != ps


def test_unique_attribute_files1(patched_path_constants_1):
    hoofd = constants.hoofdlocationset.attrib_files
    sub = constants.sublocationset.attrib_files
    ws = constants.waterstandlocationset.attrib_files
    msw = constants.mswlocationset.attrib_files
    ps = constants.pslocationset.attrib_files
    assert hoofd and sub and ws
    assert not msw and not ps
    assert hoofd != sub != ws


def test_unique_attribute_files2(patched_path_constants_2):
    hoofd = constants.hoofdlocationset.attrib_files
    sub = constants.sublocationset.attrib_files
    ws = constants.waterstandlocationset.attrib_files
    msw = constants.mswlocationset.attrib_files
    ps = constants.pslocationset.attrib_files
    assert hoofd and sub and ws
    assert not msw and not ps
    assert hoofd != sub != ws
