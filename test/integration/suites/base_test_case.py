##########################################################################
# $Id: base_test_case.py 8633 2015-07-16 15:47:11Z boverhof $
# Joshua R. Boverhof, LBNL
# See LICENSE.md for copyright notice!
#
#   $Author: boverhof $
#   $Date: 2015-07-16 08:47:11 -0700 (Thu, 16 Jul 2015) $
#   $Rev: 8633 $
#
###########################################################################
import unittest, uuid, urllib.request,urllib.error, os, time, json, tempfile, logging
import configparser as _CP
from turbine.commands import _open_config, _setup_logging
from turbine.commands import turbine_simulation_script as tsim


class Config(object):
    """ Reads test.cfg in working directory, sections 'deployment' and 'credentials'.
    Instance Attributes:
        username
        password
        url
    Properties:
        newt_sessionid
    """
    def __init__(self):
        cp = _CP.ConfigParser(defaults=dict(path=''))
        cp.read('integration_test.cfg')
        sec = 'Authentication'
        if not cp.has_section(sec):
            raise RuntimeError('configuration requires %s section', sec)
        self.username = cp.get(sec,'username')
        self.password = cp.get(sec, 'password')



class BaseIntegrationTestCase(unittest.TestCase):
    config_name = 'integration_test.cfg'
    _module_name = __name__

    def setUp(self):
        """ Open up configuration and setup logging before doing anything.
        """
        self.cp = cp = _open_config(self.config_name)
        _setup_logging(cp)
        self.log = logging.getLogger('%s.%s.%s' %(self._module_name, self.__class__.__name__,self._testMethodName))

    def getOptionAsBoolean(self, option):
        """ Returns option in section with same name as class TestCase
        """
        section = self.__class__.__name__
        return self.cp.getboolean(section, option)

    def getOption(self, option, **kw):
        """ Returns option in section with same name as class TestCase
        """
        section = self.__class__.__name__
        return self.cp.get(section, option, **kw)

    def getOptionAsInt(self, option):
        """ Returns option in section with same name as class TestCase
        """
        section = self.__class__.__name__
        return self.cp.getint(section, option)


class _CreateSimulationTest(BaseIntegrationTestCase):

    simulation_file_resource_name = 'aspenfile'

    @property
    def simulation_name(self):
        return self.getOption("simulation")
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
        log = logging.getLogger('session_test_suite._CreateSimulationTest')
        simulation = self.getOption("simulation")
        log.debug("setUp:   simulation '%s'" %simulation)
        try:
            data = tsim.main_get([simulation, self.config_name], func=None)
        except urllib.error.HTTPError:
            #self.create_test_simulation()
            log.debug("create simulation '%s'" %simulation)
            name = self.simulation_name
            data = tsim.main_create([name, self.application, self.config_name])

        print("DATA: %s", data)
        self.failUnlessEqual(len(data), 4)
        self.failUnlessEqual(type(data), dict)
        self.failUnlessEqual(set(data.keys()), set([u'Application', u'Name', u'StagedInputs', u'Id']))
        uuid.UUID(data['Id'])

        self.update_test_simulation()

        data = tsim.main_get([simulation, self.config_name], func=None)
        self.failUnlessEqual(len(data), 4)
        self.failUnlessEqual(type(data), dict)
        self.failUnlessEqual(set(data.keys()), set([u'Application', u'Name', u'StagedInputs', u'Id']))
        uuid.UUID(data['Id'])

    def update_test_simulation(self):
        """
        """
        config_path = self.simulation_config
        self.failUnless(os.path.isfile(config_path), 'No File "%s"' %config_path)
        backup_path = self.simulation_file
        self.failUnless(os.path.isfile(backup_path))

        name = self.simulation_name
        #data = tsim.main_create([name, self.application, self.config_name])

        #self.failUnlessEqual(type(data), dict)
        #self.failUnlessEqual(len(data), 3, data)

        self.log.debug('PUT sinter config')
        self.failUnless(tsim.main_update(['-r', 'configuration', name, config_path, self.config_name]))

        #d2 = open(config_path).read()
        #self.failUnlessEqual(data, d2, 'sinter config file does not match')

        self.log.debug('PUT Simulation Resource: ' + self.simulation_file_resource_name)
        self.failUnless(tsim.main_update(['-r', self.simulation_file_resource_name, name, backup_path, self.config_name]))

        #self.failUnlessEqual(data, open(backup_path).read(), 'backup file does not match')
