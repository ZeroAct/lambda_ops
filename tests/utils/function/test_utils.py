import inspect
from typing import Literal, Union

from lamops.utils.function import get_function_spec


def test_get_function_spec_basic():
    def foo(a: int, b: str = "default") -> str:
        """Function description.

        Args:
            a: Description of a.
            b: Description of b.

        Returns:
            Description of return.
        """
        return b

    info = get_function_spec(foo)
    assert info.description == "Function description."

    assert "a" in info.argument_spec
    arg_a = info.argument_spec["a"]
    assert arg_a.type == int
    assert arg_a.required is True
    assert arg_a.description == "Description of a."

    assert "b" in info.argument_spec
    arg_b = info.argument_spec["b"]
    assert arg_b.type == str
    assert arg_b.required is False
    assert arg_b.default == "default"
    assert arg_b.description == "Description of b."

    ret_spec = info.return_spec
    assert ret_spec.type == str
    assert ret_spec.description == "Description of return."


def test_get_function_spec_no_docstring():
    def foo(a, b):
        return a + b

    info = get_function_spec(foo)
    assert info.description in ("", None)
    for param in info.argument_spec.values():
        assert param.type == inspect.Parameter.empty
    assert info.return_spec.type == type(None)


def test_get_function_spec_union_and_literal():
    def bar(x: Union[int, str]) -> Union[str, int]:
        """Bar function.

        Args:
            x: Input value.
        Returns:
            Result value.
        """
        return x

    info_bar = get_function_spec(bar)
    x_spec = info_bar.argument_spec["x"]
    assert hasattr(x_spec.type, "__origin__")
    assert x_spec.type.__origin__ is Union
    assert set(x_spec.type.__args__) == {int, str}

    ret_type = info_bar.return_spec.type
    assert hasattr(ret_type, "__origin__")
    assert ret_type.__origin__ is Union
    assert set(ret_type.__args__) == {str, int}

    def baz(y: Literal["a", "b"]) -> Literal[True, False]:
        """Baz function.

        Args:
            y: Only allowed values 'a' or 'b'.
        Returns:
            Boolean result.
        """
        return y == "a"

    info_baz = get_function_spec(baz)
    y_spec = info_baz.argument_spec["y"]
    assert hasattr(y_spec.type, "__origin__")
    assert y_spec.type.__origin__ is Literal
    assert set(y_spec.type.__args__) == {"a", "b"}

    ret_baz_type = info_baz.return_spec.type
    assert hasattr(ret_baz_type, "__origin__")
    assert ret_baz_type.__origin__ is Literal
    assert set(ret_baz_type.__args__) == {True, False}


def test_get_function_spec_var_args():
    def qux(a: int, *args: float, **kwargs: str) -> None:
        """Qux function.

        Args:
            a: An integer.
            args: Additional float arguments.
            kwargs: Additional string keyword arguments.
        """
        pass

    info = get_function_spec(qux)
    assert "a" in info.argument_spec
    assert "args" in info.argument_spec
    assert "kwargs" in info.argument_spec

    assert info.argument_spec["a"].type == int
    assert info.argument_spec["args"].type == float
    assert info.argument_spec["kwargs"].type == str

    assert info.return_spec.type == type(None)


def test_get_function_spec_kw_only():
    def kw_only(*, flag: bool = True) -> bool:
        """Keyword-only function.

        Args:
            flag: A boolean flag.
        Returns:
            The flag value.
        """
        return flag

    info = get_function_spec(kw_only)
    assert "flag" in info.argument_spec
    flag_spec = info.argument_spec["flag"]
    assert flag_spec.type == bool
    assert flag_spec.required is False
    assert flag_spec.default is True
    assert info.return_spec.type == bool


def test_get_function_spec_no_params():
    def nop() -> None:
        """No parameter function.

        Returns:
            None.
        """
        pass

    info = get_function_spec(nop)
    assert info.argument_spec == {}
    assert info.return_spec.type == type(None)
