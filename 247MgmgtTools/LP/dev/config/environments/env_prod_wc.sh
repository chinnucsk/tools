#========================================
# Description of ZAMA West Coast production environment
#========================================

# Performance counter service ports for different components (default (DPP) - 8801)
  ZAMA_STCOL_PERF_PORT=8802
  ZAMA_VLDR_PERF_PORT=8803
  ZAMA_VBKP_PERF_PORT=8804
  ZAMA_GRTB_PERF_PORT=8805

                 # 172.21.155.11 172.21.155.12 172.21.155.13 172.21.155.25 172.21.155.26 172.21.155.27 172.21.155.28 172.21.155.29
  ZAMA_GRTB_HOSTS=(rtbbid1us3    rtbbid2us3    rtbbid3us3    rtbbid4us3    rtbbid5us3    rtbbid6us3    rtbbid7us3    rtbbid8us3)
  ZAMA_GRTB_HOSTS_NUM=500
  ZAMA_GRTB_PORT=11100
  ZAMA_GRTB_PROXY_TIMEOUT=40

                  # 10.73.44.105 10.73.44.106 172.21.155.106 172.21.155.107
  ZAMA_STCOL_HOSTS=(rtbmem1us2   rtbmem2us2   rtbmem1us3     rtbmem2us3)
  ZAMA_STCOL_PORT=11102
  ZAMA_NEW_STCOL_PORT=11104

  ZAMA_STCOL_POLL_PERIOD=1000

                         # 172.21.155.107
  ZAMA_STCOL_ACCESS_POINT="rtbmem1us3"
  ZAMA_STCOL_ACCESS_POINT_PORT=${ZAMA_STCOL_PORT}
  ZAMA_NEW_STCOL_ACCESS_POINT_PORT=${ZAMA_NEW_STCOL_PORT}

# <<< ZAMA RTB DB configuration
                            #172.21.155.17             172.21.155.18             172.21.155.19             172.21.155.20
  ZAMA_UMDB_NODES=(0000_0000@rtbmdb2us3      0001_0000@rtbmdb3us3      0002_0000@rtbmdb4us3      0003_0000@rtbmdb5us3)

                             #172.21.155.21             172.21.155.22             172.21.155.23             172.21.155.24
  ZAMA_ASMDB_NODES=(0000_0000@rtbmdb6us3      0001_0000@rtbmdb7us3      0002_0000@rtbmdb8us3      0003_0000@rtbmdb9us3)

                            #172.21.155.17             172.21.155.22             172.21.155.23             172.21.155.24             172.21.155.17               172.21.155.22               172.21.155.23               172.21.155.24
  ZAMA_FCDB_NODES=(0000_0000@rtbmdb2us3:6380 0001_0000@rtbmdb7us3:6380 0002_0000@rtbmdb8us3:6380 0003_0000@rtbmdb9us3:6380 0004_0000@rtbmdb2us3:6381   0005_0000@rtbmdb7us3:6381   0006_0000@rtbmdb8us3:6381   0007_0000@rtbmdb9us3:6381)
  # definition of FC DB nodes if half of them be transferred to rtbmdb[6-9]...:
                            #172.21.155.21             172.21.155.18             172.21.155.19             172.21.155.20             172.21.155.18             172.21.155.19             172.21.155.20             172.21.155.21
  # ZAMA_FCDB_NODES=(0000_0000@rtbmdb2us3:6380 0001_0000@rtbmdb7us3:6380 0002_0000@rtbmdb8us3:6380 0003_0000@rtbmdb9us3:6380 0004_0000@rtbmdb3us3:6380 0005_0000@rtbmdb4us3:6380 0006_0000@rtbmdb5us3:6380 0007_0000@rtbmdb6us3:6380)

  ZAMA_RTBDB_GROUPS=(UMDB ASMDB FCDB)
  # RTB DB config file names for "all separate" config...:
  ZAMA_RTBDB_CONFIGS=(rsvc_umdb_config.xml rsvc_asmdb_config.xml rsvc_fcdb_config.xml)
  ZAMA_RTBDB_CREATE_CONFIG=1
  ZAMA_RTBDB_CLIENT_TIMEOUT=20
