import sys
import os
import zlib

def access_single(chr, target):

	if target <= 0:
		print "Invalid target coordinate.";
		sys.exit();

	#Decompress:
	#os.system("bzip2 -d -k ./var_dbsnp/chr"+chr+"_formatted.txt.bz2");

	#Read variations:
	cfileData = open("./var_dbsnp/chr"+chr+"_formatted",'r').read();
	cfileList = zlib.decompress(cfileData).split('\n');
	tList = cfileList[0].strip();
	pList = cfileList[1].strip().split();
	sList = cfileList[2].strip().split();
	#cfile.close();

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
		if target < p:
			get_ref_single(chr, refLoc - 1);
			found = True;
			break;

		#If SNP:
		if t == '0':
			target = target - p;
			prevDiff = 0;
			if target == 0:
				found = True;
				sys.stdout.write(s);
				break;

		#If deletion:
		if t == '1':
			numDel = int(s);
			refLoc = refLoc + numDel;
			target = target - p + 1;
			prevDiff = 1 - numDel;

		#If insertion:
		if t == '2':
			numIns = len(s);
			if target <= p + numIns - 1:
				sys.stdout.write(s[target - p]);
				found = True;
				break;
			
			refLoc = refLoc - numIns;
			target = target - p - numIns + 1;
			prevDiff = 1;

	#If no more variation:
	if not found:
		get_ref_single(chr, refLoc - 1);

	sys.stdout.write('\n');
	#os.system("rm ./var_dbsnp/chr"+chr+"_formatted.txt");

def get_ref_single(chr, loc):
	rfile = open("../chr/chr"+chr+".fa",'r')

	rfile.readline();
	n = loc / 50;
	p = loc % 50;

	rfile.seek(n*51,1);

	base_ref = rfile.readline().strip()[p];
	rfile.close()

	count = 0;
	dfile = open("../with_dbsnp/dbSNP/chr" + chr + ".txt",'r');
	dfile.readline();
	
	while True:

		dline = dfile.readline();
		if len(dline) == 0: break;
		di = int(dline.split()[3]);

		if di > loc + 1: break;
		if di < loc + 1:
			count = count + 1;
			continue;

		count = count + 1;
		#os.system("bzip2 -d -k ./vector_dbsnp/vec" + chr + ".txt.bz2");
		#vfile = open("./vector_dbsnp/vec" + chr ).read();
		vline = zlib.decompress(open("./vector_dbsnp/vec" + chr ).read());
		#vfile.close();
		#os.system("rm ./vector_dbsnp/vec" + chr + ".txt");

		if vline[count - 1] == '1':
			ds = dline.split()[9];
			if base_ref == ds[0]:
				sys.stdout.write(ds[2]);
				dfile.close();
				return;
			else:
				sys.stdout.write(ds[0]);
				dfile.close();
				return;
		else:
			sys.stdout.write(base_ref);
			dfile.close();
			return;

	sys.stdout.write(base_ref);
	dfile.close();

def access_range(chr, start, end):

	numRead = end - start + 1;
	readCount = 0;

	target = start;

	#Decompress:
	#os.system("bzip2 -d -k ./var_dbsnp/chr"+chr+"_formatted.txt.bz2");

	#Read variations:
	cfileData = open("./var_dbsnp/chr"+chr+"_formatted",'r').read();
	cfileList = zlib.decompress(cfileData).split('\n');
	tList = cfileList[0].strip();
	pList = cfileList[1].strip().split();
	sList = cfileList[2].strip().split();
	#cfile.close();

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
			get_ref_range(chr, refLoc - 1);
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
		get_ref_range(chr, refLoc - 1);
		refLoc = refLoc + 1;
		readCount = readCount + 1;

	sys.stdout.write('\n');

	#os.system("rm ./var_dbsnp/chr"+chr+"_formatted.txt");

def get_ref_range(chr, loc):
	rfile = open("../chr/chr"+chr+".fa",'r')

	rfile.readline();
	n = loc / 50;
	p = loc % 50;

	rfile.seek(n*51,1);

	base_ref = rfile.readline().strip()[p];
	rfile.close()

	global count;
	dfile = open("../with_dbsnp/dbSNP/chr" + chr + ".txt",'r');
	dfile.readline();

	global loc_db;
	#print loc_db
	#count not the same!!!
	if loc_db != -1:
		dfile.seek(loc_db, 0);
	
	while True:

		dline = dfile.readline();
		loc_db = dfile.tell() - len(dline);
		if len(dline) == 0: break;
		di = int(dline.split()[3]);

		if di > loc + 1: break;
		if di < loc + 1:
			count = count + 1;
			continue;

		#os.system("bzip2 -d -k ./vector_dbsnp/vec" + chr + ".txt.bz2");
		#vfile = open("./vector_dbsnp/vec" + chr ).read();
		vline = zlib.decompress(open("./vector_dbsnp/vec" + chr ).read());
		#vfile.close();
		#os.system("rm ./vector_dbsnp/vec" + chr + ".txt");

		if vline[count] == '1':
			ds = dline.split()[9];
			if base_ref == ds[0]:
				sys.stdout.write(ds[2]);
				dfile.close();
				return;
			else:
				sys.stdout.write(ds[0]);
				dfile.close();
				return;
		else:
			sys.stdout.write(base_ref);
			dfile.close();
			return;

	sys.stdout.write(base_ref);
	dfile.close();



#Target chromosome from user:
chr = sys.argv[1];

loc_db = -1;
count = 0;

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