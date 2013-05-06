#!/bin/bash
# 
# The tomcat configuration file.
# $Id: tomcat-env.sh 127 2009-06-08 07:54:12Z jasonb $

# Where this config file may be found when it's installed.
APP_ENV="/opt/tomcat/conf/tomcat-env.sh"

# Where your Java installation lives.  Unfortunately, this must be
# hard-coded here because JAVA_HOME on the build machine may not be
# the proper JAVA_HOME on the machine the webapp is deployed onto.
JAVA_HOME="/usr/java/latest"

# Where your Tomcat installation lives.
CATALINA_HOME="/opt/tomcat"
JASPER_HOME="/opt/tomcat"
CATALINA_TMPDIR="/opt/tomcat/temp"

# The path to this application's writeable runtime Tomcat tree.
CATALINA_BASE="/opt/tomcat"

# The ID of this package's JVM.
JVM_ID="appmgr"

# Set JPDA_OPTS as shown below if you want to run the JPDA debugger (server)
# in the Tomcat JVM.
#JPDA_OPTS="-Xdebug \
#  -Xrunjdwp:transport=dt_socket,address=8000,server=y,suspend=n"

# When using Java 1.5 ("Java 5") or higher, you may set JMX_OPTS to
# enable the built-in JMX monitoring/management agent connector.  Use
# jconsole to connect to it.
# See http://java.sun.com/j2se/1.5.0/docs/guide/management/agent.html
#
# Uncomment this block to enable localhost-only JMX:
#JMX_OPTS="-Dcom.sun.management.jmxremote=true \
#  -Dcom.sun.management.jmxremote.ssl=false \
#  -Dcom.sun.management.jmxremote.authenticate=false"
#
# Uncomment this block to enable remote JMX (make sure hostname -i does
# not resolve to '127.0.0.1' or it won't work.. edit /etc/hosts to fix it):
#JMX_OPTS="-Dcom.sun.management.jmxremote.port=8008 \
#  -Dcom.sun.management.jmxremote.ssl=false \
#  -Dcom.sun.management.jmxremote.authenticate=false \
#  -Dcom.sun.management.jmxremote.password.file=/path/to/password/file"
#  -Dcom.sun.management.jmxremote.access.file=/path/to/access/file"

# You can pass extra JVM startup parameters to java here if you wish.
JAVA_OPTS="-Djvm=$JVM_ID -Xms384M -Xmx384M -XX:MaxPermSize=200m \
  -Djava.awt.headless=true -Djava.net.preferIPv4Stack=true $JPDA_OPTS \
  $JMX_OPTS"

# This option makes the JVM's default character encoding UTF-8, which           
# usually helps with internationalization/localization.                         
JAVA_OPTS="$JAVA_OPTS -Dfile.encoding=UTF-8 -DjavaEncoding=UTF-8"

# Uncomment this option to turn on the Java SecurityManager, and set the
# security policy file.  If you do not set the policy file path here, the
# default is to use $CATALINA_BASE/conf/catalina.policy.  NOTE: these
# options should be commented out in nearly all Tomcat installations!
#JAVA_OPTS="$JAVA_OPTS -Djava.security.manager \
#  -Djava.security.policy=$CATALINA_BASE/conf/catalina.policy"

# Uncomment this option to get JVM debug info from the SecurityManager.
#JAVA_OPTS="$JAVA_OPTS -Djava.security.debug=all"

# Uncomment this option to set the security manager implementation.
#JAVA_OPTS="$JAVA_OPTS -Djava.security.manager=[put-class-name-here]"

# Uncomment this option to make the JVM print some detailed information
# about what's in the heap if it throws an OutOfMemoryError. Another
# way to inspect the heap is to use this command:
# jmap -dump:format=b,file=heap.hprof 17470
# .. where 17470 is the process ID of the Tomcat JVM.  Use the command:
# jhat -J-Xmx800M heap.hprof
# .. to analyze the heap dump.
#JAVA_OPTS="$JAVA_OPTS -XX:+HeapDumpOnOutOfMemoryError"

# Uncomment this option to set the SMTP relay server that JavaMail should
# use when sending emails.  Use -Dmail.debug to turn on debugging.
# If this is unset, Javamail defaults to using localhost's SMTP server.
#JAVA_OPTS="$JAVA_OPTS -Dmail.smtp.host=mail.host.example.com"

# What user should run tomcat.
TOMCAT_USER="appmgr"

# You can change your Tomcat locale here.  The default is your OS's default
# locale that you specified at OS installation time.
#LANG=en_US

# Time to wait in seconds before sending signals to stop the JVM process.
# The total maximum wait time is three times the number you set here!
# One SHUTDOWN_WAIT duration waiting for a Tomcat shutdown command to
# bring down the JVM, another SHUTDOWN_WAIT duration waiting for a
# SIGTERM signal to bring it down if the shutdown command failed to, and
# one last SHUTDOWN_WAIT duration after sending a SIGKILL if the SIGTERM
# failed to bring it down.
let SHUTDOWN_WAIT=2

# If you wish to further customize your tomcat environment, put your own
# definitions here (i.e. LD_LIBRARY_PATH for the APR connector's lib
# directory, some jdbc driver libs, etc).  Just do not forget to export them.
#
# If you wish to use the APR connector, point LD_LIBRARY_PATH to the
# directory that contains the libtcnative-1.so.0 shared library file
# (possibly with newer numbers on the file name).
#export LD_LIBRARY_PATH=/opt/tomcat/apr-connector/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/var/home/appmgr/lib64/PROD/
export JAVA_OPTS="$JAVA_OPTS -Xmx512m -XX:MaxPermSize=512m -Djava.security.egd=file:/dev/urandom -Dcom.sun.management.jmxremote.port=8111 -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.authenticate=false"
