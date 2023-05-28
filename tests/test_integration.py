import unittest
from pathlib import Path
from cloud_hashtable import *


class Integration_Test(unittest.TestCase):

    def hashtable_test(self, ht: HashTable, clear: bool = True):
        # insert
        self.assertTrue(ht.insert(key=b'01', value=b'002'))  # can insert new key
        self.assertTrue(ht.insert(key=b'01', value=b'003'))  # can insert on collision
                
        # look_up
        self.assertEqual(ht.look_up(key=b'01'), b'003')  # finds value to known key
        self.assertEqual(ht.look_up(key=b'02'), None)  # cannot find unknown key
                
        # delete
        self.assertTrue(ht.delete(key=b'01'))  # can delete stored key
        self.assertFalse(ht.delete(key=b'01'))  # cannot delete deleted key
        self.assertFalse(ht.delete(key=b'02'))  # cannot delete unknown key
                
        if clear:
            # clear
            ht.insert(key=b'01', value=b'002')
            ht.clear()
            self.assertEqual(ht.look_up(key=b'01'), None)  # cannot find unknown key

    def test_FileStorage_HashTable(self):
        try:
            temp_file = Path('temp_file')
            create_file(temp_file, b'00000', count=8)

            storage = FileStorage(temp_file, item_length=5)
            ht = SpecialKey_1Hash_HashTable(storage, empty_key=b'00')
            self.hashtable_test(ht)
        finally:
            storage.close()
            temp_file.unlink()

    def test_MultiFileStorage_HashTable(self):
        try:
            temp_file1 = Path('temp_file1')
            temp_file2 = Path('temp_file2')
            create_file(temp_file1, b'00000', count=8)
            create_file(temp_file2, b'00000', count=8)

            storage = MultiFileStorage([temp_file1, temp_file2], item_length=5)
            ht = SpecialKey_1Hash_HashTable(storage, empty_key=b'00')
            self.hashtable_test(ht)
        finally:
            storage.close()
            temp_file1.unlink()
            temp_file2.unlink()

    def test_server_client(self):
        try:
            server_ht = SpecialKey_1Hash_HashTable(storage=[b'00000']*8, empty_key=b'00')
            server = create_rpc_server('1234', server_ht)
            server.start()

            ht = RemoteHashTable('localhost:1234')
            self.hashtable_test(ht, clear=False)
        finally:
            ht.close()
            server.stop(grace=None)


if __name__ == '__main__':
    unittest.main(verbosity=2)
