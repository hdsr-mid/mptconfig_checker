from mptconfig import constants
from typing import Dict

import logging


# TODO: remove this complete file:
#  integration test with two different configs: paths to different config and get_series_startenddate.csv

logger = logging.getLogger(__name__)


def dict_compare(d1: Dict, d2: Dict):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o: (d1[o], d2[o]) for o in shared_keys if d1[o] != d2[o]}
    same = set(o for o in shared_keys if d1[o] == d2[o])
    return added, removed, modified, same


def validate_expected_summary(new_summary: Dict) -> None:
    expected_summary = constants.PATHS["expected_summary"]
    assert expected_summary, "this should not happen, no expected_summary found"

    added, removed, modified, same = dict_compare(d1=expected_summary, d2=new_summary)

    if same:
        logger.info("nice, summary is as expected")
        return

    logger.warning("not nice, summary is unexpected")
    for x in added:
        logger.warning(f"added={x}")

    for x in removed:
        logger.warning(f"removed={x}")

    for x in modified:
        logger.warning(f"modified={x}")
