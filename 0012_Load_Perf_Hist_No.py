#!/usr/bin/env python

# +-----------------------------------------------------------------------------------------+
# | U\                                                                           2018-03-12 |
# | Load_Perf_No.py (No - Non Object Oriented Version - Closer to UNIX shell)   Mohan Palat |
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
# |         Load_Perf_No.py 121 | tee Load_Perf_2018-03-12-03-00-PM.log                     |
# |                                                                                         |
# | Modifications:                                                                          |
# |                                                                                         |
# | Who         Date     Change                                                             |
# | ----------- -------- ------------------------------------------------------------------ |
# | Mohan Palat 20180312 Initial Revision                                                   |
# +-----------------------------------------------------------------------------------------+

import os
import datetime

i = 0
tf = 0
ppbin = '/usr/local/dstage/INVODS/batch/PreProcHeaderTrailer '
cybfldr = '/usr/local/dstage/INVODS/cyberf/MARKIT/'
stgfldr = '/usr/local/dstage/INVODS/cyberf/stage/MARKIT/'
wrkfldr = '/usr/local/dstage/INVODS/WorkFiles/'
dsshell = 'sh /usr/local/dstage/INVODS/batch/INVODS_generic.sh '

print '\n\n%s\n%s\n%s\n\n' % ('=' * 26, datetime.datetime.now(), '=' * 26)

l = os.listdir(cybfldr)
l.sort();
for f in l:
    if f.endswith('.zip'):
        i += 1
        if i <= 121:
            #########################################
            #               Init Log                #
            #########################################
            tf = i
            print '=' * (len(f)+5)
            print '%03d. %s' % (i, f)
            print '=' * (len(f)+5)
            #########################################
            #                Unzip                  #
            #########################################
            uzipfil = wrkfldr + f[:-4]
            print 'Unzipped file is', uzipfil
            oscmd = 'unzip -jo ' + cybfldr + f + ' -d ' + wrkfldr
            print oscmd
            result = os.system(oscmd)
            print 'Result for unzip = ', result
            if result != 0:
                print 'Unable to continue'
                break
            #########################################
            #       Collect Tail Rowcount           #
            #########################################
            if i == 1:
                oscmd = 'tail -v -n1 ' + uzipfil + ' > '  + wrkfldr + 'Load_Perf_Tail.log'
            else:
                oscmd = 'tail -v -n1 ' + uzipfil + ' >> ' + wrkfldr + 'Load_Perf_Tail.log'
            result = os.system(oscmd)
            print 'Result for Tail = ', result
            if result != 0:
                print 'Unable to continue'
                break
            oscmd = 'echo >> ' + wrkfldr + 'Load_Perf_Tail.log'
            result = os.system(oscmd)
            #########################################
            #               Strip                   #
            #########################################
            stgfil = stgfldr + f[:-4]
            print 'Staged file is', stgfil
            oscmd = ppbin + ' -i ' + uzipfil + ' -o ' + stgfil + ' -s > /dev/null '
            result = os.system(oscmd)
            print 'Result for Strip = ', result
            if result != 0:
                print 'Unable to continue'
                break
            #########################################
            #         Load Stage DS Job             #
            #########################################
            # dspar1  = ' "INVODS_010100_MARKIT_PERF_NONGIA_STG" '
            # dspar1  = ' "INVODS_010105_MARKIT_PERF_NONGIA_STG_NO_TRUNCATE" '
            dspar1  = ' "MO_INVODS_010105_MARKIT_PERF_NONGIA_STG_NO_TRUNCATE" '
            dspar2 = '"-param jpFileName='
            dspar2 += "'" + f[:-4] + "'" + '"'
            oscmd = dsshell + dspar1 + dspar2
            result = os.system(oscmd)
            print 'Result for DataStage Load Stage = ', result
            # print oscmd
            if result != 0:
                print 'Unable to continue'
                break
            #########################################
            #               Clean up                #
            #########################################
            print "Removing ", uzipfil
            os.remove(uzipfil)
            print "Removing ", stgfil
            os.remove(stgfil)
            print '\n\n%s\n%s\n%s\n\n' % ('=' * 26, datetime.datetime.now(), '=' * 26)

print "\n============ Trailer Records Log =================\n" 
oscmd = 'cat ' + wrkfldr + 'Load_Perf_Tail.log'
result = os.system(oscmd)
print "\n"

try:
    fo = open(wrkfldr + 'Load_Perf_Tail.log', 'r')
    i = 0
    tp = 0
    for eachline in fo:
        i += 1
        if i % 2 == 0:
            tp +=  int(eachline[25:-1])
    fo.close()
    print 'Total Performance Records Received from Markit: %d in %d files' % (tp, tf) 
except IOError, e:
    print 'File Processing Error: ', e

print '\n\n%s\n%s\n%s\n\n' % ('=' * 26, datetime.datetime.now(), '=' * 26)

