#========================================
# Description of ZAMA East Coast production environment
#========================================

                 # 10.73.44.103 10.73.44.104 10.73.44.215 10.73.44.222 10.73.44.229 10.73.44.236 10.73.44.243 10.73.44.250
  ZAMA_GRTB_HOSTS=(rtbbid1us2   rtbbid2us2   rtbbid3us2   rtbbid4us2   rtbbid5us2   rtbbid6us2   rtbbid7us2   rtbbid8us2 rtbbid9us2 rtbbid10us2 rtbbid13us2 rtbbid14us2 rtbbid15us2 rtbbid16us2 rtbbid17us2 rtbbid18us2 rtbbid19us2 rtbbid20us2)
  ZAMA_GRTB_HOSTS_NUM=500
  ZAMA_GRTB_PORT=11100

                  # 10.73.44.105 10.73.44.106
  ZAMA_STCOL_HOSTS=(rtbmem1us2 rtbmem2us2)
  ZAMA_STCOL_PORT=11102
  ZAMA_NEW_STCOL_PORT=11104
  ZAMA_STCOL_PERF_PORT=8802

  ZAMA_STCOL_POLL_PERIOD=1000

                         # 10.73.44.105
  ZAMA_STCOL_ACCESS_POINT="rtbmem1us2"
  ZAMA_STCOL_ACCESS_POINT_PORT=${ZAMA_STCOL_PORT}
  ZAMA_NEW_STCOL_ACCESS_POINT_PORT=${ZAMA_NEW_STCOL_PORT}

# <<< ZAMA RTB DB configuration
                            #10.73.44.122           10.73.44.123           10.73.44.124           10.73.44.129
  ZAMA_UMDB_NODES=(0000_0000@rtbmdb2us2   0001_0000@rtbmdb3us2   0002_0000@rtbmdb4us2   0003_0000@rtbmdb5us2)

                             #10.73.44.140           10.73.44.141           10.73.44.155           10.73.44.156
  ZAMA_ASMDB_NODES=(0000_0000@rtbmdb6us2   0001_0000@rtbmdb7us2   0002_0000@rtbmdb8us2   0003_0000@rtbmdb9us2)

                            #10.73.44.122                10.73.44.123                10.73.44.124                10.73.44.129              10.73.44.122                10.73.44.123                10.73.44.124                10.73.44.129
  ZAMA_FCDB_NODES=(0000_0000@rtbmdb2us2:6380   0001_0000@rtbmdb3us2:6380   0002_0000@rtbmdb4us2:6380   0003_0000@rtbmdb5us2:6380 0004_0000@rtbmdb2us2:6381   0005_0000@rtbmdb3us2:6381   0006_0000@rtbmdb4us2:6381   0007_0000@rtbmdb5us2:6381)
  # definition of FC DB nodes if half of them be transferred to rtbmdb[6-9]...:
                            #10.73.44.122              10.73.44.123              10.73.44.124              10.73.44.129              10.73.44.140              10.73.44.141              10.73.44.155              10.73.44.156
  # ZAMA_FCDB_NODES=(0000_0000@rtbmdb2us2:6380 0001_0000@rtbmdb3us2:6380 0002_0000@rtbmdb4us2:6380 0003_0000@rtbmdb5us2:6380 0004_0000@rtbmdb6us2:6380 0005_0000@rtbmdb7us2:6380 0006_0000@rtbmdb8us2:6380 0007_0000@rtbmdb9us2:6380)

  ZAMA_RTBDB_GROUPS=(UMDB ASMDB FCDB)
  # RTB DB config file names for "all separate" config...:
  ZAMA_RTBDB_CONFIGS=(rsvc_umdb_config.xml rsvc_asmdb_config.xml rsvc_fcdb_config.xml)
  ZAMA_RTBDB_CREATE_CONFIG=1
