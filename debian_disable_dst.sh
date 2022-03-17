#!/bin/bash
######################
#   Disable DST      #
######################
# If daylight saving time is enabled in your machine
# you can use this script to disable it.
# Please note that you may need to restart your applications
# as the DST is changed
# This script has been only tested on Debian 10 for Asia/Tehran
# Feel free to make any desired changes and apply for a pull request 
# to help the others!

#################
#   Credits     #
#################
# Author: Mahmoud Ahmadi
# Git: https://github.com/ma-ahmadi1989/check-servers-time-settings.git


#################
#   Configs     #
#################
working_dir="/tmp/tehran-no-dst"



#################
#   Show Time   #
#################
# Let's make a backup before any changes!
run_date=$(date +"%Y-%m-%d_%H-%M-%S")
cp /usr/share/zoneinfo/Asia/Tehran /usr/share/zoneinfo/Asia/Tehran_${run_date}



# You may already ran this
# cleaning the path
rm -rf ${working_dir}


# Make a working directory
mkdir -p ${working_dir}
cd ${working_dir}/

# Make the DST disabled zone file
# Reference: https://github.com/eggert/tz
echo "
# Zone  NAME          GMTOFF  RULES FORMAT [UNTIL]
Zone    Asia/Tehran   3:25:44 -     LMT    1916
                      3:25:44 -     TMT    1946    # Tehran Mean Time
                      3:30    -     IRST   1977 Nov
                      4:00    -     IRST   1979
                      3:30    -     IRST

" > tehran_dst_disabled

# Make the binary zone file
zic -d . tehran_dst_disabled


# Make a backup from current zonefiles
cp /usr/share/zoneinfo/Asia/Tehran /usr/share/zoneinfo/Asia/Tehran_dst_enabled
unlink /etc/localtime


# Apply new zone file
cp Asia/Tehran /usr/share/zoneinfo/Asia/Tehran
ln -s /usr/share/zoneinfo/Asia/Tehran /etc/localtime


# Check the result
echo "Date: $(date)"
dst_stat=$(zdump -v /etc/localtime | grep -i 2022 | wc -l )
if [ ${dst_stat} -eq 4 ]
then
    echo "DST is Enabled"
elif [ ${dst_stat} -eq 0 ]
then
    echo "DST is Disabled"
fi

echo ""
echo "Note: Run the following commands to rollback the changes:"
echo "- unlink /etc/localtime"
echo "- cp /usr/share/zoneinfo/Asia/Tehran_dst_enabled /usr/share/zoneinfo/Asia/Tehran"
echo "- ln -s /usr/share/zoneinfo/Asia/Tehran /etc/localtime"
echo "You also have a another backup at /usr/share/zoneinfo/Asia/Tehran_${run_date}"