# -*- coding: utf-8 -*-
#
# Copyright (c), 2016-2017, SISSA (International School for Advanced Studies).
# All rights reserved.
# This file is distributed under the terms of the MIT License.
# See the file 'LICENSE' in the root directory of the present
# distribution, or http://opensource.org/licenses/MIT.
#
# @author Davide Brunato <brunato@sissa.it>
#
from .core import etree_get_namespaces
from .exceptions import (
    XMLSchemaException, XMLSchemaParseError, XMLSchemaValidationError,
    XMLSchemaDecodeError, XMLSchemaEncodeError, XMLSchemaXPathError,
    XMLSchemaRegexError, XMLSchemaNotBuiltError
)
from .resources import fetch_resource, load_xml_resource, fetch_schema
from .schema import XsdGlobals, XMLSchema
from .converters import (
    XMLSchemaConverter, ParkerConverter, BadgerFishConverter, AbderaConverter, JsonMLConverter
)

__version__ = '0.9.14'
__author__ = "Davide Brunato"
__contact__ = "brunato@sissa.it"
__copyright__ = "Copyright 2016-2017, SISSA"
__license__ = "MIT"
__status__ = "Production/Stable"


def validate(xml_document, schema=None, cls=XMLSchema, use_defaults=True):
    if schema is None:
        schema = fetch_schema(xml_document)
    cls(schema, validation='strict').validate(xml_document, use_defaults)


def to_dict(xml_document, schema=None, cls=XMLSchema, path=None, process_namespaces=True, **kwargs):
    if schema is None:
        schema = fetch_schema(xml_document)
    return cls(schema, validation='strict').to_dict(
        xml_document, path=path, process_namespaces=process_namespaces, **kwargs
    )
