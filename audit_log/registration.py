class FieldRegistry(object):
    _registry = {}
    
    def __init__(self, fieldcls):
        self._fieldcls = fieldcls

    
    def add_field(self, model, field):
        reg = self.__class__._registry.setdefault(self._fieldcls, {}).setdefault(model, [])
        reg.append(field)

    def get_fields(self, model):
        fields = self.__class__._registry.setdefault(self._fieldcls, {}).get(model, [])

        # If the model inherits a concrete model which inherits an AuthStamp model
        for base_model in model.__bases__:
            fields.extend(self.__class__._registry.setdefault(self._fieldcls, {}).get(base_model, []))
        return fields

    def __contains__(self, model):
        fields = set(self.__class__._registry.setdefault(self._fieldcls, {}))
        models = {model, model.__bases__}
        for m in models:
            if m in fields:
                return True
        return False


