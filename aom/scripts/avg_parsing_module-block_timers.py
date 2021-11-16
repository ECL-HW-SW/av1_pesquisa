############################## TOTAL TIME PARSING #####################
# TOTAL TIME MODULE

filein1 = open('./result_module_timers.csv','r')

lines_modu = filein1.readlines()

total_out_modu = open('./total_module_timers.csv','w')

line = 0
i = -1
while line != lines_modu[-1]:
    i += 1
    line = lines_modu[i];

    try:
        if 'KEY_FRAME' in lines_modu[i + 1]:
            # line_l = line.split(';')
            # if len(line_l[1]) > 50:
            #     line_l[1] = 'all_disable'
            #     line = ';'.join(line_l)
            total_out_modu.write(line)
    except:
        total_out_modu.write(lines_modu[-1])
        total_out_modu.write('\n')

total_out_modu.close()
