#!/bin/bash

SWT=~/git/eclipse.platform.swt
SWT_BIN=~/git/eclipse.platform.swt.binaries

today=`date '+%Y_%m_%d__%H_%M_%S'`
LOG_FILE=/home/eclipse/google-drive/SWT-Performance-Tests/logs/$today.log
LOG_ERROR_FILE=/home/eclipse/google-drive/SWT-Performance-Tests/logs/error/$today.error.log

cd $SWT
git pull

r # rebuild gtk .so

cd $SWT/tests

/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.181.b15-5.fc28.x86_64/bin/java -ea -Djava.library.path=/home/eclipse/git/eclipse.platform.swt.binaries/bundles/org.eclipse.swt.gtk.linux.x86_64 -Dfile.encoding=UTF-8 -classpath /home/eclipse/Apps/eclipse-SDK-newest-linux-gtk-x86_64/eclipse/plugins/org.junit_4.12.0.v201504281640/junit.jar:/home/eclipse/Apps/eclipse-SDK-newest-linux-gtk-x86_64/eclipse/plugins/org.hamcrest.core_1.3.0.v20180420-1519.jar:/home/eclipse/git/eclipse.platform.swt/bundles/org.eclipse.swt/bin:/home/eclipse/Apps/eclipse-SDK-newest-linux-gtk-x86_64/eclipse/plugins/org.eclipse.core.runtime_3.15.100.v20180907-0807.jar:/home/eclipse/Apps/eclipse-SDK-newest-linux-gtk-x86_64/eclipse/plugins/javax.inject_1.0.0.v20091030.jar:/home/eclipse/Apps/eclipse-SDK-newest-linux-gtk-x86_64/eclipse/plugins/org.eclipse.osgi_3.13.200.v20180906-2135.jar:/home/eclipse/Apps/eclipse-SDK-newest-linux-gtk-x86_64/eclipse/plugins/org.eclipse.osgi.compatibility.state_1.1.200.v20180827-1536.jar:/home/eclipse/Apps/eclipse-SDK-newest-linux-gtk-x86_64/eclipse/plugins/org.eclipse.equinox.common_3.10.100.v20180827-1235.jar:/home/eclipse/Apps/eclipse-SDK-newest-linux-gtk-x86_64/eclipse/plugins/org.eclipse.core.jobs_3.10.200.v20180912-1356.jar:/home/eclipse/Apps/eclipse-SDK-newest-linux-gtk-x86_64/eclipse/plugins/org.eclipse.equinox.registry_3.8.200.v20181008-1820.jar:/home/eclipse/Apps/eclipse-SDK-newest-linux-gtk-x86_64/eclipse/plugins/org.eclipse.equinox.preferences_3.7.200.v20180827-1235.jar:/home/eclipse/Apps/eclipse-SDK-newest-linux-gtk-x86_64/eclipse/plugins/org.eclipse.core.contenttype_3.7.100.v20180817-1401.jar:/home/eclipse/Apps/eclipse-SDK-newest-linux-gtk-x86_64/eclipse/plugins/org.eclipse.equinox.app_1.4.0.v20181009-1752.jar:/home/eclipse/git/eclipse.platform.releng/bundles/org.eclipse.test.performance/bin:/home/eclipse/git/eclipse.platform.swt/tests/org.eclipse.swt.tests/bin:/home/eclipse/Apps/eclipse-SDK-newest-linux-gtk-x86_64/eclipse/configuration/org.eclipse.osgi/171/0/.cp:/home/eclipse/Apps/eclipse-SDK-newest-linux-gtk-x86_64/eclipse/configuration/org.eclipse.osgi/170/0/.cp org.eclipse.swt.tests.junit.performance.Test_situational 2>>$LOG_ERROR_FILE | tee -a $LOG_FILE
