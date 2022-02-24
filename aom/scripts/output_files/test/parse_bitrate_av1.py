import os, re

CQS = [55,43,32,20]

fileout3 = open('./result_bdbr_psnr_av1.csv','w')

linha3 = (
    'sequencia' + ';' +
    'parameter' + ';' +
    'cqs' + ';' +
    'yuvpsnr' + ';' +
    'ypsnr' + ';' +
    'upsnr' + ';' +
    'vpsnr' + ';' +
    'br' + ';' +
    'time(ms)'
)

fileout3.write(linha3)
fileout3.close()


files = sorted(os.listdir('.'))

for cq in CQS:

    for file in files:

        if not 'cq%s'%cq in file:
            continue

        if '.py' in file or '.csv' in file or os.path.isdir(file):
            continue

        filein = open('./%s'%(file),'r')
        lines = filein.readlines()

        if '_set_' in file or '.py' in file:
            name = file.split('_set_')[1]
        else:
            name = 'orig'

        line = 0
        i = 0
        while line != lines[-1]:
            i+=1
            line=lines[i];

            fileout3 = open('./result_bdbr_psnr_av1.csv','a')

            if '(Overall/Avg/Y/U/V)' in line:
                bdbr = re.split('[ ]+', line)
                yuvpsnr = bdbr[4]
                ypsnr = bdbr[6]
                upsnr = bdbr[7]
                vpsnr = bdbr[8]
                br = bdbr[9]
                time_total = bdbr[11]

                fileout3.write('\n')

                seq = lines[1].split('.')[0]
                seq = seq.split('/')[-1]
                fileout3.write(seq)
                fileout3.write(';')
                param = lines[2].split('coded')[1]
                if param == '.webm\n':
                    param = 'orig'
                else:
                    param = param.split('.')[0].strip('_')
                    if len(param) > 50:
                        param = 'all_disable'
                fileout3.write(param)
                fileout3.write(';')
                fileout3.write('%s'%cq)
                fileout3.write(';')
                fileout3.write(ypsnr)
                fileout3.write(';')
                fileout3.write(yuvpsnr)
                fileout3.write(';')
                fileout3.write(upsnr)
                fileout3.write(';')
                fileout3.write(vpsnr)
                fileout3.write(';')
                fileout3.write(br)
                fileout3.write(';')
                fileout3.write('%s'%time_total)
                fileout3.write(';')

                fileout3.close()