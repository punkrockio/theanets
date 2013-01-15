#!/usr/bin/env python

import cPickle
import gzip
import logging
import os
import sys
import tempfile
import urllib

import lmj.tnn

logging.basicConfig(
    stream=sys.stdout,
    format='%(levelname).1s %(asctime)s %(message)s',
    level=logging.INFO)

URL = 'http://www.iro.umontreal.ca/~lisa/deep/data/mnist/mnist.pkl.gz'
DATASET = os.path.join(tempfile.gettempdir(), 'mnist.pkl.gz')

if not os.path.isfile(DATASET):
    logging.info('downloading mnist digit dataset from %s' % URL)
    urllib.urlretrieve(URL, DATASET)
    logging.info('saved mnist digits to %s' % DATASET)

class Main(lmj.tnn.Main):
    def get_network(self):
        return lmj.tnn.Classifier

    def get_datasets(self):
        return [(x, y.astype('int32')) for x, y in cPickle.load(gzip.open(DATASET))]

m = Main()
path = os.path.join(tempfile.gettempdir(), 'mnist-classifier-%s.pkl.gz' % m.opts.layers)
if os.path.exists(path):
    m.net.load(path)
m.train()
m.net.save(path)
