#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>

using namespace std;
int loc_db_global = -1;
int count_global = 0;

int get_ref_single(string chr, int loc){
	string chrFilename = "../chr/chr";
	chrFilename.append(chr);
	chrFilename.append(".fa");
	ifstream chrFile(chrFilename.c_str());
	string chrLine;
	getline(chrFile, chrLine);

	int n = loc / 50;
	int p = loc % 50;

	chrFile.seekg(n * 51, chrFile.cur);
	getline(chrFile, chrLine);

	char base_ref = chrLine[p];

	int count = 0;
	string dfileName = "./dbSNP/chr";
	dfileName.append(chr);
	dfileName.append(".txt");
	ifstream dFile(dfileName.c_str());
	string dLine;
	getline(dFile, dLine);


	while (true){

		getline(dFile, dLine);
		if (dLine.size() == 0) break;

		int dLoc = 0;
		int dSpace;

		for (int i = 0; i < 4; i++){
	        dSpace = dLine.find('\t',dLoc + 1);
	        if (i == 3){
	        	break;
	        }
	        dLoc = dSpace + 1;
		}


		// cout << dLoc <<endl;
		// cout << dSpace << endl;
		//  cout << dLine.substr(dLoc, dSpace - dLoc)<< endl;

		int di = stoi(dLine.substr(dLoc, dSpace - dLoc));

		if (di > loc + 1){
			break;
		}
		if (di < loc + 1){
			count = count + 1;
			continue;
		}

		count = count + 1;

		string unzipCommand = "bzip2 -d -k ./vector_dbsnp/vec";
		unzipCommand.append(chr);
		unzipCommand.append(".txt.bz2");
		system(unzipCommand.c_str());

		string vFilename = "./vector_dbsnp/vec";
		vFilename.append(chr);
		vFilename.append(".txt");
		ifstream vFile(vFilename.c_str());
		string vLine;
		getline(vFile, vLine);

		string deleteCommand = "rm ./vector_dbsnp/vec";
		deleteCommand.append(chr);
		deleteCommand.append(".txt");
		system(deleteCommand.c_str());

		if (vLine[count - 1] == '1'){
			dLoc = 0;
			dSpace = 0;

			for (int i = 0; i < 10; i++){
		        dSpace = dLine.find('\t',dLoc + 1);
		        if (i == 9){
		        	break;
		        }
		        dLoc = dSpace + 1;
			}

			string ds = dLine.substr(dLoc, dSpace - dLoc);

			if (base_ref == ds[0]){
				cout << ds[2];
				return 0;
			}else{
				cout << ds[0];
				return 0;
			}
		}else{
			cout << base_ref;
			return 0;
		}
	}

	cout << base_ref;
	return 0;
}

int get_ref_range(string chr, int loc){
	string chrFilename = "../chr/chr";
	chrFilename.append(chr);
	chrFilename.append(".fa");
	ifstream chrFile(chrFilename.c_str());
	string chrLine;
	getline(chrFile, chrLine);

	int n = loc / 50;
	int p = loc % 50;

	chrFile.seekg(n * 51, chrFile.cur);
	getline(chrFile, chrLine);

	char base_ref = chrLine[p];
    

	string dfileName = "./dbSNP/chr";
	dfileName.append(chr);
	dfileName.append(".txt");
	ifstream dFile(dfileName.c_str());
	string dLine;
	getline(dFile, dLine);

	if (loc_db_global != -1){
		dFile.seekg(loc_db_global, dFile.beg);
	}


	while (true){

		getline(dFile, dLine);
		loc_db_global = int(dFile.tellg()) - int(dLine.size()) - 1;
		if (dLine.size() == 0) break;

		int dLoc = 0;
		int dSpace;

		for (int i = 0; i < 4; i++){
	        dSpace = dLine.find('\t',dLoc + 1);
	        if (i == 3){
	        	break;
	        }
	        dLoc = dSpace + 1;
		}
		//cout << dLine << endl;
		//cout << dLine.substr(dLoc, dSpace - dLoc) << endl;

		int di = stoi(dLine.substr(dLoc, dSpace - dLoc));


		if (di > loc + 1){
			break;
		}
		if (di < loc + 1){
			count_global = count_global + 1;
			continue;
		}

		//count_global = count_global + 1;

		string unzipCommand = "bzip2 -d -k ./vector_dbsnp/vec";
		unzipCommand.append(chr);
		unzipCommand.append(".txt.bz2");
		system(unzipCommand.c_str());

		string vFilename = "./vector_dbsnp/vec";
		vFilename.append(chr);
		vFilename.append(".txt");
		ifstream vFile(vFilename.c_str());
		string vLine;
		getline(vFile, vLine);

		string deleteCommand = "rm ./vector_dbsnp/vec";
		deleteCommand.append(chr);
		deleteCommand.append(".txt");
		system(deleteCommand.c_str());

		if (vLine[count_global] == '1'){
			dLoc = 0;
			dSpace = 0;

			for (int i = 0; i < 10; i++){
		        dSpace = dLine.find('\t',dLoc + 1);
		        if (i == 9){
		        	break;
		        }
		        dLoc = dSpace + 1;
			}

			string ds = dLine.substr(dLoc, dSpace - dLoc);
            
//            if (ds[0] == '-'){
//                cout << "*** " << endl;
//                cout << ds << endl;;
//            }

			if (base_ref == ds[0]){
				cout << ds[2];
				return 0;
			}else{
				cout << ds[0];
				return 0;
			}
		}else{
			cout << base_ref;
			return 0;
		}
	}

	cout << base_ref;
	return 0;
}

