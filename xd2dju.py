from zipfile import ZipFile

test_file = "pain.xd"

with ZipFile(test_file, 'r') as zip:
    zip.printdir()