#!/bin/bash

# First try to source the ENV file
if [ ! -f $HOME/.lgc_mon2.sh ]
then
echo Missing environment file. Exiting...
exit 1
fi

. $HOME/.lgc_mon2.sh


restart_lgc()
{
	pkill lgc.exe
	sleep 10
	lgc_dead=`pgrep -u appmgr lgc.exe|wc -l`
	[ "$lgc_dead" -ge 1 ] && pkill -9 lgc.exe
	/var/home/appmgr/lgc/bin/lgc.exe  -t $TOPO_FILE -e $ENV_FILE
	touch /tmp/restarted_lgc
	echo $REASON on `uname -n` | mail -s 'LGC has hung. Restarting.' mig-techops@247realmedia.com dmitry.krasnovsky@247realmedia.com
	rm $LOG_DIR/lgc_mon2.lock
	exit 0
}

echo Starting `date`
# Check for a lock file

lock=`find $LOG_DIR -name lgc_mon2.lock -mmin -10|wc -l`
if [ "$lock" -gt 0 ]
then
echo Detected a recent lock file. Exiting...
exit 0
fi

touch $LOG_DIR/lgc_mon2.lock

# If lgc was already restarted within the last three mins don't restart again
just_restarted=`find /tmp -maxdepth 1 -name restarted_lgc -mmin -10|wc -l`
if [ "$just_restarted" -ne 0 ]
then
  echo lgc was restarted within the last 10 mins
  rm $LOG_DIR/lgc_mon2.lock
  exit 0
fi

log_updated=`find $LGC_LOG_DIR -follow -name lgc_current.log -mmin -${LOG_UPDATE_INTERVAL}|wc -l`
if [ "$log_updated" -eq 0 ]
then
  REASON="lgc log was not updated for more than ${LOG_UPDATE_INTERVAL} min. Restarting lgc"
  echo $REASON
  restart_lgc
fi

# Obtain the list of producers that we talk to
PRODUCERS=`grep FL_REQ $LGC_LOG_DIR/lgc_current.log|grep '@'|sed 's/.*"\(.*\)_@.*/\1/'|sort -u`

# Check counters for each producer

for producer in $PRODUCERS
do
  echo Checking $producer
  stats=`grep $producer $LGC_LOG_DIR/lgc_current.log |grep FL_REQ|awk '{print $8}'|tail -3`
  echo For producer $producer obtained the following stats $stats
  count=`echo $stats|awk '{print NF}'`
  if [ "$count" -ge 3 ] 
  then
    status=`echo $stats|awk '$1 == $3 {print "restart"}'`
    if [ "$status" == "restart" ]
    then
      echo Received restart status for producer $producer. Confirming that producers is alive before restarting lgc.
      LGC_CFG_FILE=`ls -tr $LGC_LOG_DIR/lgc_work_configuration*cfg|tail -1`
      if [ ! -f "$LGC_CFG_FILE" ]
      then
	REASON="Could not find lgc_work_configuration file. Restarting lgc"
	echo $REASON
	restart_lgc
      fi
      producer_ip=`sed -n "/$producer/,/Producer name/p" "$LGC_CFG_FILE"|awk '/address/ {print $NF}'|head -1`
      producer_port=`sed -n "/$producer/,/Producer name/p" "$LGC_CFG_FILE"|awk '/port/ {print $NF}'|head -1`
      if [ -z "producer_ip" -o -z "producer_port" ]
      then
	echo Internal error in lgc_mon2.sh on `uname -n`|mail mig-techops@247realmedia.com
	exit 1
      fi
      if nc -z -w 5 $producer_ip $producer_port >/dev/null     
      then
	echo Producer $producer at $producer_ip on port $producer_port is responding. Restarting lgc.
	REASON="FL_REQ counter for producer $producer did not increase. Restarting lgc"
	restart_lgc
      else
	echo Producer $producer at $producer_ip on port $producer_port is not responding. Ignore lgc restart reqest.
      fi
    fi
  else
  echo Insufficient stats for producer $producer
  fi
done

rm $LOG_DIR/lgc_mon2.lock
exit 0


