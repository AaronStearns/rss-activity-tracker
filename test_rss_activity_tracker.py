import unittest 
#import rss_activity_tracker
  
x = {}
class TestScript(unittest.TestCase): 
  
  def test_add(self):
    self.assertIs(x, dict())
  
if __name__ == '__main__': 
    unittest.main() 