// int get_ref(string chr, int loc){
// 	string chrFilename = "../chr/chr";
// 	chrFilename.append(chr);
// 	chrFilename.append(".fa");
// 	ifstream chrFile(chrFilename.c_str());
// 	string chrLine;
// 	getline(chrFile, chrLine);

// 	int n = loc / 50;
// 	int p = loc % 50;

// 	chrFile.seekg(n * 51, chrFile.cur);
// 	getline(chrFile, chrLine);

// 	cout << chrLine[p];

// 	return 0;
// }


int access_single(string chr, int target){

	//Check if target is valid:
	if (target <= 0){
		cout << "Invalid target coordinate." << endl;
		return -1;
	}

	//Decompress the variation file:
	string unzipCommand = "bzip2 -d -k ./var_dbsnp/chr";
	unzipCommand.append(chr);
	unzipCommand.append("_formatted.txt.bz2");
	system(unzipCommand.c_str());

	//Read variations:
	string varFilename = "./var_dbsnp/chr";
	varFilename.append(chr);
	varFilename.append("_formatted.txt");
	ifstream varFile(varFilename.c_str());
    string tList; 
	getline(varFile, tList);
	string pListString;
	getline(varFile, pListString);
	string sListString;
	getline(varFile, sListString);

    
    
    int pLoc = 0;
    int sLoc = 0;

	//Pointer at reference genome:
	int refLoc = target;
	//Difference used to adjust relative distance:
	int prevDiff = 0;
	//Flag to indicate whether base pair has been found:
	bool found = false;

	//Going through the variation to find the target:
	for (int i = 0; i < tList.size(); i++){
		char t = tList[i];
        
        int pSpace = pListString.find(' ',pLoc + 1);
        int p = stoi(pListString.substr(pLoc, pSpace - pLoc));
        pLoc = pSpace + 1;

        
        int sSpace = sListString.find(' ',sLoc + 1);
        string s = sListString.substr(sLoc, sSpace - sLoc);
        sLoc = sSpace + 1;
        

		//Update the relative position
		p = p + prevDiff;

		//If access point is before next variation:
		if (target < p){
			get_ref_single(chr, refLoc - 1);
			found = true;
			break;
		}

		//If SNP:
		if (t == '0'){
			target = target - p;
			prevDiff = 0;
			if (target == 0){
				found = true;
				cout << s;
				break;
			}
		}

		//If deletion:
		if (t == '1'){
			int numDel = stoi(s);
			refLoc = refLoc + numDel;
			target = target - p + 1;
			prevDiff = 1 - numDel;
		}

		//If insertion:
		if (t == '2'){
			int numIns = s.size();
			if (target <= p + numIns - 1){
				cout << s[target - p];
				found = true;
				break;
			}

			refLoc = refLoc - numIns;
			target = target - p - numIns + 1;
			prevDiff = 1;
		}
	}

	//If no more variation:
	if (!found){
		get_ref_single(chr, refLoc - 1);
	}

	cout << '\n';

	//Delete decompressed file:
	string deleteCommand = "rm ./var_dbsnp/chr";
	deleteCommand.append(chr);
	deleteCommand.append("_formatted.txt");
	system(deleteCommand.c_str());

	return 0;
}



