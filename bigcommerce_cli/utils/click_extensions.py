import json

from click.types import ParamType


class DictParamType(ParamType):
    """
    The DictParamType accepts a string 'value' in JSON format like '{"key": "value", ...}' and
    converts it to a python dict.
    """
    name = 'dict'

    def convert(self, value, params, ctx):
        if value is None:
            return None
        elif isinstance(value, str):
            try:
                return json.loads(value)
            except TypeError:
                self.fail('Could not convert value to dict')
        elif isinstance(value, dict):
            return value
        else:
            self.fail(f'Invalid type {type(value)} for value, expected string or dict')
