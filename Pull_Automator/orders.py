import os
import json
import re
from gsheets import Sheets
import tempfile

OAUTH_CREDENTIALS_JSON = os.environ['OAUTH_CREDENTIALS_JSON']
STORAGE_JSON = os.environ['STORAGE_JSON']
BLACKBOOK_URL = os.environ['BLACKBOOK_URL']

credentials_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
credentials_file.write(OAUTH_CREDENTIALS_JSON)
credentials_file.flush()

storage_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
storage_file.write(STORAGE_JSON)
storage_file.flush()

sheets = Sheets.from_files(credentials_file.name, storage_file.name)

class OrderSheet:
    def __init__(self):
        s = sheets.get(BLACKBOOK_URL)
        test = s.find('Order Form').to_frame()
        test.columns = test.iloc[0]
        test = test.iloc[1:].reset_index(drop=True)
        test = test['Out Going'].dropna().tolist()

        self.orders = []
        for row in test:
            splits = row.split(', ')
            for item in splits:
                item = item.replace(' ore', '')
                quant, item = self.set_quantity(item)
                for _ in range(quant):
                    self.orders.append(item)

    def set_quantity(self, item):
        m = re.match(r'^\s*(\d{1,2})\s*(.*)$', item)
        num = int(m.group(1)) if m else 1
        text = m.group(2) if m else item
        return num, text