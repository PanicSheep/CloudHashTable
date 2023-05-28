import unittest
from cloud_hashtable import *


class SpecialKey_1Hash_HashTableTest(unittest.TestCase):
    @staticmethod
    def empty_hashtable():
        return SpecialKey_1Hash_HashTable(storage=[b'\x00\x00']*8, empty_key=b'\x00')

    def test_split(self):
        ht = SpecialKey_1Hash_HashTable(storage=[], empty_key=b'\x00\x00')
        key, value = ht._split(b'\x12\x34\x56')
        self.assertEqual(key, b'\x12\x34')
        self.assertEqual(value, b'\x56')

    def test_join(self):
        ht = self.empty_hashtable()
        self.assertEqual(ht._join(b'\x12\x03', b'\x45\x06'), b'\x12\x03\x45\x06')

    def test_insert(self):
        ht = self.empty_hashtable()
        self.assertTrue(ht.insert(key=b'\x01', value=b'\x02'))  # can insert new key
        self.assertTrue(ht.insert(key=b'\x01', value=b'\x03'))  # can insert on collision

    def test_delete(self):
        ht = self.empty_hashtable()
        ht.insert(key=b'\x01', value=b'\x02')
        self.assertTrue(ht.delete(key=b'\x01'))  # can delete stored key
        self.assertFalse(ht.delete(key=b'\x01'))  # cannot delete deleted key
        self.assertFalse(ht.delete(key=b'\x02'))  # cannot delete unknown key

    def test_look_up(self):
        ht = self.empty_hashtable()
        ht.insert(key=b'\x01', value=b'\x02')
        self.assertEqual(ht.look_up(key=b'\x01'), b'\x02')  # finds value to known key
        self.assertEqual(ht.look_up(key=b'\x02'), None)  # cannot find unknown key

    def test_clear(self):
        ht = self.empty_hashtable()
        ht.insert(key=b'\x01', value=b'\x02')
        ht.clear()
        self.assertEqual(ht.look_up(key=b'\x01'), None)  # cannot find unknown key


class SpecialKey_MultiHash_HashTableTest(unittest.TestCase):
    @staticmethod
    def empty_hashtable():
        return SpecialKey_MultiHash_HashTable(storage=[b'\x00\x00']*8, empty_key=b'\x00')

    def test_split(self):
        ht = SpecialKey_MultiHash_HashTable(storage=[], empty_key=b'\x00\x00')
        key, value = ht._split(b'\x12\x34\x56')
        self.assertEqual(key, b'\x12\x34')
        self.assertEqual(value, b'\x56')

    def test_join(self):
        ht = self.empty_hashtable()
        self.assertEqual(ht._join(b'\x12\x03', b'\x45\x06'), b'\x12\x03\x45\x06')

    def test_insert(self):
        ht = self.empty_hashtable()
        self.assertTrue(ht.insert(key=b'\x01', value=b'\x02'))  # can insert new key
        self.assertTrue(ht.insert(key=b'\x01', value=b'\x03'))  # can insert on collision

    def test_delete(self):
        ht = self.empty_hashtable()
        ht.insert(key=b'\x01', value=b'\x02')
        self.assertTrue(ht.delete(key=b'\x01'))  # can delete stored key
        self.assertFalse(ht.delete(key=b'\x01'))  # cannot delete deleted key
        self.assertFalse(ht.delete(key=b'\x02'))  # cannot delete unknown key

    def test_look_up(self):
        ht = self.empty_hashtable()
        ht.insert(key=b'\x01', value=b'\x02')
        self.assertEqual(ht.look_up(key=b'\x01'), b'\x02')  # finds value to known key
        self.assertEqual(ht.look_up(key=b'\x02'), None)  # cannot find unknown key

    def test_clear(self):
        ht = self.empty_hashtable()
        ht.insert(key=b'\x01', value=b'\x02')
        ht.clear()
        self.assertEqual(ht.look_up(key=b'\x01'), None)  # cannot find unknown key


if __name__ == '__main__':
    unittest.main(verbosity=2)
