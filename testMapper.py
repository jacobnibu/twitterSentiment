#!/usr/bin/env python
import sys, happybase, socket

connection = happybase.Connection('localhost')
table = connection.table('tweets')
#machine_name = socket.gethostname()

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    words = line.split()
    # increase counters
    for index, word in enumerate(words):
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py
        #
        # tab-delimited; the trivial word count is 1
        print '%s\t%s' % (word, 1)
#	index +=1
#	table.put(machine_name+str(index), {'cf1:': word})
