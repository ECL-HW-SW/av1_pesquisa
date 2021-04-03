/*
 * Copyright (c) 2016, Alliance for Open Media. All rights reserved
 *
 * This source code is subject to the terms of the BSD 2 Clause License and
 * the Alliance for Open Media Patent License 1.0. If the BSD 2 Clause License
 * was not distributed with this source code in the LICENSE file, you can
 * obtain it at www.aomedia.org/license/software. If the Alliance for Open
 * Media Patent License 1.0 was not distributed with this source code in the
 * PATENTS file, you can obtain it at www.aomedia.org/license/patent.
 */
#ifndef AOM_APPS_AOMENC_H_
#define AOM_APPS_AOMENC_H_

#include "aom/aom_codec.h"
#include "aom/aom_encoder.h"
#include <time.h>
#ifdef __cplusplus
extern "C" {
#endif

enum TestDecodeFatality {
  TEST_DECODE_OFF,
  TEST_DECODE_FATAL,
  TEST_DECODE_WARN,
};

// // @grellert ECL timers

// typedef struct {
//   time_t block_timer_begin[22];
//   time_t block_timer_end[22];
//   double block_timer_acc[22];
//   unsigned pass;
// } ECLTimers;

typedef enum {
  I420,  // 4:2:0 8+ bit-depth
  I422,  // 4:2:2 8+ bit-depth
  I444,  // 4:4:4 8+ bit-depth
  YV12,  // 4:2:0 with uv flipped, only 8-bit depth
} ColorInputType;

/* Configuration elements common to all streams. */
struct AvxEncoderConfig {
  aom_codec_iface_t *codec;
  int passes;
  int pass;
  unsigned int usage;
  ColorInputType color_type;
  int quiet;
  int verbose;
  int limit;
  int skip_frames;
  int show_psnr;
  enum TestDecodeFatality test_decode;
  int have_framerate;
  struct aom_rational framerate;
  int debug;
  int show_q_hist_buckets;
  int show_rate_hist_buckets;
  int disable_warnings;
  int disable_warning_prompt;
  int experimental_bitstream;
  aom_chroma_sample_position_t csp;
  cfg_options_t encoder_config;

  //@grellert
  ECLTimers ecl_timers;

  int disable_prune_partitions_before_search;
  int disable_prune_partitions_after_split;
  int disable_prune_4_way_partition_search;  // seg fault

  int disable_av1_prune_ab_partitions;  // seg fault
  int disable_av1_ml_prune_4_partition;
  int disable_prune_4_partition_using_split_info;
  int disable_av1_ml_prune_rect_partition;
  int disable_prune_partitions_after_none;
};

#ifdef __cplusplus
}  // extern "C"
#endif

#endif  // AOM_APPS_AOMENC_H_
