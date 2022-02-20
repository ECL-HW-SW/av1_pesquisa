from bjontegaard import bdbr,bdpsnr,plotRDCurves

params = ["all_disable",
        "set_disable_av1_ml_prune_rect_partition",
        "set_disable_prune_partitions_after_none",
        "set_disable_prune_partitions_after_split",
        "set_disable_prune_partitions_before_search",
        "set_minpartitionsize8",
        "set_minpartitionsize16",
        "set_minpartitionsize32",
        "set_minpartitionsize64",
        "set_minpartitionsize128",
]

out =  open('./total_bdbr.csv','w')

csv_ref = open('./result_bdbr_psnr.csv','r')
csv_test = open('./result_bdbr_psnr.csv','r')

linhas = csv_ref.readlines()
tam = len(linhas)

# lines = csv_ref.readlines()
tlines = csv_test.readlines()

for param in params:
    x=0
    i=1
    for lines in linhas:
        try:
            lines = linhas[i]
        except IndexError:
            continue

        print(lines)
        if ";orig;" in lines:

            if ";55;" in lines:
                nome37,conf,cq,yuv37,y37,u37,v37,b37,t37,dummy2 = lines.split(";")
                n = nome37 + ';' + param + ';' + cq
                y37,u37,v37,yuv37,b37,t37 = map(float,[y37,u37,v37,yuv37,b37,t37])
            if ";43;" in lines:
                nome32,conf,cq,yuv32,y32,u32,v32,b32,t32,dummy2 = lines.split(";")
                n = nome32 + ';' + param + ';' + cq
                y32,u32,v32,yuv32,b32,t32 = map(float,[y32,u32,v32,yuv32,b32,t32])
            if ";32;" in lines:
                nome27,conf,cq,yuv27,y27,u27,v27,b27,t27,dummy2 = lines.split(";")
                n = nome27 + ';' + param + ';' + cq
                y27,u27,v27,yuv27,b27,t27 = map(float,[y27,u27,v27,yuv27,b27,t27])
            if ";20;" in lines:
                nome22,conf,cq,yuv22,y22,u22,v22,b22,t22,dummy2 = lines.split(";")
                n = nome22 + ';' + param + ';' + cq
                y22,u22,v22,yuv22,b22,t22 = map(float,[y22,u22,v22,yuv22,b22,t22])

        if "%s"%param in lines:

            if ";55;" in lines:
                nome37t,conf,cq,yuv37t,y37t,u37t,v37t,b37t,t37t,dummy2 = lines.split(";")
                y37t,u37t,v37t,yuv37t,b37t,t37t = map(float,[y37t,u37t,v37t,yuv37t,b37t,t37t])
            if ";43;" in lines:
                nome32t,conf,cq,yuv32t,y32t,u32t,v32t,b32t,t32t,dummy2 = lines.split(";")
                y32t,u32t,v32t,yuv32t,b32t,t32t = map(float,[y32t,u32t,v32t,yuv32t,b32t,t32t])
            if ";32;" in lines:
                nome27t,conf,cq,yuv27t,y27t,u27t,v27t,b27t,t27t,dummy2 = lines.split(";")
                y27t,u27t,v27t,yuv27t,b27t,t27t = map(float,[y27t,u27t,v27t,yuv27t,b27t,t27t])
            if ";20;" in lines:
                nome22t,conf,cq,yuv22t,y22t,u22t,v22t,b22t,t22t,dummy2 = lines.split(";")
                y22t,u22t,v22t,yuv22t,b22t,t22t = map(float,[y22t,u22t,v22t,yuv22t,b22t,t22t])

        num = x/43
        num = str(num)
        x+=1
        i+=1
        if num.split('.')[1] == '0' and num.split('.')[0] != '0':
            x=0
            print('\n\nIN\n\n')
            ref = [[b22,y22,u22,v22,yuv22],[b27,y27,u27,v27,yuv27],[b32,y32,u32,v32,yuv32],[b37,y37,u37,v37,yuv37]]
            
            test = [[b22t,y22t,u22t,v22t,yuv22t],[b27t,y27t,u27t,v27t,yuv27t],[b32t,y32t,u32t,v32t,yuv32t],[b37t,y37t,u37t,v37t,yuv37t]]
            
            ttest = (t22t+t37t+t27t+t32t)/4
            tref = (t22+t37+t27+t32)/4
            dt=tref/ttest

            bdb = bdbr(ref,test,1)
            bdp = bdpsnr(ref,test,1) 
            # plotRDCurves(ref,test,1,"./Curva%s_%s.pdf"%(n,param),n)
            line = str(n) + ';' + str(bdb) + ';' + str(bdp) + ';' + str(dt) + ';\n'
            out.write(line)