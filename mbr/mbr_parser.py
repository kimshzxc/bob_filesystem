import sys
import struct


def read_sectors(fd, sector, count = 1):
    fd.seek(sector * 512)
    return fd.read(count * 512)

def print_table_entry(table):
    print("=======================================")
    print("Active: ", table[0])
    print("CHS1 : ", table[1], table[2], table[3])
    print("FileSystem : ", table[4])
    print("CHS2 : ", table[5], table[6], table[7])
    print("Starting LBA : ", struct.unpack_from("<L", table, 8)[0])
    print("size : ", struct.unpack_from("<L", table, 12)[0])
    print("")



def go_to_EBR_partition(table,i,ebr_start,next):
    # EBR parser
    if table[4] == 5:
        i = i+1
        next_data = read_sectors(f, ebr_start+next)
        print("[",i,"th  EBR  Partition  Starting Address =", (ebr_start+next) * 512,"]")
        ndata = next_data[446:446 + 64]
        intable1 = ndata[0:16]
        intable2 = ndata[16:32]
        print_table_entry(intable1)
        go_to_EBR_partition(intable1,i,struct.unpack_from("<L", intable1, 8)[0],next)
        print_table_entry(intable2)
        go_to_EBR_partition(intable2,i,struct.unpack_from("<L", intable2, 8)[0],next)


filename = "mbr_128.dd"
f = open(filename, "rb")
data = read_sectors(f, 0)

if data[-2] != 0x55 and \
    data[-1] != 0xAA:
    print("이 파티션은 Boot Record가 아닙니다.")

partition_data = data[446:446+64]

table1 = partition_data[0:16]
table2 = partition_data[16:32]
table3 = partition_data[32:48]
table4 = partition_data[48:64]

print("1 Partition")
print_table_entry(table1)
print("2 Partition")
print_table_entry(table2)
print("3 Partition")
print_table_entry(table3)
print("4 Partition")
print_table_entry(table4)
go_to_EBR_partition(table4,0,0,struct.unpack_from("<L", table4, 8)[0])