# >>>
  ZAMA_TRACKER_PHYS_HOSTS=("10.73.44.103" "10.73.44.104" "10.73.44.215" "10.73.44.222" "10.73.44.229" "10.73.44.236" "10.73.44.243" "10.73.44.250")

  ZAMA_GPXY_PHYS_HOSTS=(${ZAMA_TRACKER_PHYS_HOSTS[@]} "10.73.44.10" "10.73.44.21" "10.73.43.140" "10.73.43.150" "10.73.43.31" "10.73.43.41" "10.73.43.51" "10.73.43.61" "10.73.43.71" "10.73.43.81" "10.73.43.110" "10.73.43.120" "10.73.43.100" "10.73.43.130")
  ZAMA_GPXY_VIRT_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})

  ZAMA_APXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_APXY_VIRT_HOSTS=("10.73.44.157" "10.73.44.158" "10.73.44.167" "10.73.44.168" "10.73.44.176" "10.73.44.177" "10.73.44.182" "10.73.44.183" "10.73.44.19" "10.73.44.64" "10.73.43.144" "10.73.43.154" "10.73.43.38" "10.73.43.48" "10.73.43.58" "10.73.43.68" "10.73.43.78" "10.73.43.88" "10.73.43.114" "10.73.43.124" "10.73.43.107" "10.73.43.134")

  ZAMA_CPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_CPXY_VIRT_HOSTS=("10.73.44.190" "10.73.44.191" "10.73.44.197" "10.73.44.201" "10.73.44.202" "10.73.44.203" "10.73.44.204" "10.73.44.209" "10.73.44.20" "10.73.44.65" "10.73.43.145" "10.73.43.155" "10.73.43.39" "10.73.43.49" "10.73.43.59" "10.73.43.69" "10.73.43.79" "10.73.43.89" "10.73.43.115" "10.73.43.125" "10.73.43.108" "10.73.43.135")

  ZAMA_FPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_FPXY_VIRT_HOSTS=("127.0.0.1" "127.0.0.1" "127.0.0.1" "127.0.0.1" "127.0.0.1" "127.0.0.1" "127.0.0.1" "127.0.0.1" "127.0.0.1" "127.0.0.1" "127.0.0.1" "127.0.0.1" "127.0.0.1" "127.0.0.1" "127.0.0.1" "127.0.0.1" "127.0.0.1" "127.0.0.1" "127.0.0.1" "127.0.0.1" "127.0.0.1" "127.0.0.1")


  ZAMA_PPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_PPXY_VIRT_HOSTS=("10.73.44.112" "10.73.44.115" "10.73.44.218" "10.73.44.225" "10.73.44.232" "10.73.44.239" "10.73.44.246" "10.73.44.53" "10.73.44.15" "10.73.44.24" "10.73.43.142" "10.73.43.152" "10.73.43.34" "10.73.43.44" "10.73.43.54" "10.73.43.64" "10.73.43.74" "10.73.43.84" "10.73.43.112" "10.73.43.122" "10.73.43.105" "10.73.43.132")


  ZAMA_MPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_MPXY_VIRT_HOSTS=("10.73.44.187" "10.73.44.193" "10.73.44.194" "10.73.44.195" "10.73.44.196" "10.73.44.210" "10.73.44.213" "10.73.44.214" "10.73.44.251" "10.73.44.252" "10.73.43.147" "10.73.43.157" "10.73.43.91" "10.73.43.92" "10.73.43.93" "10.73.43.94" "10.73.43.95" "10.73.43.96" "10.73.43.117" "10.73.43.127" "10.73.43.119" "10.73.43.134")

  ZAMA_RPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_RPXY_VIRT_HOSTS=("10.73.44.37" "10.73.44.38" "10.73.44.39" "10.73.44.41" "10.73.44.42" "10.73.44.43" "10.73.44.47" "10.73.44.48" "10.73.44.4" "10.73.44.5" "10.73.43.146" "10.73.43.156" "10.73.43.40" "10.73.43.50" "10.73.43.60" "10.73.43.70" "10.73.43.80" "10.73.43.90" "10.73.43.116" "10.73.43.126" "10.73.43.118" "10.73.43.136")

  ZAMA_YPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_YPXY_VIRT_HOSTS=("10.73.44.120" "10.73.44.121" "10.73.44.221" "10.73.44.228" "10.73.44.235" "10.73.44.242" "10.73.44.249" "10.73.44.56" "10.73.44.18"  "10.73.44.60" "10.73.43.37" "10.73.43.143" "10.73.43.153" "10.73.43.47" "10.73.43.57" "10.73.43.67" "10.73.43.77" "10.73.43.87" "10.73.43.113" "10.73.43.123" "10.73.43.106" "10.73.43.133")

  ZAMA_EPXY_PHYS_HOSTS=(${ZAMA_GPXY_PHYS_HOSTS[@]})
  ZAMA_EPXY_VIRT_HOSTS=("10.73.44.67" "10.73.44.68" "10.73.44.69" "10.73.44.70" "10.73.44.71" "10.73.44.72" "10.73.44.73" "10.73.44.74" "10.73.44.75" "10.73.44.253" "10.73.43.72" "10.73.43.82" "10.73.43.32" "10.73.43.42" "10.73.43.52" "10.73.43.62" "10.73.43.151" "10.73.43.141" "10.73.43.111" "10.73.43.121" "10.73.43.103" "10.73.43.131")

  ZAMA_TRACKER_VIRT_HOSTS=("10.73.44.110" "10.73.44.113" "10.73.44.216" "10.73.44.223" "10.73.44.230" "10.73.44.237" "10.73.44.244" "10.73.44.51")

  ZAMA_CLK_TRACKER_PHYS_HOSTS=(${ZAMA_TRACKER_PHYS_HOSTS[@]})
  ZAMA_CLK_TRACKER_VIRT_HOSTS=("10.73.44.116" "10.73.44.117" "10.73.44.219" "10.73.44.226" "10.73.44.233" "10.73.44.240" "10.73.44.247" "10.73.44.54")

  ZAMA_CNV_TRACKER_PHYS_HOSTS=(${ZAMA_TRACKER_PHYS_HOSTS[@]})
  ZAMA_CNV_TRACKER_VIRT_HOSTS=("10.73.44.118" "10.73.44.119" "10.73.44.220" "10.73.44.227" "10.73.44.234" "10.73.44.241" "10.73.44.248" "10.73.44.55")

  ZAMA_MATCHER_PHYS_HOSTS=(${ZAMA_TRACKER_PHYS_HOSTS[@]})
  ZAMA_MATCHER_VIRT_HOSTS=("10.73.44.111" "10.73.44.114" "10.73.44.217" "10.73.44.224" "10.73.44.231" "10.73.44.238" "10.73.44.245" "10.73.44.52")

  ZAMA_APIPXY_PHYS_HOSTS=(${ZAMA_TRACKER_PHYS_HOSTS[@]})
  ZAMA_APIPXY_VIRT_HOSTS=("10.73.44.76" "10.73.44.77" "10.73.44.78" "10.73.44.79" "10.73.44.80" "10.73.44.96" "10.73.44.97" "10.73.44.184")

  ZAMA_ARTB_URI_HOSTNAME="rtb-apx.bidder7.mookie1.com"
  ZAMA_CRTB_URI_HOSTNAME="rtb-cwb.bidder7.mookie1.com"
  ZAMA_FRTB_URI_HOSTNAME="rtb-fan.bidder7.mookie1.com"
  ZAMA_GRTB_URI_HOSTNAME="rtb-adx.bidder7.mookie1.com"
  ZAMA_MRTB_URI_HOSTNAME="rtb-aml.bidder7.mookie1.com"
  ZAMA_RRTB_URI_HOSTNAME="rtb-rbc.bidder7.mookie1.com"
  ZAMA_YRTB_URI_HOSTNAME="rtb-rmx.bidder7.mookie1.com"
  ZAMA_ERTB_URI_HOSTNAME="rtb-esm.bidder7.mookie1.com"
  ZAMA_PRTB_URI_HOSTNAME="rtb-pbm.bidder7.mookie1.com"

  ZAMA_API_URI_HOSTNAME="api.bidder7.mookie1.com"

  ZAMA_GTRK_URI_HOSTNAME="tracker.bidder7.mookie1.com"

  ZAMA_CTRK_URI_HOSTNAME=${ZAMA_GTRK_URI_HOSTNAME}
  ZAMA_FTRK_URI_HOSTNAME=${ZAMA_GTRK_URI_HOSTNAME}
  ZAMA_MTRK_URI_HOSTNAME=${ZAMA_GTRK_URI_HOSTNAME}
  ZAMA_RTRK_URI_HOSTNAME=${ZAMA_GTRK_URI_HOSTNAME}
  ZAMA_STRK_URI_HOSTNAME=${ZAMA_GTRK_URI_HOSTNAME}
  ZAMA_YTRK_URI_HOSTNAME=${ZAMA_GTRK_URI_HOSTNAME}
  ZAMA_ETRK_URI_HOSTNAME=${ZAMA_GTRK_URI_HOSTNAME}
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

  ZWF_DEFAULT_PORT=11200

                 # rtbsloop1us2
  ZWF_LGRDR_HOSTS=(10.73.44.107)
  ZWF_LGRDR_PORT=${ZWF_DEFAULT_PORT}

                 # rtbmem1us2
  ZWF_SCFDR_HOSTS=(10.73.44.105)
  ZWF_SCFDR_PORT=${ZWF_DEFAULT_PORT}

  ZWF_FCFDR_HOSTS=${ZWF_LGRDR_HOSTS}
  ZWF_FCFDR_PORT=11202

  ZWF_BID_FILTERING_TYPE="time_framed_with_resource_limiting:900:150000"