# >>>

  ZAMA_GPXY_PHYS_HOSTS=("172.21.155.11" "172.21.155.12" "172.21.155.13" "172.21.155.25" "172.21.155.26" "172.21.155.27" "172.21.155.28" "172.21.155.29")
  ZAMA_GPXY_VIRT_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})

  ZAMA_APXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_APXY_VIRT_HOSTS=("172.21.155.141" "172.21.155.142" "172.21.155.143" "172.21.155.144" "172.21.155.145" "172.21.155.146" "172.21.155.147" "172.21.155.148")

  ZAMA_CPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_CPXY_VIRT_HOSTS=("__specify_contextweb_proxy_virt_IP_on_bid101__" "__specify_contextweb_proxy_virt_IP_on_bid102__" "__specify_contextweb_proxy_virt_IP_on_bid103__" "__specify_contextweb_proxy_virt_IP_on_bid104__" "__specify_contextweb_proxy_virt_IP_on_bid105__" "__specify_contextweb_proxy_virt_IP_on_bid106__" "__specify_contextweb_proxy_virt_IP_on_bid107__" "__specify_contextweb_proxy_virt_IP_on_bid108__")

  # NOTE: name reuse - from now on (7/2/2012 11:30) 'F' in names mean Facebook!!!
  ZAMA_FPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_FPXY_VIRT_HOSTS=("__specify_facebook_proxy_virt_IP_on_bid101__" "__specify_facebook_proxy_virt_IP_on_bid102__" "__specify_facebook_proxy_virt_IP_on_bid103__" "__specify_facebook_proxy_virt_IP_on_bid104__" "__specify_facebook_proxy_virt_IP_on_bid105__" "__specify_facebook_proxy_virt_IP_on_bid106__" "__specify_facebook_proxy_virt_IP_on_bid107__" "__specify_facebook_proxy_virt_IP_on_bid108__")

  ZAMA_MPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_MPXY_VIRT_HOSTS=(__specify_admeld_proxy_virt_IP_on_bid101__ __specify_admeld_proxy_virt_IP_on_bid102__ __specify_admeld_proxy_virt_IP_on_bid103__ __specify_admeld_proxy_virt_IP_on_bid104__ __specify_admeld_proxy_virt_IP_on_bid105__ __specify_admeld_proxy_virt_IP_on_bid106__ __specify_admeld_proxy_virt_IP_on_bid107__ __specify_admeld_proxy_virt_IP_on_bid108__)

  ZAMA_RPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_RPXY_VIRT_HOSTS=("172.21.155.160" "172.21.155.161" "172.21.155.162" "172.21.155.163" "172.21.155.164" "172.21.155.165" "172.21.155.166" "172.21.155.167")


  ZAMA_PPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_PPXY_VIRT_HOSTS=("172.21.155.181" "172.21.155.182" "172.21.155.183" "172.21.155.184" "172.21.155.185" "172.21.155.186" "172.21.155.187" "172.21.155.188")

  ZAMA_OPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_OPXY_VIRT_HOSTS=("172.21.155.108" "172.21.155.111" "172.21.155.113" "172.21.155.114" "172.21.155.115" "172.21.155.116" "172.21.155.117" "172.21.155.118")


  ZAMA_TRACKER_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_TRACKER_VIRT_HOSTS=("172.21.155.100" "172.21.155.103")

  ZAMA_CLK_TRACKER_PHYS_HOSTS=(${ZAMA_TRACKER_PHYS_HOSTS[@]})
  ZAMA_CLK_TRACKER_VIRT_HOSTS=("__specify_clk_tracker_virt_IP_on_bid101__" "__specify_clk_tracker_virt_IP_on_bid102__")

  ZAMA_CNV_TRACKER_PHYS_HOSTS=(${ZAMA_TRACKER_PHYS_HOSTS[@]})
  ZAMA_CNV_TRACKER_VIRT_HOSTS=("__specify_cnv_tracker_virt_IP_on_bid101__" "__specify_cnv_tracker_virt_IP_on_bid102__")

  ZAMA_MATCHER_PHYS_HOSTS=(${ZAMA_TRACKER_PHYS_HOSTS[@]})
  ZAMA_MATCHER_VIRT_HOSTS=("172.21.155.101" "172.21.155.104" "172.21.155.133" "172.21.155.134" "172.21.155.135" "172.21.155.136" "172.21.155.137" "172.21.155.138")

  ZAMA_ARTB_URI_HOSTNAME="rtb-apx.bidder8.mookie1.com"
  ZAMA_CRTB_URI_HOSTNAME="rtb-cwb.bidder7.mookie1.com"
  ZAMA_FRTB_URI_HOSTNAME="rtb-fb.bidder8.mookie1.com"
  ZAMA_GRTB_URI_HOSTNAME="rtb-adx.bidder8.mookie1.com"
  ZAMA_MRTB_URI_HOSTNAME="rtb-aml.bidder7.mookie1.com"
  ZAMA_RRTB_URI_HOSTNAME="rtb-rbc.bidder8.mookie1.com"
  ZAMA_YRTB_URI_HOSTNAME="rtb-rmx.bidder7.mookie1.com"
  ZAMA_PRTB_URI_HOSTNAME="rtb-pbm.bidder8.mookie1.com"
  ZAMA_ORTB_URI_HOSTNAME="rtb-opx.bidder8.mookie1.com"

  ZAMA_GTRK_URI_HOSTNAME="tracker.bidder7.mookie1.com"

  ZAMA_CTRK_URI_HOSTNAME=${ZAMA_GTRK_URI_HOSTNAME}
  ZAMA_FTRK_URI_HOSTNAME=${ZAMA_GTRK_URI_HOSTNAME}
  ZAMA_MTRK_URI_HOSTNAME=${ZAMA_GTRK_URI_HOSTNAME}
  ZAMA_RTRK_URI_HOSTNAME=${ZAMA_GTRK_URI_HOSTNAME}
  ZAMA_STRK_URI_HOSTNAME=${ZAMA_GTRK_URI_HOSTNAME}
  ZAMA_YTRK_URI_HOSTNAME=${ZAMA_GTRK_URI_HOSTNAME}
  ZAMA_PTRK_URI_HOSTNAME=${ZAMA_GTRK_URI_HOSTNAME}

  ZAMA_CLTRK_URI_HOSTNAME="tracker-clk.bidder7.mookie1.com"
  ZAMA_CVTRK_URI_HOSTNAME="tracker-cnv.bidder7.mookie1.com"

  ZAMA_MATCHER_URI_HOSTNAME="matcher.bidder7.mookie1.com"

  ZAMA_AMTCH_URI_HOSTNAME="matcher-apx.bidder7.mookie1.com"
  ZAMA_CMTCH_URI_HOSTNAME="matcher-cwb.bidder7.mookie1.com"
  ZAMA_GMTCH_URI_HOSTNAME=${ZAMA_MATCHER_URI_HOSTNAME}
  ZAMA_MMTCH_URI_HOSTNAME="matcher-aml.bidder7.mookie1.com"
  ZAMA_RMTCH_URI_HOSTNAME="matcher-rbc.bidder7.mookie1.com"
  ZAMA_YMTCH_URI_HOSTNAME="matcher-rmx.bidder7.mookie1.com"
  ZAMA_PMTCH_URI_HOSTNAME="matcher-pbm.bidder7.mookie1.com"
  ZAMA_OMTCH_URI_HOSTNAME="matcher-opx.bidder7.mookie1.com"

  ZWF_DEFAULT_PORT=11200

                 # rtbsloop1us2
  ZWF_LGRDR_HOSTS=(10.73.44.107)
  ZWF_LGRDR_PORT=${ZWF_DEFAULT_PORT}

                 # rtbmem1us2   rtbmem2us2   rtbmem1us3     rtbmem2us3
  ZWF_SCFDR_HOSTS=(10.73.44.105 10.73.44.106 172.21.155.106 172.21.155.107)
  ZWF_SCFDR_PORT=${ZWF_DEFAULT_PORT}

                 # rtbsloop1us2 rtbvln3us3 aka rtbsloop1us3
  ZWF_FCFDR_HOSTS=(10.73.44.107 172.21.155.30)
  ZWF_FCFDR_PORT=11202

  ZWF_BID_FILTERING_TYPE="time_framed_with_resource_limiting:900:150000"

  ZWF_WF_DEFINITION_TEMPLATE="template_zama_wfd_multidc.xml"
  ZWF_WF_COMMUNICATION_TEMPLATE="template_zama_wfc_multidc.xml"

