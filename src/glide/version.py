# Copyright EinStack
# SPDX-License-Identifier: APACHE-2.0
import sys
from typing import Final


PYTHON_VERSION: Final[str] = ".".join(
    (
        str(sys.version_info.major),
        str(sys.version_info.minor),
        str(sys.version_info.micro),
    )
)
__version__: Final[str] = "{}"
