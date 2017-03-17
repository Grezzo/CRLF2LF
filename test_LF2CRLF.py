import unittest
import os
import shutil
import stat

from LF2CRLF import LF2CRLF

class LF2CRLF_Tests(unittest.TestCase):

    def test_ansi_windows_line_ending(self):
        lf2crlf = LF2CRLF(os.path.join('Test Files', 'ANSI Windows.txt'))
        self.assertEqual(lf2crlf.win_line_end, b'\r\n')
        self.assertEqual(lf2crlf.unix_line_end, b'\n')
        self.assertFalse(lf2crlf.unix_endings)
        content = lf2crlf.content
        lf2crlf.convert()
        self.assertEqual(content, lf2crlf.content)
        
    def test_unix_read_only(self):
        lf2crlf = LF2CRLF(os.path.join('Test Files', 'Unix Read Only.txt'))
        self.assertEqual(lf2crlf.win_line_end, b'\r\0\n\0')
        self.assertEqual(lf2crlf.unix_line_end, b'\n\0')
        self.assertTrue(lf2crlf.unix_endings)
        content = lf2crlf.content
        lf2crlf.convert()
        self.assertNotEqual(content, lf2crlf.content)
        
    def test_utf8_single_line(self):
        lf2crlf = LF2CRLF(os.path.join('Test Files', 'UTF-8 Single Line.txt'))
        self.assertEqual(lf2crlf.win_line_end, b'\r\n')
        self.assertEqual(lf2crlf.unix_line_end, b'\n')
        self.assertFalse(lf2crlf.unix_endings)
        content = lf2crlf.content
        lf2crlf.convert()
        self.assertEqual(content, lf2crlf.content)
        
    def test_utf8_unix(self):
        lf2crlf = LF2CRLF(os.path.join('Test Files', 'UTF-8 Unix.txt'))
        self.assertEqual(lf2crlf.win_line_end, b'\r\n')
        self.assertEqual(lf2crlf.unix_line_end, b'\n')
        self.assertTrue(lf2crlf.unix_endings)
        content = lf2crlf.content
        lf2crlf.convert()
        self.assertNotEqual(content, lf2crlf.content)
        
    def test_utf8_windows(self):
        lf2crlf = LF2CRLF(os.path.join('Test Files', 'UTF-8 Windows.txt'))
        self.assertEqual(lf2crlf.win_line_end, b'\r\n')
        self.assertEqual(lf2crlf.unix_line_end, b'\n')
        self.assertFalse(lf2crlf.unix_endings)
        content = lf2crlf.content
        lf2crlf.convert()
        self.assertEqual(content, lf2crlf.content)
        
    def test_utf16_be_unix(self):
        lf2crlf = LF2CRLF(os.path.join('Test Files', 'UTF-16 BE Unix.txt'))
        self.assertEqual(lf2crlf.win_line_end, b'\0\r\0\n')
        self.assertEqual(lf2crlf.unix_line_end, b'\0\n')
        self.assertTrue(lf2crlf.unix_endings)
        content = lf2crlf.content
        lf2crlf.convert()
        self.assertNotEqual(content, lf2crlf.content)
        
    def test_utf16_be_windows(self):
        lf2crlf = LF2CRLF(os.path.join('Test Files', 'UTF-16 BE Windows.txt'))
        self.assertEqual(lf2crlf.win_line_end, b'\0\r\0\n')
        self.assertEqual(lf2crlf.unix_line_end, b'\0\n')
        self.assertFalse(lf2crlf.unix_endings)
        content = lf2crlf.content
        lf2crlf.convert()
        self.assertEqual(content, lf2crlf.content)
        
    def test_utf16_le_unix(self):
        lf2crlf = LF2CRLF(os.path.join('Test Files', 'UTF-16 LE Unix.txt'))
        self.assertEqual(lf2crlf.win_line_end, b'\r\0\n\0')
        self.assertEqual(lf2crlf.unix_line_end, b'\n\0')
        self.assertTrue(lf2crlf.unix_endings)
        content = lf2crlf.content
        lf2crlf.convert()
        self.assertNotEqual(content, lf2crlf.content)
        
    def test_utf16_le_windows(self):
        lf2crlf = LF2CRLF(os.path.join('Test Files', 'UTF-16 LE Windows.txt'))
        self.assertEqual(lf2crlf.win_line_end, b'\r\0\n\0')
        self.assertEqual(lf2crlf.unix_line_end, b'\n\0')
        self.assertFalse(lf2crlf.unix_endings)
        content = lf2crlf.content
        lf2crlf.convert()
        self.assertEqual(content, lf2crlf.content)
        
    def test_save(self):
        shutil.copy2(
            os.path.join('Test Files', 'UTF-8 Unix.txt'),
            os.path.join('Test Files', 'save test.txt')
        )
        with open(os.path.join('Test Files', 'save test.txt'), 'rb') as file:
            content = file.read()
        lf2crlf = LF2CRLF(os.path.join('Test Files', 'save test.txt'))
        lf2crlf.convert()
        lf2crlf.save()
        with open(os.path.join('Test Files', 'save test.txt'), 'rb') as file:
            new_content = file.read()
        os.remove(os.path.join('Test Files', 'save test.txt'))
        self.assertNotEqual(content, new_content)
        
    def test_save_fail(self):
        shutil.copy2(
            os.path.join('Test Files', 'Unix Read Only.txt'),
            os.path.join('Test Files', 'save test.txt')
        )
        with open(os.path.join('Test Files', 'save test.txt'), 'rb') as file:
            content = file.read()
        lf2crlf = LF2CRLF(os.path.join('Test Files', 'save test.txt'))
        lf2crlf.convert()
        with self.assertRaises(PermissionError):
            lf2crlf.save()
        os.chmod(os.path.join('Test Files', 'save test.txt'), stat.S_IWRITE )
        os.remove(os.path.join('Test Files', 'save test.txt'))


        
if __name__ == '__main__':
    unittest.main()