#  ZAMA_MATCHER_ADMELD_CM_URI="{protocol}://tag.admeld.com/id?redirect={protocol}://${ZAMA_MMTCH_URI_HOSTNAME}${ZAMA_MATCHER_ADMELD_ENTRY_URI_PATH}?uid=[admeld_user_id]%26can={allowed_chain}"
  ZAMA_MATCHER_APPNEXUS_CM_URI="{protocol}://ib.adnxs.com/getuid?{protocol}://${ZAMA_AMTCH_URI_HOSTNAME}${ZAMA_MATCHER_APPNEXUS_ENTRY_URI_PATH}?can={allowed_chain}%26adnxs_uid=\$UID"
  ZAMA_MATCHER_CTXWEB_CM_URI="{protocol}://bh.contextweb.com/bh/rtset?do=add\&pid=536088\&ev={mookie}\&rurl={protocol}://${ZAMA_CMTCH_URI_HOSTNAME}/do-association?return=ctxweb%26can={allowed_chain}"
  ZAMA_MATCHER_FACEBOOK_CM_URI="{protocol}://www.facebook.com/fr/u.php?p=323034224450795\&m={mookie}"
  ZAMA_MATCHER_GOOGLE_CM_URI_V1="{protocol}://cm.g.doubleclick.net/pixel?nid=themig\&can={allowed_chain}"
  ZAMA_MATCHER_GOOGLE_CM_URI_V2="{protocol}://cm.g.doubleclick.net/pixel?google_nid=themig\&google_cm\&google_sc\&can={allowed_chain}\&v2"
  ZAMA_MATCHER_GOOGLE_CM_URI=${ZAMA_MATCHER_GOOGLE_CM_URI_V2}
  ZAMA_MATCHER_RUBICON_CM_URI='{protocol}://pixel.rubiconproject.com/tap.php?v=7259\&nid=2211\&put={mookie}\&expires={ttl_in_days}'
  ZAMA_MATCHER_PUBMATIC_CM_URIS="http://image2.pubmatic.com/AdServer/Pug?vcode=bz0yJnR5cGU9MSZjb2RlPTI0NzgmdGw9MTI5NjAw\&piggybackCookie=uid:{mookie}\&r=http://${ZAMA_PMTCH_URI_HOSTNAME}/do-association?return=pubmatic%26can={allowed_chain} \\\\\n\\t\\thttps://simage2.pubmatic.com/AdServer/Pug?vcode=bz0yJnR5cGU9MSZjb2RlPTI0NzgmdGw9MTI5NjAw\&piggybackCookie=uid:{mookie}\&r=https://${ZAMA_PMTCH_URI_HOSTNAME}/do-association?return=pubmatic%26can={allowed_chain}"
  ZAMA_MATCHER_OPENX_CM_URI="{protocol}://r.openx.net/set?pid=c63efebc-c767-c810-6d13-67f0191ec590\&rtb={mookie}"

  ZAMA_LGC_TOPOLOGY_TEMPLATE="template_lgc_zama_topology_multidc.xml"

  ZAMA_RTLG_PERIOD=10

  ZAMA_LGC_EXTERN_IOBUFF_SIZE=16777216

  ZAMA_MATCHER_ASM_LOGGING="not_used"

