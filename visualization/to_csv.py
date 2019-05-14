def to_csv(file):
    res = []
    with open(file, 'r') as result:
        for line in result:
            res.append(line.split()[:-1])
    for i in range(len(res)):
        if len(res[i]) >= 3:
            res[i] = [(' ').join(res[i][:-1]), res[i][-1]]
        else:
            res[i] = [res[i][0], res[i][1]]

    with open(''.join(file.split('.')[:-1]) + '.csv', 'w') as out:
        out.write('name, rank\n')
        for line in res:
            out.write("{0}, {1}\n".format(line[0], line[1]))


files = ['data/out-10-0.15.txt', 'data/out-10-0.3.txt', 'data/out-10-0.5.txt', 'data/out-10-0.7.txt',
         'data/out-10-0.85.txt']


for i in files:
    to_csv(i)
