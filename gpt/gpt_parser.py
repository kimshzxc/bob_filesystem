import struct

def read_sectors(fd, sector, count = 1):
    fd.seek(sector * 512)
    return fd.read(count * 512)

def read_partiton(fd, number, sector,count = 1):
    fd.seek(sector * 512 + number * 128)
    return fd.read(128)

filename = "gpt_128.dd"
f = open(filename, "rb")
data = read_sectors(f, 1)

partition_data = data[72:80]


Partition_Entries_starting_LBA = struct.unpack_from("<L",partition_data,0)[0]  ## Partition

print("Partition Entries starting LBA = ",Partition_Entries_starting_LBA)

i = 0   #Start index

while(1):
    data = read_partiton(f, i, Partition_Entries_starting_LBA)
    if(struct.unpack_from("<L",data[32:40],0)[0]==0 ) or (i == 128):
        break
    print()
    print(i+1,"th Partition Information")
    start = struct.unpack_from("<L",data[32:40],0)[0]
    last = struct.unpack_from("<L",data[40:48],0)[0]
    print("[Start Address] =",hex(start*512))
    print("[Size] =",hex((last-start+1)*512))
    i = i+1

