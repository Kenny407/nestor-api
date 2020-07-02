# pylint: disable=duplicate-code
"""Schemas class to validate the Nestor configurations"""

from validator.config.config import SupportedValidations
from validator.schemas.application import APPLICATION_SCHEMA
from validator.schemas.project import PROJECT_SCHEMA
from validator.schemas.specs import SPECS

SCHEMAS = {
    str(SupportedValidations.APPLICATIONS): {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "definitions": SPECS,
        **APPLICATION_SCHEMA,
    },
    str(SupportedValidations.PROJECTS): {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "definitions": SPECS,
        **PROJECT_SCHEMA,
    },
}
