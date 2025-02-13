#!/usr/bin/env python


import msgspec

###############################################################################


class IndividualTokenDetails(msgspec.Struct):
    """Basic Details for a GitHub Token."""

    token: str
    expiration_date: str | None | None = None


class MultipleTokenDetails(msgspec.Struct):
    """List of TokenDetails."""

    tokens: dict[str, IndividualTokenDetails] | None
