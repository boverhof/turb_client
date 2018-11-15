##########################################################################
# $Id: excel_test_suite.py 4711 2014-02-12 23:31:24Z boverhof $
# Joshua R. Boverhof, LBNL
# See LICENSE.md for copyright notice!
# 
#   $Author: boverhof $
#   $Date: 2014-02-12 15:31:24 -0800 (Wed, 12 Feb 2014) $
#   $Rev: 4711 $
#
###########################################################################
import unittest, uuid, urllib3, os, time, json, tempfile, logging
from base_test_case import _CreateSimulationTest
from turbine.commands import turbine_session_script as tss
from turbine.commands import turbine_simulation_script as tsim
from turbine.commands import turbine_job_script as tjob
         
                
#class SessionExcelTest(_CreateSimulationTest):
class OptimizationExcelTest(_CreateSimulationTest):
    """
    Excel Session Test
    """
    _module_name = "excel_test_suite"
    simulation_file_resource_name = 'spreadsheet'

    def test_PUT_Session(self):
        guid = tss.main_create_session([self.config_name], func=None)
        self.failUnlessEqual(type(guid), uuid.UUID)
        print "ZZZ"*20
        self.log.debug("Session GUID: %s" %guid)

        jobs_file = self.getOption("jobs_file")
        d = json.load(open(jobs_file))
        count = len(d)

        job_id_list = tss.main_create_jobs([str(guid), jobs_file, self.config_name], func=None)
        self.assertEqual(len(job_id_list), count)
        
        data = tss.main_get_results([str(guid), self.config_name], func=None)
        self.assertEqual(len(data), count)
        
        num = tss.main_start_jobs(([str(guid), self.config_name]), func=None)
        self.log.debug("Session Started: %d" %num)
        self.assertEqual(num, count)
        
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
                
        data = tss.main_get_results([str(guid), self.config_name], func=None)
        self.assertEqual(len(data), 1)
        data = data[0]
        self.assertEqual(data["State"], "success")
        self.assertEqual(data["Status"], 0)
        simulation = self.getOption("simulation")
        self.assertEqual(data["Simulation"], simulation)
        self.assertEqual(data["Initialize"], False)
        self.assertTrue(data["Output"].has_key('B49'))
        self.assertTrue(type(data["Output"]['B49']), dict)
        self.assertEqual(data["Output"]['B49']['value'], 126.08761416126971)


if __name__ == "__main__":
    unittest.main()
