#========================================
# Description of ZAMA East Coast Staging environment
#========================================

                 # 10.73.47.200      10.73.47.201      10.73.47.202      10.73.47.203
  ZAMA_GRTB_HOSTS=(rtbbid1us2-stg1   rtbbid2us2-stg1   rtbbid3us2-stg1   rtbbid4us2-stg1)
  ZAMA_GRTB_HOSTS_NUM=50
  ZAMA_GRTB_PORT=11100
  ZAMA_GRTB_PROXY_TIMEOUT=2000
 
                 # 10.73.47.204    10.73.47.205
  ZAMA_STCOL_HOSTS=(rtbmem1us2-stg1 rtbmem2us2-stg1)
  ZAMA_STCOL_PORT=11102
  ZAMA_NEW_STCOL_PORT=11104
  ZAMA_STCOL_PERF_PORT=8802

  ZAMA_STCOL_POLL_PERIOD=1000


  ZAMA_VDB_DEF_TIMEOUT_R_MSEC=2000
  ZAMA_VDB_DEF_TIMEOUT_W_MSEC=2000

                         # 10.73.44.105
  ZAMA_STCOL_ACCESS_POINT="rtbmem1us2-stg1"
  ZAMA_STCOL_ACCESS_POINT_PORT=${ZAMA_STCOL_PORT}
  ZAMA_NEW_STCOL_ACCESS_POINT_PORT=${ZAMA_NEW_STCOL_PORT}

