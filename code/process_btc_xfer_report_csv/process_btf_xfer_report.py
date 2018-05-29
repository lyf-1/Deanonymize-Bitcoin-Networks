import csv
import time


# process btf_xfer_report.csv file
# rewrite to a .txt file
def write_to_txt(filename):
    file = open(filename, 'a')

    # '2011/12/31 23:59:59' == 1325347199
    # get all records in 2011 year
    flag_timestamp = 1325347199
    for i in range(1, 11):
        csv_data = csv.reader(open('btc_xfer_report/btc_xfer_report-' + str(i) + '.csv', 'r'))
        cnt = 0
        for row in csv_data:
            '''
            if cnt == 5:
                break
            '''
            # transform time to timestamp
            time_array = time.strptime(row[2], "%Y-%m-%d %H:%M:%S")
            timestamp = int(time.mktime(time_array))
            if timestamp > flag_timestamp:
                continue

            file.write('%s\t' % row[0])
            file.write('%s\t' % row[3])
            file.write('%s\t' % row[4])
            file.write('%d\t' % timestamp)
            file.write('%s\n' % row[2])
            cnt += 1
            print(i, cnt)
    file.close()


'''
if __name__ == '__main__':
    write_to_txt('btc_xfer_report2011.txt')
    print('over')
'''