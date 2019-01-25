import sys

file_in = sys.argv[1]
file_out = sys.argv[2]

with open(file_out, 'wb') as fout:
        fout.write(b'\xff' * 0x1000)
        with open(file_in, 'rb') as fin:
            data = fin.read()
            fout.write(data)