#  ZAMA_MATCHER_ADMELD_CM_URI="{protocol}://tag.admeld.com/id?redirect={protocol}://${ZAMA_MMTCH_URI_HOSTNAME}${ZAMA_MATCHER_ADMELD_ENTRY_URI_PATH}?uid=[admeld_user_id]%26can={allowed_chain}"
  ZAMA_MATCHER_APPNEXUS_CM_URI="{protocol}://ib.adnxs.com/getuid?{protocol}://${ZAMA_AMTCH_URI_HOSTNAME}${ZAMA_MATCHER_APPNEXUS_ENTRY_URI_PATH}?can={allowed_chain}%26adnxs_uid=\$UID"
  ZAMA_MATCHER_CTXWEB_CM_URI="{protocol}://bh.contextweb.com/bh/rtset?do=add\&pid=536088\&ev={mookie}\&rurl={protocol}://${ZAMA_CMTCH_URI_HOSTNAME}/do-association?return=ctxweb%26can={allowed_chain}"
  ZAMA_MATCHER_GOOGLE_CM_URI="{protocol}://cm.g.doubleclick.net/pixel?nid=themig\&can={allowed_chain}"
  ZAMA_MATCHER_RUBICON_CM_URI='{protocol}://pixel.rubiconproject.com/tap.php?v=7259\&nid=2211\&put={mookie}\&expires={ttl_in_days}'
  ZAMA_MATCHER_PUBMATIC_CM_URIS="http://image2.pubmatic.com/AdServer/Pug?vcode=bz0yJnR5cGU9MSZjb2RlPTI0NzgmdGw9MTI5NjAw\&piggybackCookie=uid:{mookie}\&r=http://${ZAMA_PMTCH_URI_HOSTNAME}/do-association?return=pubmatic%26can={allowed_chain} \\\\\n\\t\\thttps://simage2.pubmatic.com/AdServer/Pug?vcode=bz0yJnR5cGU9MSZjb2RlPTI0NzgmdGw9MTI5NjAw\&piggybackCookie=uid:{mookie}\&r=https://${ZAMA_PMTCH_URI_HOSTNAME}/do-association?return=pubmatic%26can={allowed_chain}"

  ZAMA_RTLG_PERIOD=10

  ZAMA_LGC_EXTERN_IOBUFF_SIZE=16777216

