class ReprMixin:
    def __repr__(self):
        def filter_properties(obj):
            properties = obj.__dict__.keys()
            for prop in properties:
                if prop[0] != "_" and not callable(prop) and not isinstance(obj, prop.__class__):
                    yield ''.join([prop, '=', repr(getattr(obj, prop))])

        return "{}(\n\t{})".format(self.__class__.__name__,
            ',\n    '.join(filter_properties(self)))

    __str__ = __repr__