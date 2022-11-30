import gdb
import struct

addr = 0x602000 
length = 0x50 
bp = 0x400e9c 
file_name = './secretgarden' 

gdb.execute("file %s"%file_name)
gdb.execute("b * %s"%hex(bp))
gdb.execute("r")

inf = gdb.inferiors()[0]
m = inf.read_memory(addr,length).tolist()

for i in range(8):
    cur = i
    while(cur < length-7):
        val = b''
        for j in range(8):
            val += m[cur + j]
        val = struct.unpack('<Q',(val))[0]
        sz = (val & 0x00000000ffffffff)
        if(0x20 <=sz <= 0x80):
            print("found sz : ",hex(sz))
            print("addr : "+hex(addr+cur-0x8))
        cur += 8