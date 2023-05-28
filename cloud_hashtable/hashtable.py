import mmh3
from .storage import Storage


# Interface
class HashTable:
    def insert(self, key: bytes, value: bytes) -> bool:
        pass

    def delete(self, key: bytes) -> bool:
        pass

    def look_up(self, key: bytes) -> bytes | None:
        "Returns value or None."
        pass

    def clear(self) -> None:
        pass

    
class SpecialKey_1Hash_HashTable(HashTable):
    """
    Hash table with:
    - fixed size
    - single hash function
    - 1 element per bucket
    - special 'empty_key' to mark a bucket as empty.
    """

    def __init__(self, storage: Storage, empty_key: bytes, hash_fkt=None) -> None:
        self.storage: Storage = storage
        self.empty_key = empty_key
        self.key_len = len(self.empty_key)
        self.hash_fkt = hash_fkt or hash

    def __hash(self, key: bytes) -> int:
        return self.hash_fkt(key) % len(self.storage)

    def _split(self, value: bytes) -> tuple[bytes]:
        return value[:self.key_len], value[self.key_len:]

    def _join(self, key: bytes, value: bytes) -> bytes:
        return b''.join([key, value])

    def insert(self, key: bytes, value: bytes) -> bool:
        h = self.__hash(key)
        stored_key, _ = self._split(self.storage[h])
        if stored_key == self.empty_key or stored_key == key:
            self.storage[h] = self._join(key, value)
            return True
        else:
            return False

    def delete(self, key: bytes) -> bool:
        h = self.__hash(key)
        stored_key, stored_value = self._split(self.storage[h])
        if stored_key == key:
            self.storage[h] = self._join(self.empty_key, stored_value)
            return True
        else:
            return False

    def look_up(self, key: bytes) -> bytes | None:
        h = self.__hash(key)
        stored_key, stored_value = self._split(self.storage[h])
        if stored_key == key:
            return stored_value
        else:
            return None

    def clear(self) -> None:
        for i in range(len(self.storage)):
            _, stored_value = self._split(self.storage[i])
            self.storage[i] = self._join(self.empty_key, stored_value)


class SpecialKey_MultiHash_HashTable(HashTable):
    """
    Hash table with:
    - fixed size
    - single hash function
    - many element per bucket
    - special 'empty_key' to mark a bucket as empty.
    """

    def __init__(self, storage: Storage, empty_key: bytes, max_probing_depth: int = 100, probing_depth: int|None = None) -> None:
        self.storage: Storage = storage
        self.empty_key = empty_key
        self.key_len = len(self.empty_key)
        self.max_probing_depth = max_probing_depth
        self.probing_depth = probing_depth or 0

    def __hash(self, key: bytes, seed) -> int:
        return mmh3.hash128(key, seed, signed=False) % len(self.storage)

    def _split(self, value: bytes) -> tuple[bytes]:
        return value[:self.key_len], value[self.key_len:]

    def _join(self, key: bytes, value: bytes) -> bytes:
        return b''.join([key, value])

    def insert(self, key: bytes, value: bytes) -> bool:
        for depth in range(self.max_probing_depth):
            h = self.__hash(key, seed=depth)
            stored_key, _ = self._split(self.storage[h])
            if stored_key == self.empty_key or stored_key == key:
                self.storage[h] = self._join(key, value)
                self.probing_depth = max(self.probing_depth, depth + 1)
                return True
        return False

    def delete(self, key: bytes) -> bool:
        for depth in range(self.probing_depth):
            h = self.__hash(key, seed=depth)
            stored_key, stored_value = self._split(self.storage[h])
            if stored_key == key:
                self.storage[h] = self._join(self.empty_key, stored_value)
                return True
        return False

    def look_up(self, key: bytes) -> bytes | None:
        for depth in range(self.probing_depth):
            h = self.__hash(key, seed=depth)
            stored_key, stored_value = self._split(self.storage[h])
            if stored_key == key:
                return stored_value
        return None

    def clear(self) -> None:
        for i in range(len(self.storage)):
            _, stored_value = self._split(self.storage[i])
            self.storage[i] = self._join(self.empty_key, stored_value)