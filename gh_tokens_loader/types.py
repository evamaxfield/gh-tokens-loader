#!/usr/bin/env python

from typing import Optional

import msgspec

###############################################################################

class IndividualTokenDetails(msgspec.Struct):
    """Basic Details for a GitHub Token."""
    token: str
    expiration_date: Optional[str | None] = None

class MultipleTokenDetails(msgspec.Struct):
    """List of TokenDetails."""
    tokens: dict[str, IndividualTokenDetails] | None