#  ZAMA_OBE_EXPLORATION_SHARE=0.25
  ZAMA_OBE_ENABLED="false"

  ZWF_FCDB_CLEANUP_FREQ_SEC=3600

  ZAMA_VHOST_ERRORLOG_TEMPLATE='ErrorLog "|/usr/sbin/rotatelogs /var/home/httpd_logs/__ZAMA_VHOST_ERRORLOG_NAME__.%Y-%m-%d-%H_%M_%S 1024M"'
  ZAMA_VHOST_ACCESSLOG_TEMPLATE='TransferLog "|/usr/sbin/rotatelogs /var/home/httpd_logs/__ZAMA_VHOST_ACCESSLOG_NAME__.%Y-%m-%d-%H_%M_%S 1024M"'
  ZAMA_VHOST_KEEPALIVE_TEMPLATE="KeepAlive On\nMaxKeepAliveRequests 1000\nKeepAliveTimeout 1"

  ZAMA_GRTB_TARGET_GGL_GEO="false"
  ZAMA_PXY_LOG_COUNTERS_PERIOD_SEC=0

  ZAMA_GRTB_CFG_BID_THREADS=40

  ZAMA_GRTB_CC_LOG_FILE="/var/home/appmgr/zama/work/grtb/iinfo/rtb_cc_log"

  ZAMA_GRTB_VENDOR_IDS_TO_MATCH="87"

  ZAMA_GRTB_EXCLUDED_AGENT_STRINGS='<excluded_agent>\n    <substring>AppleWebKit</substring>\n    <substring>Safari</substring>\n    <substring negated="true">Chrome</substring>\n  </excluded_agent>'

  ZAMA_GRTB_ALLOW_NO_SEAT_CAMPAIGNS="true"

  ZAMA_UDS_SOCKETS_NUM=1

  ZAMA_UDP_PACING_CHK_PERIOD=100000
  ZAMA_UDP_PACING_RCVQ_MIN=10000
  ZAMA_UDP_PACING_RCVQ_MAX=40000
  ZAMA_UDP_PACING_RCVQ_PCT_CHANGE=110

