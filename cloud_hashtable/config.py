from ruamel import yaml

data = {
    'empty_key': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'.decode("utf-8"),
    'item_length': 25,
    'files': [r'G:\hashtable\a', r'G:\hashtable\b', r'G:\hashtable\c']
}
print(yaml.dump(data))

with open(r'G:\hashtable\first.yaml', 'r') as file:
    print(yaml.safe_load(file))

    
def create_config(
    config_file: str,
    port: int,
    empty_key: bytes,
    item_length: int,
    file_size: int,
    files: list[str]
):
    data = {
        'port': port,
        'empty_key': empty_key.decode("utf-8"),
        'item_length': item_length,
        'file_size': file_size,
        'files': files,
        }
    with open(config_file, 'w') as outfile:
        yaml.dump(data, outfile)

    return config_file

create_config(
    r'G:\hashtable\first.yaml',
    12350,
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    25,
    1_000_000,
    [r'G:\hashtable\a', r'G:\hashtable\b', r'G:\hashtable\c']
    )