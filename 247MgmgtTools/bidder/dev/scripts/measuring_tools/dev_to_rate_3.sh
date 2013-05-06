#!/bin/bash

IS_ROTATED='a'
LOG='b'

#enum eBidTrace
#{
#    eBidUndefined = 0,
#    eBid          = 1,
#    eNoBid        = 2,
#    eBidSkipped   = 3,
#    eBidTimeout   = 4,
#    eBidNoAvail   = 5
#};

while [ "$IS_ROTATED" != "$LOG" ]
do
  LOG=`ls -tr /var/home/httpd_logs/access_log.201*[0-9]|tail -1`
  sec="$1"
  src="cat"
  [ -z "${sec}" ]  ||  [ "no_header" == "${sec}" ]  &&  { sec=$(date -d '1 second ago' '+%d/%b/%Y:%H:%M:%S') ; src="tail -n 40000" ; }
  num=$(nice ${src} "$LOG" | nice grep "$sec" |                                                    \
    nice awk 'BEGIN{tout=60000;};                                                                  \
      / \"POST \/rtb\/google /                                                                     \
      {                                                                                            \
        g_nr++;                                                                                    \
        g_sz+=$(NF - 4);                                                                           \
        g_tt+=$(NF - 1); g_tb+=$(NF - 1);                                                          \
        if( $(NF - 5) != 200     ){ g_e++; g_tb-=$(NF - 1) };                                      \
        if(      $NF ~ /"1"/     ){ g_eb++ }                                                       \
        else if( $NF ~ /"2"/     ){ g_nb++; g_nbsz+=$(NF - 4) }                                    \
        else if( $NF ~ /"3"/     ){ g_pd++; g_nbsz+=$(NF - 4); g_tb-=$(NF - 1) }                   \
        else if( $NF ~ /"4"/     ){ g_bd++; g_nbsz+=$(NF - 4); g_tb-=$(NF - 1) }                   \
        else if( $NF ~ /"0"/     ){ g_br++; g_nbsz+=$(NF - 4); g_tb-=$(NF - 1) };                  \
        if( $(NF - 1) > (tout-1) ){ g_t++ };                                                       \
      } ;                                                                                          \
      / \"GET \/rtb\/cwb?/                                                                         \
      {                                                                                            \
        c_nr++;                                                                                    \
        c_sz+=$(NF - 4);                                                                           \
        c_tt+=$(NF - 1); c_tb+=$(NF - 1);                                                          \
        if( $(NF - 5) != 200     ){ c_e++; c_tb-=$(NF - 1) };                                      \
        if(      $NF ~ /"1"/     ){ c_eb++ }                                                       \
        else if( $NF ~ /"2"/     ){ c_nb++; c_nbsz+=$(NF - 4) }                                    \
        else if( $NF ~ /"3"/     ){ c_pd++; c_nbsz+=$(NF - 4); c_tb-=$(NF - 1) }                   \
        else if( $NF ~ /"4"/     ){ c_bd++; c_nbsz+=$(NF - 4); c_tb-=$(NF - 1) }                   \
        else if( $NF ~ /"0"/     ){ c_br++; c_nbsz+=$(NF - 4); c_tb-=$(NF - 1) };                  \
        if( $(NF - 1) > (tout-1) ){ c_t++ };                                                       \
      } ;                                                                                          \
      / \"POST \/rtb\/rbc /                                                                        \
      {                                                                                            \
        r_nr++;                                                                                    \
        r_sz+=$(NF - 4);                                                                           \
        r_tt+=$(NF - 1); r_tb+=$(NF - 1);                                                          \
        if( $(NF - 5) != 200     ){ r_e++; r_tb-=$(NF - 1) };                                      \
        if(      $NF ~ /"1"/     ){ r_eb++ }                                                       \
        else if( $NF ~ /"2"/     ){ r_nb++; r_nbsz+=$(NF - 4) }                                    \
        else if( $NF ~ /"3"/     ){ r_pd++; r_nbsz+=$(NF - 4); r_tb-=$(NF - 1) }                   \
        else if( $NF ~ /"4"/     ){ r_bd++; r_nbsz+=$(NF - 4); r_tb-=$(NF - 1) }                   \
        else if( $NF ~ /"0"/     ){ r_br++; r_nbsz+=$(NF - 4); r_tb-=$(NF - 1) };                  \
        if( $(NF - 1) > (tout-1) ){ r_t++ };                                                       \
      } ;                                                                                          \
      / \"POST \/rtb\/apx /                                                                        \
      {                                                                                            \
        a_nr++;                                                                                    \
        a_sz+=$(NF - 4);                                                                           \
        a_tt+=$(NF - 1); a_tb+=$(NF - 1);                                                          \
        if( $(NF - 5) != 200     ){ a_e++; a_tb-=$(NF - 1) };                                      \
        if(      $NF ~ /"1"/     ){ a_eb++ }                                                       \
        else if( $NF ~ /"2"/     ){ a_nb++; a_nbsz+=$(NF - 4) }                                    \
        else if( $NF ~ /"3"/     ){ a_pd++; a_nbsz+=$(NF - 4); a_tb-=$(NF - 1) }                   \
        else if( $NF ~ /"4"/     ){ a_bd++; a_nbsz+=$(NF - 4); a_tb-=$(NF - 1) }                   \
        else if( $NF ~ /"0"/     ){ a_br++; a_nbsz+=$(NF - 4); a_tb-=$(NF - 1) };                  \
        if( $(NF - 1) > (tout-1) ){ a_t++ };                                                       \
      } ;                                                                                          \
      / \"POST \/rtb\/esm2 /                                                                       \
      {                                                                                            \
        e_nr++;                                                                                    \
        e_sz+=$(NF - 4);                                                                           \
        e_tt+=$(NF - 1); e_tb+=$(NF - 1);                                                          \
        if( $(NF - 5) != 200     ){ e_e++; e_tb-=$(NF - 1) };                                      \
        if(      $NF ~ /"1"/     ){ e_eb++ }                                                       \
        else if( $NF ~ /"2"/     ){ e_nb++; e_nbsz+=$(NF - 4) }                                    \
        else if( $NF ~ /"3"/     ){ e_pd++; e_nbsz+=$(NF - 4); e_tb-=$(NF - 1) }                   \
        else if( $NF ~ /"4"/     ){ e_bd++; e_nbsz+=$(NF - 4); e_tb-=$(NF - 1) }                   \
        else if( $NF ~ /"0"/     ){ e_br++; e_nbsz+=$(NF - 4); e_tb-=$(NF - 1) };                  \
        if( $(NF - 1) > (tout-1) ){ e_t++ };                                                       \
      } ;                                                                                          \
      / \"GET \/rtb\/aml?/                                                                         \
      {                                                                                            \
        m_nr++;                                                                                    \
        m_sz+=$(NF - 4);                                                                           \
        m_tt+=$(NF - 1); m_tb+=$(NF - 1);                                                          \
        if( $(NF - 5) != 200     ){ m_e++; m_tb-=$(NF - 1) };                                      \
        if(      $NF ~ /"1"/     ){ m_eb++ }                                                       \
        else if( $NF ~ /"2"/     ){ m_nb++; m_nbsz+=$(NF - 4) }                                    \
        else if( $NF ~ /"3"/     ){ m_pd++; m_nbsz+=$(NF - 4); m_tb-=$(NF - 1) }                   \
        else if( $NF ~ /"4"/     ){ m_bd++; m_nbsz+=$(NF - 4); m_tb-=$(NF - 1) }                   \
        else if( $NF ~ /"0"/     ){ m_br++; m_nbsz+=$(NF - 4); m_tb-=$(NF - 1) };                  \
        if( $(NF - 1) > (tout-1) ){ m_t++ };                                                       \
      } ;                                                                                          \
      / \"GET \/rtb\/pbm?/                                                                         \
      {                                                                                            \
        p_nr++;                                                                                    \
        p_sz+=$(NF - 4);                                                                           \
        p_tt+=$(NF - 1); p_tb+=$(NF - 1);                                                          \
        if( $(NF - 5) != 200     ){ p_e++; p_tb-=$(NF - 1) };                                      \
        if(      $NF ~ /"1"/     ){ p_eb++ }                                                       \
        else if( $NF ~ /"2"/     ){ p_nb++; p_nbsz+=$(NF - 4) }                                    \
        else if( $NF ~ /"3"/     ){ p_pd++; p_nbsz+=$(NF - 4); p_tb-=$(NF - 1) }                   \
        else if( $NF ~ /"4"/     ){ p_bd++; p_nbsz+=$(NF - 4); p_tb-=$(NF - 1) }                   \
        else if( $NF ~ /"0"/     ){ p_br++; p_nbsz+=$(NF - 4); p_tb-=$(NF - 1) };                  \
        if( $(NF - 1) > (tout-1) ){ p_t++ };                                                       \
      } ;                                                                                          \
      / \"POST \/rtb\/fb /                                                                         \
      {                                                                                            \
        f_nr++;                                                                                    \
        f_sz+=$(NF - 4);                                                                           \
        f_tt+=$(NF - 1); f_tb+=$(NF - 1);                                                          \
        if( $(NF - 5) != 200     ){ f_e++; f_tb-=$(NF - 1) };                                      \
        if(      $NF ~ /"1"/     ){ f_eb++ }                                                       \
        else if( $NF ~ /"2"/     ){ f_nb++; f_nbsz+=$(NF - 4) }                                    \
        else if( $NF ~ /"3"/     ){ f_pd++; f_nbsz+=$(NF - 4); f_tb-=$(NF - 1) }                   \
        else if( $NF ~ /"4"/     ){ f_bd++; f_nbsz+=$(NF - 4); f_tb-=$(NF - 1) }                   \
        else if( $NF ~ /"0"/     ){ f_br++; f_nbsz+=$(NF - 4); f_tb-=$(NF - 1) };                  \
        if( $(NF - 1) > (tout-1) ){ f_t++ };                                                       \
      } ;                                                                                          \
      / \"POST \/rtb\/opx /                                                                        \
      {                                                                                            \
        o_nr++;                                                                                    \
        o_sz+=$(NF - 4);                                                                           \
        o_tt+=$(NF - 1); o_tb+=$(NF - 1);                                                          \
        if( $(NF - 5) != 200     ){ o_e++; o_tb-=$(NF - 1) };                                      \
        if(      $NF ~ /"1"/     ){ o_eb++ }                                                       \
        else if( $NF ~ /"2"/     ){ o_nb++; o_nbsz+=$(NF - 4) }                                    \
        else if( $NF ~ /"3"/     ){ o_pd++; o_nbsz+=$(NF - 4); o_tb-=$(NF - 1) }                   \
        else if( $NF ~ /"4"/     ){ o_bd++; o_nbsz+=$(NF - 4); o_tb-=$(NF - 1) }                   \
        else if( $NF ~ /"0"/     ){ o_br++; o_nbsz+=$(NF - 4); o_tb-=$(NF - 1) };                  \
        if( $(NF - 1) > (tout-1) ){ o_t++ };                                                       \
      } ;                                                                                          \
      END                                                                                          \
      {                                                                                            \
        if ( 0 != a_nr) { printf( "A%c%-8d%-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d%-6d%-6d\n",\
                                  (a_eb != a_nr-a_br-a_nb-a_e-a_pd-a_bd) ? "!" : " ",                          \
                                  a_nr, a_br, a_t, a_bd, a_pd, a_e, a_nb, a_eb,                                \
                                  ((a_eb)*100)/a_nr,                                                           \
                                  ((a_e+a_pd+a_bd)*100)/a_nr,                                                  \
                                  (a_sz-a_nbsz)/1000, a_nbsz/1000, ((a_sz-a_nbsz)*100)/a_sz,                   \
                                  a_tt/a_nr, a_tb/(a_nr-a_e-a_pd-a_bd-a_br) ); }                               \
        if ( 0 != c_nr) { printf( "C%c%-8d%-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d%-6d%-6d\n",\
                                  (c_eb != c_nr-c_br-c_nb-c_e-c_pd-c_bd) ? "!" : " ",                          \
                                  c_nr, c_br, c_t, c_bd, c_pd, c_e, c_nb, c_eb,                                \
                                  ((c_eb)*100)/c_nr,                                                           \
                                  ((c_e+c_pd+c_bd)*100)/c_nr,                                                  \
                                  (c_sz-c_nbsz)/1000, c_nbsz/1000, ((c_sz-c_nbsz)*100)/c_sz,                   \
                                  c_tt/c_nr, c_tb/(c_nr-c_e-c_pd-c_bd-c_br) ); }                               \
        if ( 0 != e_nr) { printf( "E%c%-8d%-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d%-6d%-6d\n",\
                                  (e_eb != e_nr-e_br-e_nb-e_e-e_pd-e_bd) ? "!" : " ",                          \
                                  e_nr, e_br, e_t, e_bd, e_pd, e_e, e_nb, e_eb,                                \
                                  ((e_eb)*100)/e_nr,                                                           \
                                  ((e_e+e_pd+e_bd)*100)/e_nr,                                                  \
                                  (e_sz-e_nbsz)/1000, e_nbsz/1000, ((e_sz-e_nbsz)*100)/e_sz,                   \
                                  e_tt/e_nr, e_tb/(e_nr-e_e-e_pd-e_bd-e_br) ); }                               \
        if ( 0 != f_nr) { printf( "F%c%-8d%-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d%-6d%-6d\n",\
                                  (f_eb != f_nr-f_br-f_nb-f_e-f_pd-f_bd) ? "!" : " ",                          \
                                  f_nr, f_br, f_t, f_bd, f_pd, f_e, f_nb, f_eb,                                \
                                  ((f_eb)*100)/f_nr,                                                           \
                                  ((f_e+f_pd+f_bd)*100)/f_nr,                                                  \
                                  (f_sz-f_nbsz)/1000, f_nbsz/1000, ((f_sz-f_nbsz)*100)/f_sz,                   \
                                  f_tt/f_nr, f_tb/(f_nr-f_e-f_pd-f_bd-f_br) ); }                               \
        if ( 0 != g_nr) { printf( "G%c%-8d%-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d%-6d%-6d\n",\
                                  (g_eb != g_nr-g_br-g_nb-g_e-g_pd-g_bd) ? "!" : " ",                          \
                                  g_nr, g_br, g_t, g_bd, g_pd, g_e, g_nb, g_eb,                                \
                                  ((g_eb)*100)/g_nr,                                                           \
                                  ((g_e+g_pd+g_bd)*100)/g_nr,                                                  \
                                  (g_sz-g_nbsz)/1000, g_nbsz/1000, ((g_sz-g_nbsz)*100)/g_sz,                   \
                                  g_tt/g_nr, g_tb/(g_nr-g_e-g_pd-g_bd-g_br) ); }                               \
        if ( 0 != m_nr) { printf( "M%c%-8d%-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d%-6d%-6d\n",\
                                  (m_eb != m_nr-m_br-m_nb-m_e-m_pd-m_bd) ? "!" : " ",                          \
                                  m_nr, m_br, m_t, m_bd, m_pd, m_e, m_nb, m_eb,                                \
                                  ((m_eb)*100)/m_nr,                                                           \
                                  ((m_e+m_pd+m_bd)*100)/m_nr,                                                  \
                                  (m_sz-m_nbsz)/1000, m_nbsz/1000, ((m_sz-m_nbsz)*100)/m_sz,                   \
                                  m_tt/m_nr, m_tb/(m_nr-m_e-m_pd-m_bd-m_br) ); }                               \
        if ( 0 != o_nr) { printf( "O%c%-8d%-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d%-6d%-6d\n",\
                                  (o_eb != o_nr-o_br-o_nb-o_e-o_pd-o_bd) ? "!" : " ",                          \
                                  o_nr, o_br, o_t, o_bd, o_pd, o_e, o_nb, o_eb,                                \
                                  ((o_eb)*100)/o_nr,                                                           \
                                  ((o_e+o_pd+o_bd)*100)/o_nr,                                                  \
                                  (o_sz-o_nbsz)/1000, o_nbsz/1000, ((o_sz-o_nbsz)*100)/o_sz,                   \
                                  o_tt/o_nr, o_tb/(o_nr-o_e-o_pd-o_bd-o_br) ); }                               \
        if ( 0 != p_nr) { printf( "P%c%-8d%-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d%-6d%-6d\n",\
                                  (p_eb != p_nr-p_br-p_nb-p_e-p_pd-p_bd) ? "!" : " ",                          \
                                  p_nr, p_br, p_t, p_bd, p_pd, p_e, p_nb, p_eb,                                \
                                  ((p_eb)*100)/p_nr,                                                           \
                                  ((p_e+p_pd+p_bd)*100)/p_nr,                                                  \
                                  (p_sz-p_nbsz)/1000, p_nbsz/1000, ((p_sz-p_nbsz)*100)/p_sz,                   \
                                  p_tt/p_nr, p_tb/(p_nr-p_e-p_pd-p_bd-p_br) ); }                               \
        if ( 0 != r_nr) { printf( "R%c%-8d%-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d%-6d%-6d\n",\
                                  (r_eb != r_nr-r_br-r_nb-r_e-r_pd-r_bd) ? "!" : " ",                          \
                                  r_nr, r_br, r_t, r_bd, r_pd, r_e, r_nb, r_eb,                                \
                                  ((r_eb)*100)/r_nr,                                                           \
                                  ((r_e+r_pd+r_bd)*100)/r_nr,                                                  \
                                  (r_sz-r_nbsz)/1000, r_nbsz/1000, ((r_sz-r_nbsz)*100)/r_sz,                   \
                                  r_tt/r_nr, r_tb/(r_nr-r_e-r_pd-r_bd-r_br) ); }                               \
        nr = a_nr+c_nr+e_nr+f_nr+g_nr+m_nr+o_nr+p_nr+r_nr;                                                     \
        br = a_br+c_br+e_br+f_br+g_br+m_br+o_br+p_br+r_br;                                                     \
        t  = a_t +c_t +e_t +f_t +g_t +m_t +o_t +p_t +r_t ;                                                     \
        bd = a_bd+c_bd+e_bd+f_bd+g_bd+m_bd+o_bd+p_bd+r_bd;                                                     \
        pd = a_pd+c_pd+e_pd+f_pd+g_pd+m_pd+o_pd+p_pd+r_pd;                                                     \
        e  = a_e +c_e +e_e +f_e +g_e +m_e +o_e +p_e +r_e ;                                                     \
        nb = a_nb+c_nb+e_nb+f_nb+g_nb+m_nb+o_nb+p_nb+r_nb;                                                     \
        eb = a_eb+c_eb+e_eb+f_eb+g_eb+m_eb+o_eb+p_eb+r_eb;                                                     \
        sz = a_sz+c_sz+e_sz+f_sz+g_sz+m_sz+o_sz+p_sz+r_sz;                                                     \
        nbsz = a_nbsz+c_nbsz+e_nbsz+f_nbsz+g_nbsz+m_nbsz+o_nbsz+p_nbsz+r_nbsz;                                 \
        tt = a_tt+c_tt+e_tt+f_tt+g_tt+m_tt+o_tt+p_tt+r_tt;                                                     \
        tb = a_tb+c_tb+e_tb+f_tb+g_tb+m_tb+o_tb+p_tb+r_tb;                                                     \
                          printf( " %c%-8d%-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d%-6d%-6d\n",\
                                  (eb != nr-nb-e-pd-bd-br) ? "!" : " ",                                        \
                                  nr, br, t, bd, pd, e, nb, eb,                                                \
                                  (eb*100)/nr,                                                                 \
                                  ((e+pd+bd)*100)/nr,                                                          \
                                  (sz-nbsz)/1000, nbsz/1000, ((sz-nbsz)*100)/sz,                               \
                                  tt/nr, tb/(nr-e-pd-bd-br) );                                                 \
      }')
  IS_ROTATED=`ls -tr /var/home/httpd_logs/access_log.201*[0-9]|tail -1`
done

for x in $@ ; do [ "no_header" == "${x}" ]  &&  no_header="1"; done
[ -z "${no_header}" ] &&  echo -e "X BidReq  BadReq  Long    BdrOut  PxyOut  Err     NoBid   EffBids % EffBids % BidLost SzEB,KB SzNB,KB % Sz EB   AvgT  AvgT_B"
echo "$num"



