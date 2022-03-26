from decimal import Decimal

from ..out_record import TransactionOutRecord
from ..dataparser import DataParser

WALLET = "Yoroi"

def parse_yoroi_tx(data_row, _parser, **_kwargs):
    row_dict = data_row.row_dict
    data_row.timestamp = DataParser.parse_timestamp(row_dict['Date'])
    row_type = row_dict['Type (Trade, IN or OUT)']

    if row_type == 'Deposit':
        deposit_tx(data_row, row_dict)

    elif row_type == 'Withdrawal':
        withdraw_tx(data_row, row_dict)

def deposit_tx(data_row, row_dict):
    if row_dict['Comment (optional)'].startswith('Staking Reward'):
        data_row.t_record = TransactionOutRecord(TransactionOutRecord.TYPE_STAKING,
                                                 data_row.timestamp,
                                                 buy_quantity=row_dict['Buy Amount'],
                                                 buy_asset=row_dict['Buy Cur.'],
                                                 wallet=WALLET)
    else:
        data_row.t_record = TransactionOutRecord(TransactionOutRecord.TYPE_DEPOSIT,
                                                 data_row.timestamp,
                                                 buy_quantity=row_dict['Buy Amount'],
                                                 buy_asset=row_dict['Buy Cur.'],
                                                 wallet=WALLET)

def withdraw_tx(data_row,row_dict):
    if Decimal(row_dict['Sell Amount']) == 0 and row_dict['Fee Amount (optional)']:
        # it is only a fee expense
        data_row.t_record = TransactionOutRecord(TransactionOutRecord.TYPE_SPEND,
                                                 data_row.timestamp,
                                                 sell_asset=row_dict['Fee Cur. (optional)'],
                                                 sell_quantity=row_dict['Fee Amount (optional)'],
                                                 wallet=WALLET)
    else:
        data_row.t_record = TransactionOutRecord(TransactionOutRecord.TYPE_WITHDRAWAL,
                                                 data_row.timestamp,
                                                 sell_quantity=row_dict['Sell Amount'],
                                                 sell_asset=row_dict['Sell Cur.'],
                                                 fee_quantity=row_dict['Fee Amount (optional)'],
                                                 fee_asset=row_dict['Fee Cur. (optional)'],
                                                wallet=WALLET)

DataParser(DataParser.TYPE_WALLET,
           "Yoroi",
           ["Type (Trade, IN or OUT)","Buy Amount","Buy Cur.","Sell Amount","Sell Cur.",
            "Fee Amount (optional)","Fee Cur. (optional)","Exchange (optional)",
            "Trade Group (optional)","Comment (optional)","Date"],
           worksheet_name="Yoroi",
           row_handler=parse_yoroi_tx)
