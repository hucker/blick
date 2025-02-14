"""
Public API for the Blick project.
"""

from .rule_files import rule_large_files  # noqa: F401
from .rule_files import rule_max_files  # noqa: F401
from .rule_files import rule_path_exists  # noqa: F401
from .rule_files import rule_paths_exist  # noqa: F401
from .rule_files import rule_stale_files  # noqa: F401
from .blick_attribute import attributes  # noqa: F401
from .blick_attribute import get_attribute  # noqa: F401
# from .splint_attribute import _convert_to_minutes # noqa:F401
from .blick_checker import BlickChecker  # noqa: F401
from .blick_checker import BlickDebugProgress  # noqa; F401
from .blick_checker import BlickNoProgress  # noqa; F401
from .blick_checker import BlickProgress  # noqa: F401
from .blick_checker import exclude_levels  # noqa: F401
from .blick_checker import exclude_phases  # noqa: F401
from .blick_checker import exclude_ruids  # noqa: F401
from .blick_checker import exclude_tags  # noqa: F401
from .blick_checker import keep_levels  # noqa: F401
from .blick_checker import keep_phases  # noqa: F401
from .blick_checker import keep_ruids  # noqa: F401
from .blick_checker import keep_tags  # noqa: F401
from .blick_exception import BlickException  # noqa: F401
from .blick_format import BM
from .blick_format import BlickBasicHTMLRenderer
from .blick_format import BlickBasicMarkdown
from .blick_format import BlickBasicRichRenderer
from .blick_format import BlickBasicStreamlitRenderer
from .blick_format import BlickMarkup
from .blick_format import BlickRenderText
# from .blick_exception import BlickTypeError  # noqa: F401
# from .blick_exception import BlickValueError  # noqa: F401
from .blick_function import BlickFunction  # noqa: F401
from .blick_immutable import BlickEnvDict  # noqa: F401
from .blick_immutable import BlickEnvList  # noqa: F401
from .blick_immutable import BlickEnvSet  # noqa: F401
from .blick_jsonrc import BlickJsonRC  # noqa: F401
from .blick_module import BlickModule  # noqa: F401
from .blick_package import BlickPackage  # noqa: F401
from .blick_rc import BlickRC  # noqa: F401
from .blick_rc_factory import blick_rc_factory  # noqa:F401
from .blick_result import BR  # noqa: F401
from .blick_result import BlickResult  # noqa: F401
from .blick_result import BlickYield  # noqa: F401
from .blick_result import overview  # noqa: F401
from .blick_ruid import empty_ruids  # noqa: F401
from .blick_ruid import module_ruids  # noqa: F401
from .blick_ruid import package_ruids  # noqa: F401
from .blick_ruid import ruid_issues  # noqa: F401
from .blick_ruid import valid_ruids  # noqa: F401
from .blick_score import ScoreBinaryFail  # noqa: F401
from .blick_score import ScoreBinaryPass  # noqa: F401
from .blick_score import ScoreByFunctionBinary  # noqa: F401
from .blick_score import ScoreByFunctionMean  # noqa: F401
from .blick_score import ScoreByResult  # noqa: F401
from .blick_score import ScoreStrategy  # noqa: F401
from .blick_tomlrc import BlickTomlRC  # noqa: F401
from .blick_util import any_to_int_list  # noqa: F401
from .blick_util import any_to_str_list  # noqa: F401
from .blick_util import str_to_bool  # noqa: F401

try:
    import narwhals as nw
    from .rule_ndf import rule_validate_ndf_schema  # noqa: F401
    from .rule_ndf import rule_validate_ndf_values_by_col  # noqa: F401
    from .rule_ndf import rule_ndf_columns_check # noqa: F401
    from .rule_ndf import extended_bool # noqa: F401
except ImportError:
    pass

# webapi using requests
try:
    import requests
    from .rule_webapi import rule_url_200  # noqa: F401
    from .rule_webapi import rule_web_api  # noqa: F401
except ImportError:
    pass


# ping rules
try:
    import ping3
    from .rule_ping import rule_ping_check  # noqa: F401
except ImportError:
    pass

# xlsx rules
try:
    import openpyxl
    from .rule_xlsx import rule_xlsx_a1_pass_fail
    from .rule_xlsx import rule_xlsx_df_pass_fail
except ImportError:
    pass

# pdf rules
try:
    import camelot  # type: ignore
    import pandas as pd  # pylint: disable=ungrouped-imports
    from .rule_pdf import extract_tables_from_pdf  # noqa: F401
    from .rule_pdf import rule_from_pdf_rule_ids  # noqa: F401
except ImportError:
    pass

# sql alchemy support
try:
    import sqlalchemy
    from .rule_sqlachemy import rule_sql_table_col_name_schema
    from .rule_sqlachemy import rule_sql_table_schema
except ImportError:
    pass
