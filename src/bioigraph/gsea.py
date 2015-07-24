#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#
#  This file is part of the `bioigraph` python module
#
#  Copyright (c) 2014-2015 - EMBL-EBI
#
#  File author(s): Dénes Türei (denes@ebi.ac.uk)
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  Website: http://www.ebi.ac.uk/~denes
#

import re
import bs4
import sys
from collections import OrderedDict

# from this module:
import dataio
import data_formats
import enrich
import mapping
import progress
from common import *

class GSEA(object):
    
    def __init__(self, user = 'denes@ebi.ac.uk', mapper = None):
        self.user = user
        self.login()
        self.mapper = mapper if mapper is not None else mapping.Mapper()
        self.info = {}
        self.groups = {}
        self.sets = {}
        self.collections = {}
        self.list_collections()
        self.ids = {
            'entrez': 'entrez',
            'symbol': 'genesymbol'
        }
        self.target_id = 'uniprot'
    
    def login(self):
        url = data_formats.urls['msigdb']['login1']
        self.pre_session = dataio.curl(url, init_url = url, 
            silent = False, cache = False, init_headers = True)
        url = data_formats.urls['msigdb']['login2']
        post = {'j_username': self.user, 'j_password': 'password'}
        self.session = dataio.curl(url, init_url = url, post = post, 
            req_headers = self.pre_session, 
            silent = False, cache = False, init_headers = True)
    
    def list_collections(self):
        renm = re.compile(r'(.+)\([^0-9]*([0-9]*)[^0-9]*\)')
        url = data_formats.urls['msigdb']['coll']
        html = dataio.curl(url, req_headers = self.session, silent = False)
        soup = bs4.BeautifulSoup(html)
        for col in soup.find('table', class_ = 'lists1').find_all('tr'):
            lname, num = renm.findall(col.find('th').text.replace('\n', ''))[0]
            sname = col.find('a').attrs['name']
            urls = dict([(d.attrs['href'].split('.')[-2], 
                data_formats.urls['msigdb']['url_stem'] % d.attrs['href']) \
                for d in col.find_all('a')[-3:]])
            self.collections[sname] = {'name': lname, 'count': int(num), 'urls': urls}
    
    def show_collections(self):
        s = '\n :: Available gene set collections:\n\n'\
            + '\tID\t\t\t#genes\tDescription\n\t%s\n\t'%('-'*75) \
            + '\n\t'.join('%s\t\t\t%u\t%s'%(sname, inf['count'], inf['name']) \
                for sname, inf in self.collections.iteritems()) \
            + '\n'
        sys.stdout.write(s)
        sys.stdout.flush()
    
    def load_collection(self, collname, id_type = 'entrez', map_ids = True):
        url = self.collections[collname]['urls'][id_type]
        data = dataio.curl(url, req_headers = self.session, silent = False, 
            cache = False, write_cache = True)
        data = data.split('\n')
        names = []
        prg = progress.Progress(len(data), 'Loading gene sets', 1)
        for line in (l.split('\t') for l in data if len(l) > 0):
            prg.step()
            setname = line[0].strip()
            self.write_set(line[2:], setname, id_type, map_ids)
            self.get_desc(setname)
            names.append((setname, self.info[setname]))
        prg.terminate()
        self.groups[collname] = names
    
    def get_desc(self, setname):
        url = data_formats.urls['msigdb']['one_set'] % setname
        txt = dataio.curl(url, req_headers = self.session, silent = True)
        self.info[setname] = txt.split('\n')[1][2:]
    
    def load_set(self, setname, map_ids = True):
        url = data_formats.urls['msigdb']['one_set'] % setname
        data = dataio.curl(url, req_headers = self.session, silent = True)
        data = data.split('\n')
        self.info[setname] = data[1][2:]
        self.write_set((j for j in (i.strip() for i in data[2:]) if len(j) > 0), 
            setname, 'symbol', map_ids)
    
    def write_set(self, id_list, setname, id_type, map_ids = True):
        self.sets[setname] = set(uniqList(flatList( \
            self.mapper.map_name(n, self.ids[id_type], self.target_id) \
                for n in id_list))) if map_ids \
            else set(id_list)

class GSEABinaryEnrichmentSet(enrich.EnrichmentSet):
    
    def __init__(self, basic_set, gsea = None, geneset_ids = None, 
        alpha = 0.05, correction_method = 'hommel', gsea_user = 'denes@ebi.ac.uk'):
        if type(gsea) is not GSEA and geneset_ids is None:
            console('Please give either a `bioigraph.gsea.GSEA` object'\
                'or a list of geneset names.')
        if geneset_ids is None: geneset_ids = gsea.sets.keys()
        if type(gsea) is not GSEA: 
            gsea = GSEA(user = gsea_user)
            for geneset_id in geneset_ids:
                gsea.load_set(geneset_id)
        self.geneset_ids = geneset_ids
        self.gsea = gsea
        self.alpha = alpha
        self.correction_method = correction_method
        self.basic_set = set(basic_set)
        self.counts_pop = self.count(self.basic_set)
        self.pop_size = len(self.basic_set)
        self.set_size = None
        self.counts_set = None
    
    def count(self, this_set):
        return dict((i, len(this_set & s)) \
            for i, s in self.gsea.sets.iteritems())
    
    def new_set(self, set_names):
        if type(set_names) is not set: set_names = set(set_names)
        self.set_size = len(set_names)
        self.counts_set = self.count(set_names)
        self.calculate()
        
    def calculate(self):
        data = dict([(gset_id, (cnt, self.counts_pop[gset_id], self.set_size, \
            self.gsea.info[gset_id])) for gset_id, cnt in self.counts_set.iteritems()])
        enrich.EnrichmentSet.__init__(self, data, self.pop_size, alpha = self.alpha, 
            correction_method = self.correction_method)
    
    def top_genesets(self, length = None, significant = True):
        return [t.data[0] for t in \
            self.toplist(length = length, significant = significant).values()]
    
    def top_geneset_ids(self, length = None, significant = True):
        return self.toplist(length = length, significant = significant).keys()
    
    def __str__(self):
        if self.counts_set is None:
            resp = '\n\t:: No calculations performed yet. Please define '\
                'a set of genes with `new_set()`.\n\n'
        else:
            resp = '\n :: Top significantly enriched genesets (max. 10):\n\n\t'\
                + '\n\t'.join([t[0].upper() + t[1:] for t in \
                self.top_genesets(length = 10, significant = True)]) + '\n'
        return resp