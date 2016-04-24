import os

chr = '1';
ufile = open('../JWB-unified-file.txt','r');
newufile = open('JWB-snp-file.txt','w');
os.system("mkdir ./vector_dbsnp");

while True:

    print chr

    vfile = open('./vector_dbsnp/vec' + chr +'.txt','w');
    
    dfile = open('./dbSNP/chr' + chr +'.txt','r');

    dfile.readline();

    dline = dfile.readline();
    if chr == '1':
        uline = ufile.readline();
    
    while len(dline) != 0:

        ulist = uline.strip().split(',');
        t_var = int(ulist[0]);
        c_var = ulist[1][3:];
        i_var = int(ulist[2]);

        dlist = dline.strip().split();
        i_db = int(dlist[3]);

        if t_var != 0 or c_var != chr:
            dline = dfile.readline();
            vfile.write('0');
            continue;

        if i_db > i_var:
            newufile.write(uline);
            uline = ufile.readline();
            continue;

        if i_db < i_var:
            dline = dfile.readline();
            vfile.write('0');
            continue;

        s_var = ulist[3];
        s_db = dlist[9];

        if (s_var[0] == s_db[0] and s_var[2] == s_db[2]) or (s_var[0] == s_db[2] and s_var[2] == s_db[0]):
            vfile.write('1');
        else:
            vfile.write('0');
            newufile.write(uline);

        uline = ufile.readline();
        dline = dfile.readline();

    while t_var == 0 and c_var == chr:
        newufile.write(uline);
        uline = ufile.readline();
        ulist = uline.strip().split(',');
        t_var = int(ulist[0]);
        c_var = ulist[1][3:];
        i_var = int(ulist[2]);

    chr = c_var
    
    dfile.close();
    vfile.close();

    if t_var != 0: 
        break;


ufile.close();
newufile.close();
os.system("bzip2 ./vector_dbsnp/*")

