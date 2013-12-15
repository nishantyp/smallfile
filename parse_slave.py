'''
parse_slave.py -- parses SSH cmd for invocation of smallfile_remote.py
Copyright 2012 -- Ben England
Licensed under the Apache License at http://www.apache.org/licenses/LICENSE-2.0
See Appendix on this page for instructions pertaining to license.
'''

import sys
import os
import time
import pickle
import smallfile
from smallfile import smf_invocation
import smf_test_params

# convert boolean value into 'Y' or 'N'

def usage(msg):  # call if CLI syntax error or invalid parameter
    print('')
    print('ERROR: ' + msg)
    print('usage: smallfile_remote.py [ --network-sync-dir path ] --as-host hostname ')
    sys.exit(1)

# parse command line and return tuple containing:
#   network sync directory
#   host identity of this remote invocation

def parse():

  prm_network_sync_dir = None

  argc = len(sys.argv)
  if argc == 1:
      print('\nfor additional help add the parameter "--help" to the command\n')
  j=1
  while j < argc:
    rawprm = sys.argv[j]
    if rawprm == '-h' or rawprm == '--help':
      usage('normally this process is run automatically by smallfile_cli.py')
    if rawprm[0:2] != '--': usage('parameter names begin with "--"')
    prm = rawprm[2:]
    if (j == argc - 1) and (argc%2 != 1): usage('all parameters consist of a name and a value')
    val = sys.argv[j+1]
    if len(rawprm) < 3: usage('parameter name not long enough' )
    pass_on_prm = rawprm + ' ' + val
    j += 2
    if prm == 'network-sync-dir': prm_network_sync_dir = val
    # --ashost should not be used by end-user
    elif prm == 'as-host': 
        prm_as_host = smallfile.get_hostname(val)
    else: usage('unrecognized parameter name')

  params = None
  param_pickle_fname = os.path.join(prm_network_sync_dir, 'param.pickle')
  if not os.path.exists(param_pickle_fname):
     time.sleep(1.1)
  pickle_fn = os.path.join(prm_network_sync_dir, 'param.pickle')
  #print(pickle_fn)
  with open(pickle_fn, 'rb') as pickled_params:
    params = pickle.load(pickled_params)
  params.is_slave = True
  params.as_host = prm_as_host
  params.master_invoke.onhost = prm_as_host
  return params
