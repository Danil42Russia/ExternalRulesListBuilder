class Tool:
    @property
    def get_rules(self) -> list[str]:
        raise NotImplementedError

    @property
    def name(self) -> str:
        class_name = self.__class__.__name__
        class_name = "".join([f"_{c.lower()}" if c.isupper() else c for c in class_name]).lstrip("_")

        return class_name
