class Tool:
    @property
    def get_rules(self) -> list[str]:
        raise NotImplementedError
