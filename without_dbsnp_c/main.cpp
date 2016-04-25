#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>

using namespace std;

std::vector<std::string> &split(const std::string &s, char delim, std::vector<std::string> &elems) {
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, delim)) {
        elems.push_back(item);
    }
    return elems;
}

std::vector<std::string> split(const std::string &s, char delim) {
    std::vector<std::string> elems;
    split(s, delim, elems);
    return elems;
}

int get_ref(char chr, int loc){
	string chrFilename = "../chr/chr";
	chrFilename.append(1, chr);
	chrFilename.append(".fa");
	ifstream chrFile(chrFilename.c_str());
	string chrLine;
	getline(chrFile, chrLine);

	int n = loc / 50;
	int p = loc % 50;

	chrFile.seekg(n * 51, chrFile.cur);
	getline(chrFile, chrLine);

	cout << chrLine[p];

	return 0;
}


int access_single(char chr, int target){

	//Check if target is valid:
	if (target <= 0){
		cout << "Invalid target coordinate." << endl;
		return -1;
	}

	//Decompress the variation file:
	string unzipCommand = "bzip2 -d -k ./var/chr";
	unzipCommand.append(1, chr);
	unzipCommand.append("_formatted.txt.bz2");
	system(unzipCommand.c_str());

	//Read variations:
	string varFilename = "./var/chr";
	varFilename.append(1,chr);
	varFilename.append("_formatted.txt");
	ifstream varFile(varFilename.c_str());
    string tList; 
	getline(varFile, tList);
	string pListString;
	getline(varFile, pListString);
	string sListString;
	getline(varFile, sListString);
    
	//vector<string> pList = split(pListString, ' ');
	//vector<string> sList = split(sListString, ' ');
    
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
        
        
        
		//int p = stoi(pList[i]);
		//string s = sList[i];

		//Update the relative position
		p = p + prevDiff;

		//If access point is before next variation:
		if (
			target < p){
			get_ref(chr, refLoc - 1);
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
		get_ref(chr, refLoc - 1);
	}

	cout << '\n';

	//Delete decompressed file:
	string deleteCommand = "rm ./var/chr";
	deleteCommand.append(1, chr);
	deleteCommand.append("_formatted.txt");
	system(deleteCommand.c_str());

	return 0;
}

int main(){
	access_single('1', 885);
}