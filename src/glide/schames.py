# Copyright EinStack
# SPDX-License-Identifier: APACHE-2.0
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class Schema(BaseModel):
    """
    A base schema for all Glide request/response schemas. It incorporates camelCase for all fields
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        protected_namespaces=(),
    )
