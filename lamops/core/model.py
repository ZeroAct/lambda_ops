from pydantic import BaseModel, ConfigDict


class UNDEFINED:
    """Means that the value is not defined."""


class LamOpsModel(BaseModel):
    model_config: ConfigDict = ConfigDict(
        from_attributes=True,
    )

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def to_dict(self, json=False, **kwargs):
        return self.model_dump(mode="json" if json else "python", **kwargs)

    @classmethod
    def from_dict(cls, obj: dict, **kwargs):
        return cls.model_validate(obj, **kwargs)

    def keys(self):
        return self.model_fields_set

    def values(self):
        fields = self.model_fields
        return {getattr(self, f) for f in fields}

    def items(self):
        fields = self.model_fields
        return {(f, getattr(self, f)) for f in fields}