int access_range(string chr, int start, int end){

	int numRead = end - start + 1;
	int readCount = 0;

	int target = start;

	//Check if range is valid:
	if (end <= start){
		cout << "Invalid target coordinate." << endl;
		return -1;
	}

	//Decompress the variation file:
	string unzipCommand = "bzip2 -d -k ./var_dbsnp/chr";
	unzipCommand.append(chr);
	unzipCommand.append("_formatted.txt.bz2");
	system(unzipCommand.c_str());

	//Read variations:
	string varFilename = "./var_dbsnp/chr";
	varFilename.append(chr);
	varFilename.append("_formatted.txt");
	ifstream varFile(varFilename.c_str());
    string tList; 
	getline(varFile, tList);
	string pListString;
	getline(varFile, pListString);
	string sListString;
	getline(varFile, sListString);
    
    
    int pLoc = 0;
    int sLoc = 0;

	//Pointer at reference genome:
	int refLoc = target;
	//Difference used to adjust relative distance:
	int prevDiff = 0;
	//Flag to indicate whether base pair has been found:
	bool found = false;

	//Going through the variation to find the target:
	for (int i = 0; i < tList.size(); i++){
		char t = tList[i];
        
        int pSpace = pListString.find(' ',pLoc + 1);
        int p = stoi(pListString.substr(pLoc, pSpace - pLoc));
        pLoc = pSpace + 1;
        
        int sSpace = sListString.find(' ',sLoc + 1);
        string s = sListString.substr(sLoc, sSpace - sLoc);
        sLoc = sSpace + 1;
        

		//Update the relative position
		p = p + prevDiff;

		//If access point is before next variation:
		while (target < p && readCount < numRead){
			get_ref_range(chr, refLoc - 1);
			readCount = readCount + 1;
			found = true;
			target = target + 1;
			refLoc = refLoc + 1;
		}

		if (readCount >= numRead){
			break;
		}

		//If SNP:
		if (t == '0'){
			target = target - p;
			prevDiff = 0;
			if (target == 0){
				found = true;
				cout << s;
				readCount = readCount + 1;
				refLoc = refLoc + 1;
				target = 1;
			}
		}

		if (readCount >= numRead){
			break;
		}

		//If deletion:
		if (t == '1'){
			int numDel = stoi(s);
			refLoc = refLoc + numDel;
			target = target - p + 1;
			prevDiff = 1 - numDel;
		}

		if (readCount >= numRead){
			break;
		}

		//If insertion:
		if (t == '2'){
			int numIns = s.size();
			if (target <= p + numIns - 1){
				refLoc = refLoc - (target - p);
				prevDiff = 1+ target - p;
				while (target <= p + numIns - 1){
					cout << s[target - p];
					readCount = readCount + 1;
					found = true;
					target = target + 1;
				}
				target = 1;
			}else{
				refLoc = refLoc - numIns;
				target = target - p - numIns + 1;
				prevDiff = 1;
			}
		}

		if (readCount >= numRead){
			break;
		}
	}

	//If no more variation:
	while (readCount < numRead){
		get_ref_range(chr, refLoc - 1);
		refLoc = refLoc + 1;
		readCount = readCount + 1;
	}

	cout << '\n';

	//Delete decompressed file:
	string deleteCommand = "rm ./var_dbsnp/chr";
	deleteCommand.append(chr);
	deleteCommand.append("_formatted.txt");
	system(deleteCommand.c_str());

	return 0;
}



int main(int argc, char* argv[]){
	string chr = argv[1];
	string range = argv[2];

	//Single access:
	if (range.find(':') == std::string::npos){
		int target = stoi(range);
		access_single(chr, target);

	//Range access:		
	}else{
		int start = stoi(range.substr(0,range.find(':')));
		int end = stoi(range.substr(range.find(':') + 1));
		access_range(chr, start, end);
	}
}