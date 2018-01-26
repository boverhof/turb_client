##########################################################################
# $Id: acm_test_suite.py 4480 2013-12-20 23:20:21Z boverhof $
# Joshua R. Boverhof, LBNL
# See LICENSE.md for copyright notice!
# 
#   $Author: boverhof $
#   $Date: 2013-12-20 15:20:21 -0800 (Fri, 20 Dec 2013) $
#   $Rev: 4480 $
#
###########################################################################
import unittest, uuid, urllib2, os, time, json, tempfile, logging
from base_test_case import _CreateSimulationTest
from turbine.commands import turbine_session_script as tss
from turbine.commands import turbine_simulation_script as tsim
from turbine.commands import turbine_job_script as tjob
         
            
class SessionHybridSplitTest(_CreateSimulationTest):
    """
    Hybrid ACM Test
    """
    _module_name = 'acm_test_suite'
    #_module_name = __module__

    def test_PUT_Session(self):
        self.log.debug("start")
        guid = tss.main_create_session([self.config_name], func=None)
        self.failUnlessEqual(type(guid), uuid.UUID)
        self.log.debug("Session GUID: %s" %guid)
        
        jobs_file = self.getOption("jobs_file")
        jobs_list = tss.main_create_jobs([str(guid), jobs_file, self.config_name], func=None)
        
        data = tss.main_get_results([str(guid), self.config_name], func=None)
        self.assertEqual(map(lambda i: i['Id'],data), jobs_list, "DATA %s   JOBS %s" %(data,jobs_list))
        
        started_num = tss.main_start_jobs(([str(guid), self.config_name]), func=None)

        self.log.debug("Session Started: %d" %started_num)
        self.assertEqual(started_num, len(jobs_list))

        if not self.getOption("poll"):
            return
    
        data = tss.main_jobs_status(([str(guid), self.config_name]), func=None)
        while data["submit"]>0:
            self.log.debug('Waiting For Submit Jobs: "%s"' %data)
            time.sleep(10)
            data = tss.main_jobs_status(([str(guid), self.config_name]), func=None)
    
        # {"pause": 0, "success": 0, "setup": 0, "terminate": 0, "running": 0, "submit": 0, "finished": 0, "error": 0, "cancel": 0, "create": 0}  
        self.assertEqual(data["submit"], 0)
        self.assertEqual(data["success"]+data["setup"]+data["running"], started_num)

        data = tss.main_jobs_status(([str(guid), self.config_name]), func=None)
        while (data["setup"]+data["running"]) > 0:
            self.log.debug('Waiting on setup/running jobs "%s"' %data)
            time.sleep(10)
            data = tss.main_jobs_status(([str(guid), self.config_name]), func=None)
        
        self.assertEqual(data["success"], started_num)

        jobs_list = map(lambda i: i['Id'], tjob.main([self.config_name, '-s', str(guid)], func=None))
        self.assertEqual(len(jobs_list), started_num)

        all_data = []
        for i in jobs_list:
            all_data.append(tjob.main([self.config_name, '-j', str(i), '-v'], func=None))

        self.assertEqual(len(all_data), started_num)

        for d in all_data:
            # ADSA.GasOut.F and ADSA.GasOut.T 
            self.log.debug("Job %s: " %d['Id'])
            self.log.debug("\tInput: ", d['Input'])
            self.log.debug("\tOutput: ")
            for k in ['ADSA.GasOut.F', 'ADSA.GasOut.T']:
                self.log.debug("\t\t%s: " %k, d['Output'][k])

    """
	Input:  {u'UQ_ADS_db': 0.9}
	Output: 
		ADSA.GasOut.F:  {u'units': u'kmol/hr', u'value': 5477.3106106953}
		ADSA.GasOut.T:  {u'units': u'C', u'value': 52.02556595576077}
	Input:  {u'UQ_ADS_db': 0.92}
	Output: 
		ADSA.GasOut.F:  {u'units': u'kmol/hr', u'value': 5481.979260174718}
		ADSA.GasOut.T:  {u'units': u'C', u'value': 51.95110556709135}
	Input:  {u'UQ_ADS_db': 0.94}
	Output: 
		ADSA.GasOut.F:  {u'units': u'kmol/hr', u'value': 5486.7590764515435}
		ADSA.GasOut.T:  {u'units': u'C', u'value': 51.871460258065305}
	Input:  {u'UQ_ADS_db': 0.96}
	Output: 
		ADSA.GasOut.F:  {u'units': u'kmol/hr', u'value': 5491.6481222316115}
		ADSA.GasOut.T:  {u'units': u'C', u'value': 51.78704560404312}
	Input:  {u'UQ_ADS_db': 0.98}
	Output: 
		ADSA.GasOut.F:  {u'units': u'kmol/hr', u'value': 5496.64427389132}
		ADSA.GasOut.T:  {u'units': u'C', u'value': 51.6982620847844}
	Input:  {u'UQ_ADS_db': 1.0}
	Output: 
		ADSA.GasOut.F:  {u'units': u'kmol/hr', u'value': 5501.745392452902}
		ADSA.GasOut.T:  {u'units': u'C', u'value': 51.60548826443257}
	Input:  {u'UQ_ADS_db': 1.02}
	Output: 
		ADSA.GasOut.F:  {u'units': u'kmol/hr', u'value': 5506.949304967232}
		ADSA.GasOut.T:  {u'units': u'C', u'value': 51.50908158996059}
	Input:  {u'UQ_ADS_db': 1.04}
	Output: 
		ADSA.GasOut.F:  {u'units': u'kmol/hr', u'value': 5512.253802290086}
		ADSA.GasOut.T:  {u'units': u'C', u'value': 51.40937885821298}
	Input:  {u'UQ_ADS_db': 1.06}
	Output: 
		ADSA.GasOut.F:  {u'units': u'kmol/hr', u'value': 5517.656636281703}
		ADSA.GasOut.T:  {u'units': u'C', u'value': 51.30669691307642}
	Input:  {u'UQ_ADS_db': 1.08}
	Output: 
		ADSA.GasOut.F:  {u'units': u'kmol/hr', u'value': 5523.155516484687}
		ADSA.GasOut.T:  {u'units': u'C', u'value': 51.20133350326285}
	Input:  {u'UQ_ADS_db': 1.1}
	Output: 
		ADSA.GasOut.F:  {u'units': u'kmol/hr', u'value': 5528.748106385507}
		ADSA.GasOut.T:  {u'units': u'C', u'value': 51.093568244040824}
    """

if __name__ == "__main__":
    unittest.main()
