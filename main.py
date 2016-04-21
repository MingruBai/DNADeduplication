import sys
import os
from access_range import access_range
from access_single import access_single

#Target chromosome from user:
chr = sys.argv[1];

#Target access point from user:
#If range acces:
if ':' in sys.argv[2]:
	start = int(sys.argv[2].split(':')[0]);
	end = int(sys.argv[2].split(':')[1]);
	if end > start:
		access_range(chr, start, end);

		#For testing:
		# for target in range(start, end+1):
		# 	access_single(chr, target);
		# print ""
		
	elif end == start:
		access_single(chr, start);
	else:
		print "Invalid target coordinate.";
		sys.exit();
		
#If single point access:
else:
	access_single(chr, int(sys.argv[2]));