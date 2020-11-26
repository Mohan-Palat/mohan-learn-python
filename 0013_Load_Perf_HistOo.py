#!/usr/bin/env python

# +-----------------------------------------------------------------------------------------+
# | U\                                                                           2018-03-12 |
# | Load_Perf_Oo.py (Oo - Object Oriented Version - Closer to C++)              Mohan Palat |
# |                                                                                         |
# | Purpose:                                                                                |
# | Markit provided 121 Performance text files, with header and trailer, zipped.            |
# | We need to a) Unzip b) strip header/trailer c) load each file into stage                |
# | Once all 121 files are loaded into the stage table, the regular stage to core DataStage |
# | process is executed to load data from all 121 files into the core table                 |
# | This Python program does the following                                                  |
# |     1. Truncate the stage table                                                         |
# |     2. Foreach Zip from the Cyberfusion Folder                                          |
# |            Unzip                                                                        |
# |            Remove header trailer (Collect the footer record count to reconcile at end)  |
# |            Load into stage table                                                        |
# |            Remove the large intermediate files created                                  |
# |     3. Total up the footer record counts for reconciling with the loaded rec count      |
# | For every command executed, throws an exception if the command did not work.            |
# |                                                                                         |
# | Parameter:                                                                              |
# |     A number N which controls the number of files out of all the files located          |
# |     Defaults to 1. If you pass a higher number, it does not try beyond the files found  |
# |                                                                                         |
# | Log:                                                                                    |
# |     Writes to stdout, Use thusly to write into a log file                               |
# |         Load_Perf_Oo.py 121 | tee Load_Perf_2018-03-12-03-00-PM.log                     |
# |                                                                                         |
# | Modifications:                                                                          |
# |                                                                                         |
# | Who         Date     Change                                                             |
# | ----------- -------- ------------------------------------------------------------------ |
# | Mohan Palat 20180312 Initial Revision                                                   |
# +-----------------------------------------------------------------------------------------+

import sys
import datetime
import os

