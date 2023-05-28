import unittest
from pathlib import Path
from cloud_hashtable import FileStorage, MultiFileStorage, create_file


class FileStorageTest(unittest.TestCase):

    def test_len(self):
        try:
            temp_file = Path('temp_file')
            with temp_file.open('wb') as f:
                f.write(b'123456')

            storage = FileStorage(temp_file, item_length=2)
            self.assertEqual(len(storage), 3)
        finally:
            storage.close()
            temp_file.unlink()

    def test_get(self):
        try:
            temp_file = Path('temp_file')
            with temp_file.open('wb') as f:
                f.write(b'1234')

            storage = FileStorage(temp_file, item_length=2)
            self.assertEqual(storage[0], b'12')
            self.assertEqual(storage[1], b'34')
        finally:
            storage.close()
            temp_file.unlink()

    def test_set(self):
        try:
            temp_file = Path('temp_file')
            with temp_file.open('wb') as f:
                f.write(b'0000')

            storage = FileStorage(temp_file, item_length=2)
            storage[0] = b'12'
            storage[1] = b'34'

            self.assertEqual(storage[0], b'12')
            self.assertEqual(storage[1], b'34')
        finally:
            storage.close()
            temp_file.unlink()

    def test_create_file(self):
        try:
            temp_file = Path('temp_file')

            create_file(temp_file, b'12', count=2)

            storage = FileStorage(temp_file, item_length=2)
            self.assertEqual(len(storage), 2)
            self.assertEqual(storage[0], b'12')
            self.assertEqual(storage[1], b'12')
        finally:
            storage.close()
            temp_file.unlink()


class MultiFileStorageTest(unittest.TestCase):

    def test_len(self):
        try:
            temp_file1 = Path('temp_file1')
            temp_file2 = Path('temp_file2')
            with temp_file1.open('wb') as f:
                f.write(b'123456')
            with temp_file2.open('wb') as f:
                f.write(b'789012')

            with MultiFileStorage([temp_file1, temp_file2], item_length=2) as storage:
                self.assertEqual(len(storage), 6)
        finally:
            temp_file1.unlink()
            temp_file2.unlink()

    def test_get(self):
        try:
            temp_file1 = Path('temp_file1')
            temp_file2 = Path('temp_file2')
            with temp_file1.open('wb') as f:
                f.write(b'1234')
            with temp_file2.open('wb') as f:
                f.write(b'5678')

            with MultiFileStorage([temp_file1, temp_file2], item_length=2) as storage:
                self.assertEqual(storage[0], b'12')
                self.assertEqual(storage[1], b'34')
                self.assertEqual(storage[2], b'56')
                self.assertEqual(storage[3], b'78')
        finally:
            temp_file1.unlink()
            temp_file2.unlink()

    def test_set(self):
        try:
            temp_file1 = Path('temp_file1')
            temp_file2 = Path('temp_file2')
            with temp_file1.open('wb') as f:
                f.write(b'0000')
            with temp_file2.open('wb') as f:
                f.write(b'0000')

            with MultiFileStorage([temp_file1, temp_file2], item_length=2) as storage:
                storage[0] = b'12'
                storage[1] = b'34'
                storage[2] = b'56'
                storage[3] = b'78'

                self.assertEqual(storage[0], b'12')
                self.assertEqual(storage[1], b'34')
                self.assertEqual(storage[2], b'56')
                self.assertEqual(storage[3], b'78')
        finally:
            temp_file1.unlink()
            temp_file2.unlink()

    def test_create_file(self):
        try:
            temp_file1 = Path('temp_file1')
            temp_file2 = Path('temp_file2')
            create_file(temp_file1, b'12', count=2)
            create_file(temp_file2, b'34', count=2)

            with MultiFileStorage([temp_file1, temp_file2], item_length=2) as storage:
                self.assertEqual(len(storage), 4)
                self.assertEqual(storage[0], b'12')
                self.assertEqual(storage[1], b'12')
                self.assertEqual(storage[2], b'34')
                self.assertEqual(storage[3], b'34')
        finally:
            temp_file1.unlink()
            temp_file2.unlink()


if __name__ == '__main__':
    unittest.main(verbosity=2)
