##########################################################################
# $Id: simulation_test_suite.py 4480 2013-12-20 23:20:21Z boverhof $
# Joshua R. Boverhof, LBNL
# See LICENSE.md for copyright notice!
#
#   $Author: boverhof $
#   $Date: 2013-12-20 15:20:21 -0800 (Fri, 20 Dec 2013) $
#   $Rev: 4480 $
#
###########################################################################
import unittest, uuid, urllib.request,urllib.error
import os, time, json, tempfile, logging
from base_test_case import BaseIntegrationTestCase
from turbine.commands import turbine_simulation_script as tsim
from turbine.commands import turbine_job_script as tjob

#class SimulationReadTest(BaseIntegrationTestCase):
#
#    def test_GET_List(self):
#        simulation_list = tss.main_list([self.config_name], func=None)
#        simulation_names = map(lambda i: i['Name'], simulation_list)
#        self.log.debug('simulation names %s' %simulation_names)
#        self.failUnless(set([]).issubset(simulation_names),
#                        '%s not superset' %simulation_names)


class SimulationWriteTest(BaseIntegrationTestCase):

    _module_name = 'simulation_test_suite'
    _sim_name = 'test-%s' %(uuid.uuid4())

    @property
    def simulation_name(self):
        #if getattr(self, '_sim_name', None) is None:
        #    self._sim_name = 'test-%s' %(uuid.uuid4())
        return self._sim_name

    @property
    def simulation_config(self):
        return self.getOption("simulation_config")

    @property
    def application(self):
        return self.getOption("application")

    @property
    def simulation_file(self):
        return self.getOption("simulation_file")

    def setUp(self):
        BaseIntegrationTestCase.setUp(self)
        #log = logging.getLogger('SimulationWriteTest')
        #simulation = self.getOption("simulation")
        #log.debug("setUp:   simulation '%s'" %simulation)

        #try:
        #    data = tsim.main_get([simulation, self.config_name], func=None)
        #except urllib.error.HTTPError:
        #    self.create_test_simulation()
        #    data = tsim.main_get([simulation, self.config_name], func=None)

        #self.failUnlessEqual(len(data), 3)
        #self.failUnlessEqual(type(data), dict)

    def test_create_simulation(self):
        """ NOTE:
        """
        config_path = self.simulation_config
        self.failUnless(os.path.isfile(config_path), 'No File "%s"' %config_path)
        #defaults_path = self.simulation_defaults
        #self.failUnless(os.path.isfile(defaults_path))
        app_path = self.simulation_file
        self.failUnless(os.path.isfile(app_path))

        name = self.simulation_name
        data = tsim.main_create([name, self.application, self.config_name])

        self.failUnlessEqual(type(data), dict)
        self.failUnlessEqual(len(data), 4, data)

        self.log.debug('PUT sinter config')
        self.failUnless(tsim.main_update(['-r', 'configuration', name, config_path, self.config_name]))

        self.log.debug('PUT Application file')
        self.failUnless(tsim.main_update(['-r', 'aspenfile', name, app_path, self.config_name]))

        data = tsim.main_get([name, self.config_name], func=None)
        self.failUnlessEqual(len(data), 4)
        self.failUnlessEqual(type(data), dict)

        data = tsim.main_get(['-r', 'configuration', name, self.config_name], func=None)
        with open(config_path, encoding='utf-8') as fd:
            self.failUnlessEqual(data, fd.read(), 'sinter config file does not match')

        data = tsim.main_get(['-r', 'aspenfile', name, self.config_name], func=None)
        # NOTE: disable universal newlines handling on Python 3 newline=''
        with open(app_path, encoding='latin-1', newline='') as fd:
            fdata = fd.read()
            self.failUnlessEqual(len(data), len(fdata), 'length aspenfile does not match')
            self.failUnlessEqual(data, fdata, 'aspenfile does not match')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
