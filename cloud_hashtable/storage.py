# Interface
class Storage:
    def __len__(self) -> int:
        pass

    def __setitem__(self, index: int, value: bytes) -> None:
        pass

    def __getitem__(self, index: int) -> bytes:
        pass
