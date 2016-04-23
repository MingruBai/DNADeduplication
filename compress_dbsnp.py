chr = '1';

vfile = open('./vector/vec' + chr +'.txt','w');

ufile = open('JWB-unified-file.txt','r');
dfile = open('./dbSNP/chr' + chr +'.txt','r');

dfile.readline();

uline = ufile.readline();
dline = dfile.readline();


while len(dline) != 0:

    count = count + 1;

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

    uline = ufile.readline();
    dline = dfile.readline();


ufile.close();
dfile.close();
vfile.close();
