from decimal import Decimal

from ..out_record import TransactionOutRecord
from ..dataparser import DataParser
from ..exceptions import UnexpectedTypeError

WALLET = "Bisq"

def parse_bisq_trades(data_row, _parser, **_kwargs):
    row_dict = data_row.row_dict
    data_row.timestamp = DataParser.parse_timestamp(row_dict['Date/Time'])

    if row_dict['Status'] == "Completed":
        if row_dict['Offer type'] == 'Sell BTC':
            data_row.t_record = TransactionOutRecord(TransactionOutRecord.TYPE_TRADE,
                                                     data_row.timestamp,
                                                     buy_asset=row_dict['Amount'].split(" ")[1],
                                                     buy_quantity=row_dict['Amount'].split(" ")[0],
                                                     sell_quantity=row_dict['Amount in BTC'],
                                                     sell_asset="BTC",
                                                     fee_quantity=Decimal(row_dict['Transaction Fee'])
                                                     + Decimal(row_dict['Trade Fee'].split(" ")[0]),
                                                     fee_asset="BTC",
                                                     wallet=WALLET)

def parse_bisq_transactions(data_row, _parser, **_kwargs):
    row_dict = data_row.row_dict
    data_row.timestamp = DataParser.parse_timestamp(row_dict['Date/Time'])

    if row_dict['Details'] == "Received funds":
        data_row.t_record = TransactionOutRecord(TransactionOutRecord.TYPE_DEPOSIT,
                                                 data_row.timestamp,
                                                 buy_quantity=row_dict['Amount in BTC'],
                                                 buy_asset="BTC",
                                                 wallet=WALLET)

    elif row_dict['Details'].startswith("Maker and tx fee"):
        data_row.t_record = TransactionOutRecord(TransactionOutRecord.TYPE_SPEND,
                                                 data_row.timestamp,
                                                 sell_quantity=Decimal(row_dict['Amount in BTC']) * -1,
                                                 sell_asset="BTC",
                                                 wallet=WALLET)

DataParser(DataParser.TYPE_EXCHANGE,
           "Bisq Trades",
           ['Trade ID', 'Date/Time','Market', 'Price', 'Deviation', 'Amount in BTC', 'Amount',
            'Transaction Fee', 'Trade Fee', 'Buyer Deposit', 'Seller Deposit', 'Offer type', 'Status'],
           worksheet_name="Bisq T",
           row_handler=parse_bisq_trades)

DataParser(DataParser.TYPE_EXCHANGE,
           "Bisq Transactions",
           ['Date/Time','Details','Address','Transaction ID','Amount in BTC','Memo','Confirmations'],
           worksheet_name="Bisq D/W",
           row_handler=parse_bisq_transactions)
