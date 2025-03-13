from lamops.core.model import LamOpsModel


def test_LamOpsModel():
    class TestModel(LamOpsModel):
        a: int
        b: str
        c: float

    model = TestModel(a=1, b="test", c=1.0)
    assert model["a"] == model.a == 1
    assert model["b"] == model.b == "test"
    assert model["c"] == model.c == 1.0

    assert model.to_dict() == {"a": 1, "b": "test", "c": 1.0}
    assert TestModel.from_dict(model) == model

    model["a"] = 2
    assert model["a"] == model.a == 2

    assert set(model.keys()) == {"a", "b", "c"}
    assert set(model.values()) == {2, "test", 1.0}
    assert set(model.items()) == {("a", 2), ("b", "test"), ("c", 1.0)}
