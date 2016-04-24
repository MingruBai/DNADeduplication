import sys
import os
import linecache

def access_range(chr, start, end):

	numRead = end - start + 1;
	readCount = 0;

	target = start;

	#Decompress:
	os.system("bzip2 -d -k ./var/chr"+chr+"_formatted.txt.bz2");

	#Read variations:
	cfile = open("./var/chr"+chr+"_formatted.txt",'r');
	tList = cfile.readline().strip();
	pList = cfile.readline().strip().split();
	sList = cfile.readline().strip().split();
	cfile.close();

	#Pointer at reference genome:
	refLoc = target;
	#Difference used to adjust relative distance:
	prevDiff = 0;
	found = False;

	for i in range(len(tList)):

		t = tList[i];
		p = int(pList[i]);
		s = sList[i];

		#Update the relative position
		p = p + prevDiff;

		#If access point is before next variation:
		while target < p and readCount < numRead:
			get_ref(chr, refLoc - 1);
			readCount = readCount + 1;
			found = True;
			target = target + 1;
			refLoc = refLoc + 1;

		if readCount >= numRead:
			break;

		#If SNP:
		if t == '0':
			target = target - p;
			prevDiff = 0;
			if target == 0:
				found = True;
				sys.stdout.write(s);
				readCount = readCount + 1;
				refLoc = refLoc + 1;
				target = 1;

		if readCount >= numRead:
			break;

		#If deletion:
		if t == '1':
			numDel = int(s);
			refLoc = refLoc + numDel;
			target = target - p + 1;
			prevDiff = 1 - numDel;

		if readCount >= numRead:
			break;

		#If insertion:
		if t == '2':
			numIns = len(s);
			if target <= p + numIns - 1:
				refLoc = refLoc - (target - p);
				prevDiff = 1 + target - p;
				while target <= p + numIns - 1:
					sys.stdout.write(s[target - p]);
					readCount = readCount + 1;
					found = True;
					target = target + 1;

				target = 1;
				
			else:
				refLoc = refLoc - numIns;
				target = target - p - numIns + 1;
				prevDiff = 1;

		if readCount >= numRead:
			break;

	#If no more variation:
	while readCount < numRead:
		get_ref(chr, refLoc - 1);
		refLoc = refLoc + 1;
		readCount = readCount + 1;

	sys.stdout.write('\n');

	os.system("rm ./var/chr"+chr+"_formatted.txt");

def get_ref(chr, loc):
	rfile = open("../chr/chr"+chr+".fa",'r')

	rfile.readline();
	n = loc / 50;
	p = loc % 50;

	rfile.seek(n*51,1);

	sys.stdout.write(rfile.readline().strip()[p]);
	rfile.close()


# def get_ref(chr, loc):
# 	rfile = open("./chr/chr"+chr+".fa",'r')
# 	rfile.readline();
# 	n = loc / 50;
# 	p = loc % 50;
# 	for i in range(n):
# 		rfile.readline();
# 	sys.stdout.write(rfile.readline().strip()[p]);
# 	rfile.close()