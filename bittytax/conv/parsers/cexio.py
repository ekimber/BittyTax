from decimal import Decimal

from ..out_record import TransactionOutRecord
from ..dataparser import DataParser
from ..exceptions import UnexpectedTypeError

WALLET = "Cexio"

def parse_cexio_trades(data_row, parser, **_kwargs):
    row_dict = data_row.row_dict
    data_row.timestamp = DataParser.parse_timestamp(row_dict['Close Date'])
 
    if row_dict['Status'] != 'Not executed':
        type = row_dict['Type'].split(" - ")[1]
        pair = row_dict['Pair'].split("/")
        base_amount=row_dict['Filled'].split(" ")
        price = Decimal(row_dict['Avg. Execution price'])
        if type == 'buy':
            data_row.t_record = TransactionOutRecord(TransactionOutRecord.TYPE_TRADE,
                                                     data_row.timestamp,
                                                     buy_quantity=base_amount[0],
                                                     buy_asset=pair[0],
                                                     sell_quantity=price * Decimal(base_amount[0]),
                                                     sell_asset=pair[1],
                                                     fee_quantity=row_dict['Fee'],
                                                     fee_asset=pair[1],
                                                     wallet=WALLET)
        elif type == 'sell':
            data_row.t_record = TransactionOutRecord(TransactionOutRecord.TYPE_TRADE,
                                                     data_row.timestamp,
                                                     buy_quantity=price * Decimal(base_amount[0]),
                                                     buy_asset=pair[1],
                                                     sell_quantity=base_amount[0],
                                                     sell_asset=pair[0],
                                                     fee_quantity=row_dict['Fee'],
                                                     fee_asset=pair[1],
                                                     wallet=WALLET)

def parse_cexio_transactions(data_row, parser, **_kwargs):
    row_dict = data_row.row_dict
    data_row.timestamp = DataParser.parse_timestamp(row_dict['DateUTC'])

    if row_dict['Type'] == 'withdraw':
        feeAmt = row_dict['FeeAmount']
        feeSym = row_dict['FeeSymbol']
        data_row.t_record = TransactionOutRecord(TransactionOutRecord.TYPE_WITHDRAWAL,
                                                 data_row.timestamp,
                                                 sell_quantity=-1*Decimal(row_dict['Amount']),
                                                 sell_asset=row_dict['Symbol'],
                                                 fee_quantity=feeAmt if feeAmt else 0,
                                                 fee_asset=feeSym if feeSym else "GBP",
                                                 wallet=WALLET)

    elif row_dict['Type'] == 'deposit':
        data_row.t_record = TransactionOutRecord(TransactionOutRecord.TYPE_DEPOSIT,
                                             data_row.timestamp,
                                             buy_quantity=row_dict['Amount'],
                                             buy_asset=row_dict['Symbol'],
                                             wallet=WALLET)


DataParser(DataParser.TYPE_EXCHANGE,
           "Cexio",
           ['ID','Pair','Type','Amount','Price','Filled','Avg. Execution price','Fee',
            'Balance change','Status','Open Date','Close Date'],
           worksheet_name="Cexio",
           row_handler=parse_cexio_trades)

DataParser(DataParser.TYPE_EXCHANGE,
           "Cexio",
           ['DateUTC','Amount','Symbol','Balance','Type','Pair','FeeSymbol','FeeAmount','Comment'],
           worksheet_name="Cexio",
           row_handler=parse_cexio_transactions)
