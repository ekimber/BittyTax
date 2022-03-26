from decimal import Decimal

from ..out_record import TransactionOutRecord
from ..dataparser import DataParser
from ..exceptions import DataFilenameError

WALLET = "Ethereum 2"

def parse_validator_rewards(data_row, _parser, **_kwargs):
    row_dict = data_row.row_dict
    data_row.timestamp = DataParser.parse_timestamp(row_dict['Date'])
    data_row.t_record = TransactionOutRecord(TransactionOutRecord.TYPE_STAKING,
                                             data_row.timestamp,
                                             buy_quantity=Decimal(row_dict['Income for date ETH']),
                                             buy_asset='ETH',
                                             buy_value=Decimal(row_dict['Income for date']),
                                             wallet=WALLET)

DataParser(DataParser.TYPE_EXPLORER,
           "Beaconcha.in",
           ['Date','End-of-date balance ETH','Income for date ETH','Price of ETH for date','Income for date'],
           worksheet_name="Beaconcha.in",
           row_handler=parse_validator_rewards)



