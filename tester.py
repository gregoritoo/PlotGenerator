import subprocess

import regex as re


class OutPutException(Exception):
    def __init__(self, message="Could not parse the provided code"):
        self.message = message
        super().__init__(self.message)


class TestModule:
    def __init__(self):
        self.cleaning_pattern = r"START CODE(.*)"
        self.filename = "temp_code_file.py"

    def _clean_code(self):
        match = re.search(self.cleaning_pattern, self.code, re.DOTALL)
        if len(match) >= 1:
            return match.group(1).replace("`", "").replace("python", "").replace("plt.show()", "")
        else:
            raise OutPutException

    def _create_temp_file(self):
        self.code = self._clean_code()
        with open(self.filename, "w") as f:
            f.write(self.code)

    def exec_code(self, code):
        self.code = code
        self._create_temp_file()
        out = subprocess.run(["python3", self.filename], capture_output=True)
        output_dic = {
            "return_code": out.__getattribute__("returncode"),
            "stderr": out.__getattribute__("stderr"),
        }
        return output_dic
