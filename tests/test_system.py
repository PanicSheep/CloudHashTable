import unittest
from pathlib import Path
from cloud_hashtable import *


class System_Test(unittest.TestCase):
    
    def test_MultiFileStorage_RemoteHashTable(self):
        try:
            server = Server(1234, b'\x00', value_length=3, file_size=8, files=['temp_file1', 'temp_file2'])

            # client
            ht = RemoteHashTable('localhost:1234')
            
            # insert
            self.assertTrue(ht.insert(key=b'\x01', value=b'\x00\x00\x02'))  # can insert new key
            self.assertTrue(ht.insert(key=b'\x01', value=b'\x00\x00\x03'))  # can insert on collision
                
            # look_up
            self.assertEqual(ht.look_up(key=b'\x01'), b'\x00\x00\x03')  # finds value to known key
            self.assertEqual(ht.look_up(key=b'\x02'), None)  # cannot find unknown key
                
            # delete
            self.assertTrue(ht.delete(key=b'\x01'))  # can delete stored key
            self.assertFalse(ht.delete(key=b'\x01'))  # cannot delete deleted key
            self.assertFalse(ht.delete(key=b'\x02'))  # cannot delete unknown key

            ht.close()
            server.stop(grace=None)
        finally:
            server.delete_storage()


if __name__ == '__main__':
    unittest.main(verbosity=2)
