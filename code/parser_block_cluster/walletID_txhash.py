import shelve
import time


# read mtgox_change info from .txt file
def read_from_txt(filename):
    f = open(filename, 'r')
    mtgox_change = []
    for line in f:
        line = line.strip('\n').split('\t')
        mtgox_change.append(line)
    return mtgox_change


def date_to_timestamp(date):
    timearray = time.strptime(date, "%Y-%m-%d %H:%M:%S")
    timestamp = int(time.mktime(timearray))
    return timestamp


def timestamp_to_date(timestamp):
    time_local = time.localtime(timestamp)
    date = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return date


def get_matched_transaction(begin, end, value):
    matched_list = []
    block_cnt = 0
    deposit_block_cnt = 0
    delt_j = 1
    if begin > end:
        delt_j = -delt_j
        while begin > end and deposit_block_cnt < 6:
            if str(begin) in idx_blocks:
                deposit_block_cnt += 1
            begin -= 1

    for j in range(begin, end, delt_j):
        if block_cnt == 30:
            break
        if str(j) not in idx_blocks:
            continue

        # print(j)
        # if j == 1311655865:
        #   print('liuyunfei')

        block_cnt += 1
        block = idx_blocks[str(j)]
        # print(j, block_cnt)
        for tx in block._tx_list:
            # if tx.output_cnt == 1 and tx._outputs[0]._value == value:
            #    matched_list.append(tx.hash)
            # if tx.hash == 'b2666817dc7851430b64c09fcdeadd980cabc78e310c541e19d830e0f08f4417':
            #   print('successful! ', tx._tx_value, value)
            if tx._tx_value == value:
                matched_list.append(tx.hash)
    # print(begin, end, begin-end, j)
    # print('block searched numbers: ', block_cnt)

    return matched_list


def withdraw_process(change):
    timestamps = int(change[3])
    value = -int(float(change[2])*1e8)

    for time in idx_blocks.keys():
        time = int(time)
        if time < timestamps:
            continue
        another_idx = time + 24 * 3600
        matched_list = get_matched_transaction(time, another_idx, value)

        return matched_list


def deposit_process(change):
    timestamps = int(change[3])
    value = int(float(change[2])*1e8)

    for time in idx_blocks.keys():
        time = int(time)
        if time < timestamps:
            continue

        another_idx = time - 24 * 3600
        matched_list = get_matched_transaction(time, another_idx,  value)

        return matched_list


if __name__ == '__main__':
    mtgox_change = read_from_txt('shelve_db100000/btf_xfer_report2011.txt')

    idx_blocks = shelve.open('shelve_db100000/blk0_7_time_block.db')
    # walletID_bitaddr_dict = {}
    withdraw_txhash = shelve.open('shelve_db100000/withdraw_txhash.db')
    deposit_txhash = shelve.open('shelve_db100000/deposit_txhash.db')

    match_success_times = 0
    multi_match_times = 0
    initial_time = time.time()
    for i in range(0, 100000):
        print(i)
        start_time = time.time()
        one_change = mtgox_change[i]
        
        if one_change[1] == 'withdraw':
            rst = withdraw_process(one_change)
            if len(rst) > 1:
                multi_match_times += 1
            if len(rst) != 1:
                # print(i, ' F ', time.time() - start_time)
                continue

            match_success_times += 1
            if one_change[0] in withdraw_txhash:
                withdraw_txhash[one_change[0]].extend(rst)
            else:
                withdraw_txhash[one_change[0]] = rst
        else:
            rst = deposit_process(one_change)
            if len(rst) > 1:
                multi_match_times += 1
            if len(rst) != 1:
                # print(i, ' F ', time.time() - start_time)
                continue

            match_success_times += 1
            if one_change[0] in deposit_txhash:
                deposit_txhash[one_change[0]].extend(rst)
            else:
                deposit_txhash[one_change[0]] = rst

        # print(i, ' Successful ', time.time() - start_time)

    withdraw_txhash.close()
    deposit_txhash.close()
    idx_blocks.close()

    print('---------------------')
    print('all time used: ', time.time() - initial_time)
