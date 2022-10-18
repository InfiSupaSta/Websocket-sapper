class Validator:

    def __set_name__(self, owner, name):
        self.self_name = '_' + name
        self.instance_name = name

    def __set__(self, instance, value):
        self.validate(attribute_name=self.instance_name, value=value)
        setattr(instance, self.self_name, value)

    def __get__(self, instance, owner):
        return getattr(instance, self.self_name)

    def validate(self, *, attribute_name, value):
        raise NotImplementedError(f"Validator must implement validate method.")


class QuantityValidator(Validator):

    def validate(self, *, attribute_name, value):

        if isinstance(value, int) and value > 0:
            return True
        elif isinstance(value, type(None)):
            return True

        error_message = f"{attribute_name} must be int(higher than zero) or None."
        raise TypeError(error_message)
