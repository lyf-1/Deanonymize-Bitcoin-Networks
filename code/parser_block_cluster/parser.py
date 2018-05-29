#!/usr/bin/env python
# coding=utf-8
import sys
import mmap
import struct
import shelve
import time
from btc import Block
from WriteToTXT import WriteToTXT


BITCOIN_CONSTANT = b"\xf9\xbe\xb4\xd9"
idx = 0
cnt_all = []


def parse_from_file(raw_data):
    length = len(raw_data)
    offset = 0
    cnt = 0
    while offset < (length-4):
        if raw_data[offset: offset+4] == BITCOIN_CONSTANT:
            offset += 4
            size = struct.unpack("<I", raw_data[offset:offset+4])[0]
            offset += 4+size
            block = Block().parse_from_hex(raw_data[offset-8-size: offset])
            filename = 'new_data/' + str(cnt) + '.txt'
            print(cnt)
            WriteToTXT(block, filename)
            if cnt == 672:
                return block
            cnt += 1
        else:
            offset += 1


# parse one blk.dat file and get all non-coinbase tx_hash
def parser_to_get_txhash(raw_data):
    length = len(raw_data)
    offset = 0
    tx_hash = []

    while offset < (length-4):
        if raw_data[offset: offset+4] == BITCOIN_CONSTANT:
            offset += 4
            size = struct.unpack("<I", raw_data[offset:offset+4])[0]
            offset += 4+size
            block = Block().parse_from_hex(raw_data[offset-8-size: offset])
            for i in range(1, block._tx_cnt):
                tx_hash.append(block._tx_list[i].hash)
        else:
            offset += 1

    return tx_hash


# parse one blk.dat file and get all block which contains 2 or more txs
def parser_to_get_blockhash(raw_data, fileidx):
    global idx
    length = len(raw_data)
    offset = 0
    cnt = 0
    while offset < (length-4):
        if raw_data[offset: offset+4] == BITCOIN_CONSTANT:
            offset += 4
            size = struct.unpack("<I", raw_data[offset:offset+4])[0]
            offset += 4+size
            block = Block().parse_from_hex(raw_data[offset-8-size: offset])
            if block._tx_cnt > 1:
                t = block._block_header._timestamp
                shelve_db[str(t)] = block
                idx += 1
                cnt += 1
                print(fileidx, idx, t)
        else:
            offset += 1
    cnt_all.append(cnt)


if __name__ == '__main__':
    begin = time.time()
    shelve_db = shelve.open('shelve_db100000/blk0_7_time_block.db')

    # blk00000.dat - blk00007.dat stores the block created in 2009, 2010, 2011 year
    # for filenum in range(0, 8):
    for filenum in range(0, 1):
        blk_file_path = 'blk_dat/blk0000'+str(filenum)+'.dat'
        with open(blk_file_path, 'rb') as f:
            data = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            # txs_hash = parser_to_get_txhash(data)
            parser_to_get_blockhash(data, filenum)
    shelve_db.close()
    end = time.time()
    print('=======')
    print(end - begin)
