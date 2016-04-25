import sys
import os

def access_single(chr, target):

	if target <= 0:
		print "Invalid target coordinate.";
		sys.exit();

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
	os.system("rm ./var/chr"+chr+"_formatted.txt");


# def get_ref(chr, loc):
# 	rfile = open("./chr/chr"+chr+".fa",'r')
# 	rfile.readline();
# 	n = loc / 50;
# 	p = loc % 50;
# 	for i in range(n):
# 		rfile.readline();
# 	sys.stdout.write(rfile.readline().strip()[p]);
# 	rfile.close()

def get_ref(chr, loc):
	rfile = open("../chr/chr"+chr+".fa",'r')
	#filename = "./chr/chr"+chr+".fa";

	#lineNum = loc / 50 + 2;
	#linePos = loc % 50;

	rfile.readline();
	n = loc / 50;
	p = loc % 50;

	#WHY IT IS SLOW!!!!!
	# for i in range(n):
	# 	rfile.readline();

	rfile.seek(n*51,1);

	#print lineNum,linePos
	#print linecache.getline(filename, lineNum)

	sys.stdout.write(rfile.readline().strip()[p]);
	#sys.stdout.write(linecache.getline(filename, lineNum).strip()[linePos]);
	rfile.close()
