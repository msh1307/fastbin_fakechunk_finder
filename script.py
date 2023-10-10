import gdb
import struct

print('addr hex: ',end='')
addr = int(input(),16)
print('len hex: ',end='')
length = int(input(),16)

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
            print("found sz : ",hex(sz&(~0b111)))
            print('malloc sz : '+hex((sz>>4<<4)-0x10))
            print("addr : "+hex(addr+cur-0x8))
        cur += 8
