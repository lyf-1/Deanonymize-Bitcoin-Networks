# -Deanonymize-Bitcoin-Networks
Learning To Deanonymize The Bitcoin Networks Using Neural Network

The main process
I. cluster
1. The bitcoin exchange record between real world user and a bitcoin company
download btc_xfer_report.csv from https://github.com/shemnon/GoxCalc/tree/master/src/main/resources. Mt.Gox leaked this file.


2. download complete bitcoin client and parser blk*****.dat file.
block structure is shown in file block_info.txt
parser code from https://github.com/huangsuoyuan/btc_parser

3. Bind users and bitcoin addresses
* rom step1, get users wallet ID, exchange value and exchange time  
* from step2, get transaction value and block time.
* match exchange record and bitcoin transaction
* using transaction hashes to get transaction details including input or output address. This can be 
  done by using API of https://blockchain.info/api/blockchain_api, or crawl website http://www.qukuai.com/search/zh-CN.
  (Transaction input address and output address are not stored in block. Output address can got by parser output script.
  But input script is different due to different kinds of means of transaction. We can use previous transaciton hash to
  parser previous transaction's output script to get current transaction's input address. Sounds a big project, so we use
  blockchain API or crawl bitcoin browser website to get input and output address.)

II. feature encoding / model user transaction characteristic 
1. handling class unbalance problem
* analysis of the number of bitcoin addresses in each user wallet
* analysis of some methods to handle this problem
* try to use GAN to generate some data

2. encode feature as input of RNN
* n user wallet ID, k bitcoin addersses.
  k*n matrix represents which user the bitcoin address belongs to [one-hot]
  The k*n matrix is the train_y of RNN
* train_x. k*365 matrix. statistic transaction amount of each bitcoin address in one day, 
  to form a sequential vector. 

III. Using RNN to learn abstract feature and classfication.
