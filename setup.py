##########################################################################
# $Id: setup.py 10252 2016-04-27 21:26:30Z ksb $
# Joshua R. Boverhof, LBNL
# See Copyright for copyright notice!
# 
#   $Author: ksb $
#   $Date: 2016-04-27 14:26:30 -0700 (Wed, 27 Apr 2016) $
#   $Rev: 10252 $
#
###########################################################################
from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup

_url = "https://svn.acceleratecarboncapture.org"
from turbine import __version__

setup(
    name="TurbineClient",
    version=__version__,
    license="See CCSI_TE_LICENSE_turb_client.txt",
    packages=['turbine', 'turbine.commands'],
    description="Turbine Science Gateway Client",
    author="Joshua Boverhof",
    author_email="jrboverhof@lbl.gov",
    maintainer="Joshua Boverhof",
    maintainer_email="jrboverhof@lbl.gov",
    url=_url,
    long_description="For additional information, please see " + _url,
    setup_requires = [],
    dependency_links = [],

    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: End Users/Desktop",
        "License :: See Accompanying license ",
        "Programming Language :: Python",
        "Natural Language :: English",
        "Operating System :: POSIX"
    ],

    scripts = ["scripts/turbine_job_script", 
        "scripts/turbine_application_list", 
        "scripts/turbine_simulation_list", 
        "scripts/turbine_simulation_update", 
        "scripts/turbine_simulation_create", 
        "scripts/turbine_simulation_delete", 
        "scripts/turbine_simulation_get", 
        "scripts/turbine_session_list",
        "scripts/turbine_session_create",
        "scripts/turbine_session_append",
        "scripts/turbine_session_kill",
        "scripts/turbine_session_start",
        "scripts/turbine_session_stop",
        "scripts/turbine_session_status",
        "scripts/turbine_session_stats",
        "scripts/turbine_session_get_results",
        "scripts/turbine_session_delete",
        "scripts/turbine_session_graphs",
        "scripts/turbine_consumer_log",
        "scripts/turbine_consumer_list"
    ],
    install_requires=[
        "python-dateutil >= 1.5",
        "python-ntlm >= 1.0.1",
    ],
    extras_require={ 
        "graphs":["rpy2",], 
    },

    # sdist
    exclude_package_data = { '': ['tools'] },
)
