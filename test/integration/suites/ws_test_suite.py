##########################################################################
# $Id: ws_test_suite.py 8633 2015-07-16 15:47:11Z boverhof $
# Joshua R. Boverhof, LBNL
# See Copyright for copyright notice!
# 
#   $Author: boverhof $
#   $Date: 2015-07-16 08:47:11 -0700 (Thu, 16 Jul 2015) $
#   $Rev: 8633 $
#
###########################################################################
import unittest
import uuid
from base_test_case import BaseIntegrationTestCase
from turbine.commands import turbine_consumer_script as tcs
from turbine.commands import turbine_simulation_script as tss
from turbine.commands import turbine_application_script as tas


class ConsumerReadTest(BaseIntegrationTestCase):

    def test_GET_List(self):
        data = tcs.main([self.config_name], func=None)
        self.log.debug('data:  %s' %data)
        #l = map(lambda i: i['Id'], data)
        #self.log.debug('consumers:  %d' %len(l))
        self.log.debug('consumers:  %d' %len(data))
        for d in data:
            #self.failUnlessEqual(d.keys(), 
            #     ['AMI', 'status', 'processID', 'instanceID', 'hostname', 'Id']
            #     )
            u = uuid.UUID(str(d))
            

class SimulationReadTest(BaseIntegrationTestCase):

    def test_GET_List(self):
        simulation_list = tss.main_list([self.config_name], func=None)
        simulation_names = map(lambda i: i['Name'], simulation_list)
        self.log.debug('simulation names %s' %simulation_names)
        self.failUnless(set([]).issubset(simulation_names), 
                        '%s not superset' %simulation_names)
    

class SessionReadTest(BaseIntegrationTestCase):

    def test_GET_List(self):
        l = tss.main_list([self.config_name], func=None)
        self.log.debug('simulation names %s' %l)
        self.failUnless(type(l) is list,'return type should be list')

                
class ApplicationReadTest(BaseIntegrationTestCase):

    def test_GET_List(self):
        l = tas.main_list([self.config_name], func=None)
        self.log.debug('Application names %s' %l)
        self.failUnless(type(l) is list,'return type should be list')


if __name__ == "__main__":
    unittest.main()
