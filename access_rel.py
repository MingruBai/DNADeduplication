import sys
import os

#Target chromosome from user:
chr = sys.argv[1];
#Target access point from user:
target = int(sys.argv[2]);

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


def get_ref(loc):
	rfile = open("./chr/chr"+chr+".fa",'r')
	rfile.readline();
	n = loc / 50;
	p = loc % 50;
	for i in range(n):
		rfile.readline();
	print rfile.readline().strip()[p];
	rfile.close()


for i in range(len(tList)):

	t = tList[i];
	p = int(pList[i]);
	s = sList[i];

	#Update the relative position
	p = p + prevDiff;

	#If access point is before next variation:
	if target < p:
		get_ref(refLoc - 1);
		found = True;
		break;

	#If SNP:
	if t == '0':
		target = target - p;
		prevDiff = 0;
		if target == 0:
			found = True;
			print s;
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
			print s[target - p];
			found = True;
			break;
		
		refLoc = refLoc - numIns;
		target = target - p - numIns + 1;
		prevDiff = 1;

#If no more variation:
if not found:
	get_ref(refLoc - 1);

os.system("rm ./var/chr"+chr+"_formatted.txt");

