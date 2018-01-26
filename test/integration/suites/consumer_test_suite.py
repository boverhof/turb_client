##########################################################################
# $Id: consumer_test_suite.py 4480 2013-12-20 23:20:21Z boverhof $
# Joshua R. Boverhof, LBNL
# See LICENSE.md for copyright notice!
# 
#   $Author: boverhof $
#   $Date: 2013-12-20 15:20:21 -0800 (Fri, 20 Dec 2013) $
#   $Rev: 4480 $
#
###########################################################################
import unittest
from base_test_case import BaseIntegrationTestCase
from turbine.commands import turbine_consumer_script as tcs

class ConsumerTest(BaseIntegrationTestCase):

    def test_GET_Consumers(self):
        data = tcs.main([self.config_name], func=None)
        l = map(lambda i: i['guid'], data)
        self.log.debug('consumers:  %d' %len(l))
        for d in data:
            self.failUnlessEqual(d.keys(), 
                 ['AMI', 'instanceID', 'guid', 'status', 'hostname']
                 )

    def test_GET_Consumer_Config(self):
        data = tcs.main_get_config([self.config_name], func=None)    
        self.failUnless(int(data) >= 0)   
        
    def test_GET_Consumer(self):
        guid = self.getOption('guid')
        self.log.debug('consumer:  %s' %guid)
        data = tcs.main_get_consumer_by_guid([guid, self.config_name], func=None)
        self.failUnlessEqual(data.keys(), ['AMI', 'instanceID', 'guid', 'status', 'hostname'])        
        self.failUnlessEqual(data['guid'], guid)
        
    def test_GET_Consumer_By_GUID(self):
        guid = self.getOption('guid')
        self.log.debug('consumer:  %s' %guid)
        data = tcs.main_get_consumer_by_guid([guid, self.config_name], func=None)
        self.failUnlessEqual(data.keys(), ['AMI', 'instanceID', 'guid', 'status', 'hostname'])        
        self.failUnlessEqual(data['guid'], guid)         
        
    def test_GET_Consumer_Log(self):
        guid = self.getOption('guid')
        self.log.debug('consumer:  %s' %guid)
        content = tcs.main_log([guid, self.config_name], func=None)     
        self.failUnlessEqual(len(content), self.getOptionAsInt('log_length'))         

                
if __name__ == "__main__":
    unittest.main()
