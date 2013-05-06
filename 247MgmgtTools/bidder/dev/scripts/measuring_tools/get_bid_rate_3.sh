#!/bin/bash

# $(date -d '1 sec ago' '+%d/%b/%Y:%H:%M:%S')

e="$3"
[ -z "${e}" ] && e=/export/home/dkrasnovsky/zama/mytls/env_prod02_mdc.sh
. ${e}

[ "wc" == "$1"  ] && b=(${bidders_wc[@]})
[ "ec" == "$1"  ] && b=(${bidders_ec[@]})
[ "eu" == "$1"  ] && b=(${bidders_eu[@]})
[ "us" == "$1"  ] && b=(${bidders_us[@]})
[ "hk" == "$1"  ] && b=(${bidders_hk[@]})
[ "all" == "$1" ] && b=(${bidders[@]})
[ -z "$1"       ] && b=(${bidders_us[@]})

[ -z '${b[@]}' ]  && { echo "unknown DC specified (${1})"; exit; }

[ -n "$2" ]  &&  ts="\"$2\""

echo -e "\nX BidReq  BadReq  Long    BdrOut  PxyOut  Err     NoBid   EffBids % EffBids % BidLost SzEB,KB SzNB,KB % Sz EB   AvgT  AvgT_B"
#  for x in "31/Aug/2012:16:16:21" "31/Aug/2012:16:16:22"; do ./dev_to_rate_3.sh "${x}" no_header ; done | q_num=${#b[@]} awk \
for x in ${b[@]} ; do echo -e "===== $x" ;                                                                       \
                      ssh $x /tmp/dk/scripts/dev_to_rate_3.sh ${ts} no_header ;                    \
