import inspect
from typing import Any

import docstring_parser

from lamops.core.model import UNDEFINED, LamOpsModel


class ArgumentSpec(LamOpsModel):
    type: Any = UNDEFINED
    default: Any = UNDEFINED
    required: bool = True
    description: str = None


class ReturnSpec(LamOpsModel):
    type: Any = UNDEFINED
    description: str = None


class FunctionSpec(LamOpsModel):
    description: str = None
    argument_spec: dict[str, ArgumentSpec] = {}
    return_spec: ReturnSpec = None


def get_function_spec(func) -> FunctionSpec:
    """Get function specification.

    Args:
        func: Function to get specification.

    Returns:
        FunctionSpec: Function specification

    Example:
        ```python
        def foo(a: int, b: str = "default") -> str:
            \"""Function description.

            Args:
                a: Description of a.
                b: Description of b.

            Returns:
                Description of return.
            \"""
            return b

        info = get_function_spec(foo)
        ```
    """
    function_spec = FunctionSpec()

    sig = inspect.signature(func)
    docstring = func.__doc__ or ""
    doc_parse = docstring_parser.parse(docstring)
    doc_desc = doc_parse.short_description
    doc_dict = {p.arg_name: p.description for p in doc_parse.params}
    doc_return_desc = doc_parse.returns and doc_parse.returns.description or ""

    function_spec.description = doc_desc

    for name, param in sig.parameters.items():
        argument_spec = ArgumentSpec(
            type=param.annotation,
            required=param.default is inspect.Parameter.empty,
            description=doc_dict.get(name, ""),
        )
        if param.default is not inspect.Parameter.empty:
            argument_spec.default = param.default

        function_spec.argument_spec[name] = argument_spec

    return_annotation = (
        sig.return_annotation if sig.return_annotation is not inspect.Signature.empty else None
    )
    if return_annotation is None:
        return_annotation = type(None)
    function_spec.return_spec = ReturnSpec(type=return_annotation, description=doc_return_desc)

    return function_spec
