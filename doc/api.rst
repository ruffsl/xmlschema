API Documentation
=================

Module level API
----------------

.. function:: validate(xml_document, schema=None, cls=None, use_defaults=True)

    Validates an XML document against a schema instance. This function builds an
    :class:`XMLSchema` object for validating the XML document. Raises an
    :exc:`XMLSchemaValidationError` if the XML document is not validated against
    the schema.

    *xml_document* can be a file-like object or a string containing the XML data
    or a file path or an URI of a resource or an ElementTree/Element instance.
    *schema* can be a file-like object or a file path or an URI of a resource or
    a string containing the schema. *cls* is the schema class to use for building
    the instance (default is :class:`XMLSchema`). *use_defaults* defines when to
    use elements and attribute defaults for filling missing required values.

.. function:: to_dict(xml_document, schema=None, cls=None, path=None, process_namespaces=True, **kwargs)

    Decodes an XML document to a Python's nested dictionary. The decoding is based
    on an XML Schema class instance. For default the document is validated during
    the decode phase. Raises an :exc:`XMLSchemaValidationError` if the XML document
    is not validated against the schema.

    *xml_document* can be a file-like object or a string containing the XML data
    or a file path or an URI of a resource or an ElementTree/Element instance.
    *schema* can be a file-like object or a file path or an URI of a resource or
    a string containing the schema. *cls* is the schema class to use for building
    the instance (default is :class:`XMLSchema`). *path* is an optional XPath
    expression that matches the subelement of the document that have to be decoded.
    *process_namespaces* indicates whether to get the namespaces from the XML
    document and use them in the decoding process. With *kwargs* you can provide
    the optional arguments of :meth:`XMLSchema.iter_decode` as keyword arguments
    to variate the decoding process.


Schema level API
----------------

