ufile = open("JWB-unified-file.txt",'r');

type = [];
chr = [];
index = [];
seq = [];

p0 = 0;
p1 = -1;
p2 = -1;

prevChr = "";
prevIndex = -1;

while(True):
    uline = ufile.readline();
    if len(uline) == 0: break;

    ulist = uline.strip().split(',');
    t = ulist[0];
    c = ulist[1][3:];
    raw_i = int(ulist[2]);

    if t == '0':
        s = ulist[3].split('/')[1];
    if t == '1':
        s = str(len(ulist[3].split('/')[0]));
    if t == '2':
        s = ulist[3].split('/')[1];

    #set pointer to start of each type:
    if t == '1' and p1 == -1:
        p1 = len(type);
    if t == '2' and p2 == -1:
        p2 = len(type);

    type.append(t);
    chr.append(c);
    index.append(raw_i);
    seq.append(s);

ufile.close();

type.append('-1');
chr.append('-1');
index.append(-1);
seq.append('-1');


cur_chr = '1';

while(True):
    print cur_chr;
    if cur_chr == '-1': break;
    chr_type = [];
    chr_index = [];
    chr_seq = [];
    prev_index = 0;

    while chr[p0] == cur_chr and chr[p1] == cur_chr and chr[p2] == cur_chr:

        if index[p0] <= index[p1] and index[p0] <= index[p2]:
            chr_type.append(type[p0]);
            chr_index.append(index[p0]);
            chr_seq.append(seq[p0]);

            prev_index = index[p0];
            p0 = p0 + 1;

        if index[p1] <= index[p0] and index[p1] <= index[p2]:
            chr_type.append(type[p1]);
            chr_index.append(index[p1]);
            chr_seq.append(seq[p1]);

            prev_index = index[p1];
            p1 = p1 + 1;

        if index[p2] <= index[p0] and index[p2] <= index[p1]:
            chr_type.append(type[p2]);
            chr_index.append(index[p2]);
            chr_seq.append(seq[p2]);

            prev_index = index[p2];
            p2 = p2 + 1;


    while chr[p0] == cur_chr and chr[p1] == cur_chr:
        if index[p0] <= index[p1]:
            chr_type.append(type[p0]);
            chr_index.append(index[p0]);
            chr_seq.append(seq[p0]);

            prev_index = index[p0];
            p0 = p0 + 1;

        if index[p1] <= index[p0]:
            chr_type.append(type[p1]);
            chr_index.append(index[p1]);
            chr_seq.append(seq[p1]);

            prev_index = index[p1];
            p1 = p1 + 1;

    while chr[p0] == cur_chr and chr[p2] == cur_chr:
        if index[p0] <= index[p2]:
            chr_type.append(type[p0]);
            chr_index.append(index[p0]);
            chr_seq.append(seq[p0]);

            prev_index = index[p0];
            p0 = p0 + 1;

        if index[p2] <= index[p0]:
            chr_type.append(type[p2]);
            chr_index.append(index[p2]);
            chr_seq.append(seq[p2]);

            prev_index = index[p2];
            p2 = p2 + 1;

    while chr[p1] == cur_chr and chr[p2] == cur_chr:
        if index[p1] <= index[p2]:
            chr_type.append(type[p1]);
            chr_index.append(index[p1]);
            chr_seq.append(seq[p1]);

            prev_index = index[p1];
            p1 = p1 + 1;

        if index[p2] <= index[p1]:
            chr_type.append(type[p2]);
            chr_index.append(index[p2]);
            chr_seq.append(seq[p2]);

            prev_index = index[p2];
            p2 = p2 + 1;

    while chr[p0] == cur_chr:
        chr_type.append(type[p0]);
        chr_index.append(index[p0]);
        chr_seq.append(seq[p0]);

        prev_index = index[p0];
        p0 = p0 + 1;

    while chr[p1] == cur_chr:
        chr_type.append(type[p1]);
        chr_index.append(index[p1]);
        chr_seq.append(seq[p1]);

        prev_index = index[p1];
        p1 = p1 + 1;

    while chr[p2] == cur_chr:
        chr_type.append(type[p2]);
        chr_index.append(index[p2]);
        chr_seq.append(seq[p2]);

        prev_index = index[p2];
        p2 = p2 + 1;

    cfile = open("./var_abs/chr" + cur_chr + "_formatted.txt",'w');
    for t in chr_type:
        cfile.write(t);
    cfile.write('\n');

    for i in chr_index:
        cfile.write(str(i));
        cfile.write(' ');
    cfile.write('\n');

    for s in chr_seq:
        cfile.write(s);
        cfile.write(' ');
    cfile.write('\n');
    cfile.close();

    cur_chr = chr[p2];