class LoadPerformance(object):
    """ Class to load a Performance Zip File From Markit into IODS """

    ppbin = '/usr/local/dstage/INVODS/batch/PreProcHeaderTrailer '
    cybfldr = '/usr/local/dstage/INVODS/cyberf/MARKIT/'
    stgfldr = '/usr/local/dstage/INVODS/cyberf/stage/MARKIT/'
    wrkfldr = '/usr/local/dstage/INVODS/WorkFiles/'
    dsshell = 'sh /usr/local/dstage/INVODS/batch/INVODS_generic.sh '
    dbprop = '/usr/local/dstage/INVODS/batch/IODSDB.prop'
    stgtbl = ' MOHAN.T_STAGE_PERFORMANCE_HISTORY '

    def __init__(self, numzips=1):
        """ Initialize with Number of Zips from available list for the object """
        print '\n\n<INI>\n%s\n%s\n%s\n\n' % ('=' * 26, datetime.datetime.now(), '=' * 26)
        self.numzips = numzips
        print "Number of Performance zip files to be preocessed %d" % self.numzips
        self.i = 0
        self.tf = 0
        sys.stdout.flush()
        self.truncate_stage_table()

    def truncate_stage_table(self):
        """ Truncate Stage Table before loading the Markit Files """
        self.dbdict = { 'init': 'dummy' }
        try:
            fo = open(self.dbprop, 'r')
            for eachline in fo:
                if eachline.find("\n") == -1:
                    self.dbdict[ eachline.split('=')[0] ] = eachline.split('=')[1]
                else:            
                    self.dbdict[ eachline.split('=')[0] ] = eachline.split('=')[1][:-1]
            fo.close()
        except IOError, e:
            print 'File Processing Error with DB Control: ', e, '\n\n'
            sys.stdout.flush()
            sys.exit(1)
        # print self.dbdict
        # 1/3 Connect
        self.oscmd = 'db2 connect to ' + self.dbdict['DB_NAME'] + ' user ' + self.dbdict['DB_ID'] + ' using ' + self.dbdict['DB_PSWD']
        # print self.oscmd
        self.result = os.system(self.oscmd)
        print 'Result for db2 connect = ', self.result
        self.res = self.result != 0
        if self.res: # Failure
            print 'Unable to continue'
            sys.exit(1)
        # 2/3 Execute SQL
        self.oscmd = ' db2 TRUNCATE ' + self.stgtbl + ' REUSE STORAGE IMMEDIATE '
        # print self.oscmd
        self.result = os.system(self.oscmd)
        print 'Result for db2 truncate stage = ', self.result
        self.res = self.result != 0
        if self.res: # Failure
            print 'Unable to continue'
            sys.exit(1)
        # 3/3 Terminate
        self.oscmd = ' db2 terminate '
        # print self.oscmd
        self.result = os.system(self.oscmd)
        print 'Result for db2 terminate = ', self.result
        sys.stdout.flush()
        self.res = self.result != 0
        if self.res: # Failure
            print 'Unable to continue'
            sys.exit(1)
        
        return self.res

    def reinit(self):
        """ Reinitialize method for each file processed """
        self.tf = self.i
        print '=' * (len(self.f)+5)
        print '%03d. %s' % (self.i, self.f)
        print '=' * (len(self.f)+5)
        sys.stdout.flush()

    def unzip(self):
        """ Unzip a zip file """
        self.uzipfil = self.wrkfldr + self.f[:-4]
        print 'Unzipped file is', self.uzipfil
        self.oscmd = 'unzip -jo ' + self.cybfldr + self.f + ' -d ' + self.wrkfldr
        print self.oscmd
        self.result = os.system(self.oscmd)
        print 'Result for unzip = ', self.result
        sys.stdout.flush()
        self.res = self.result != 0
        if self.res: # Failure
            print 'Unable to continue'
        return self.res

    def collect_tail(self):
        """ Collect the record count from trailer record """
        if self.i == 1:
            self.oscmd = 'tail -v -n1 ' + self.uzipfil + ' > '  + self.wrkfldr + 'Load_Perf_Tail.log'
        else:
            self.oscmd = 'tail -v -n1 ' + self.uzipfil + ' >> ' + self.wrkfldr + 'Load_Perf_Tail.log'
        self.result = os.system(self.oscmd)
        print 'Result for Tail = ', self.result
        sys.stdout.flush()
        self.res = self.result != 0
        if self.res: # Failure
            print 'Unable to continue'
            return self.res
        self.oscmd = 'echo >> ' + self.wrkfldr + 'Load_Perf_Tail.log'
        self.result = os.system(self.oscmd)
        print 'Result for >> Load_Perf_Tail.log', self.result
        sys.stdout.flush()
        self.res = self.result != 0
        if self.res: # Failure
            print 'Unable to continue'
        return self.res

    def strip_ht(self):
        """ Strip Header and Trailer """
        self.stgfil = self.stgfldr + self.f[:-4]
        print 'Staged file is', self.stgfil
        self.oscmd = self.ppbin + ' -i ' + self.uzipfil + ' -o ' + self.stgfil + ' -s > /dev/null '
        result = os.system(self.oscmd)
        print 'Result for Strip HT = ', self.result
        sys.stdout.flush()
        self.res = self.result != 0
        if self.res: # Failure
            print 'Unable to continue'
        return self.res

    def call_datastage_job(self):
        """ Call DataStage Job to Load the Performance Stage Table """
        # self.dspar1  = ' "INVODS_010100_MARKIT_PERF_NONGIA_STG" '
        # self.dspar1  = ' "INVODS_010105_MARKIT_PERF_NONGIA_STG_NO_TRUNCATE" '
        self.dspar1  = ' "MO_INVODS_010105_MARKIT_PERF_NONGIA_STG_NO_TRUNCATE" '
        self.dspar2 = '"-param jpFileName='
        self.dspar2 += "'" + self.f[:-4] + "'" + '"'
        self.oscmd = self.dsshell + self.dspar1 + self.dspar2
        self.result = os.system(self.oscmd)
        print 'Result for DataStage Load Stage = ', self.result
        # print oscmd
        sys.stdout.flush()
        self.res = self.result != 0
        if self.res: # Failure
            print 'Unable to continue'
        sys.stdout.flush()
        return self.res

    def cleanup(self):
        """ Remove staged and unzipped file before working with next zip file """
        print "Removing ", self.uzipfil
        os.remove(self.uzipfil)
        print "Removing ", self.stgfil
        os.remove(self.stgfil)
        print '\n%s\n%s\n%s\n' % ('=' * 26, datetime.datetime.now(), '=' * 26)
        sys.stdout.flush()

    def reconcile_reccount(self):
        """ Add record counts from collected trailer record to verify that all got loaded """
        # from ibm_db import connect
        print "\n============ Trailer Records Log =================\n" 
        sys.stdout.flush()
        oscmd = 'cat ' + self.wrkfldr + 'Load_Perf_Tail.log'
        result = os.system(oscmd)
        print "\n"
        sys.stdout.flush()
        try:
            fo = open(self.wrkfldr + 'Load_Perf_Tail.log', 'r')
            i = 0
            tp = 0
            for eachline in fo:
                i += 1
                if i % 2 == 0:
                    tp +=  int(eachline[25:-1])
            fo.close()
            print 'Total Performance Records Received from Markit: %d in %d files' % (tp, self.tf) 
            sys.stdout.flush()
        except IOError, e:
            print 'File Processing Error: ', e

    def Go(self):
        """ Loop through each Zip file and process them """
        l = os.listdir(self.cybfldr)
        l.sort();
        for self.f in l:
            if self.f.endswith('.zip'):
                self.i += 1
                if self.i <= self.numzips:
                    self.reinit()
                    if self.unzip():
                        break
                    if self.collect_tail():
                        break
                    if self.strip_ht():
                        break
                    if self.call_datastage_job():
                        break
                    self.cleanup()
        self.reconcile_reccount()

def main():
    """ Main (From my beloved C++) """
    if len(sys.argv) > 1: 
        lp = LoadPerformance(int(sys.argv[1]))
    else:
        lp = LoadPerformance()
    print '\n\n<BOP>\n%s\n%s\n%s\n\n' % ('=' * 26, datetime.datetime.now(), '=' * 26)
    lp.Go()
    print '\n\n<EOP>\n%s\n%s\n%s\n\n' % ('=' * 26, datetime.datetime.now(), '=' * 26)
    sys.exit(0)

main()


