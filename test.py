import unittest

from main import Job


class TestExpandVariables(unittest.TestCase):
    def setUp(self):
        self.job = Job([{"name": "one", "value": "firstValue"}, {"name": "two", "value": "secondValue"}], [])

    def test_template_syntax(self):
        expanded_script = self.job.expand_variables("echo ${{ variables.one }}")
        self.assertEqual(expanded_script, "echo firstValue")        

    def test_macro_syntax(self):
        expanded_script = self.job.expand_variables("echo $(one)")
        self.assertEqual(expanded_script, "echo firstValue")        

    def test_both(self):
        expanded_script = self.job.expand_variables("echo $(one) ${{ variables.two }}")
        self.assertEqual(expanded_script, "echo firstValue secondValue")
        

if __name__ == "__main__":
    unittest.main()