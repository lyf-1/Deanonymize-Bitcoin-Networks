# write a block detailed information to a .txt file
import binascii

class WriteToTXT:
    def __init__(self, block, filename):
        file = open(filename, 'w')
        file.write('magic_number: \t%d\n' % block._magic_number)
        file.write('block_size: \t%d\n' % block._block_size)

        # block header detail info
        file.write('\nBlock Header \n')
        file.write('version: \t%d\n' %  block._block_header._version)
        file.write('previous_block_hash: \t%s\n'% block._block_header._previous_block_hash)
        file.write('merkle_root_hash: \t%s\n'% block._block_header._merkle_root)
        file.write('timestamp: \t%s\n' % block._block_header._timestamp)
        file.write('nBits: \t%x\n' % block._block_header._bits)
        file.write('nonce: \t%s\n' % block._block_header._nonce)
        file.write('current_block_hash: \t%s\n' % block._block_header.hash)

        # transaction detail info
        file.write('\ntransaction_number: \t%d\n' % block._tx_cnt)
        for i in range(block._tx_cnt):
            file.write('\n\n')
            file.write('='*60+'New Transaction'+'='*60+'\n')
            file.write('self hash: \t%s\n' % block._tx_list[i].hash)
            file.write('version: \t%d\n' % block._tx_list[i]._version)

            # transaction input detailed info
            file.write('\n\ntx_inputs_cnt: \t%d\n' % block._tx_list[i].input_cnt)
            for j in range(block._tx_list[i].input_cnt):
                file.write('-'*20+'\n')
                file.write('previous_transaction_hash: \t%s\n' % block._tx_list[i]._inputs[j]._previous_transaction_hash)
                file.write('previous_transaction_index: \t%d\n' % block._tx_list[i]._inputs[j]._previous_transaction_index)
                # file.write('script_bytes: \t%d\n' % block._tx_list[i]._inputs[j].script_bytes)
                file.write('script_signature: \t%s\n' % block._tx_list[i]._inputs[j]._script)
                # file.write('input_address: \t%s\n' % block._tx_list[i]._inputs[j].input_address)
                file.write('sequence_num : \t%s\n' % block._tx_list[i]._inputs[j]._sequence_number)

            # transaction output detailed info
            file.write('\n\ntx_outputs_cnt: \t%d\n' % block._tx_list[i].output_cnt)
            for j in range(block._tx_list[i].output_cnt):
                file.write('-' * 20 + '\n')
                file.write('value : \t%f BTC\n' % block._tx_list[i]._outputs[j]._value)
                # file.write('pk_script_size : \t%d\n' % block._tx_list[i]._outputs[j].pk_script_size)
                file.write('pk_script : \t%s\n' % binascii.b2a_hex(block._tx_list[i]._outputs[j]._script))
                # file.write('output_address: \t%s\n' % block._tx_list[i].outputs[j].output_address)

            # file.write('\n\nlock_time: \t%d\n' % block._tx_list[i]._lock_time)