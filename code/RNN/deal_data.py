# -*-coding:utf-8-*-#
import shelve
import json
import urllib.request
import time
import numpy as np


addrs = 404
ids = 100
days = 371


def datatoint(data):
    y = int(data[:4])
    m = int(data[5:7])
    d = int(data[8:10])
    month_set = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    result = d - 1
    for i in range(m):
        result += month_set[i]
    return result


def deal_data():
    file_data = open("testdata.txt", 'r')
    file_data_ = open("testdata2.txt", 'w')
    bitaddr_trade = eval(file_data.read())

    data_txt = {}
    addr_count = 0
    addr_day = np.zeros((addrs, days))
    data_count = 0
    print(str(addrs) + '*' + str(days) + '\n')
    for addr in bitaddr_trade.keys():
        addr_txt = {}
        trade = bitaddr_trade[addr]

        blk_info = [list(i) for i in trade]
        # print(blk_info)
        info = {}
        for item in blk_info:
            if item[0] in info:
                info[item[0]] += item[1]
            else:
                info[item[0]] = item[1]

        for blk_time in info:
            if blk_time[:4] == "2011":
                day = datatoint(blk_time)
                addr_txt[day] = info[blk_time]
                addr_day[addr_count, day] = float(info[blk_time])
                data_count += 1
        data_txt[addr_count] = addr_txt
        addr_count += 1
    print(addr_day)
    print(data_count)
    file_data_.write(str(data_txt))
    addr_day.tofile("addr_day.bin")


def deal_txt():
    f = open("testdata_label.txt", 'r')
    label = eval(f.read())
    f.close()
    label2 = {}
    addr_count = 0
    addr_id = np.zeros((addrs, ids))
    print(str(addrs) + '*' + str(ids) + '\n')
    for addr in label.keys():
        labelid = label[addr] - 1
        label2[addr_count] = labelid
        addr_id[addr_count, labelid] = 1
        addr_count += 1
    print(addr_id)
    addr_id.tofile("addr_id.bin")


if __name__ == "__main__":
    deal_data()
    deal_txt()
