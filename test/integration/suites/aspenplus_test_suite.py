##########################################################################
# $Id: aspenplus_test_suite.py 4744 2014-02-19 18:03:08Z boverhof $
# Joshua R. Boverhof, LBNL
# See LICENSE.md for copyright notice!
# 
#   $Author: boverhof $
#   $Date: 2014-02-19 10:03:08 -0800 (Wed, 19 Feb 2014) $
#   $Rev: 4744 $
#
###########################################################################
import unittest, uuid, urllib.request,urllib.error, os, time, json, tempfile, logging
from base_test_case import BaseIntegrationTestCase,_CreateSimulationTest
from turbine.commands import turbine_session_script as tss
from turbine.commands import turbine_simulation_script as tsim
from turbine.commands import turbine_job_script as tjob
         
                
class SessionMEATest(_CreateSimulationTest):
    """
    MEA AspenPlus Test
    """
    _module_name = 'aspenplus_test_suite'
    def test_PUT_Session(self):
        self.log.debug("start")
        guid = tss.main_create_session([self.config_name], func=None)
        self.failUnlessEqual(type(guid), uuid.UUID)
        self.log.debug("Session GUID: %s" %guid)
        
        jobs_file = self.getOption("jobs_file")
        job_list = tss.main_create_jobs([str(guid), jobs_file, self.config_name], func=None)
        
        data = tss.main_get_results([str(guid), self.config_name], func=None)
        self.assertEqual(len(data), len(job_list))
        
        job_start_list = tss.main_start_jobs(([str(guid), self.config_name]), func=None)
        self.log.debug("Session Started: %s" %data)
        self.assertEqual(len(job_list), job_start_list)
        
        if not self.getOption("poll"):
            return
    
        for state in ('submit', 'locked', 'setup', 'running'):
            self.log.debug('Waiting on state "%s"' %state)
            data1 = tss.main_jobs_status(([str(guid), self.config_name]), func=None)
            while data1[state]>0:
                data2 = tss.main_jobs_status(([str(guid), self.config_name]), func=None)
                self.log.debug("Poll until finished: %s" %data2)
                if data1 == data2:
                    time.sleep(10)
                data1 = data2

            self.assertNotEqual(state, "error")

        
if __name__ == "__main__":
    unittest.main()
