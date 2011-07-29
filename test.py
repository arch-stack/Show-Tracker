#!/usr/bin/python2.6

import unittest
import exceptions
import datetime
import tempfile
import os
import shutil

from src.dataclasses import show, season, episode
from src.storage import storage
from src.settings import settings

class dataclasses_datastructures(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_show(self):
        obj = show(u'a', u'b', u'c', u'd', 1)
        self.assertEqual(obj.name, u'a', 'name is assigned incorrectly')
        self.assertEqual(obj.description, u'b', 'description is assigned incorrectly')
        self.assertEqual(obj.image, u'c', 'image is assigned incorrectly')
        self.assertEqual(obj.id, u'd', 'id is assigned incorrectly')
        self.assertEqual(obj.data, 1, 'data is assigned incorrectly')
        
        self.assertRaises(exceptions.TypeError, show, (1, 1, 1, 1))
    
    def test_season(self):
        obj = season(u'a', u'b', 1, u'c', u'd', 2)
        self.assertEqual(obj.description, u'a', 'description is assigned incorrectly')
        self.assertEqual(obj.image, u'b', 'image is assigned incorrectly')
        self.assertEqual(obj.number, 1, 'number is assigned incorrectly')
        self.assertEqual(obj.id, u'c', 'id is assigned incorrectly')
        self.assertEqual(obj.showid, u'd', 'showid is assigned incorrectly')
        self.assertEqual(obj.data, 2, 'data is assigned incorrectly')
        
        self.assertRaises(exceptions.TypeError, season, (1, 1, '', 1, 1))
    
    def test_episode(self):
        obj = episode(u'a', u'b', 1, datetime.datetime(2000, 1, 1), u'c', u'd', u'e', True, 2)
        self.assertEqual(obj.name, u'a', 'name is assigned incorrectly')
        self.assertEqual(obj.description, u'b', 'description is assigned incorrectly')
        self.assertEqual(obj.number, 1, 'number is assigned incorrectly')
        self.assertEqual(obj.date, datetime.datetime(2000, 1, 1), 'date is assigned incorrectly')
        self.assertEqual(obj.id, u'c', 'id is assigned incorrectly')
        self.assertEqual(obj.showid, u'd', 'showid is assigned incorrectly')
        self.assertEqual(obj.seasonid, u'e', 'seasonid is assigned incorrectly')
        self.assertTrue(obj.watched, 'watched is assigned incorrectly')
        self.assertEqual(obj.data, 2, 'data is assigned incorrectly')
        
        self.assertRaises(exceptions.TypeError, episode, (1, 1, '', '', 1, 1, 1, 1, ''))
    
class storage_test(unittest.TestCase):
    def setUp(self):
        self.temppath = tempfile.mkdtemp()
    
    def tearDown(self):
        if os.path.exists(self.temppath):
            shutil.rmtree(self.temppath, True)
            
    def test_exists(self):
        obj = storage(self.temppath)
        obj.savedata('testex', '123')
        self.assertTrue(obj.exists('testex'), 'Object should exist')
        self.assertFalse(obj.exists('testnoex'), 'Object shouldn\'t exist')
    
    def test_saveload(self):
        obj = storage(self.temppath)
        obj.savedata('test', '123')
        self.assertEqual(obj.getdata('test'), '123', 'Data not loaded correctly')

class settings_test(unittest.TestCase):
    def setUp(self):
        self.obj = settings()
        
    def tearDown(self):
        pass
        
    def test_default(self):
        self.assertTrue(self.obj.get('test', 'testdef', bool, True))
        
    def test_conversion(self):
        self.obj.set('test', 'testconv', 1)
        self.assertTrue(self.obj.get('test', 'testconv', bool))
        
    def test_get(self):
        self.obj.set('test', 'test1', True)
        self.assertFalse(self.assertRaises(exceptions.TypeError, self.obj.get('test', 'test1', bool)))
        self.assertTrue(self.obj.get('test', 'test1', bool), 'Setting not loaded correctly')
    
    def test_remove(self):
        self.obj.set('test', 'testrem', 1)
        self.obj.remove('test', 'testrem')
        self.assertNotEqual(self.obj.get('test', 'testrem', int, 2), 1)
        
                    
if __name__ == "__main__":
    suite = unittest.TestSuite([ 
        unittest.TestLoader().loadTestsFromTestCase(dataclasses_datastructures),
        unittest.TestLoader().loadTestsFromTestCase(storage_test),
        unittest.TestLoader().loadTestsFromTestCase(settings_test)
    ])
    unittest.TextTestRunner(verbosity = 2).run(suite)