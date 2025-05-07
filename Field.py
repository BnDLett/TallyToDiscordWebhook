from enum import Enum
from typing import Any


class Field:
    key: str
    label: str
    value: Any

    def __init__(self, key: str, label: str, value: Any):
        self.key = key
        self.label = label
        self.value = value


class Checkbox:
    field: Field

    def __init__(self, key: str, label: str, value: bool):
        self.field = Field(key, label, value)


class Option:
    id: str
    text: str


class InputText(Field):
    value: str


class TextArea(Field):
    value: str


class LinearScale(Field):
    value: int


class Checkboxes(Field):
    value: list[Checkbox]

    def __init__(self, key: str, label: str, value: list[Checkbox]):
        super().__init__(key, label, value)


class MultipleChoice(Field):
    value: Option


FieldTypes = {
    'INPUT_TEXT': InputText,
    'TEXTAREA': TextArea,
    'LINEAR_SCALE': LinearScale,
    'CHECKBOXES': Checkboxes,
    'MULTIPLE_CHOICE': MultipleChoice,
}
