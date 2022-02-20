import os, re

CQS = [55,43,32,20]

fileout1 = open('./result_module_timers.csv','w')
fileout2 = open('./result_block_timers.csv','w')
fileout3 = open('./result_bdbr_psnr.csv','w')

linha1 = (
    'sequencia'+';'+
    'parameter'+';'+
    'cqs'+';'+
    'n_frame'+';'+
    'frame_type'+';'+
    'av1_encode_strategy_time'     + ';' +
    'av1_get_second_pass_params_time'  + ';' +
    'denoise_and_encode_time'  + ';' +
    'apply_filtering_time'     + ';' +
    'av1_tpl_setup_stats_time'     + ';' +
    'encode_frame_to_data_rate_time'   + ';' +
    'encode_with_recode_loop_time'     + ';' +
    'loop_filter_time'     + ';' +
    'cdef_time'    + ';' +
    'loop_restoration_time'    + ';' +
    'av1_pack_bitstream_final_time'    + ';' +
    'av1_encode_frame_time'    + ';' +
    'av1_compute_global_motion_time'   + ';' +
    'av1_setup_motion_field_time'  + ';' +
    'encode_sb_row_time'   + ';' +
    'rd_pick_partition_time'   + ';' +
    'av1_prune_partitions_time'    + ';' +
    'none_partition_search_time'   + ';' +
    'split_partition_search_time'  + ';' +
    'rectangular_partition_search_time'    + ';' +
    'ab_partitions_search_time'    + ';' +
    'rd_pick_4partition_time'  + ';' +
    'encode_sb_time'   + ';' +
    'rd_pick_sb_modes_time'    + ';' +
    'av1_rd_pick_intra_mode_sb_time'   + ';' +
    'av1_rd_pick_inter_mode_sb_time'   + ';' +
    'set_params_rd_pick_inter_mode_time'   + ';' +
    'skip_inter_mode_time'     + ';' +
    'handle_inter_mode_time'   + ';' +
    'evaluate_motion_mode_for_winner_candidates_time'  + ';' +
    'do_tx_search_time'    + ';' +
    'handle_intra_mode_time'   + ';' +
    'refine_winner_mode_tx_time'   + ';' +
    'av1_search_palette_mode_time'     + ';' +
    'handle_newmv_time'    + ';' +
    'compound_type_rd_time'    + ';' +
    'interpolation_filter_search_time'     + ';' +
    'motion_mode_rd_time'  + ';'
)

fileout1.write(linha1)
fileout1.close()

linha2 = (
    'sequencia' + ';' +
    'parameter' + ';' +
    'cqs' + ';' +
    'block' + ';' +
    'time' + ';' +
    'count'
)

fileout2.write(linha2)
fileout2.close()


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


folders = next(os.walk('.'))[1]
arq=0
ps = len(folders)
cqs = len(CQS)

# BEGIN PARSING

