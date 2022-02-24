# av1_pesquisa

# Drive com videos do AV1

https://drive.google.com/drive/folders/1QyL9iqsmzeeeXID8ztCC-s9vjnk44Gtu?usp=sharing

# Parametros de Teste

5.3.  Operating Points

   Four operating modes are defined.  High latency is intended for on
   demand streaming, one-to-many live streaming, and stored video.  Low
   latency is intended for videoconferencing and remote access.  Both of
   these modes come in CQP and unconstrained variants.  When testing
   still image sets, such as subset1, high latency CQP mode should be
   used.

5.3.1.  Common settings

   Encoders should be configured to their best settings when being
   compared against each other:

   o  av1: -codec=av1 -ivf -frame-parallel=0 -tile-columns=0 -cpu-used=0
      -threads=1

5.3.2.  High Latency CQP

   High Latency CQP is used for evaluating incremental changes to a
   codec.  This method is well suited to compare codecs with similar
   coding tools.  It allows codec features with intrinsic frame delay.

   o  av1: -end-usage=q -cq-level=x -auto-alt-ref=2

5.3.3.  Low Latency CQP

   Low Latency CQP is used for evaluating incremental changes to a
   codec.  This method is well suited to compare codecs with similar
   coding tools.  It requires the codec to be set for zero intrinsic
   frame delay.

   o  av1: -end-usage=q -cq-level=x -lag-in-frames=0

5.3.4.  Unconstrained High Latency

   The encoder should be run at the best quality mode available, using
   the mode that will provide the best quality per bitrate (VBR or
   constant quality mode).  Lookahead and/or two-pass are allowed, if
   supported.  One parameter is provided to adjust bitrate, but the
   units are arbitrary.  Example configurations follow:

   o  av1: -end-usage=q -cq-level=x -lag-in-frames=25 -auto-alt-ref=2

5.3.5.  Unconstrained Low Latency

   The encoder should be run at the best quality mode available, using
   the mode that will provide the best quality per bitrate (VBR or
   constant quality mode), but no frame delay, buffering, or lookahead
   is allowed.  One parameter is provided to adjust bitrate, but the
   units are arbitrary.  Example configurations follow:

   o  av1: -end-usage=q -cq-level=x -lag-in-frames=0
