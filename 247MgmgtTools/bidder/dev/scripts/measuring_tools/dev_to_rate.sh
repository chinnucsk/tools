#!/bin/bash

IS_ROTATED='a'
LOG='b'

while [ "$IS_ROTATED" != "$LOG" ]
do
  LOG=`ls -tr /var/home/httpd_logs/access_log.201*[0-9]|tail -1`
  sec=`date -d '1 second ago' '+%d/%b/%Y:%H:%M:%S'`
  num=`nice tail -40000 "$LOG" | nice grep "$sec" |                                                \
    nice awk 'BEGIN{tout=60000;};                                                                  \
      "\"POST" == $6  &&  "/rtb/google" == $7                                                      \
      {                                                                                            \
        g_nr++;                                                                                    \
        g_sz+=$(NF - 3);                                                                           \
        if( $(NF - 4) != 200 ){ g_e++ };                                                           \
        if( $(NF - 3) == 2   ){ g_nb++; g_nbsz+=$(NF - 3) };                                       \
        if( $(NF - 3) == 0   ){ $NF < tout  ? g_pd++ : g_bd++; g_nbsz+=$(NF - 3) };                \
        if( $NF > (tout-1)   ){ g_t++};                                                            \
      } ;                                                                                          \
      "\"GET" == $6  &&  $7 ~ "^/rtb/cwb"                                                          \
      {                                                                                            \
        c_nr++;                                                                                    \
        c_sz+=$(NF - 3);                                                                           \
        if( $(NF - 4) != 200 ){ c_e++ };                                                           \
        if( $(NF - 3) == 14  ){ c_nb++; c_nbsz+=$(NF - 3) };                                       \
        if( $(NF - 3) == 16  ){ $NF < tout  ? c_pd++ : c_bd++; c_nbsz+=$(NF - 3) };                \
        if( $NF > (tout-1)   ){ c_t++};                                                            \
      } ;                                                                                          \
      "\"POST" == $6  &&  $7 ~ "^/rtb/rbc"                                                         \
      {                                                                                            \
        r_nr++;                                                                                    \
        r_sz+=$(NF - 3);                                                                           \
        if( $(NF - 4) != 200 ){ r_e++ };                                                           \
        if( $(NF - 3) == 14  ){ r_nb++; r_nbsz+=$(NF - 3) };                                       \
        if( $(NF - 3) == 16  ){ $NF < tout  ? r_pd++ : r_bd++; r_nbsz+=$(NF - 3) };                \
        if( $NF > (tout-1)   ){ r_t++};                                                            \
      } ;                                                                                          \
      "\"POST" == $6  &&  $7 ~ "^/rtb/apx"                                                         \
      {                                                                                            \
        a_nr++;                                                                                    \
        a_sz+=$(NF - 3);                                                                           \
        if( $(NF - 4) != 200 ){ a_e++ };                                                           \
        if( $(NF - 3) == 44  ){ a_nb++; a_nbsz+=$(NF - 3) };                                       \
        if( $(NF - 3) == 46  ){ $NF < tout  ? a_pd++ : a_bd++; a_nbsz+=$(NF - 3) };                \
        if( $NF > (tout-1)   ){ a_t++};                                                            \
      } ;                                                                                          \
      "\"POST" == $6  &&  "/rtb/esm" == $7                                                         \
      {                                                                                            \
        e_nr++;                                                                                    \
        e_sz+=$(NF - 3);                                                                           \
        if( $(NF - 4) != 200 ){ e_e++ };                                                           \
        if( $(NF - 3) == 2   ){ e_nb++; e_nbsz+=$(NF - 3) };                                       \
        if( $(NF - 3) == "-" ){ $NF < tout  ? e_pd++ : e_bd++; e_nbsz+=$(NF - 3) };                \
        if( $NF > (tout-1)   ){ e_t++};                                                            \
      } ;                                                                                          \
      "\"GET" == $6  &&  $7 ~ "^/rtb/aml"                                                          \
      {                                                                                            \
        m_nr++;                                                                                    \
        m_sz+=$(NF - 3);                                                                           \
        if( $(NF - 4) != 200 ){ m_e++ };                                                           \
        if( $(NF - 3) == 32  ){ m_nb++; m_nbsz+=$(NF - 3) };                                       \
        if( $(NF - 3) == 34  ){ $NF < tout  ? m_pd++ : m_bd++; m_nbsz+=$(NF - 3) };                \
        if( $NF > (tout-1)   ){ m_t++};                                                            \
      } ;                                                                                          \
      "\"GET" == $6  &&  $7 ~ "^/rtb/pbm"                                                          \
      {                                                                                            \
        p_nr++;                                                                                    \
        p_sz+=$(NF - 3);                                                                           \
        if( $(NF - 4) != 200 ){ p_e++ };                                                           \
        if( $(NF - 3) == 93  ){ p_nb++; p_nbsz+=$(NF - 3) };                                       \
        if( $NF > (tout-1)   ){ p_t++};                                                            \
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
        nr = a_nr+c_nr+e_nr+g_nr+m_nr+p_nr+r_nr;                                                   \
        t  = a_t+c_t+e_t+g_t+m_t+p_t+r_t;                                                          \
        bd = a_bd+c_bd+e_bd+g_bd+m_bd+p_bd+r_bd;                                                   \
        pd = a_pd+c_pd+e_pd+g_pd+m_pd+p_pd+r_pd;                                                   \
        e  = a_e+c_e+e_e+g_e+m_e+p_e+r_e;                                                          \
        nb = a_nb+c_nb+e_nb+g_nb+m_nb+p_nb+r_nb;                                                   \
        sz = a_sz+c_sz+e_sz+g_sz+m_sz+p_sz+r_sz;                                                   \
        nbsz = a_nbsz+c_nbsz+e_nbsz+g_nbsz+m_nbsz+p_nbsz+r_nbsz;                                   \
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


