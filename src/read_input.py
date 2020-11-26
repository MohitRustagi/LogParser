import abc
import csv

from collections import namedtuple

class BaseInput(abc.ABC):
    """Base class for input to make code scalable"""
    @abc.abstractmethod
    def read(self):
        pass


class CSVSmallInput(BaseInput):
    """Must be used for small input size.
    
       Reads csv and return rows.
    """
    def clean_url(self, url):
        """Replace integers in uri with '{id}'."""
        parsed_content = url.split('/')

        if not parsed_content:
            return ""
        if parsed_content[-1].isdigit():
            parsed_content[-1] = '{id}'
        else:
            for i, each_content in enumerate(parsed_content):
                if each_content.isdigit():
                    parsed_content[i] = '{id}'
        parsed_content = "/".join(parsed_content)
        return parsed_content

    def read(self, path):
        try:
            file = open(path, 'r')
        except FileNotFoundError:
            raise RuntimeError(f"Invalid file path {path}.")
        else:
            columns = []
            all_content = []
            file_content = csv.reader(file)
            for i, each_row in enumerate(file_content):
                if i == 0:
                    continue
                if not each_row:
                    continue
                each_row[1] = self.clean_url(each_row[1])
                if not all(each_row):
                    raise RuntimeError(f"Invalid content {each_row}")
                all_content.append(each_row)    
            file.close()
            return all_content
            

