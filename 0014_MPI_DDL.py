#!/usr/bin/env python

import datetime

i = 0
fobo = open('/prustaff/x084978/Python/MPI/MPI_DML.SQL', 'w')
fobo.write('\n\n-- IODS DML @ %s\n\n' % datetime.datetime.now())
for f in ['INSERT_IODSMANUAL.T_MASTER_DDA_NO_RANK_INVESTMENT.sql',
          'INSERT_IODSMPI.T_REF_ASSET_CLASS_PEER_XREF.SQL',
          'INSERT_IODSMPI.T_REF_LIPPERCATEGORY_PEER_XREF.SQL',
          'INSERT_IODSMPI.T_REF_LIPPER_CATEGORY.SQL',
          'INSERT_IODSMPI.T_REF_MPI_HEADER_BENCHMARK_PERFORMANCE.SQL',
          'INSERT_IODSMPI.T_REF_MPI_HEADER_INVESTMENT_PERFORMANCE.SQL',
          'INSERT_IODSMPI.T_REF_MPI_STATISTICS_TYPES.SQL',
          'INSERT_IODSMPI.T_REF_MPI_STUDY_TYPES.SQL',
          'INSERT_IODSMPI.T_REF_MSTARCATEGORY_PEER_XREF.SQL',
          'INSERT_IODSMPI.T_REF_PEER_TYPE_.SQL',
          'INSERT_IODSMPI.T_REF_PEER_UNIVERSE.SQL'
         ]:
    fn = '/prustaff/x084978/Python/MPI/DML Scripts/' + f
    i += 1
    print 'Processing %02d: %s' % (i, fn)
    fobi = open(fn, 'r')
    fobo.write('\n-- Begin %02d: %s --\n\n' % (i, fn))
    for eachLine in fobi:
        fobo.write(eachLine)
    fobi.close()    
    fobo.write('\n-- End %02d: %s --\n\n' % (i, fn))
fobo.close()