for folder in folders:

    if '__' in folder or 'output_files' in folder or '.ipynb' in folder or 'NN' in folder:
        ps-=1
        continue

    for cq in CQS:

        pathin = '%s/cq_%s/log/'%(folder,cq)

        files = sorted(os.listdir('%s'%pathin))


        for file in files:

            fs = len(files)

            filein = open('%s/%s'%(pathin,file),'r')
            lines = filein.readlines()

            if '_set_' in file:
                name = file.split('_set_')[1]
            else:
                name = 'orig'

            line = 0
            i = 0
            print('processando... (%s%s)'%(pathin,file))
            while line != lines[-1]:
                i+=1
                line=lines[i];

                fileout1 = open('./result_module_timers.csv','a')
                fileout2 = open('./result_block_timers.csv','a')
                fileout3 = open('./result_bdbr_psnr.csv','a')

                # MODULE TIMERS PARSING

                if 'Frame number' in line:

                    fileout1.write('\n')

                    seq = lines[1].split('.')[0]
                    seq = seq.split('/')[-1]
                    fileout1.write(seq)
                    fileout1.write(';')

                    param = lines[2].split('coded')[1]
                    if param == '.webm\n':
                        param = 'orig'
                    else:
                        param = param.split('.')[0].strip('_')
                        if len(param) > 50:
                            param = 'all_disable'

                    fileout1.write(param)
                    fileout1.write(';')

                    fileout1.write('%s'%cq)
                    fileout1.write(';')

                    n_frame = line.split(',')[0].split(': ')[-1]
                    fileout1.write(n_frame)
                    fileout1.write(';')

                    frame_type = line.split(",")[1].split(': ')[-1]
                    fileout1.write(frame_type)
                    fileout1.write(';')

                if 'av1_encode_strategy_time' in line:

                    av1_encode_strategy_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(av1_encode_strategy_time)
                    fileout1.write(';')

                if 'denoise_and_encode_time' in line:

                    denoise_and_encode_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(denoise_and_encode_time)
                    fileout1.write(';')

                if 'encode_frame_to_data_rate_time' in line:

                    encode_frame_to_data_rate_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(encode_frame_to_data_rate_time)
                    fileout1.write(';')

                if 'encode_with_recode_loop_time' in line:

                    encode_with_recode_loop_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(encode_with_recode_loop_time)
                    fileout1.write(';')

                if 'encode_sb_row_time' in line:

                    encode_sb_row_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(encode_sb_row_time)
                    fileout1.write(';')

                if 'rd_pick_sb_modes_time' in line:

                    rd_pick_sb_modes_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(rd_pick_sb_modes_time)
                    fileout1.write(';')

                if 'av1_encode_frame_time' in line:

                    av1_encode_frame_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(av1_encode_frame_time)
                    fileout1.write(';')

                if 'rd_pick_partition_time' in line:

                    rd_pick_partition_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(rd_pick_partition_time)
                    fileout1.write(';')

                if 'av1_rd_pick_intra_mode_sb_time' in line:

                    av1_rd_pick_intra_mode_sb_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(av1_rd_pick_intra_mode_sb_time)
                    fileout1.write(';')

                if 'rectangular_partition_search_time' in line:

                    rectangular_partition_search_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(rectangular_partition_search_time)
                    fileout1.write(';')

                if 'none_partition_search_time' in line:

                    none_partition_search_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(none_partition_search_time)
                    fileout1.write(';')

                if 'split_partition_search_time' in line:

                    split_partition_search_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(split_partition_search_time)
                    fileout1.write(';')

                if 'rd_pick_4partition_time' in line:

                    rd_pick_4partition_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(rd_pick_4partition_time)
                    fileout1.write(';')

                if 'av1_rd_pick_inter_mode_sb_time' in line:

                    av1_rd_pick_inter_mode_sb_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(av1_rd_pick_inter_mode_sb_time)
                    fileout1.write(';')

                if 'ab_partitions_search_time' in line:

                    ab_partitions_search_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(ab_partitions_search_time)
                    fileout1.write(';')

                if 'handle_inter_mode_time' in line:

                    handle_inter_mode_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(handle_inter_mode_time)
                    fileout1.write(';')

                if 'motion_mode_rd_time' in line:

                    motion_mode_rd_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(motion_mode_rd_time)
                    fileout1.write(';')

                if 'loop_restoration_time' in line:

                    loop_restoration_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(loop_restoration_time)
                    fileout1.write(';')

                if 'cdef_time' in line:

                    cdef_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(cdef_time)
                    fileout1.write(';')

                if 'handle_intra_mode_time' in line:

                    handle_intra_mode_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(handle_intra_mode_time)
                    fileout1.write(';')

                if 'handle_newmv_time' in line:

                    handle_newmv_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(handle_newmv_time)
                    fileout1.write(';')

                if 'av1_prune_partitions_time' in line:

                    av1_prune_partitions_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(av1_prune_partitions_time)
                    fileout1.write(';')

                if 'av1_tpl_setup_stats_time' in line:

                    av1_tpl_setup_stats_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(av1_tpl_setup_stats_time)
                    fileout1.write(';')

                if 'av1_compute_global_motion_time' in line:

                    av1_compute_global_motion_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(av1_compute_global_motion_time)
                    fileout1.write(';')

                if 'interpolation_filter_search_time' in line:

                    interpolation_filter_search_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(interpolation_filter_search_time)
                    fileout1.write(';')

                if 'encode_sb_time' in line:

                    encode_sb_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(encode_sb_time)
                    fileout1.write(';')

                if 'loop_filter_time' in line:

                    loop_filter_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(loop_filter_time)
                    fileout1.write(';')

                if 'set_params_rd_pick_inter_mode_time' in line:

                    set_params_rd_pick_inter_mode_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(set_params_rd_pick_inter_mode_time)
                    fileout1.write(';')

                if 'skip_inter_mode_time' in line:

                    skip_inter_mode_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(skip_inter_mode_time)
                    fileout1.write(';')

                if 'av1_pack_bitstream_final_time' in line:

                    av1_pack_bitstream_final_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(av1_pack_bitstream_final_time)
                    fileout1.write(';')

                if 'refine_winner_mode_tx_time' in line:

                    refine_winner_mode_tx_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(refine_winner_mode_tx_time)
                    fileout1.write(';')

                if 'compound_type_rd_time' in line:

                    compound_type_rd_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(compound_type_rd_time)
                    fileout1.write(';')

                if 'evaluate_motion_mode_for_winner_candidates_time' in line:

                    evaluate_motion_mode_for_winner_candidates_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(evaluate_motion_mode_for_winner_candidates_time)
                    fileout1.write(';')

                if 'do_tx_search_time' in line:

                    do_tx_search_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(do_tx_search_time)
                    fileout1.write(';')

                if 'av1_get_second_pass_params_time' in line:

                    av1_get_second_pass_params_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(av1_get_second_pass_params_time)
                    fileout1.write(';')

                if 'av1_setup_motion_field_time' in line:

                    av1_setup_motion_field_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(av1_setup_motion_field_time)
                    fileout1.write(';')

                if 'apply_filtering_time' in line:

                    apply_filtering_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(apply_filtering_time)
                    fileout1.write(';')

                if 'av1_search_palette_mode_time' in line:

                    av1_search_palette_mode_time = line.split('total:')[1].split('us')[0]
                    fileout1.write(av1_search_palette_mode_time)
                    fileout1.write(';')

                # BLOCK TIMERS PARSING

                if 'Partition times for pass 0' in line:
                    i+=23

                if 'BLOCK_' in line:

                    fileout2.write('\n')

                    seq = lines[1].split('.')[0]
                    seq = seq.split('/')[-1]
                    fileout2.write(seq)
                    fileout2.write(';')

                    param = lines[2].split('coded')[1]
                    if param == '.webm\n':
                        param = 'orig'
                    else:
                        param = param.split('.')[0].strip('_')
                        if len(param) > 50:
                            param = 'all_disable'

                    fileout2.write(param)
                    fileout2.write(';')

                    fileout2.write('%s'%cq)
                    fileout2.write(';')

                if 'BLOCK_4X4' in line:

                    BLOCK_4X4C = line.split(' ')[0].strip('x')
                    BLOCK_4X4N = line.split(' ')[1]
                    BLOCK_4X4T = line.split(' ')[2].strip('\n')
                    fileout2.write('%s;%s;%s'%(BLOCK_4X4N, BLOCK_4X4T, BLOCK_4X4C))
                    fileout2.write(';')

                if 'BLOCK_4X8' in line:

                    BLOCK_4X4C = line.split(' ')[0].strip('x')
                    BLOCK_4X8N = line.split(' ')[1]
                    BLOCK_4X4T = line.split(' ')[2].strip('\n')
                    fileout2.write('%s;%s;%s'%(BLOCK_4X8N, BLOCK_4X4T, BLOCK_4X4C))
                    fileout2.write(';')

                if 'BLOCK_8X4' in line:

                    BLOCK_8X4C = line.split(' ')[0].strip('x')
                    BLOCK_8X4N = line.split(' ')[1]
                    BLOCK_8X4T = line.split(' ')[2].strip('\n')
                    fileout2.write('%s;%s;%s'%(BLOCK_8X4N, BLOCK_8X4T, BLOCK_8X4C))
                    fileout2.write(';')

                if 'BLOCK_8X8' in line:

                    BLOCK_8X8C = line.split(' ')[0].strip('x')
                    BLOCK_8X8N = line.split(' ')[1]
                    BLOCK_8X8T = line.split(' ')[2].strip('\n')
                    fileout2.write('%s;%s;%s'%(BLOCK_8X8N, BLOCK_8X8T, BLOCK_8X8C))
                    fileout2.write(';')

                if 'BLOCK_8X16' in line:

                    BLOCK_8X16C = line.split(' ')[0].strip('x')
                    BLOCK_8X16N = line.split(' ')[1]
                    BLOCK_8X16T = line.split(' ')[2].strip('\n')
                    fileout2.write('%s;%s;%s'%(BLOCK_8X16N, BLOCK_8X16T, BLOCK_8X16C))
                    fileout2.write(';')

                if 'BLOCK_16X8' in line:

                    BLOCK_16X8C = line.split(' ')[0].strip('x')
                    BLOCK_16X8N = line.split(' ')[1]
                    BLOCK_16X8T = line.split(' ')[2].strip('\n')
                    fileout2.write('%s;%s;%s'%(BLOCK_16X8N, BLOCK_16X8T, BLOCK_16X8C))
                    fileout2.write(';')

                if 'BLOCK_16X16' in line:

                    BLOCK_16X16C = line.split(' ')[0].strip('x')
                    BLOCK_16X16N = line.split(' ')[1]
                    BLOCK_16X16T = line.split(' ')[2].strip('\n')
                    fileout2.write('%s;%s;%s'%(BLOCK_16X16N, BLOCK_16X16T, BLOCK_16X16C))
                    fileout2.write(';')

                if 'BLOCK_16X32' in line:

                    BLOCK_16X32C = line.split(' ')[0].strip('x')
                    BLOCK_16X32N = line.split(' ')[1]
                    BLOCK_16X32T = line.split(' ')[2].strip('\n')
                    fileout2.write('%s;%s;%s'%(BLOCK_16X32N, BLOCK_16X32T, BLOCK_16X32C))
                    fileout2.write(';')

                if 'BLOCK_32X16' in line:

                    BLOCK_32X16C = line.split(' ')[0].strip('x')
                    BLOCK_32X16N = line.split(' ')[1]
                    BLOCK_32X16T = line.split(' ')[2].strip('\n')
                    fileout2.write('%s;%s;%s'%(BLOCK_32X16N, BLOCK_32X16T, BLOCK_32X16C))
                    fileout2.write(';')

                if 'BLOCK_32X32' in line:

                    BLOCK_32X32C = line.split(' ')[0].strip('x')
                    BLOCK_32X32N = line.split(' ')[1]
                    BLOCK_32X32T = line.split(' ')[2].strip('\n')
                    fileout2.write('%s;%s;%s'%(BLOCK_32X32N, BLOCK_32X32T, BLOCK_32X32C))
                    fileout2.write(';')

                if 'BLOCK_32X64' in line:

                    BLOCK_32X64C = line.split(' ')[0].strip('x')
                    BLOCK_32X64N = line.split(' ')[1]
                    BLOCK_32X64T = line.split(' ')[2].strip('\n')
                    fileout2.write('%s;%s;%s'%(BLOCK_32X64N, BLOCK_32X64T, BLOCK_32X64C))
                    fileout2.write(';')

                if 'BLOCK_64X32' in line:

                    BLOCK_64X32C = line.split(' ')[0].strip('x')
                    BLOCK_64X32N = line.split(' ')[1]
                    BLOCK_64X32T = line.split(' ')[2].strip('\n')
                    fileout2.write('%s;%s;%s'%(BLOCK_64X32N, BLOCK_64X32T, BLOCK_64X32C))
                    fileout2.write(';')

                if 'BLOCK_64X64' in line:

                    BLOCK_64X64C = line.split(' ')[0].strip('x')
                    BLOCK_64X64N = line.split(' ')[1]
                    BLOCK_64X64T = line.split(' ')[2].strip('\n')
                    fileout2.write('%s;%s;%s'%(BLOCK_64X64N, BLOCK_64X64T, BLOCK_64X64C))
                    fileout2.write(';')

                if 'BLOCK_64X128' in line:

                    BLOCK_64X128C = line.split(' ')[0].strip('x')
                    BLOCK_64X128N = line.split(' ')[1]
                    BLOCK_64X128T = line.split(' ')[2].strip('\n')
                    fileout2.write('%s;%s;%s'%(BLOCK_64X128N, BLOCK_64X128T, BLOCK_64X128C))
                    fileout2.write(';')

                if 'BLOCK_128X64' in line:

                    BLOCK_128X64C = line.split(' ')[0].strip('x')
                    BLOCK_128X64N = line.split(' ')[1]
                    BLOCK_128X64T = line.split(' ')[2].strip('\n')
                    fileout2.write('%s;%s;%s'%(BLOCK_128X64N, BLOCK_128X64T, BLOCK_128X64C))
                    fileout2.write(';')

                if 'BLOCK_128X128' in line:

                    BLOCK_128X128C = line.split(' ')[0].strip('x')
                    BLOCK_128X128N = line.split(' ')[1]
                    BLOCK_128X128T = line.split(' ')[2].strip('\n')
                    fileout2.write('%s;%s;%s'%(BLOCK_128X128N, BLOCK_128X128T, BLOCK_128X128C))
                    fileout2.write(';')

                if 'BLOCK_4X16' in line:

                    BLOCK_4X16C = line.split(' ')[0].strip('x')
                    BLOCK_4X16N = line.split(' ')[1]
                    BLOCK_4X16T = line.split(' ')[2].strip('\n')
                    fileout2.write('%s;%s;%s'%(BLOCK_4X16N, BLOCK_4X16T, BLOCK_4X16C))
                    fileout2.write(';')

                if 'BLOCK_16X4' in line:

                    BLOCK_16X4C = line.split(' ')[0].strip('x')
                    BLOCK_16X4N = line.split(' ')[1]
                    BLOCK_16X4T = line.split(' ')[2].strip('\n')
                    fileout2.write('%s;%s;%s'%(BLOCK_16X4N, BLOCK_16X4T, BLOCK_16X4C))
                    fileout2.write(';')

                if 'BLOCK_8X32' in line:

                    BLOCK_8X32C = line.split(' ')[0].strip('x')
                    BLOCK_8X32N = line.split(' ')[1]
                    BLOCK_8X32T = line.split(' ')[2].strip('\n')
                    fileout2.write('%s;%s;%s'%(BLOCK_8X32N, BLOCK_8X32T, BLOCK_8X32C))
                    fileout2.write(';')

                if 'BLOCK_32X8' in line:

                    BLOCK_32X8C = line.split(' ')[0].strip('x')
                    BLOCK_32X8N = line.split(' ')[1]
                    BLOCK_32X8T = line.split(' ')[2].strip('\n')
                    fileout2.write('%s;%s;%s'%(BLOCK_32X8N, BLOCK_32X8T, BLOCK_32X8C))
                    fileout2.write(';')

                if 'BLOCK_16X64' in line:

                    BLOCK_16X64C = line.split(' ')[0].strip('x')
                    BLOCK_16X64N = line.split(' ')[1]
                    BLOCK_16X64T = line.split(' ')[2].strip('\n')
                    fileout2.write('%s;%s;%s'%(BLOCK_16X64N, BLOCK_16X64T, BLOCK_16X64C))
                    fileout2.write(';')

                if 'BLOCK_64X16' in line:

                    BLOCK_64X16C = line.split(' ')[0].strip('x')
                    BLOCK_64X16N = line.split(' ')[1]
                    BLOCK_64X16T = line.split(' ')[2].strip('\n')
                    fileout2.write('%s;%s;%s'%(BLOCK_64X16N, BLOCK_64X16T, BLOCK_64X16C))
                    fileout2.write(';')

                # Stream 0 PSNR (Overall/Avg/Y/U/V) 40.218 40.246 39.228 42.774 44.485 1244640 bps  667502 ms

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

            fileout1.close()
            fileout2.close()
            fileout3.close()

            arq+=1
arqs = ps*fs*len(CQS)
print('Fim do parsing! Concluidos %s de %s arquivos!'%(arq,arqs))
