import grpc
from .hashtable_pb2 import KeyValue, Key, Value
from .hashtable_pb2_grpc import HashTableStub
from .hashtable import HashTable


class RemoteHashTable(HashTable):
    def __init__(self, target: str) -> None:
        self.channel = grpc.insecure_channel(target)
        self.stub = HashTableStub(self.channel)

    def close(self) -> None:
        self.channel.close

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()
        return False

    def insert(self, key: bytes, value: bytes) -> bool:
        ret = self.stub.Insert(KeyValue(key=key, value=value))
        return ret.value

    def delete(self, key: bytes) -> bool:
        ret = self.stub.Delete(Key(key=key))
        return ret.value

    def look_up(self, key: bytes) -> bytes | None:
        "Returns value or None."
        ret = self.stub.LookUp(Key(key=key))
        if ret.HasField('value'):
            return ret.value
        else:
            return None

    def clear(self) -> None:
        pass
