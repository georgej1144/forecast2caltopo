"""The ``caic-python`` module.

Also defines ``__version__``:

The current version of ``caic-python`` - set by ``make change-version``.

Must map to ``pyproject.toml``'s version. Using ``make change-version``
or ``scripts/change-version.py`` ensures this.
"""

import logging
import sys
from . import models
import pydantic
from json import load, JSONDecodeError
__version__ = "0.1.10"

_CONFIG_FILE_ = "config.json"

_CONFIG_ = None

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.ERROR)

handler = logging.StreamHandler()
handler.setLevel(logging.ERROR)
LOGGER.addHandler(handler)

try:
    with open(_CONFIG_FILE_) as file:
        _CONFIG_ = models.ConfigObject(**load(file))
except pydantic.ValidationError as err:
                LOGGER.error(f"Unable to decode config object. version mismatch?: {err.errors()}")
except JSONDecodeError:
    _CONFIG_ = None
    print(f"Error loading config:\n{JSONDecodeError.msg}")

