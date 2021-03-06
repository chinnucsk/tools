#========================================
# Description of ZAMA QA environment
#========================================

# Performance counter service ports for different components
  ZWF_PERF_PORT=8801
  ZAMA_STCOL_PERF_PORT=8802
  ZAMA_VLDR_PERF_PORT=8803
  ZAMA_VBKP_PERF_PORT=8804
  ZAMA_GRTB_PERF_PORT=8805

                 # 10.65.48.31    10.65.48.32	10.65.48.115)
  ZAMA_GRTB_HOSTS=(rtbbid1us2-qa2 rtbbid2us2-qa2)
  ZAMA_GRTB_HOSTS_NUM=2
  ZAMA_GRTB_PORT=11100

                  # 10.65.48.33    10.65.48.248
  ZAMA_STCOL_HOSTS=(rtbmem1us2-qa2 rtbmem2us2-qa2)
  ZAMA_STCOL_PORT=11102
  ZAMA_NEW_STCOL_PORT=11104

  # 5 min
  ZAMA_STCOL_POLL_PERIOD=5000

                         # 10.65.48.33
  ZAMA_STCOL_ACCESS_POINT="rtbmem1us2-qa2"
  ZAMA_STCOL_ACCESS_POINT_PORT=${ZAMA_STCOL_PORT}
  ZAMA_NEW_STCOL_ACCESS_POINT_PORT=${ZAMA_NEW_STCOL_PORT}


  ZAMA_GPXY_PHYS_HOSTS=("10.73.48.135" "10.73.48.136")
  ZAMA_GPXY_VIRT_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})

  ZAMA_APXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_APXY_VIRT_HOSTS=("10.73.48.187" "10.73.48.192")

  ZAMA_CPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_CPXY_VIRT_HOSTS=("10.73.48.194" "10.73.48.195")

  ZAMA_FPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_FPXY_VIRT_HOSTS=("10.73.48.182" "10.73.48.190")

  ZAMA_MPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_MPXY_VIRT_HOSTS=("10.73.48.198" "10.73.48.199")

  ZAMA_EPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_EPXY_VIRT_HOSTS=("10.73.48.200" "10.73.48.201")

  ZAMA_RPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_RPXY_VIRT_HOSTS=("10.73.48.196" "10.73.48.197")

  ZAMA_YPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_YPXY_VIRT_HOSTS=("10.73.48.183" "10.73.48.189")

  ZAMA_PPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_PPXY_VIRT_HOSTS=("10.73.48.204" "10.73.48.205")

  ZAMA_APIPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_APIPXY_VIRT_HOSTS=("10.73.48.202" "10.73.48.203")

  ZAMA_TRACKER_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_TRACKER_VIRT_HOSTS=("10.73.48.175" "10.73.48.186")

  ZAMA_CLK_TRACKER_PHYS_HOSTS=(${ZAMA_TRACKER_PHYS_HOSTS[@]})
  ZAMA_CLK_TRACKER_VIRT_HOSTS=("10.73.48.184" "10.73.48.191")
  ZAMA_CLK_TRACKER_FB_VIRT_HOSTS=(${ZAMA_CLK_TRACKER_VIRT_HOSTS[@]})

  ZAMA_CNV_TRACKER_PHYS_HOSTS=(${ZAMA_TRACKER_PHYS_HOSTS[@]})
  ZAMA_CNV_TRACKER_VIRT_HOSTS=("10.73.48.185" "10.73.48.193")

  ZAMA_MATCHER_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_MATCHER_VIRT_HOSTS=("10.73.48.176" "10.73.48.188")

  ZAMA_ARTB_URI_HOSTNAME=${ZAMA_APXY_VIRT_HOSTS[0]}
  ZAMA_CRTB_URI_HOSTNAME=${ZAMA_CPXY_VIRT_HOSTS[0]}
  ZAMA_FRTB_URI_HOSTNAME=${ZAMA_FPXY_VIRT_HOSTS[0]}
  ZAMA_GRTB_URI_HOSTNAME=${ZAMA_GPXY_VIRT_HOSTS[0]}
  ZAMA_MRTB_URI_HOSTNAME=${ZAMA_GPXY_VIRT_HOSTS[0]}
  ZAMA_RRTB_URI_HOSTNAME=${ZAMA_GPXY_VIRT_HOSTS[0]}
  ZAMA_YRTB_URI_HOSTNAME=${ZAMA_YPXY_VIRT_HOSTS[0]}
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

                 # rtbsloop1us2-qa2
  ZWF_LGRDR_HOSTS=(10.73.48.101)
  ZWF_LGRDR_PORT=${ZWF_DEFAULT_PORT}

                 # rtbmem1us2-qa2 rtbmem2us2-qa2
  ZWF_SCFDR_HOSTS=(10.73.48.140    10.73.48.207)
  ZWF_SCFDR_PORT=${ZWF_DEFAULT_PORT}

  ZWF_FCFDR_HOSTS=${ZWF_LGRDR_HOSTS}
  ZWF_FCFDR_PORT=11202

  ZWF_BID_FILTERING_TYPE=""

  ZAMA_COMMON_LOG_LEVEL=trace
  ZAMA_GRTB_PROXY_TIMEOUT=2000

  ZAMA_GRTB_STALE_SLEEP_PERIOD_SEC=1
  ZAMA_GRTB_MAX_STALE_BIDS=500000

  ZAMA_GRTB_LOG_FLAGS="LOG_GEO LOG_EXCHANGE_INFO"

  ZAMA_GRTB_VENDOR_IDS_TO_MATCH="87"

  ZAMA_PRIMARY_DB_HOST="ztdb-qa-scan.dc.ash.247realmedia.com."
  ZAMA_PRIMARY_DB_SVCNAME="S1ZAPLP"
  ZAMA_PRIMARY_DB_USER="zap_bidder_pressuser"
  ZAMA_PRIMARY_DB_PSWD="zap_bidder_pressuser"

  ZAMA_ASM_DEF_EXPIRATION_SEC=0

  ZAMA_VHOST_SSL_ENGINE_STATE="on"

  ZAMA_GRTB_EXCLUDED_AGENT_STRINGS='<excluded_agent>\n    <substring>AppleWebKit</substring>\n    <substring>Safari</substring>\n    <substring negated="true">Chrome</substring>\n  </excluded_agent>'

  ZAMA_OBE_ENABLED="true"

  ZAMA_PRESS_LOG_ALL_CAMPAIGNS="true"
  ZAMA_PRESS_AUTO_NEGATE_SEGMENT_LIST='auto_negate_segment_list="20000510"'

  ZAMA_VDB_READER_ACCESS_POINT=rtbvln1us2-qa2.dc.ash.247realmedia.com
  ZAMA_VDB_READER_ACCESS_POINT_PORT_MIN=30210
  ZAMA_VDB_READER_ACCESS_POINT_PORT_MAX=30240

  ZAMA_VDB_WRITER_ACCESS_POINT=${ZAMA_VDB_READER_ACCESS_POINT}
  ZAMA_VDB_WRITER_ACCESS_POINT_PORT_MIN=${ZAMA_VDB_READER_ACCESS_POINT_PORT_MIN}
  ZAMA_VDB_WRITER_ACCESS_POINT_PORT_MAX=${ZAMA_VDB_READER_ACCESS_POINT_PORT_MAX}

  ZAMA_VDB_ADMIN_ACCESS_POINT=${ZAMA_VDB_READER_ACCESS_POINT}
  ZAMA_VDB_ADMIN_ACCESS_POINT_PORT_MIN=30300
  ZAMA_VDB_ADMIN_ACCESS_POINT_PORT_MAX=${ZAMA_VDB_ADMIN_ACCESS_POINT_PORT_MIN}

  ZAMA_VDB_DEF_TIMEOUT_R_MSEC=2000
  ZAMA_VDB_DEF_TIMEOUT_W_MSEC=2000

  ZAMA_VDB_SVC_CONFIGS=(qa2_vdb_svc_config.xml@rtbvln1us2-qa2)

  ZAMA_VLDR_UPLOADER_THREADS=2
  # '0' - disables throttling
  ZAMA_VLDR_THROTTLE_ON_READ_IPS=0

  ZAMA_COMMON_DEF_PROTO_LOGGING="Off"

  ZAMA_GRTB_PERF_PORT=8805