# <<< ZAMA RTB DB configuration
                            #10.73.47.214                10.73.47.215                10.73.47.216           10.73.44.129
  ZAMA_UMDB_NODES=(0000_0000@rtbmdb2us2-stg1   0001_0000@rtbmdb3us2-stg1   0002_0000@rtbmdb4us2-stg1   0003_0000@rtbmdb5us2-stg1)

                             #10.73.44.140           10.73.44.141           10.73.44.155           10.73.44.156
  ZAMA_ASMDB_NODES=(0000_0000@rtbmdb6us2-stg1   0001_0000@rtbmdb7us2-stg1   0002_0000@rtbmdb8us2-stg1   0003_0000@rtbmdb9us2-stg1)

                            #10.73.47.214                     10.73.47.215                     10.73.47.216                10.73.44.129              10.73.44.122                10.73.44.123                10.73.47.216                10.73.44.129
  ZAMA_FCDB_NODES=(0000_0000@rtbmdb2us2-stg1:6380   0001_0000@rtbmdb3us2-stg1:6380   0002_0000@rtbmdb4us2-stg1:6380   0003_0000@rtbmdb5us2-stg1:6380 0004_0000@rtbmdb2us2-stg1:6381   0005_0000@rtbmdb3us2-stg1:6381   0006_0000@rtbmdb4us2-stg1:6381   0007_0000@rtbmdb5us2-stg1:6381)
  # definition of FC DB nodes if half of them be transferred to rtbmdb[6-9
   # definition of FC DB nodes if half of them be transferred to rtbmdb[6-9]...:	   # definition of FC DB nodes if half of them be transferred to rtbmdb[6-9
                             #10.73.44.122              10.73.44.123              10.73.47.216              10.73.44.129              10.73.44.140              10.73.44.141              10.73.44.155              10.73.44.156
   # ZAMA_FCDB_NODES=(0000_0000@rtbmdb2us2-stg1:6380 0001_0000@rtbmdb3us2-stg1:6380 0002_0000@rtbmdb4us2-stg1:6380 0003_0000@rtbmdb5us2-stg1:6380 0004_0000@rtbmdb6us2-stg1:6380 0005_0000@rtbmdb7us2-stg1:6380 0006_0000@rtbmdb8us2-stg1:6380 0007_0000@rtbmdb9us2-stg1:6380)

   ZAMA_RTBDB_GROUPS=(UMDB ASMDB FCDB)
   # RTB DB config file names for "all separate" config...:
   ZAMA_RTBDB_CONFIGS=(rsvc_umdb_config.xml rsvc_asmdb_config.xml rsvc_fcdb_config.xml)
   ZAMA_RTBDB_CREATE_CONFIG=1
 # >>>
   ZAMA_TRACKER_PHYS_HOSTS=("10.73.47.200" "10.73.47.201" "10.73.47.202" "10.73.47.203")

   ZAMA_GPXY_PHYS_HOSTS=(${ZAMA_TRACKER_PHYS_HOSTS[@]})
   ZAMA_GPXY_VIRT_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})

   ZAMA_APXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
   ZAMA_APXY_VIRT_HOSTS=("10.73.47.166" "10.73.47.176" "10.73.47.186" "10.73.47.196")

   ZAMA_CPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
   ZAMA_CPXY_VIRT_HOSTS=("10.73.47.167" "10.73.47.177" "10.73.47.187" "10.73.47.197")

   ZAMA_FPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
   ZAMA_FPXY_VIRT_HOSTS=("10.73.47.162" "10.73.47.172" "10.73.47.182" "10.73.47.192")

   ZAMA_PPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
   ZAMA_PPXY_VIRT_HOSTS=("10.73.47.238" "10.73.47.239" "10.73.47.243" "10.73.47.244")

   ZAMA_MPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
   ZAMA_MPXY_VIRT_HOSTS=("10.73.47.168" "10.73.47.178" "10.73.47.188" "10.73.47.198")

   ZAMA_RPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
   ZAMA_RPXY_VIRT_HOSTS=("10.73.47.162" "10.73.47.172" "10.73.47.182" "10.73.47.192")

   ZAMA_EPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
   ZAMA_EPXY_VIRT_HOSTS=("10.73.47.165" "10.73.47.175" "10.73.47.185" "10.73.47.195")

   ZAMA_TRACKER_VIRT_HOSTS=("10.73.47.160" "10.73.47.170" "10.73.47.180" "10.73.47.190")

   ZAMA_CLK_TRACKER_PHYS_HOSTS=(${ZAMA_TRACKER_PHYS_HOSTS[@]})
   ZAMA_CLK_TRACKER_VIRT_HOSTS=("10.73.47.163" "10.73.47.173" "10.73.47.183" "10.73.47.193")

   ZAMA_CNV_TRACKER_PHYS_HOSTS=(${ZAMA_TRACKER_PHYS_HOSTS[@]})
   ZAMA_CNV_TRACKER_VIRT_HOSTS=("10.73.47.164" "10.73.47.174" "10.73.47.184" "10.73.47.194")

   ZAMA_MATCHER_PHYS_HOSTS=(${ZAMA_TRACKER_PHYS_HOSTS[@]})
   ZAMA_MATCHER_VIRT_HOSTS=("10.73.47.161" "10.73.47.171" "10.73.47.181" "10.73.47.191")

   ZAMA_APIPXY_PHYS_HOSTS=(${ZAMA_TRACKER_PHYS_HOSTS[@]})
   ZAMA_APIPXY_VIRT_HOSTS=("10.73.47.169" "10.73.47.179" "10.73.47.189" "10.73.47.199")

   ZAMA_ARTB_URI_HOSTNAME=${ZAMA_APXY_VIRT_HOSTS[0]}
   ZAMA_CRTB_URI_HOSTNAME=${ZAMA_CPXY_VIRT_HOSTS[0]}
   ZAMA_GRTB_URI_HOSTNAME=${ZAMA_GPXY_VIRT_HOSTS[0]}
   ZAMA_MRTB_URI_HOSTNAME=${ZAMA_GPXY_VIRT_HOSTS[0]}
   ZAMA_RRTB_URI_HOSTNAME=${ZAMA_GPXY_VIRT_HOSTS[0]}
   ZAMA_ERTB_URI_HOSTNAME=${ZAMA_EPXY_VIRT_HOSTS[0]}
   ZAMA_PRTB_URI_HOSTNAME=${ZAMA_PPXY_VIRT_HOSTS[0]}

   ZAMA_GTRK_URI_HOSTNAME=${ZAMA_TRACKER_VIRT_HOSTS[0]}
   ZAMA_CTRK_URI_HOSTNAME=${ZAMA_GTRK_URI_HOSTNAME}
   ZAMA_FTRK_URI_HOSTNAME=${ZAMA_GTRK_URI_HOSTNAME}
   ZAMA_MTRK_URI_HOSTNAME=${ZAMA_GTRK_URI_HOSTNAME}
   ZAMA_RTRK_URI_HOSTNAME=${ZAMA_GTRK_URI_HOSTNAME}
   ZAMA_STRK_URI_HOSTNAME=${ZAMA_GTRK_URI_HOSTNAME}
   ZAMA_YTRK_URI_HOSTNAME=${ZAMA_GTRK_URI_HOSTNAME}
   ZAMA_ETRK_URI_HOSTNAME=${ZAMA_GTRK_URI_HOSTNAME}
   ZAMA_PTRK_URI_HOSTNAME=${ZAMA_GTRK_URI_HOSTNAME}


   ZAMA_CLTRK_URI_HOSTNAME=${ZAMA_CLK_TRACKER_VIRT_HOSTS[0]}
   ZAMA_CVTRK_URI_HOSTNAME=${ZAMA_CNV_TRACKER_VIRT_HOSTS[0]}

   ZAMA_MATCHER_URI_HOSTNAME=${ZAMA_MATCHER_VIRT_HOSTS[0]}

   ZAMA_AMTCH_URI_HOSTNAME=${ZAMA_MATCHER_URI_HOSTNAME}
   ZAMA_CMTCH_URI_HOSTNAME=${ZAMA_MATCHER_URI_HOSTNAME}
   ZAMA_GMTCH_URI_HOSTNAME=${ZAMA_MATCHER_URI_HOSTNAME}
   ZAMA_MMTCH_URI_HOSTNAME=${ZAMA_MATCHER_URI_HOSTNAME}
   ZAMA_RMTCH_URI_HOSTNAME=${ZAMA_MATCHER_URI_HOSTNAME}
   ZAMA_YMTCH_URI_HOSTNAME=${ZAMA_MATCHER_URI_HOSTNAME}
   ZAMA_EMTCH_URI_HOSTNAME=${ZAMA_MATCHER_URI_HOSTNAME}
   ZAMA_PMTCH_URI_HOSTNAME=${ZAMA_MATCHER_URI_HOSTNAME}

   ZWF_DEFAULT_PORT=11200

                  # rtbsloop1us2-stg1
   ZWF_LGRDR_HOSTS=(10.73.47.206)
   ZWF_LGRDR_PORT=${ZWF_DEFAULT_PORT}

                  # rtbmem1us2-stg1 rtbmem2us2-stg1
   ZWF_SCFDR_HOSTS=(10.73.47.204 10.73.47.205)
   ZWF_SCFDR_PORT=${ZWF_DEFAULT_PORT}

   ZWF_FCFDR_HOSTS=${ZWF_LGRDR_HOSTS}
   ZWF_FCFDR_PORT=11202

   ZAMA_RTLG_PERIOD=10

   ZAMA_LGC_EXTERN_IOBUFF_SIZE=16777216

 #  ZAMA_OBE_EXPLORATION_SHARE=0.25
   ZAMA_OBE_ENABLED="false"

   ZWF_FCDB_CLEANUP_FREQ_SEC=3600

   ZAMA_VHOST_ERRORLOG_TEMPLATE='ErrorLog "|/usr/sbin/rotatelogs /var/home/httpd_logs/__ZAMA_VHOST_ERRORLOG_NAME__.%Y-%m-%d-%H_%M_%S 1024M"'

   ZAMA_TRACKER_VHOST_KEEPALIVE_CFG="KeepAlive On\nMaxKeepAliveRequests 1000\nKeepAliveTimeout 300"

  ZAMA_GRTB_TARGET_GGL_GEO="false"
  ZAMA_PXY_LOG_COUNTERS_PERIOD_SEC=0

  #ZAMA_GRTB_CFG_BID_THREADS=40