#  ZAMA_OBE_EXPLORATION_SHARE=0.25
  ZAMA_OBE_ENABLED="false"

  ZWF_FCDB_CLEANUP_FREQ_SEC=3600

                  # 10.73.44.105  172.21.155.106 172.21.155.107
  ZAMA_STCOL_HOSTS=(rtbmem1us2    rtbmem2us2	rtbmem1us3	rtbmem2us3)

                  # rtbmem1us2   rtbmem2us2 rtbmem1us3     rtbmem2us3
  ZWF_SCFDR_HOSTS=(10.73.44.105 10.73.43.100 172.21.155.106 172.21.155.107)
                  # rtbsloop1us2 rtbvln3us3 aka rtbsloop1us3
  ZWF_FCFDR_HOSTS=(10.73.44.107 172.21.155.30)

  ZWF_WF_DEFINITION_TEMPLATE="template_zama_wfd_multidc.xml"
  ZWF_WF_COMMUNICATION_TEMPLATE="template_zama_wfc_multidc.xml"

  ZAMA_MATCHER_MIRROR_URI_HOSTNAME="matcher.bidder8.mookie1.com"

  ZAMA_LGC_TOPOLOGY_TEMPLATE="template_lgc_zama_topology_multidc.xml"

  ZAMA_VHOST_ERRORLOG_TEMPLATE='ErrorLog "|/usr/sbin/rotatelogs /var/home/httpd_logs/__ZAMA_VHOST_ERRORLOG_NAME__.%Y-%m-%d-%H_%M_%S 1024M"'
  ZAMA_VHOST_ACCESSLOG_TEMPLATE='TransferLog "|/usr/sbin/rotatelogs /var/home/httpd_logs/__ZAMA_VHOST_ACCESSLOG_NAME__.%Y-%m-%d-%H_%M_%S 1024M"'

  ZAMA_TRACKER_VHOST_KEEPALIVE_CFG="KeepAlive On\nMaxKeepAliveRequests 1000\nKeepAliveTimeout 300"

  ZAMA_GRTB_TARGET_GGL_GEO="false"
  ZAMA_PXY_LOG_COUNTERS_PERIOD_SEC=0

  ZAMA_GRTB_CFG_BID_THREADS=40

  ZAMA_GRTB_CC_LOG_FILE="/var/home/appmgr/zama/work/grtb/iinfo/rtb_cc_log"
