import re


def to_snake_case(name: str) -> str:
    name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub(r"__([A-Z])", r"_\1", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()


class Tool:
    def __init__(self) -> None:
        print(f"Started parser {self.name}")

    @property
    def get_rules(self) -> list[str]:
        raise NotImplementedError

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def file_name(self) -> str:
        class_name = to_snake_case(self.name)

        return class_name
