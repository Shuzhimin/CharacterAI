# 2024/4/25
# zhangzhong

import functools
import inspect
from types import UnionType
from typing import Callable, Union, get_args, get_origin, get_type_hints

from app.common.model import Function, FunctionTool, Parameters, Property


def is_optional(tp) -> bool:
    origin = get_origin(tp)
    args = get_args(tp)
    return origin in [Union, UnionType] and type(None) in args


def type_to_str(tp):
    if tp is int or tp is float:
        return "number"
    elif tp is bool:
        return "boolean"
    elif tp is str:
        return "string"
    elif tp is list or tp is tuple:
        return "array"
    elif tp is dict:
        return "object"
    elif tp is None:
        return "null"
    else:
        assert False, f"unsupport type: {tp}"


class Tool:
    tools: list[dict] = []
    functions: dict[str, Callable] = {}

    def __init__(self):
        pass

    def __call__(self, func: Callable) -> Callable:
        assert func.__doc__ is not None, "tool's doc must given"
        signature = inspect.signature(func)
        type_hints = get_type_hints(func)
        properties = {}
        required: list[str] = []
        for name, param in signature.parameters.items():
            # all the parameters must have type hint
            assert name in type_hints, f"parameter {name} must have type hint"
            properties[name] = Property(
                # 我们还要实现一个从type 到字符串的转换
                type=type_to_str(type_hints[name]),
                description=param.annotation.__metadata__[0],
            )
            if not is_optional(type_hints[name]):
                required.append(name)

        function_tool = FunctionTool(
            function=Function(
                name=func.__name__,
                description=func.__doc__,
                parameters=Parameters(properties=properties, required=required),
            )
        )
        # how to get the arguments of a function
        self.tools.append(function_tool.model_dump())
        self.functions[func.__name__] = func

        @functools.wraps(func)
        def tool(*args, **kwargs):
            return func(*args, **kwargs)

        return tool

    @classmethod
    def dispatch(cls, name: str, *args, **kwargs):
        # 这里需要dispatch的话，我就需要找到对应的函数才行，那么这些函数就必须在注册时候放起来
        # 只有这样我们才能进行一个访问
        return cls.functions[name](*args, **kwargs)
