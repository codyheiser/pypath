# -*- coding: utf-8 -*-
#from ez_setup import use_setuptools
#use_setuptools()
__revision__ = "$Id$"
import sys
import os
from setuptools import setup, find_packages
import glob

_MAJOR = 0
_MINOR = 1
_MICRO = 23
version = '%d.%d.%d' % (_MAJOR, _MINOR, _MICRO)
release = '%d.%d' % (_MAJOR, _MINOR)

def which(exe):
    '''
    Checks if executable is available.
    Source:
    http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
    '''
    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)
    
    def ext_candidates(fpath):
        yield fpath
        for ext in os.environ.get("PATHEXT", "").split(os.pathsep):
            yield fpath + ext
    
    fpath, fname = os.path.split(exe)
    if fpath:
        if is_exe(exe):
            return True
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, exe)
            for candidate in ext_candidates(exe_file):
                if is_exe(candidate):
                    return True
    return False


def query_yes_no(question, default="yes"):
    """
    From http://stackoverflow.com/questions/3041986/python-command-line-yes-no-input
    
    Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)
    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

metainfo = {
    'authors': {
    'Türei':('Dénes Türei','denes@ebi.ac.uk'),
    },
    'version': version,
    'license': 'LGPL',
    'download_url': ['http://157.181.231.40/~denes/bioigraph'],
    'url': ['http://157.181.231.40/~denes/bioigraph'],
    'description': 'Work with molecular networks in Python igraph',
    'platforms': ['Linux', 'Unix', 'MacOSX', 'Windows'],
    'keywords': ['graph', 'network', 'protein', 'mRNA', 'DNA', 'signaling',
                 'SignaLink', 'Signor', 'InnateDB', 'IntAct', 'Reactome',
                 'MPPI', 'NCI-PID', 'DIP', 'MatrixDB', 'PANTHER',
                 'PhosphoSite', 'PhosphoPoint', 'DEPOD', 'SPIKE', 'KEGG',
                 'Autophagy', 'ARN', 'NRF2', 'NRF2ome', 'Guide to Pharmacology', 
                 'regulation',
                 'phosphorylation', 'kinase', 'phosphatase',
                 'dephosphorylation', 'directed graph'],
    'classifiers': [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: GNU Library or Lesser General Public License (LGPL)',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.7',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Scientific/Engineering :: Mathematics']
}

#package_data = [
    #'bioigraph/data/alzpw-ppi.csv', 
    #'bioigraph/data/arn_014.csv', 
    #'bioigraph/data/arn.csv', 
    #'bioigraph/data/arn_lr01.csv', 
    #'bioigraph/data/ca1.csv', 
    #'bioigraph/data/cancer_gene_census.csv', 
    #'bioigraph/data/cell-map-edge-attributes.txt', 
    #'bioigraph/data/dd_refs.csv', 
    #'bioigraph/data/depod-refs.csv', 
    #'bioigraph/data/dip_human_core_processed.csv', 
    #'bioigraph/data/entrez_uniprot.csv', 
    #'bioigraph/data/gdsc.sif', 
    #'bioigraph/data/gold_standard.csv', 
    #'bioigraph/data/gold_standard.xlsx', 
    #'bioigraph/data/innatedb.csv', 
    #'bioigraph/data/intact_filtered.csv', 
    #'bioigraph/data/krishnadev_atg_1.tab', 
    #'bioigraph/data/krishnadev_atg.tab', 
    #'bioigraph/data/krishnadev_vegeredmeny.csv', 
    #'bioigraph/data/kshirsagar_atg_1.tab', 
    #'bioigraph/data/kshirsagar_atg.tab', 
    #'bioigraph/data/kshirsagar_vegeredmeny.csv', 
    #'bioigraph/data/macrophage-strict.csv', 
    #'bioigraph/data/matrixdb_core.csv', 
    #'bioigraph/data/mppi_human_rep.csv', 
    #'bioigraph/data/nci-pid-strict.csv', 
    #'bioigraph/data/netpath_refs.csv', 
    #'bioigraph/data/nrf2ome.csv', 
    #'bioigraph/data/phosphopoint.csv', 
    #'bioigraph/data/phosphosite_human_hc.csv', 
    #'bioigraph/data/phosphosite_human_noref.csv', 
    #'bioigraph/data/salmonella_atg.tar.gz', 
    #'bioigraph/data/sec_ac.txt', 
    #'bioigraph/data/shlecker_atg_1.tab', 
    #'bioigraph/data/shlecker_vegeredmeny.csv', 
    #'bioigraph/data/signor_ppi.tsv', 
    #'bioigraph/data/slk01human.csv', 
    #'bioigraph/data/spike_hc.csv', 
    #'bioigraph/data/swissprot2.csv', 
    #'bioigraph/data/swissprot-gsymbol-name.csv', 
    #'bioigraph/data/trembl2.csv', 
    #'bioigraph/data/uniprot-all-human.tab',
    #'bioigraph/data/intogene_cancerdrivers.tsv'
#]

with open('README.rst') as f:
    readme = f.read()
with open('HISTORY.rst') as f:
    history = f.read()

# choosing module for mysql access:
deps = ['python-igraph', 'pandas', 'bioservices', 'beautifulsoup4', 'pymysql', 
    'pyopenssl', 'ndg-httpsclient', 'chembl_webresource_client', 'pyasn1',
    'twisted']

#mysql = 'pymysql'
#if which('mysql') and which('mysql_config'):
    #mysql_alt = query_yes_no('Looks like MySQL is installed on your system. \n'\
        #'Do you want to use MySQL-python instead of pymysql?')
    #if mysql_alt:
        #mysql = 'MySQL-python'

#deps.append(mysql)

setup(
    name = 'bioigraph',
    version = version,
    maintainer = metainfo['authors']['Türei'][0],
    maintainer_email = metainfo['authors']['Türei'][1],
    author = metainfo['authors']['Türei'][0],
    author_email = metainfo['authors']['Türei'][1],
    long_description = readme + '\n\n' + history,
    keywords = metainfo['keywords'],
    description = metainfo['description'],
    license = metainfo['license'],
    platforms = metainfo['platforms'],
    url = metainfo['url'],
    download_url = metainfo['download_url'],
    classifiers = metainfo['classifiers'],
    # package installation
    package_dir = {'':'src'},
    packages = list(set(find_packages() + ['bioigraph', 'bioigraph.data'])),
    include_package_data = True,
    install_requires = deps
)
