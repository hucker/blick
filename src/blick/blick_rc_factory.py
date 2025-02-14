"""
This module makes dealing with configuration files a bit easier as it supports JSON and TOML
out of the box.

I also have begun using the patch statement and this was a reasonable place to use it soe
I have provided two implementations.
"""

import sys

from .blick_exception import BlickException
from .blick_inirc import BlickIniRC
from .blick_jsonrc import BlickJsonRC
from .blick_rc import BlickRC
from .blick_tomlrc import BlickTomlRC
from .blick_xmlrc import BlickXMLRC

if sys.version_info[:2] >= (3, 10):
    def blick_rc_factory(param: dict | str, section: str = "") -> BlickRC:
        """
        Factory function to create an instance of BlickRC or its subclasses for Python 3.10 and above.
        """
        match param:
            case dict(d):
                if section == "":
                    return BlickRC(rc_d=d)
                else:
                    return BlickRC(rc_d=d[section])
            case str(s) if s.endswith('.toml'):
                return BlickTomlRC(cfg=s, section=section)
            case str(s) if s.endswith('.json'):
                return BlickJsonRC(cfg=s, section=section)
            case str(s) if s.endswith('.xml'):
                return BlickXMLRC(cfg=s, section=section)
            case str(s) if s.endswith('.ini'):
                return BlickIniRC(cfg=s, section=section)
            case _:
                raise BlickException('Invalid parameter type for splint_rc_factory.')
else:  # pragma: no cover
    def blick_rc_factory(param, section: str = "") -> BlickRC:
        """
        Factory function to create an instance of BlickRC or its subclasses for Python below 3.10.
        """
        if isinstance(param, dict):
            if not section:
                return BlickRC(rc_d=param)
            else:
                return BlickRC(rc_d=param[section])
        elif isinstance(param, str):
            if param.endswith('.toml'):
                return BlickTomlRC(cfg=param, section=section)
            elif param.endswith('.json'):
                return BlickJsonRC(cfg=param, section=section)
            elif param.endswith('.xml'):
                return BlickXMLRC(cfg=param, section=section)
            elif param.endswith('.ini'):
                return BlickIniRC(cfg=param, section=section)

        raise BlickException(f'Invalid parameter type for splint_rc_factory {param=}-{section=}.')
