"""  Created on 24/01/2024::
------------- test_all.py -------------
 
**Authors**: L. Mingarelli
"""

from haver import Haver
import os

haver = Haver(api_key=os.getenv('HAVER_API_KEY'))


if haver._is_connected:
    class TestHaver:

        def test_HAVER_connection(self):
            assert haver._is_connected

        def test_HAVER_explore(self):
            haver.get_databases()
            assert haver.database_info('EPFRBCF')['description'] == 'Bond Country Flows: ETFs/Mutu Fnd: Africa: Est Ending Alloc (EOP, Mil. US$)'
            assert 'A111F9SE' in haver.get_series('USECON')
            haver.get_series('USECON', like='A111F9S', limit=4, full_info=False)
            # haver.search(query='defined')

        def test_HAVER_recessions(self):
            # assert haver.recessions().shape[0] > 300
            pass

        def test_HAVER_read(self):
            assert haver.read(database='EUDATA', series='N997CE')

        def test_HAVER_read_df(self):
            assert haver.read_df(haver_codes=['N997CE@EUDATA']).shape[0] > 100





