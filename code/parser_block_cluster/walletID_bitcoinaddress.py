import shelve
import json
import urllib
import socket
import lxml.html
import time


def get_address(html, address_type):
    # address_type = 0 input address
    # address_type = 1 output address
    address = []
    try:
        tree = lxml.html.fromstring(html)
        ul = tree.cssselect('ul')[address_type]
        addre = ul.cssselect('span.trade_address')
        for ele in addre:
            address.append(ele.text_content())
        '''
        for element in a:
            tmpurl = element.get('href')
            links.append(tmpurl)
        '''
    except Exception as e:
        pass

    return address


# parser single transaction and extract output address
def parse_transaction(tx, address_type):
    address = []
    # input address
    if address_type == 0:
        for inp in tx['inputs']:
            address.append(inp['prev_out']['addr'])
    # output address
    else:
        for out in tx['out']:
            address.append(out['addr'])

    return address


def match_walletID_bitaddr(ID_txhash, address_type):
    global idx
    socket.setdefaulttimeout(3)
    for walletId in ID_txhash.keys():
        idx += 1
        print(idx)
        try:
            txhashes = ID_txhash[walletId]
        except Exception as e:
            continue

        for txhash in txhashes:
            try:
                request = urllib.request.urlopen('http://www.qukuai.com/search/zh-CN/BTC/' + txhash)
                html = request.read()
                request.close()
                address = get_address(html, address_type)
                # print('method2 ', walletId, address)
            except Exception as e:
                try:
                    html = urllib.request.urlopen('https://blockchain.info/rawtx/' + txhash)
                    hjson = json.loads(html.read())
                    address = parse_transaction(hjson, address_type)
                    # print('method1 ', address)
                except Exception as e:
                    print('get address failed')
                    continue

            if walletId not in walletId_bitaddr:
                # print('1 ', walletId, address)
                walletId_bitaddr[walletId] = address
            else:
                # print( 'not 1 ', walletId, address)
                walletId_bitaddr[walletId].extend(address)


if __name__ == '__main__':
    withdraw_txhash = shelve.open('shelve_db100000/withdraw_txhash.db')
    deposit_txhash = shelve.open('shelve_db100000/deposit_txhash.db')

    walletId_bitaddr = {}

    idx = 0
    t1 = time.time()
    match_walletID_bitaddr(withdraw_txhash, 1)
    idx = 0
    match_walletID_bitaddr(deposit_txhash, 0)
    print(time.time()-t1)

    for id in walletId_bitaddr.keys():
        # tmpaddr = set(bitaddr)
        walletId_bitaddr[id] = set(walletId_bitaddr[id])
        
    withdraw_txhash.close()
    deposit_txhash.close()

    file = open('shelve_db100000/walletId_bitaddr.txt', 'w')
    file.write(str(walletId_bitaddr))
    file.close()

    # file.close()
