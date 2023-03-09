import os
import tempfile
import unittest
from mypy_pragma import add_mypy, remove_mypy


class TestMypyPragma(unittest.TestCase):

    def setUp(self):
        # Create temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder_path = self.temp_dir.name
        # Create test files
        self.file1 = os.path.join(self.folder_path, "file1.py")
        with open(self.file1, "w") as f:
            f.write("#!/usr/bin/env python\n# My Model\ndata = 'something\ncheck = 'done''")
        self.file2 = os.path.join(self.folder_path, "file2.py")
        with open(self.file2, "w") as f:
            f.write("")

    def tearDown(self):
        # Remove temporary directory and test files
        self.temp_dir.cleanup()

    def test_add_mypy(self):
        # Call add_mypy with test files
        add_mypy([self.file1, self.file2])
        # Check that mypy pragma was added to files
        with open(self.file1) as f:
            contents = f.read()
            self.assertIn("# mypy: enable-option", contents)
        with open(self.file2) as f:
            contents = f.read()
            self.assertNotIn("# mypy: enable-option", contents)

    def test_remove_mypy(self):
        # Add mypy pragma to test files
        with open(self.file1, "a") as f:
            f.write("#!/usr/bin/env python\n# My Model\n# mypy: enable-option\n")
        with open(self.file2, "a") as f:
            f.write("# mypy: enable-option\n")
        # Call remove_mypy with test files
        remove_mypy([self.file1, self.file2])
        # Check that mypy pragma was removed from files
        with open(self.file1) as f:
            contents = f.read()
            self.assertNotIn("# mypy: enable-option", contents)
        with open(self.file2) as f:
            contents = f.read()
            self.assertNotIn("# mypy: enable-option", contents)


if __name__ == '__main__':
    unittest.main()