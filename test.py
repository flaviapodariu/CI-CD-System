import unittest
import os
from main import Job, readYamlFile


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
        
class TestRunJob(unittest.TestCase): 
    def setUp(self) -> None:
        self.fileName = "test.yaml"
        self.file = readYamlFile(self.fileName)
        self.job = Job(self.file["variables"], self.file["steps"])

    def test_write_to_file(self): 
        self.job.run_job()
        self.output_file = "test/output"
        
        self.assertEqual(self.check_output(self.output_file), "This is a test\n")

    def check_output(self, file): 
        try: 
            f = open(file, 'r')
        except Exception as err: 
            print(f"Unexpected {err=}, {type(err)=}")
            raise
            
        res = f.readline()
        f.close()
        return res

    def tearDown(self) -> None:
        os.system(f"rm -rf test")

if __name__ == "__main__":
    unittest.main()