#  ZAMA_GRTB_CC_LOG_FILE="/var/home/appmgr/zama/work/grtb/iinfo/rtb_cc_log"
#  ZAMA_GRTB_PERF_COUNTERS_FILE="not_used"

  ZAMA_GRTB_VENDOR_IDS_TO_MATCH="87"

#  ZAMA_GRTB_VDB_CONFIGURATION=""

  ZAMA_VDB_READER_ACCESS_POINT="10.73.47.146"
  ZAMA_VDB_READER_ACCESS_POINT_PORT_MIN=30210
  ZAMA_VDB_READER_ACCESS_POINT_PORT_MAX=30239

  ZAMA_VDB_WRITER_ACCESS_POINT=${ZAMA_VDB_READER_ACCESS_POINT}
  ZAMA_VDB_WRITER_ACCESS_POINT_PORT_MIN=${ZAMA_VDB_READER_ACCESS_POINT_PORT_MIN}
  ZAMA_VDB_WRITER_ACCESS_POINT_PORT_MAX=${ZAMA_VDB_READER_ACCESS_POINT_PORT_MAX}

# enable reading from Violinm for matcher/fc_feeder/bidder
  ZAMA_VDB_CONFIG_READER_SECTION_BEGIN="<!-- reader section begin -->"
  ZAMA_VDB_CONFIG_READER_SECTION_END="<!-- reader section end -->"

  ZAMA_UDS_SOCKETS_NUM=4

  ZAMA_UDP_PACING_CHK_PERIOD=50000
  ZAMA_UDP_PACING_RCVQ_MIN=100
  ZAMA_UDP_PACING_RCVQ_MAX=5000
  ZAMA_UDP_PACING_RCVQ_PCT_CHANGE=110

  ZAMA_TRK_CREATIVE_AUDIT_TIMEOUT=2000
  ZAMA_TRK_GET_CREATIVE_TIMEOUT=2000

  ZAMA_PRIMARY_DB_HOST="10.73.47.127"
  ZAMA_PRIMARY_DB_SVCNAME="S3ZAPLP"
  ZAMA_PRIMARY_DB_USER="ZAP_BIDDER_PRESSUSER"
  ZAMA_PRIMARY_DB_PSWD="ZAP_BIDDER_PRESSUSER"
