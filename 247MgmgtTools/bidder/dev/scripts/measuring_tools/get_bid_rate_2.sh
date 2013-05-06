#!/bin/bash

e=$2
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

echo -e "\nX BidReq  Long    BdrOut  PxyOut  Err     NoBid   EffBids % EffBids % BidLost SzEB,KB SzNB,KB % Sz EB"
for x in ${b[@]} ; do echo -e "===== $x" ;                                                             \
                      ssh $x /tmp/dk/scripts/dev_to_rate_2.sh no_header ;                              \
done | q_num=${#b[@]} awk                                                                              \
  '                                                                                                    \
  { print; }                                                                                           \
  /^A /{a_nr+=$2; a_t+=$3; a_bd+=$4; a_pd+=$5; a_e+=$6; a_nb+=$7; a_sz+=$13; a_nbsz+=$14;};            \
  /^C /{c_nr+=$2; c_t+=$3; c_bd+=$4; c_pd+=$5; c_e+=$6; c_nb+=$7; c_sz+=$13; c_nbsz+=$14; };           \
  /^E /{e_nr+=$2; e_t+=$3; e_bd+=$4; e_pd+=$5; e_e+=$6; e_nb+=$7; e_sz+=$13; e_nbsz+=$14; };           \
  /^F /{f_nr+=$2; f_t+=$3; f_bd+=$4; f_pd+=$5; f_e+=$6; f_nb+=$7; f_sz+=$13; f_nbsz+=$14; };           \
  /^G /{g_nr+=$2; g_t+=$3; g_bd+=$4; g_pd+=$5; g_e+=$6; g_nb+=$7; g_sz+=$13; g_nbsz+=$14; };           \
  /^M /{m_nr+=$2; m_t+=$3; m_bd+=$4; m_pd+=$5; m_e+=$6; m_nb+=$7; m_sz+=$13; m_nbsz+=$14; };           \
  /^O /{o_nr+=$2; o_t+=$3; o_bd+=$4; o_pd+=$5; o_e+=$6; o_nb+=$7; o_sz+=$13; o_nbsz+=$14; };           \
  /^P /{p_nr+=$2; p_t+=$3; p_bd+=$4; p_pd+=$5; p_e+=$6; p_nb+=$7; p_sz+=$13; p_nbsz+=$14; };           \
  /^R /{r_nr+=$2; r_t+=$3; r_bd+=$4; r_pd+=$5; r_e+=$6; r_nb+=$7; r_sz+=$13; r_nbsz+=$14; };           \
  /^S /{e_nr+=$2; e_t+=$3; e_bd+=$4; e_pd+=$5; e_e+=$6; e_nb+=$7; e_sz+=$13; e_nbsz+=$14; };           \
  END                                                                                                  \
  {                                                                                                    \
    printf( "\n===== Total\nX BidReq  Long    BdrOut  PxyOut  Err     NoBid   EffBids %% EffBids %% BidLost SzEB,MB SzNB,MB %% Sz EB\n" ); \
    if ( 0 != a_nr) { printf( "A %-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d\n",                        \
                              a_nr, a_t, a_bd, a_pd, a_e, a_nb,                                                       \
                              a_nr-a_nb-a_e-a_pd-a_bd,                                                                \
                              ((a_nr-a_nb-a_e-a_pd-a_bd)*100)/a_nr,                                                   \
                              ((a_e+a_pd+a_bd)*100)/a_nr,                                                             \
                              (a_sz+500)/1000, (a_nbsz+500)/1000, (a_sz+a_nbsz)>0 ? (a_sz*100)/(a_sz+a_nbsz) : 0 ); } \
    if ( 0 != c_nr) { printf( "C %-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d\n",                        \
                              c_nr, c_t, c_bd, c_pd, c_e, c_nb,                                                       \
                              c_nr-c_nb-c_e-c_pd-c_bd,                                                                \
                              ((c_nr-c_nb-c_e-c_pd-c_bd)*100)/c_nr,                                                   \
                              ((c_e+c_pd+c_bd)*100)/c_nr,                                                             \
                              (c_sz+500)/1000, (c_nbsz+500)/1000, (c_sz+c_nbsz)>0 ? (c_sz*100)/(c_sz+c_nbsz) : 0 ); } \
    if ( 0 != e_nr) { printf( "E %-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d\n",                        \
                              e_nr, e_t, e_bd, e_pd, e_e, e_nb,                                                       \
                              e_nr-e_nb-e_e-e_pd-e_bd,                                                                \
                              ((e_nr-e_nb-e_e-e_pd-e_bd)*100)/e_nr,                                                   \
                              ((e_e+e_pd+e_bd)*100)/e_nr,                                                             \
                              (e_sz+500)/1000, (e_nbsz+500)/1000, (e_sz+e_nbsz)>0 ? (e_sz*100)/(e_sz+e_nbsz) : 0 ); } \
    if ( 0 != f_nr) { printf( "F %-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d\n",                        \
                              f_nr, f_t, f_bd, f_pd, f_e, f_nb,                                                       \
                              f_nr-f_nb-f_e-f_pd-f_bd,                                                                \
                              ((f_nr-f_nb-f_e-f_pd-f_bd)*100)/f_nr,                                                   \
                              ((f_e+f_pd+f_bd)*100)/f_nr,                                                             \
                              (f_sz+500)/1000, (f_nbsz+500)/1000, (f_sz+f_nbsz)>0 ? (f_sz*100)/(f_sz+f_nbsz) : 0 ); } \
    if ( 0 != g_nr) { printf( "G %-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d\n",                        \
                              g_nr, g_t, g_bd, g_pd, g_e, g_nb,                                                       \
                              g_nr-g_nb-g_e-g_pd-g_bd,                                                                \
                              ((g_nr-g_nb-g_e-g_pd-g_bd)*100)/g_nr,                                                   \
                              ((g_e+g_pd+g_bd)*100)/g_nr,                                                             \
                              (g_sz+500)/1000, (g_nbsz+500)/1000, (g_sz+g_nbsz)>0 ? (g_sz*100)/(g_sz+g_nbsz) : 0 ); } \
    if ( 0 != m_nr) { printf( "M %-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d\n",                        \
                              m_nr, m_t, m_bd, m_pd, m_e, m_nb,                                                       \
                              m_nr-m_nb-m_e-m_pd-m_bd,                                                                \
                              ((m_nr-m_nb-m_e-m_pd-m_bd)*100)/m_nr,                                                   \
                              ((m_e+m_pd+m_bd)*100)/m_nr,                                                             \
                              (m_sz+500)/1000, (m_nbsz+500)/1000, (m_sz+m_nbsz)>0 ? (m_sz*100)/(m_sz+m_nbsz) : 0 ); } \
    if ( 0 != o_nr) { printf( "O %-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d\n",                        \
                              o_nr, o_t, o_bd, o_pd, o_e, o_nb,                                                       \
                              o_nr-o_nb-o_e-o_pd-o_bd,                                                                \
                              ((o_nr-o_nb-o_e-o_pd-o_bd)*100)/o_nr,                                                   \
                              ((o_e+o_pd+o_bd)*100)/o_nr,                                                             \
                              (o_sz+500)/1000, (o_nbsz+500)/1000, (o_sz+o_nbsz)>0 ? (o_sz*100)/(o_sz+o_nbsz) : 0 ); } \
    if ( 0 != p_nr) { printf( "P %-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d\n",                        \
                              p_nr, p_t, p_bd, p_pd, p_e, p_nb,                                                       \
                              p_nr-p_nb-p_e-p_pd-p_bd,                                                                \
                              ((p_nr-p_nb-p_e-p_pd-p_bd)*100)/p_nr,                                                   \
                              ((p_e+p_pd+p_bd)*100)/p_nr,                                                             \
                              (p_sz+500)/1000, (p_nbsz+500)/1000, (p_sz+p_nbsz)>0 ? (p_sz*100)/(p_sz+p_nbsz) : 0 ); } \
    if ( 0 != r_nr) { printf( "R %-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d\n",                        \
                              r_nr, r_t, r_bd, r_pd, r_e, r_nb,                                                       \
                              r_nr-r_nb-r_e-r_pd-r_bd,                                                                \
                              ((r_nr-r_nb-r_e-r_pd-r_bd)*100)/r_nr,                                                   \
                              ((r_e+r_pd+r_bd)*100)/r_nr,                                                             \
                              (r_sz+500)/1000, (r_nbsz+500)/1000, (r_sz+r_nbsz)>0 ? (r_sz*100)/(r_sz+r_nbsz) : 0 ); } \
    nr = a_nr+c_nr+e_nr+f_nr+g_nr+m_nr+o_nr+p_nr+r_nr;                                                                \
    t  = a_t+c_t+e_t+f_t+g_t+m_t+o_t+p_t+r_t;                                                                         \
    bd = a_bd+c_bd+e_bd+f_bd+g_bd+m_bd+o_bd+p_bd+r_bd;                                                                \
    pd = a_pd+c_pd+e_pd+f_pd+g_pd+m_pd+o_pd+p_pd+r_pd;                                                                \
    e  = a_e+c_e+e_e+f_e+g_e+m_e+o_e+p_e+r_e;                                                                         \
    nb = a_nb+c_nb+e_nb+f_nb+g_nb+m_nb+o_nb+p_nb+r_nb;                                                                \
    sz = a_sz+c_sz+e_sz+f_sz+g_sz+m_sz+o_sz+p_sz+r_sz;                                                                \
    nbsz = a_nbsz+c_nbsz+e_nbsz+f_nbsz+g_nbsz+m_nbsz+o_nbsz+p_nbsz+r_nbsz;                                            \
                      printf( "  %-8d%-8d%-8d%-8d%-8d%-8d%-8d%% %-8d%% %-8d%-8d%-8d%% %-8d\n",                        \
                              nr, t, bd, pd, e, nb,                                                                   \
                              nr-nb-e-pd-bd,                                                                          \
                              ((nr-nb-e-pd-bd)*100)/nr,                                                               \
                              ((e+pd+bd)*100)/nr,                                                                     \
                              (sz+500)/1000, (nbsz+500)/1000, (sz+nbsz)>0 ? (sz*100)/(sz+nbsz) : 0 );                 \
  }'




