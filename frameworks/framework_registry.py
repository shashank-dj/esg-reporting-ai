from frameworks.csrd_gri_mapping import get_csrd_gri_mapping
from frameworks.sasb_mapping import get_sasb_mapping
from frameworks.tcfd_mapping import get_tcfd_mapping


def get_all_framework_mappings():
    return {
        "CSRD / GRI": get_csrd_gri_mapping(),
        "SASB": get_sasb_mapping(),
        "TCFD": get_tcfd_mapping(),
    }
