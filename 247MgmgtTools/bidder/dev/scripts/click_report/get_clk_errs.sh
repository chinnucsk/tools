#!/bin/bash

grep "$(date -d "yesterday" +"%b %d")" /var/home/httpd_logs/zama_click_tracker.log.2012-*[0-9] | grep "[error]" | egrep "Missing |Failed " | awk   \
'                                                                                                                                         \
  BEGIN{ FS="GET |, referer: " }                                                                                                          \
  {                                                                                                                                       \
    if( 0 != match( $2, "&c=([^&]+)", c ) )                                                                                               \
      { cid = c[1] }                                                                                                                      \
    else                                                                                                                                  \
      {                                                                                                                                   \
        if( "" != $3  &&  0 != match( $3, "&c=([^&]+)", c ) )                                                                             \
          { cid = c[1] }                                                                                                                  \
        else                                                                                                                              \
          { cid = "unknown" }                                                                                                             \
      }                                                                                                                                   \
    cids[ cid ]++;                                                                                                                        \
  }                                                                                                                                       \
  /Missing query string/                                   { e_qs[ cid ]++ }                                                              \
  /Missing one of the required parameters in query string/ { e_mp[ cid ]++ }                                                              \
  /Missing url in query string/                            { e_mu[ cid ]++ }                                                              \
  /Failed to decode redirect URL/                          { e_fd[ cid ]++ }                                                              \
  /Failed to parse redirect URL/                           { e_fp[ cid ]++ }                                                              \
  /Missing scheme in redirect URL/                         { e_ms[ cid ]++ }                                                              \
  /Missing host in redirect URL/                           { e_mh[ cid ]++ }                                                              \
  END                                                                                                                                     \
  {                                                                                                                                       \
    ni = 1;                                                                                                                               \
    for( idx in cids ){ idxs[ ni ] = idx; ni++ }                                                                                          \
    sz = asort( idxs );                                                                                                                   \
    for( ni = 1; ni <= sz; ni++ ){ printf( "%s %d\n", idxs[ ni ], cids[ idxs[ ni ] ] ); t += cids[ idxs[ ni ] ]; }                        \
                                                                                                                                          \
  }                                                                                                                                       \
'
