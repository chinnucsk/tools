#!/bin/bash

IS_ROTATED='a'
LOG='b'

while [ "$IS_ROTATED" != "$LOG" ]
do
  LOG=`ls -tr /var/home/httpd_logs/access_log.201*[0-9]|tail -1`
  sec=`date -d '1 second ago' '+%d/%b/%Y:%H:%M:%S'`
  num=`nice tail -40000 "$LOG" | nice grep "$sec" |                                                \
    nice awk 'BEGIN{tout=60000;};                                                                  \
      / \"POST \/rtb\/google/                                                                      \
      {                                                                                            \
        g_nr++;                                                                                    \
        g_sz+=$(NF - 4);                                                                           \
        if( $(NF - 5) != 200     ){ g_e++ };                                                       \
        if( $(NF - 4) == 2       ){ g_nb++; g_nbsz+=$(NF - 4) };                                   \
        if( $(NF - 4) == 0       ){ $(NF - 1) < tout  ? g_pd++ : g_bd++; g_nbsz+=$(NF - 4) };      \
        if( $(NF - 1) > (tout-1) ){ g_t++};                                                        \
      } ;                                                                                          \
      / \"GET \/rtb\/cwb/                                                                          \
      {                                                                                            \
        c_nr++;                                                                                    \
        c_sz+=$(NF - 4);                                                                           \
        if( $(NF - 5) != 200     ){ c_e++ };                                                       \
        if( $(NF - 4) == 14      ){ c_nb++; c_nbsz+=$(NF - 4) };                                   \
        if( $(NF - 4) == 16      ){ $(NF - 1) < tout  ? c_pd++ : c_bd++; c_nbsz+=$(NF - 4) };      \
        if( $(NF - 1) > (tout-1) ){ c_t++};                                                        \
      } ;                                                                                          \
      / \"POST \/rtb\/rbc/                                                                         \
      {                                                                                            \
        r_nr++;                                                                                    \
        r_sz+=$(NF - 4);                                                                           \
        if( $(NF - 5) != 200     ){ r_e++ };                                                       \
        if( $(NF - 4) == 14      ){ r_nb++; r_nbsz+=$(NF - 4) };                                   \
        if( $(NF - 4) == 16      ){ $(NF - 1) < tout  ? r_pd++ : r_bd++; r_nbsz+=$(NF - 4) };      \
        if( $(NF - 1) > (tout-1) ){ r_t++};                                                        \
      } ;                                                                                          \
      / \"POST \/rtb\/apx/                                                                         \
      {                                                                                            \
        a_nr++;                                                                                    \
        a_sz+=$(NF - 4);                                                                           \
        if( $(NF - 5) != 200     ){ a_e++ };                                                       \
        if( $(NF - 4) == 44      ){ a_nb++; a_nbsz+=$(NF - 4) };                                   \
        if( $(NF - 4) == 46      ){ $(NF - 1) < tout  ? a_pd++ : a_bd++; a_nbsz+=$(NF - 4) };      \
        if( $(NF - 1) > (tout-1) ){ a_t++};                                                        \
      } ;                                                                                          \
      / \"POST \/rtb\/esm/                                                                         \
      {                                                                                            \
        e_nr++;                                                                                    \
        e_sz+=$(NF - 4);                                                                           \
        if( $(NF - 5) != 200     ){ e_e++ };                                                       \
        if( $(NF - 4) == 2       ){ e_nb++; e_nbsz+=$(NF - 4) };                                   \
        if( $(NF - 4) == "-"     ){ $(NF - 1) < tout  ? e_pd++ : e_bd++; e_nbsz+=$(NF - 4) };      \
        if( $(NF - 1) > (tout-1) ){ e_t++};                                                        \
      } ;                                                                                          \
      / \"GET \/rtb\/aml/                                                                          \
      {                                                                                            \
        m_nr++;                                                                                    \
        m_sz+=$(NF - 4);                                                                           \
        if( $(NF - 5) != 200     ){ m_e++ };                                                       \
        if( $(NF - 4) == 32      ){ m_nb++; m_nbsz+=$(NF - 4) };                                   \
        if( $(NF - 4) == 34      ){ $(NF - 1) < tout  ? m_pd++ : m_bd++; m_nbsz+=$(NF - 4) };      \
        if( $(NF - 1) > (tout-1) ){ m_t++};                                                        \
      } ;                                                                                          \
      / \"GET \/rtb\/pbm/                                                                          \
      {                                                                                            \
        p_nr++;                                                                                    \
        p_sz+=$(NF - 4);                                                                           \
        if( $(NF - 5) != 200     ){ p_e++ };                                                       \
        if( $(NF - 4) == 93      ){ p_nb++; p_nbsz+=$(NF - 4) };                                   \
        if( $(NF - 1) > (tout-1) ){ p_t++};                                                        \
      } ;                                                                                          \
      / \"POST \/rtb\/fb/                                                                          \
      {                                                                                            \
        f_nr++;                                                                                    \
        f_sz+=$(NF - 4);                                                                           \
        if( $(NF - 5) != 200     ){ f_e++ };                                                       \
        if( $NF ~ /"1"/          ){ f_pd++; f_nbsz+=$(NF - 4) }                                    \
        if( $(NF - 1) > (tout-1) ){ f_t++; if( $NF ~ /"0"/ ){ f_bd++; f_nbsz+=$(NF - 4) } };       \
      } ;                                                                                          \
      / \"POST \/rtb\/opx/                                                                         \
      {                                                                                            \
        o_nr++;                                                                                    \
        o_sz+=$(NF - 4);                                                                           \
        if( $(NF - 5) != 200     ){ o_e++ };                                                       \
        if( $(NF - 4) == 40      ){ o_nb++; o_nbsz+=$(NF - 4) };                                   \
        if( $NF ~ /"1"/          ){ o_pd++; o_nbsz+=$(NF - 4) }                                    \
        if( $(NF - 1) > (tout-1) ){ o_t++; if( $NF ~ /"0"/ ){ o_bd++; o_nbsz+=$(NF - 4) } };       \
      } ;                                                                                          \
      END                                                                                          \
      {                                                                                            \
        if ( 0 != a_nr) { printf( "A %-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d\n", \
                                  a_nr, a_t, a_bd, a_pd, a_e, a_nb,                                \
                                  a_nr-a_nb-a_e-a_pd-a_bd,                                         \
                                  ((a_nr-a_nb-a_e-a_pd-a_bd)*100)/a_nr,                            \
                                  ((a_e+a_pd+a_bd)*100)/a_nr,                                      \
                                  (a_sz-a_nbsz)/1000, a_nbsz/1000, ((a_sz-a_nbsz)*100)/a_sz ); }   \
        if ( 0 != c_nr) { printf( "C %-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d\n", \
                                  c_nr, c_t, c_bd, c_pd, c_e, c_nb,                                \
                                  c_nr-c_nb-c_e-c_pd-c_bd,                                         \
                                  ((c_nr-c_nb-c_e-c_pd-c_bd)*100)/c_nr,                            \
                                  ((c_e+c_pd+c_bd)*100)/c_nr,                                      \
                                  (c_sz-c_nbsz)/1000, c_nbsz/1000, ((c_sz-c_nbsz)*100)/c_sz ); }   \
        if ( 0 != e_nr) { printf( "E %-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d\n", \
                                  e_nr, e_t, e_bd, e_pd, e_e, e_nb,                                \
                                  e_nr-e_nb-e_e-e_pd-e_bd,                                         \
                                  ((e_nr-e_nb-e_e-e_pd-e_bd)*100)/e_nr,                            \
                                  ((e_e+e_pd+e_bd)*100)/e_nr,                                      \
                                  (e_sz-e_nbsz)/1000, e_nbsz/1000, ((e_sz-e_nbsz)*100)/e_sz ); }   \
        if ( 0 != f_nr) { printf( "F %-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d\n", \
                                  f_nr, f_t, f_bd, f_pd, f_e, f_nb,                                \
                                  f_nr-f_nb-f_e-f_pd-f_bd,                                         \
                                  ((f_nr-f_nb-f_e-f_pd-f_bd)*100)/f_nr,                            \
                                  ((f_e+f_pd+f_bd)*100)/f_nr,                                      \
                                  (f_sz-f_nbsz)/1000, f_nbsz/1000, ((f_sz-f_nbsz)*100)/f_sz ); }   \
        if ( 0 != g_nr) { printf( "G %-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d\n", \
                                  g_nr, g_t, g_bd, g_pd, g_e, g_nb,                                \
                                  g_nr-g_nb-g_e-g_pd-g_bd,                                         \
                                  ((g_nr-g_nb-g_e-g_pd-g_bd)*100)/g_nr,                            \
                                  ((g_e+g_pd+g_bd)*100)/g_nr,                                      \
                                  (g_sz-g_nbsz)/1000, g_nbsz/1000, ((g_sz-g_nbsz)*100)/g_sz ); }   \
        if ( 0 != m_nr) { printf( "M %-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d\n", \
                                  m_nr, m_t, m_bd, m_pd, m_e, m_nb,                                \
                                  m_nr-m_nb-m_e-m_pd-m_bd,                                         \
                                  ((m_nr-m_nb-m_e-m_pd-m_bd)*100)/m_nr,                            \
                                  ((m_e+m_pd+m_bd)*100)/m_nr,                                      \
                                  (m_sz-m_nbsz)/1000, m_nbsz/1000, ((m_sz-m_nbsz)*100)/m_sz ); }   \
        if ( 0 != o_nr) { printf( "O %-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d\n", \
                                  o_nr, o_t, o_bd, o_pd, o_e, o_nb,                                \
                                  o_nr-o_nb-o_e-o_pd-o_bd,                                         \
                                  ((o_nr-o_nb-o_e-o_pd-o_bd)*100)/o_nr,                            \
                                  ((o_e+o_pd+o_bd)*100)/o_nr,                                      \
                                  (o_sz-o_nbsz)/1000, o_nbsz/1000, ((o_sz-o_nbsz)*100)/o_sz ); }   \
        if ( 0 != p_nr) { printf( "P %-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d\n", \
                                  p_nr, p_t, p_bd, p_pd, p_e, p_nb,                                \
                                  p_nr-p_nb-p_e-p_pd-p_bd,                                         \
                                  ((p_nr-p_nb-p_e-p_pd-p_bd)*100)/p_nr,                            \
                                  ((p_e+p_pd+p_bd)*100)/p_nr,                                      \
                                  (p_sz-p_nbsz)/1000, p_nbsz/1000, ((p_sz-p_nbsz)*100)/p_sz ); }   \
        if ( 0 != r_nr) { printf( "R %-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d\n", \
                                  r_nr, r_t, r_bd, r_pd, r_e, r_nb,                                \
                                  r_nr-r_nb-r_e-r_pd-r_bd,                                         \
                                  ((r_nr-r_nb-r_e-r_pd-r_bd)*100)/r_nr,                            \
                                  ((r_e+r_pd+r_bd)*100)/r_nr,                                      \
                                  (r_sz-r_nbsz)/1000, r_nbsz/1000, ((r_sz-r_nbsz)*100)/r_sz ); }   \
        nr = a_nr+c_nr+e_nr+f_nr+g_nr+m_nr+o_nr+p_nr+r_nr;                                         \
        t  = a_t+c_t+e_t+f_t+g_t+m_t+o_t+p_t+r_t;                                                  \
        bd = a_bd+c_bd+e_bd+f_bd+g_bd+m_bd+o_bd+p_bd+r_bd;                                         \
        pd = a_pd+c_pd+e_pd+f_pd+g_pd+m_pd+o_pd+p_pd+r_pd;                                         \
        e  = a_e+c_e+e_e+f_e+g_e+m_e+o_e+p_e+r_e;                                                  \
        nb = a_nb+c_nb+e_nb+f_nb+g_nb+m_nb+o_nb+p_nb+r_nb;                                         \
        sz = a_sz+c_sz+e_sz+f_sz+g_sz+m_sz+o_sz+p_sz+r_sz;                                         \
        nbsz = a_nbsz+c_nbsz+e_nbsz+f_nbsz+g_nbsz+m_nbsz+o_nbsz+p_nbsz+r_nbsz;                     \
                          printf( "  %-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d\n", \
                                  nr, t, bd, pd, e, nb,                                            \
                                  nr-nb-e-pd-bd,                                                   \
                                  ((nr-nb-e-pd-bd)*100)/nr,                                        \
                                  ((e+pd+bd)*100)/nr,                                              \
                                  (sz-nbsz)/1000, nbsz/1000, ((sz-nbsz)*100)/sz );                 \
      }'`
  IS_ROTATED=`ls -tr /var/home/httpd_logs/access_log.201*[0-9]|tail -1`
done

[ -z "$1" ] &&  echo -e "X BidReq  Long    BdrOut  PxyOut  Err     NoBid   EffBids % EffBids % BidLost SzEB,KB SzNB,KB % Sz EB"
echo "$num"