done | q_num=${#b[@]} awk                                                                                        \
  '                                                                                                              \
  { print; }                                                                                                     \
  /^A /{a_nr+=$2; a_br+=$3; a_t+=$4; a_bd+=$5; a_pd+=$6; a_e+=$7; a_nb+=$8; a_eb+=$9; a_sz+=$14; a_nbsz+=$15; a_tt+=$18; a_tb+=$19; a_ns++; }; \
  /^C /{c_nr+=$2; c_br+=$3; c_t+=$4; c_bd+=$5; c_pd+=$6; c_e+=$7; c_nb+=$8; c_eb+=$9; c_sz+=$14; c_nbsz+=$15; c_tt+=$18; c_tb+=$19; c_ns++; }; \
  /^E /{e_nr+=$2; e_br+=$3; e_t+=$4; e_bd+=$5; e_pd+=$6; e_e+=$7; e_nb+=$8; e_eb+=$9; e_sz+=$14; e_nbsz+=$15; e_tt+=$18; e_tb+=$19; e_ns++; }; \
  /^F /{f_nr+=$2; f_br+=$3; f_t+=$4; f_bd+=$5; f_pd+=$6; f_e+=$7; f_nb+=$8; f_eb+=$9; f_sz+=$14; f_nbsz+=$15; f_tt+=$18; f_tb+=$19; f_ns++; }; \
  /^G /{g_nr+=$2; g_br+=$3; g_t+=$4; g_bd+=$5; g_pd+=$6; g_e+=$7; g_nb+=$8; g_eb+=$9; g_sz+=$14; g_nbsz+=$15; g_tt+=$18; g_tb+=$19; g_ns++; }; \
  /^M /{m_nr+=$2; m_br+=$3; m_t+=$4; m_bd+=$5; m_pd+=$6; m_e+=$7; m_nb+=$8; m_eb+=$9; m_sz+=$14; m_nbsz+=$15; m_tt+=$18; m_tb+=$19; m_ns++; }; \
  /^O /{o_nr+=$2; o_br+=$3; o_t+=$4; o_bd+=$5; o_pd+=$6; o_e+=$7; o_nb+=$8; o_eb+=$9; o_sz+=$14; o_nbsz+=$15; o_tt+=$18; o_tb+=$19; o_ns++; }; \
  /^P /{p_nr+=$2; p_br+=$3; p_t+=$4; p_bd+=$5; p_pd+=$6; p_e+=$7; p_nb+=$8; p_eb+=$9; p_sz+=$14; p_nbsz+=$15; p_tt+=$18; p_tb+=$19; p_ns++; }; \
  /^R /{r_nr+=$2; r_br+=$3; r_t+=$4; r_bd+=$5; r_pd+=$6; r_e+=$7; r_nb+=$8; r_eb+=$9; r_sz+=$14; r_nbsz+=$15; r_tt+=$18; r_tb+=$19; r_ns++; }; \
  /^S /{e_nr+=$2; e_br+=$3; e_t+=$4; e_bd+=$5; e_pd+=$6; e_e+=$7; e_nb+=$8; e_eb+=$9; e_sz+=$14; e_nbsz+=$15; e_tt+=$18; e_tb+=$19; e_ns++; }; \
  END                                                                                                            \
  {                                                                                                              \
    printf( "\n===== Total\nX BidReq  BadReq  Long    BdrOut  PxyOut  Err     NoBid   EffBids %% EffBids %% BidLost SzEB,MB SzNB,MB %% Sz EB   AvgT  AvgT_B\n" ); \
    if ( 0 != a_nr) { printf( "A%c%-8d%-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d%-6d%-6d\n",           \
                              (a_eb != a_nr-a_br-a_nb-a_e-a_pd-a_bd) ? "!" : " ",                                     \
                              a_nr, a_br, a_t, a_bd, a_pd, a_e, a_nb, a_eb,                                           \
                              ((a_eb)*100)/a_nr,                                                                      \
                              ((a_e+a_pd+a_bd)*100)/a_nr,                                                             \
                              (a_sz+500)/1000, (a_nbsz+500)/1000, (a_sz+a_nbsz)>0 ? (a_sz*100)/(a_sz+a_nbsz) : 0,     \
                              a_tt/a_ns, a_tb/a_ns ); }                                                               \
    if ( 0 != c_nr) { printf( "C%c%-8d%-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d%-6d%-6d\n",           \
                              (c_eb != c_nr-c_br-c_nb-c_e-c_pd-c_bd) ? "!" : " ",                                     \
                              c_nr, c_br, c_t, c_bd, c_pd, c_e, c_nb, c_eb,                                           \
                              ((c_eb)*100)/c_nr,                                                                      \
                              ((c_e+c_pd+c_bd)*100)/c_nr,                                                             \
                              (c_sz+500)/1000, (c_nbsz+500)/1000, (c_sz+c_nbsz)>0 ? (c_sz*100)/(c_sz+c_nbsz) : 0,     \
                              c_tt/c_ns, c_tb/c_ns ); }                                                               \
    if ( 0 != e_nr) { printf( "E%c%-8d%-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d%-6d%-6d\n",           \
                              (e_eb != e_nr-e_br-e_nb-e_e-e_pd-e_bd) ? "!" : " ",                                     \
                              e_nr, e_br, e_t, e_bd, e_pd, e_e, e_nb, e_eb,                                           \
                              ((e_eb)*100)/e_nr,                                                                      \
                              ((e_e+e_pd+e_bd)*100)/e_nr,                                                             \
                              (e_sz+500)/1000, (e_nbsz+500)/1000, (e_sz+e_nbsz)>0 ? (e_sz*100)/(e_sz+e_nbsz) : 0,     \
                              e_tt/e_ns, e_tb/e_ns ); }                                                               \
    if ( 0 != f_nr) { printf( "F%c%-8d%-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d%-6d%-6d\n",           \
                              (f_eb != f_nr-f_br-f_nb-f_e-f_pd-f_bd) ? "!" : " ",                                     \
                              f_nr, f_br, f_t, f_bd, f_pd, f_e, f_nb, f_eb,                                           \
                              ((f_eb)*100)/f_nr,                                                                      \
                              ((f_e+f_pd+f_bd)*100)/f_nr,                                                             \
                              (f_sz+500)/1000, (f_nbsz+500)/1000, (f_sz+f_nbsz)>0 ? (f_sz*100)/(f_sz+f_nbsz) : 0,     \
                              f_tt/f_ns, f_tb/f_ns ); }                                                               \
    if ( 0 != g_nr) { printf( "G%c%-8d%-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d%-6d%-6d\n",           \
                              (g_eb != g_nr-g_br-g_nb-g_e-g_pd-g_bd) ? "!" : " ",                                     \
                              g_nr, g_br, g_t, g_bd, g_pd, g_e, g_nb, g_eb,                                           \
                              ((g_eb)*100)/g_nr,                                                                      \
                              ((g_e+g_pd+g_bd)*100)/g_nr,                                                             \
                              (g_sz+500)/1000, (g_nbsz+500)/1000, (g_sz+g_nbsz)>0 ? (g_sz*100)/(g_sz+g_nbsz) : 0,     \
                              g_tt/g_ns, g_tb/g_ns ); }                                                               \
    if ( 0 != m_nr) { printf( "M%c%-8d%-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d%-6d%-6d\n",           \
                              (m_eb != m_nr-m_br-m_nb-m_e-m_pd-m_bd) ? "!" : " ",                                     \
                              m_nr, m_br, m_t, m_bd, m_pd, m_e, m_nb, m_eb,                                           \
                              ((m_eb)*100)/m_nr,                                                                      \
                              ((m_e+m_pd+m_bd)*100)/m_nr,                                                             \
                              (m_sz+500)/1000, (m_nbsz+500)/1000, (m_sz+m_nbsz)>0 ? (m_sz*100)/(m_sz+m_nbsz) : 0,     \
                              m_tt/m_ns, m_tb/m_ns ); }                                                               \
    if ( 0 != o_nr) { printf( "O%c%-8d%-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d%-6d%-6d\n",           \
                              (o_eb != o_nr-o_br-o_nb-o_e-o_pd-o_bd) ? "!" : " ",                                     \
                              o_nr, o_br, o_t, o_bd, o_pd, o_e, o_nb, o_eb,                                           \
                              ((o_eb)*100)/o_nr,                                                                      \
                              ((o_e+o_pd+o_bd)*100)/o_nr,                                                             \
                              (o_sz+500)/1000, (o_nbsz+500)/1000, (o_sz+o_nbsz)>0 ? (o_sz*100)/(o_sz+o_nbsz) : 0,     \
                              o_tt/o_ns, o_tb/o_ns ); }                                                               \
    if ( 0 != p_nr) { printf( "P%c%-8d%-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d%-6d%-6d\n",           \
                              (p_eb != p_nr-p_br-p_nb-p_e-p_pd-p_bd) ? "!" : " ",                                     \
                              p_nr, p_br, p_t, p_bd, p_pd, p_e, p_nb, p_eb,                                           \
                              ((p_eb)*100)/p_nr,                                                                      \
                              ((p_e+p_pd+p_bd)*100)/p_nr,                                                             \
                              (p_sz+500)/1000, (p_nbsz+500)/1000, (p_sz+p_nbsz)>0 ? (p_sz*100)/(p_sz+p_nbsz) : 0,     \
                              p_tt/p_ns, p_tb/p_ns ); }                                                               \
    if ( 0 != r_nr) { printf( "R%c%-8d%-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d%-6d%-6d\n",           \
                              (r_eb != r_nr-r_br-r_nb-r_e-r_pd-r_bd) ? "!" : " ",                                     \
                              r_nr, r_br, r_t, r_bd, r_pd, r_e, r_nb, r_eb,                                           \
                              ((r_eb)*100)/r_nr,                                                                      \
                              ((r_e+r_pd+r_bd)*100)/r_nr,                                                             \
                              (r_sz+500)/1000, (r_nbsz+500)/1000, (r_sz+r_nbsz)>0 ? (r_sz*100)/(r_sz+r_nbsz) : 0,     \
                              r_tt/r_ns, r_tb/r_ns ); }                                                               \
    nr = a_nr+c_nr+e_nr+f_nr+g_nr+m_nr+o_nr+p_nr+r_nr;                                                                \
    br = a_br+c_br+e_br+f_br+g_br+m_br+o_br+p_br+r_br;                                                                \
    t  = a_t +c_t +e_t +f_t +g_t +m_t +o_t +p_t +r_t ;                                                                \
    bd = a_bd+c_bd+e_bd+f_bd+g_bd+m_bd+o_bd+p_bd+r_bd;                                                                \
    pd = a_pd+c_pd+e_pd+f_pd+g_pd+m_pd+o_pd+p_pd+r_pd;                                                                \
    e  = a_e +c_e +e_e +f_e +g_e +m_e +o_e +p_e +r_e ;                                                                \
    nb = a_nb+c_nb+e_nb+f_nb+g_nb+m_nb+o_nb+p_nb+r_nb;                                                                \
    eb = a_eb+c_eb+e_eb+f_eb+g_eb+m_eb+o_eb+p_eb+r_eb;                                                                \
    sz = a_sz+c_sz+e_sz+f_sz+g_sz+m_sz+o_sz+p_sz+r_sz;                                                                \
    nbsz = a_nbsz+c_nbsz+e_nbsz+f_nbsz+g_nbsz+m_nbsz+o_nbsz+p_nbsz+r_nbsz;                                            \
    tt = a_tt+c_tt+e_tt+f_tt+g_tt+m_tt+o_tt+p_tt+r_tt;                                                                \
    tb = a_tb+c_tb+e_tb+f_tb+g_tb+m_tb+o_tb+p_tb+r_tb;                                                                \
                      printf( " %c%-8d%-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d\n",                   \
                              (eb != nr-nb-e-pd-bd-br) ? "!" : " ",                                                   \
                              nr, br, t, bd, pd, e, nb, eb,                                                           \
                              (eb*100)/nr,                                                                            \
                              ((e+pd+bd)*100)/nr,                                                                     \
                              (sz+500)/1000, (nbsz+500)/1000, (sz+nbsz)>0 ? (sz*100)/(sz+nbsz) : 0 );                 \
  }'




