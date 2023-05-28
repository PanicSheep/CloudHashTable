import os
from pathlib import Path
from .storage import Storage


class FileStorage(Storage):
    def __init__(self, filename: Path | str, item_length: int) -> None:
        self.file = Path(filename).open('r+b')
        self.item_length = item_length

    def close(self) -> None:
        self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()
        return False

    def __len__(self) -> int:
        self.file.seek(0, os.SEEK_END)
        return self.file.tell() // self.item_length

    def __setitem__(self, index: int, item) -> None:
        self.file.seek(index * self.item_length)
        self.file.write(item)

    def __getitem__(self, index: int):
        self.file.seek(index * self.item_length)
        return self.file.read(self.item_length)


def create_file(filename: Path | str, item, count: int) -> FileStorage:
    with Path(filename).open('wb') as f:
        for _ in range(count):
            f.write(item)


class MultiFileStorage(Storage):
    def __init__(self, filenames: list[str], item_length: int) -> None:
        self.files = [FileStorage(f, item_length) for f in filenames]
        self.file_length = len(self.files[0])
        self.item_length = item_length

    def close(self) -> None:
        for f in self.files:
            f.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()
        return False

    def __len__(self) -> int:
        return self.file_length * len(self.files)

    def __setitem__(self, index: int, item) -> None:
        div, mod = divmod(index, self.file_length)
        self.files[div][mod] = item

    def __getitem__(self, index: int):
        div, mod = divmod(index, self.file_length)
        return self.files[div][mod]
