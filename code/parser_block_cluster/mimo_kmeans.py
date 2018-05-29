# -*-coding:utf-8-*-#
import shelve
import json
import urllib.request
import lxml.html
import socket
import time
from walletID_txhash import date_to_timestamp, timestamp_to_date
from sklearn.cluster import KMeans
from sklearn import metrics
import numpy as np

# data to the day of 2011 year
def datatoint(data):
    y = int(data[:4])
    m = int(data[5:7])
    d = int(data[8:10])
    month_set = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    result = d
    for i in range(m):
        result += month_set[i]
    return result


# get input & output relationship
# return 'one input addr - one output addr - value - timestamp' feature
def mimo_bitcoin(inputs, outputs, timestamp):
    i = 0
    j = 0
    input_output = []
    while i < len(inputs) and j < len(outputs):
        # print(i, j,  len(inputs),  len(outputs))
        if inputs[i][1] < outputs[j][1]:
            if inputs[i][0] != outputs[j][0]:
                input_output.append([inputs[i][0], outputs[j][0], inputs[i][1], timestamp])
            outputs[j][1] -= inputs[i][1]
            inputs[i][1] = 0
            i += 1
        elif inputs[i][1] == outputs[j][1]:
            if inputs[i][0] != outputs[j][0]:
                input_output.append([inputs[i][0], outputs[j][0], inputs[i][1], timestamp])
            inputs[i][1] = outputs[j][1] = 0
            i += 1
            j += 1
        else:
            if inputs[i][0] != outputs[j][0]:
                input_output.append([inputs[i][0], outputs[j][0], outputs[j][1], timestamp])
            inputs[i][1] -= outputs[j][1]
            outputs[j][1] = 0
            j += 1
    return input_output


# crawler website using tx_hash
# and parser the relatioship of multple-inputs & multiple-outputs 
def get_tx_info(txhash):
    socket.setdefaulttimeout(3)
    print("connect to the web")
    request = urllib.request.urlopen('http://www.qukuai.com/search/zh-CN/BTC/' + txhash)
    html = request.read()
    request.close()
    tree = lxml.html.fromstring(html)

    time = tree.cssselect('span.desc_item')[0].text
    timestamps = date_to_timestamp(time)
    # value = tree.cssselect('span.info_text')[3].text
    # value = value.rstrip(' ').strip('\n').lstrip(' ')

    ul = tree.cssselect('ul')

    tx_inputs = []
    tx_outputs = []

    inp = ul[0].cssselect('span.trade_address')
    inp_v = ul[0].cssselect('span.trdde_num')
    out = ul[1].cssselect('span.trade_address')
    out_v = ul[1].cssselect('span.trdde_num')
    for i in range(len(inp)):
        tx_inputs.append([inp[i].text, float(inp_v[i].text)])
    for i in range(len(out)):
        tx_outputs.append([out[i].text, float(out_v[i].text)])

    inp_out_val_time = mimo_bitcoin(tx_inputs, tx_outputs, timestamps)

    return inp_out_val_time


def trans_address_to_int():
    # read feature from .txt file
    f = open('shelve_db100000/tx100000_info.txt', 'r')
    features = f.readlines()

    txs_feature = []
    address_dict = {}
    address_idx = 0

    for feat in features:
        feat = feat.rstrip('\t\n').split('\t')
        feat[2] = float(feat[2])
        timestamp = int(feat[3])
        date = timestamp_to_date(timestamp)
        feat[3] = datatoint(date)
        for i in range(2):
            if feat[i] not in address_dict:
                address_dict[feat[i]] = address_idx
                address_idx += 1
            feat[i] = address_dict[feat[i]]

        txs_feature.append(feat)
    f.close()

    return address_dict, txs_feature


def kmeans(x):
    scores = []
    for num_clusters in range(3347, 3348, 1000):
        kmeans_model = KMeans(n_clusters=num_clusters, random_state=0).fit(x)
        distance = kmeans_model.inertia_
        # common method to assess the performance of cluster: Silhouette Coefficient and Calinski-Harabasz Index
        # use Calinski-Harabasz Index to assess the score of k-kmeans_model with k = 2
        # score = metrics.calinski_harabaz_score(x, kmeans_model.labels_)
        print(num_clusters, distance)
        scores.append(distance)
    return scores, kmeans_model.labels_


if __name__ == '__main__':
    '''
    withdraw_txhash = shelve.open('shelve_db100000/withdraw_txhash.db')
    deposit_txhash = shelve.open('shelve_db100000/deposit_txhash.db')

    all_tx_feature = []

    cnt = 0
    for key in withdraw_txhash:
        for txhash in withdraw_txhash[key]:
            tx_feature = get_tx_info(txhash)
            all_tx_feature.extend(tx_feature)

    for key in deposit_txhash:
        for txhash in deposit_txhash[key]:
            tx_feature = get_tx_info(txhash)
            all_tx_feature.extend(tx_feature)

    # write tx_feature to file tx100000_info.txt
    '''

    # test kmeans
    # our dataset contains 3347 different users wallet
    # kmeans results show that k is between 3000 and 4000
    address_dict, txs_feature = trans_address_to_int()
    txs_feature = np.array(txs_feature)
    scores, kmeans_label = kmeans(txs_feature)

