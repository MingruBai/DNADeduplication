import sys
import os

def access_single(chr, target):

	if target <= 0:
		print "Invalid target coordinate.";
		sys.exit();

	#Decompress:
	os.system("bzip2 -d -k ./var_dbsnp/chr"+chr+"_formatted.txt.bz2");

	#Read variations:
	cfile = open("./var_dbsnp/chr"+chr+"_formatted.txt",'r');
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
		if target < p:
			get_ref(chr, refLoc - 1);
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
		get_ref(chr, refLoc - 1);

	sys.stdout.write('\n');
	os.system("rm ./var_dbsnp/chr"+chr+"_formatted.txt");


# def get_ref(chr, loc):
# 	rfile = open("./chr/chr"+chr+".fa",'r')
# 	rfile.readline();
# 	n = loc / 50;
# 	p = loc % 50;
# 	for i in range(n):
# 		rfile.readline();
# 	sys.stdout.write(rfile.readline().strip()[p]);
# 	rfile.close();

def get_ref(chr, loc):
	rfile = open("./chr/chr"+chr+".fa",'r')

	rfile.readline();
	n = loc / 50;
	p = loc % 50;

	rfile.seek(n*51,1);

	base_ref = rfile.readline().strip()[p];
	rfile.close()

	count = 0;
	dfile = open("./dbSNP/chr" + chr + ".txt",'r');
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
		os.system("bzip2 -d -k ./vector_dbsnp/vec" + chr + ".txt.bz2");
		vfile = open("./vector_dbsnp/vec" + chr + ".txt");
		vline = vfile.readline();
		vfile.close();
		os.system("rm ./vector_dbsnp/vec" + chr + ".txt");

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
