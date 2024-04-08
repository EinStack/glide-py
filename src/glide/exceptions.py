# Copyright EinStack
# SPDX-License-Identifier: APACHE-2.0


class GlideUnavailable(Exception):
    """
    Occurs when Glide API is not available
    """


class GlideClientError(Exception):
    """
    Occurs when there is an issue with sending a Glide request
    """


class GlideClientMismatch(Exception):
    """
    Occurs when there is a sign of possible compatibility issues between Glide API and the client version
    """
