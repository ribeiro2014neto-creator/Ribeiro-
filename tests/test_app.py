import unittest,tempfile
from pathlib import Path
import server
class Workflow(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();server.DB=Path(self.tmp.name)/'test.sqlite3'
  with server.connect() as c:
   c.execute('CREATE TABLE lots (id INTEGER PRIMARY KEY,name TEXT,entry TEXT,heads INTEGER,weight REAL)')
   c.execute('CREATE TABLE events (id INTEGER PRIMARY KEY,lot INTEGER,kind TEXT,day TEXT,amount REAL,heads INTEGER,carcass REAL,note TEXT)')
  server.save(dict(kind='lot',name='Nelore',day='2026-01-01',heads=100,amount=350))
 def tearDown(self):self.tmp.cleanup()
 def test_full_cycle_persists(self):
  server.save(dict(kind='feed',lot=1,day='2026-01-02',amount=800))
  server.save(dict(kind='weigh',lot=1,day='2026-01-31',amount=380))
  server.save(dict(kind='slaughter',lot=1,day='2026-03-02',heads=40,amount=16400,carcass=9020))
  server.save(dict(kind='slaughter',lot=1,day='2026-03-12',heads=60,amount=25200,carcass=13860))
  s=server.state();self.assertEqual(len(s['events']),4);self.assertEqual(sum(e['heads'] for e in s['events'] if e['kind']=='slaughter'),100)
 def test_overselling_rejected(self):
  with self.assertRaises(ValueError):server.save(dict(kind='slaughter',lot=1,day='2026-03-01',heads=101,amount=40000,carcass=22000))
 def test_invalid_carcass_rejected(self):
  with self.assertRaises(ValueError):server.save(dict(kind='slaughter',lot=1,day='2026-03-01',heads=10,amount=4000,carcass=5000))
 def test_feed_before_entry_rejected(self):
  with self.assertRaises(ValueError):server.save(dict(kind='feed',lot=1,day='2025-12-31',amount=800))
if __name__=='__main__':unittest.main()