#  ZAMA_GRTB_PERF_COUNTERS_FILE="not_used"

  ZAMA_GRTB_VENDOR_IDS_TO_MATCH="87"

  ZAMA_GRTB_EXCLUDED_AGENT_STRINGS='<excluded_agent>\n    <substring>AppleWebKit</substring>\n    <substring>Safari</substring>\n    <substring negated="true">Chrome</substring>\n  </excluded_agent>'

  ZAMA_UDS_SOCKETS_NUM=4

  ZAMA_UDP_PACING_CHK_PERIOD=50000
  ZAMA_UDP_PACING_RCVQ_MIN=100
  ZAMA_UDP_PACING_RCVQ_MAX=5000
  ZAMA_UDP_PACING_RCVQ_PCT_CHANGE=110

  ZAMA_TRK_CREATIVE_AUDIT_TIMEOUT=2000
  ZAMA_TRK_GET_CREATIVE_TIMEOUT=2000

  ZAMA_PRIMARY_DB_HOST="db1011-scan.dc.ash.247realmedia.com"
  ZAMA_PRIMARY_DB_SVCNAME="P1ZAPLP"
  ZAMA_PRIMARY_DB_USER="ZAP_BIDDER_PRESSUSER"
  ZAMA_PRIMARY_DB_PSWD="roo1utsad5"

  ZAMA_VDB_READER_ACCESS_POINT=239.192.25.10
  ZAMA_VDB_READER_ACCESS_POINT_PORT_MIN=30210
  ZAMA_VDB_READER_ACCESS_POINT_PORT_MAX=30239

  ZAMA_VDB_WRITER_ACCESS_POINT=${ZAMA_VDB_READER_ACCESS_POINT}
  ZAMA_VDB_WRITER_ACCESS_POINT_PORT_MIN=${ZAMA_VDB_READER_ACCESS_POINT_PORT_MIN}
  ZAMA_VDB_WRITER_ACCESS_POINT_PORT_MAX=${ZAMA_VDB_READER_ACCESS_POINT_PORT_MAX}

# enable reading from Violinm for matcher/fc_feeder/bidder
  ZAMA_VDB_CONFIG_READER_SECTION_BEGIN="<!-- reader section begin -->"
  ZAMA_VDB_CONFIG_READER_SECTION_END="<!-- reader section end -->"

  ZAMA_VDB_SVC_CONFIGS=(ec_vdb-1_svc_config.xml@rtbvln1us2 ec_vdb-2_svc_config.xml@rtbvln2us2)

