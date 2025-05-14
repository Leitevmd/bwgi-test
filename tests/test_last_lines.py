import unittest
import tempfile
import os
from bwgi_test import last_lines

class TestLastLines(unittest.TestCase):
    def test_all_cases_with_subtests(self):
        test_cases = [
            (
                "regular_lines_with_newline",
                ["Line 1\n", "Line 2\n", "Line 3\n"],
                ["Line 3\n", "Line 2\n", "Line 1\n"],
                None
            ),
            (
                "no_final_newline",
                ["Line 1\n", "Line 2\n", "Last line"],
                ["Last line", "Line 2\n", "Line 1\n"],
                None
            ),
            (
                "empty_file",
                [],
                [],
                None
            ),
            (
                "single_line_with_newline",
                ["Only one line\n"],
                ["Only one line\n"],
                None
            ),
            (
                "single_line_without_newline",
                ["No newline"],
                ["No newline"],
                None
            ),
            (
                "whitespace_only_lines",
                ["   \n", "\t\t\n", "\n"],
                ["\n", "\t\t\n", "   \n"],
                None
            ),
            (
                "windows_crlf_newlines",
                ["Line 1\r\n", "Line 2\r\n", "Line 3\r\n"],
                ["Line 3\r\n", "Line 2\r\n", "Line 1\r\n"],
                None
            ),
            (
                "multibyte_utf8_characters",
                ["Línea 1\n", "😀 emoji\n", "你好 world\n"],
                ["你好 world\n", "😀 emoji\n", "Línea 1\n"],
                None
            ),
            (
                "utf8_split_boundary",
                ["😀😀😀😀😀\n", "Line after emojis\n"],
                ["Line after emojis\n", "😀😀😀😀😀\n"],
                5
            ),
            (
                "small_buffer_regular_text",
                ["ABC\n", "DEF\n", "GHI\n", "JKL\n"],
                ["JKL\n", "GHI\n", "DEF\n", "ABC\n"],
                7
            ),
        ]

        for name, input_lines, expected_output, buffer_size in test_cases:
            with self.subTest(name=name):
                with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as tmp:
                    tmp.writelines(input_lines)
                    temp_path = tmp.name

                try:
                    if buffer_size is None:
                        result = list(last_lines(temp_path))
                    else:
                        result = list(last_lines(temp_path, buffer_size=buffer_size))
                    self.assertEqual(result, expected_output)
                finally:
                    os.remove(temp_path)

    def test_iterator_behavior(self):
        input_lines = ["One\n", "Two\n", "Three\n"]
        expected_sequence = ["Three\n", "Two\n", "One\n"]

        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as tmp:
            tmp.writelines(input_lines)
            temp_path = tmp.name

        try:
            iterator = last_lines(temp_path)
            for i, expected_line in enumerate(expected_sequence):
                with self.subTest(step=i):
                    self.assertEqual(next(iterator), expected_line)

            with self.subTest("stop_iteration"):
                with self.assertRaises(StopIteration):
                    next(iterator)

        finally:
            os.remove(temp_path)

if __name__ == '__main__':
    unittest.main()