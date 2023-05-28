from ruamel import yaml
from concurrent import futures
from pathlib import Path
from .file_storage import MultiFileStorage, create_file
from .hashtable import HashTable, SpecialKey_1Hash_HashTable, SpecialKey_MultiHash_HashTable
import grpc
from google.protobuf.wrappers_pb2 import BoolValue
from .hashtable_pb2 import Value
from .hashtable_pb2_grpc import HashTableServicer, add_HashTableServicer_to_server


class HashTableServicer(HashTableServicer):
    def __init__(self, ht: HashTable) -> None:
        super().__init__()
        self.ht = ht

    def Insert(self, request, context):
        ret = self.ht.insert(request.key, request.value)
        return BoolValue(value=ret)

    def Delete(self, request, context):
        ret = self.ht.delete(request.key)
        return BoolValue(value=ret)

    def LookUp(self, request, context):
        ret = self.ht.look_up(request.key)
        return Value(value=ret)
    

def create_rpc_server(port: int, hashtable: HashTable):
    rpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    add_HashTableServicer_to_server(HashTableServicer(hashtable), rpc_server)
    rpc_server.add_insecure_port(f'[::]:{port}')
    return rpc_server


class Server:
    def __init__(
        self,
        port: int,
        empty_key: bytes,
        value_length: int,
        file_size: int,
        files: list[str],
        config_file: str|None = None
    ) -> None:
        self.port = port
        self.empty_key = empty_key
        self.value_length = value_length
        self.file_size = file_size
        self.files = files
        self.config_file = config_file

        # create hashtable files
        key_length = len(empty_key)
        init_value = b'\x00' * value_length
        init_item = b''.join([empty_key, init_value])
        for file in files:
            if not Path(file).exists():
                create_file(file, init_item, file_size)

        self.storage = MultiFileStorage(files, key_length + value_length)
        self.hashtable = SpecialKey_MultiHash_HashTable(self.storage, empty_key)
        self.rpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        add_HashTableServicer_to_server(HashTableServicer(self.hashtable), self.rpc_server)
        self.rpc_server.add_insecure_port(f'[::]:{self.port}')
        self.rpc_server.start()

    @staticmethod
    def from_config(config_file: str):
        with open(config_file, 'r') as file:
            data = yaml.safe_load(file)
        port = data['port']
        empty_key = data['empty_key'].encode('utf-8')
        value_length = data['value_length']
        file_size = data['file_size']
        files = data['files']
        probing_depth = data['probing_depth']
        return Server(port, empty_key, value_length, file_size, files, probing_depth, config_file)

    def safe_config(self, config_file: str) -> None:
        self.config_file = config_file
        data = {
            'port': self.port,
            'empty_key': self.empty_key.decode("utf-8"),
            'value_length': self.value_length,
            'file_size': self.file_size,
            'files': self.files,
            'probing_depth': self.hashtable.probing_depth,
            }
        with open(config_file, 'w') as outfile:
            yaml.dump(data, outfile)

    def delete_storage(self) -> None:
        self.storage.close()
        for file in self.files:
            Path(file).unlink()

    def stop(self, grace: float | None):
        if self.config_file:
            self.safe_config(self.config_file)
        self.rpc_server.stop(grace)
        self.storage.close()
