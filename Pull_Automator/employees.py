import os
import json
import tempfile
from gsheets import Sheets

OAUTH_CREDENTIALS_JSON = os.environ['OAUTH_CREDENTIALS_JSON']
STORAGE_JSON = os.environ['STORAGE_JSON']
BLACKBOOK_URL = os.environ['BLACKBOOK_URL']

credentials_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
credentials_file.write(OAUTH_CREDENTIALS_JSON)
credentials_file.flush()

storage_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
storage_file.write(STORAGE_JSON)
storage_file.flush()

class GathingSkills:
    def __init__(self):
        self.employees={}
        sheets = Sheets.from_files(credentials_file.name, storage_file.name)

        s = sheets.get(BLACKBOOK_URL)

        test=s.find('Gathing skills').to_frame()
        test.rename(columns={'Unnamed: 0':'Employee','Black Market':'Black_Market'},inplace=True)
        test=test[test['Employee'].notna()]
        test=test[test['Employee']!='Ships'].fillna(0)
        self.df=(test.iloc[:,:5])
        for row in self.df.itertuples():
            self.employees[row.Employee]=[]
            for name,value in zip(row._fields,row[1:]):
                self.employees[row.Employee].append(value)

    def __iter__(self):
        return iter(self.employees.values())                

    def __getattr__(self,name):
        return getattr(self.employees,name)
    
    def __repr__(self):
        return repr(self.employees)