.. class:: XMLSchema(source, namespace=None, check_schema=False, global_maps=None)

    The class for an XML Schema instance, created using :class:`XMLSchemaValidator`.
    *source* can be an URI that reference to a resource or a file path or a file-like
    object or a string containing the schema. *namespace* is an optional argument
    that contains the URI of the namespace. When specified it must be equal to the
    *targetNamespace* declared in the schema. *check_schema* is a boolean value
    indicating whether the schema must be validated against XSD meta-schema before
    building. *global_maps* is an optional argument containing an :class:`XsdGlobal`
    instance, a mediator object for sharing declaration data between dependents
    schema instances.

    .. attribute::root

        The XML schema Element root.

    .. attribute:: text

        The XML schema source text.

    .. attribute:: uri

        The schema resource URI. It's None if the schema is built from a string.

    .. attribute:: target_namespace

        Is the *targetNamespace* of the schema, the namespace to which the schema's
        declarations belong. If it's empty none namespace is associated with the schema.
        In this case the schema declarations can be reused from other namespaces as
        *chameleon* definitions.

    .. py:attribute:: element_form

        *elementFormDefault* for the schema, default to ``'unqualified'``.

    .. py:attribute:: attribute_form

        *attributeFormDefault* for the schema, default to ``'unqualified'``.

    .. attribute:: schema_locations
    .. py:attribute:: no_namespace_schema_location

        Schema location hints. Usually specified in XML files, sometimes it's used
        in schemas when the namespace definitions are splitted into more files.

    .. attribute:: built

        Boolean flag that is ``True`` if schema declarations has been parsed and
        built, ``False`` if not.

    .. attribute:: namespaces

        A map from prefixes used by the schema to the correspondent namespace URI.
        This mapping can be different between each schema resource, so it's saved
        at schema's instance level.

    .. attribute:: maps

        An instance of :class:`XsdGlobal` that match the *global_maps* argument or
        a new :class:`XsdGlobal` object when this argument is not provided.

    .. attribute:: types
    .. attribute:: attributes
    .. attribute:: attribute_groups
    .. attribute:: groups
    .. attribute:: elements

        Dictionary views of the global declarations defined by the schema instance.
        The global declarations are taken from the declarations of :attr:`maps`.
        In the schema's views the global declaration names are registered with the
        local part only.

    .. classmethod:: create_schema(*args, **kwargs)

        Creates a new schema instance of the same class of the caller.

    .. classmethod:: check_schema(schema)

        Validates the given schema against the XSD :attr:`META_SCHEMA`.

        :raises: :exc:`XMLSchemaValidationError` if the schema is invalid.

    .. method:: validate(xml_document, use_defaults=True)

        Validates an XML document against the schema instance. *xml_document* can be
        a path to a file or an URI of a resource or an opened file-like object or
        an Element Tree instance or a string containing XML data. *use_defaults*
        indicates whether to use default values for filling missing attributes or
        elements.

        :raises: :exc:`XMLSchemaValidationError` if the XML document is invalid.

    .. method:: is_valid(xml_document, use_defaults=True)

        Like :meth:`validate` except that do not raises an exception but returns
        ``True`` if the XML document is valid, ``False`` if is invalid.

    .. method:: iter_errors(xml_document, path=None, use_defaults=True)

        Creates an iterator for errors generated by the validation of an XML
        document against the schema instance. *path* is an optional XPath expression
        that defines the parts of the document that have to be validated.
        *use_defaults* indicates whether to use default values for filling missing
        attributes or elements.

    .. method:: iter_decode(xml_document, path=None, validate=True, namespaces=None, \
                use_defaults=True, skip_errors=False, dict_class=dict, force_list=True, \
                text_key='#', attribute_prefix='@', **kwargs)

        Creates an iterator for decoding an XML document using the schema instance.
        Yields objects that can be dictionaries or simple data values.
        *path* is an optional XPath expression that matches the parts of the document
        that have to be decoded. *validate* defines if generates validation errors also.
        *namespaces* is an optional mapping from namespace prefix to full name.
        *use_defaults* indicates whether to use default values for filling missing
        attributes or elements. *skip_errors* indicates to skip a value with the XML
        value string in case of decoding error. *dict_class* the dictionary-like class
        that have to used instead of :class:`dict`. *force_list* indicates whether to
        force list at first insertion for elements declared in the schema with
        *maxOccurs* greater then 1 or ``'unbounded'``. *text_key* is the predefined key
        (default to ``'#text'``) for the text part of complex elements in the decoded
        dictionaries. *attribute_prefix* is the prefix character (default is ``'@'``)
        for naming attributes in the decoded dictionaries.

    .. method:: to_dict(xml_document, path=None, process_namespaces=True, **kwargs)

        Decodes an XML document to a nested dictionary, using the schema instance.
        *path* is an optional XPath expression that matches the subelement of the
        document that have to be decoded. *process_namespaces* indicates whether to
        get the namespaces from the XML document and use them in the decoding process.
        With *kwargs* you can provide the optional arguments of :meth:`iter_decode`
        as keyword arguments to variate the decoding process.

    .. method:: iter(name=None)

        Creates a schema iterator for elements declarations. The iteration starts
        from global XSD elements, going deep into the XSD declarations graph.
        If *name* argument is not ``None`` yields only the XSD elements matching
        the name.

    .. method:: iterchildren(name=None)

        Creates an iterator for global elements, sorted by name. If *name* is not
        ``None`` yields only the XSD global element matching the name.

    .. method:: find(path, namespaces=None)

        Finds the first XSD element or attribute declaration matching the path.
        Returns an XSD declaration or ``None`` if there is no match.
        *path* is an XPath expression. *namespaces* is an optional mapping from
        namespace prefix to full name.

    .. method:: findall(path, namespaces=None)

        Finds all matching XSD element or attribute declarations matching the path.
        Returns a list containing all matching declarations in the schema order.
        An empty list is returned if there is no match. *path* is an XPath expression.
        *namespaces* is an optional mapping from namespace prefix to full name.

    .. method:: iterfind(path, namespaces=None)

        Finds all matching XSD element or attribute declarations matching the path.
        Returns an iterable yielding all matching declarations in the schema order.
        *path* is an XPath expression. *namespaces* is an optional mapping from
        namespace prefix to full name.


XSD globals maps API
--------------------

.. autoclass:: xmlschema.XsdGlobals
    :members: copy, register, get_globals, iter_schemas, clear, build

XSD components API
------------------

.. autoclass:: xmlschema.xsdbase.XsdBase
    :members: id, validate, iter_errors, decode, encode, iter_decode, iter_encode

Errors and exceptions
---------------------

.. autoexception:: xmlschema.XMLSchemaException

.. autoexception:: xmlschema.XMLSchemaParseError

.. autoexception:: xmlschema.XMLSchemaRegexError

.. autoexception:: xmlschema.XMLSchemaXPathError

.. autoexception:: xmlschema.XMLSchemaComponentError

.. autoexception:: xmlschema.XMLSchemaValidationError

.. autoexception:: xmlschema.XMLSchemaDecodeError

.. autoexception:: xmlschema.XMLSchemaEncodeError
