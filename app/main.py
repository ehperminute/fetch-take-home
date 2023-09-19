from hashlib import md5
from sqs import extract_entries, poll
from config import FIELDS_TO_HASH
from postgres import entry_to_tuple, insert_postgres, change_column_type
from time import sleep

#replaces cells values in the masked columns by their hashes
def mask_data(data_entry, fields=FIELDS_TO_HASH):
    for field in FIELDS_TO_HASH:
        if field in data_entry and data_entry[field] != 'NULL':
            data_entry[field] = md5(data_entry[field].encode()).hexdigest()

def mainloop():
    if poll():
        entries = extract_entries()
        for entry in entries:
            mask_data(entry)
        insert_postgres(entries)
    sleep(10)

def main():
    change_column_type()
    while True:
        mainloop()


if __name__ == '__main__':
    main()

