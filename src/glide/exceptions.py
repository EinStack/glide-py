# Copyright EinStack
# SPDX-License-Identifier: APACHE-2.0


class GlideError(Exception):
    """The base exception for all Glide server errors"""


class GlideUnavailable(GlideError):
    """
    Occurs when Glide API is not available
    """


class GlideClientError(GlideError):
    """
    Occurs when there is an issue with sending a Glide request
    """


class GlideClientMismatch(GlideError):
    """
    Occurs when there is a sign of possible compatibility issues between Glide API and the client version
    """


class GlideChatStreamError(GlideError):
    """
    Occurs when chat stream ends with an error
    """

    def __init__(self, message: str, err_name: str) -> None:
        super().__init__(message)

        self.err_name = err_name
