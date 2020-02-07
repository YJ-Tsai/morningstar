import datetime
import logging
import unittest

import yaml

from morningstar.models.instrument import Instrument
from morningstar.morningstar_client import MorningstarClient
from morningstar.provider.morningstar import Morningstar

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONFIG_PATH = 'config-morningstar.yml.dist'
CONFIG = yaml.safe_load(open(CONFIG_PATH))['provider']['morningstar']
CONFIG_LIVE = None
try:
    from morningstar.config import config
    CONFIG_LIVE = config.get("provider")['morningstar']
except:
    logger.info("Skipping live tests.")
    pass


class MorningstarClientTest(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.client = MorningstarClient(Morningstar(config=CONFIG))
        if CONFIG_LIVE is not None:
            self.client_live = MorningstarClient(Morningstar(config=CONFIG_LIVE))

    @unittest.skipIf(CONFIG_LIVE is None, "Live configuration missing")
    def test_get_traded_currencies(self):
        currencies = self.client_live.get_traded_currencies(instrument="182.1.NESN")
        self.assertEqual(["CHF"], currencies)

    @unittest.skipIf(CONFIG_LIVE is None, "Live configuration missing")
    def test_get_prices_by_most_available(self):
        instrument, prices = self.client_live.get_prices_by_most_available(
            isin="CH0038863350",
            currency="CHF",
            start_date="01-01-2019",
            end_date="03-01-2019"
        )
        self.assertEqual(Instrument.from_string("215.1.NESR"), instrument)

    @unittest.skipIf(CONFIG_LIVE is None, "Live configuration missing")
    def test_find_instruments_by_isin_and_currency(self):
        instruments = self.client_live.find_instruments_by_isin_and_currency(isin="CH0038863350", currency="CHF")
        self.assertTrue(Instrument.from_string("215.1.NESR") in instruments)

    @unittest.skipIf(CONFIG_LIVE is None, "Live configuration missing")
    def test_get_instrument_prices(self):
        prices = self.client_live.get_instrument_prices(
            instrument="182.1.NESN",
            start_date="03-01-2019",
            end_date="04-01-2019"
        )
        self.assertEqual(
            [
                datetime.datetime(2019, 1, 4, 0, 0),
                datetime.datetime(2019, 1, 3, 0, 0)
            ],
            list(prices.keys())
        )

    @unittest.skipIf(CONFIG_LIVE is None, "Live configuration missing")
    def test_get_instrument_prices(self):
        meta_data = self.client_live.get_instrument_meta(
            instrument="182.1.UBSG",
        )
        ref_data = {
                'Symbol': 'UBSG',
                'Exchange': '182',
                'Security Type': '1',
                'Listed Currency': 'CHF',
                'Company name': 'UBS GROUP N',
                'ISIN code': 'CH0244767585',
                'Country': 'CH',
                'Local instrument cod': '024476758',
                'Exchange code': 'XVTX',
                'MS Performance ID': '0P0000A5G3',
                'Morningstar Industry': 'Banks - Diversified',
                'Morningstar Group Na': 'Banks',
                'Morningstar Sector N': 'Financial Services',
                'MS Investment ID (Se': 'E0CHE010PE',
                'FIGI country code': 'BBG007936GV2',
                'Shareclass-level FIG': 'BBG007936GX0',
                'Global ID investment': 'Equity',
                'Dividend per share': '0.686497',
                'The currency of the ': 'USD',
                'The Record date of a': '06.05.2020',
                'Effective Date - Cor': '05.05.2020',
                'EDI Local flag': 'UBSG',
                'MS Medium Business D': "UBS is the world's largest wealth manager and is the product of multiple mergers over the years. Apart from wealth and asset management, it operates a universal bank in Switzerland and a global investment bank.",
                'Market Cap': '44856902998',
                'Dividend Yield': '5.64',
                'PE Ratio': '1.5147',
                'Debt to equity ratio': '2.915621',
                'Price to Book': '0.851571',
                'Listing start date (': '20141128',
                'Listing end date (st': '99991231',
                'EDI Primary Exchange': 'CHSSX'}
        self.assertEqual(meta_data, ref_data)

    @unittest.skipIf(CONFIG_LIVE is None, "Live configuration missing")
    def test_get_fx_prices(self):
        prices = self.client_live.get_fx_prices(
            base_currency="USD",
            counter_currency="CHF",
            start_date="01-01-2019",
            end_date="03-01-2019"
        )
        self.assertEqual(
            [
                datetime.datetime(2019, 1, 3, 0, 0),
                datetime.datetime(2019, 1, 2, 0, 0),
                datetime.datetime(2019, 1, 1, 0, 0)
            ],
            list(prices.keys())
        )