# Violin Configs

  ZAMA_VDB_READER_ACCESS_POINT=239.192.27.10
  ZAMA_VDB_READER_ACCESS_POINT_PORT_MIN=30210
  ZAMA_VDB_READER_ACCESS_POINT_PORT_MAX=30239

  ZAMA_VDB_WRITER_ACCESS_POINT=${ZAMA_VDB_READER_ACCESS_POINT}
  ZAMA_VDB_WRITER_ACCESS_POINT_PORT_MIN=${ZAMA_VDB_READER_ACCESS_POINT_PORT_MIN}
  ZAMA_VDB_WRITER_ACCESS_POINT_PORT_MAX=${ZAMA_VDB_READER_ACCESS_POINT_PORT_MAX}

  ZAMA_VDB_ADMIN_ACCESS_POINT=${ZAMA_VDB_READER_ACCESS_POINT}
  ZAMA_VDB_ADMIN_ACCESS_POINT_PORT_MIN=30300
  ZAMA_VDB_ADMIN_ACCESS_POINT_PORT_MAX=${ZAMA_VDB_ADMIN_ACCESS_POINT_PORT_MIN}

  ZAMA_VDB_SVC_CONFIGS=(wc_vdb-1_svc_config.xml@rtbvln1us3 wc_vdb-2_svc_config.xml@rtbvln2us3)

  ZAMA_VLDR_UPLOADER_THREADS=8

  ZAMA_COMMON_DEF_PROTO_LOGGING="Off"

