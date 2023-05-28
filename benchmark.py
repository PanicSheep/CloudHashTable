import time
import random
from cloud_hashtable import Server, RemoteHashTable

try:
    key_length = 16
    value_length = 16
    port = 12345

    start = time.perf_counter()
    server = Server(port, b'\x00' * key_length, value_length, 32 * 1024 * 1024, ['temp_file'], 0)
    end = time.perf_counter()
    file_size = 1024 # MB
    speed = round(file_size / (end - start))
    print(f'File creation: {speed} MB/s')

    ht = RemoteHashTable(f'localhost:{port}')

    keys = [random.randint(1, pow(2, key_length * 8) - 1).to_bytes(key_length, byteorder='big') for _ in range(1_000)]
    values = [random.randint(1, pow(2, value_length * 8) - 1).to_bytes(value_length, byteorder='big') for _ in range(1_000)]

    start = time.perf_counter()
    for key, value in zip(keys, values):
        ht.insert(key, value)
    end = time.perf_counter()
    diff = (end - start) * 1_000
    print(f'RemoteHashTable.insert: {diff:.1f} us')

    server.stop(None)
finally:
    server.delete_storage()
