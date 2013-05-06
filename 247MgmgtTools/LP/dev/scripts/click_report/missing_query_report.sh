#!/bin/bash

BIDDERS="rtbbid1us2 rtbbid2us2 rtbbid3us2 rtbbid4us2 rtbbid5us2 rtbbid6us2 rtbbid7us2 rtbbid8us2"
DUMPFILE="tmp/zama_missing_query.txt_$(date +%m%d%Y)_dump"
OUTFILE="tmp/missing_query_report.txt"

echo "" > $DUMPFILE
for x in $BIDDERS ; do 
	 ssh $x /usr/lib/nagios/plugins/extra/get_clk_errs.sh >> $DUMPFILE 
done

echo "Campaign-ID	Errors" > $OUTFILE
for i in $( awk '{print $1}' $DUMPFILE | sort -u | grep ^[[:digit:]]); do 
echo "$i		$(grep $i $DUMPFILE |awk '{ SUM += $2} END { print SUM }')" >> $OUTFILE
done


	mail -s "Missing Clicks Report for $(date -d "yesterday" +%m-%d-%Y)" b3rtb@themig.com  mig-techops@247realmedia.com ZTCoreDev@themig.com < $OUTFILE
#	mail -s "Missing Clicks Report for $(date -d "yesterday" +%m-%d-%Y)" yevgeni.chechelnitski@247realmedia.com < $OUTFILE
		if [ $? = "0" ]
			then
				rm -f $OUTFILE
				echo "$OUTFILE has been deleted"
			else	
				echo "$OUTFILE Does not exist"
		fi
