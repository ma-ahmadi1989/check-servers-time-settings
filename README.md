# About this script
This script gets a list of target machines in a csv format and checks the time settings of each one. The result will also be saved in csv under ./result.csv

# Requirements
- SSH access to the target machines from the local machine
- python3.8 installed on the local machine

</br>

# How to run
To use the script in a clean way run the following commands
- #apt install virtualenv python3-virtualenv
- #git clone https://github.com/ma-ahmadi1989/check-servers-time-settings.git
- #cd check-servers-time-settings/
- #virtualenv -p /usr/bin/python3.8 env
- #source  env/bin/activate
- #pip install -r requirements.txt
- #python server_time_settings_check.py a_server_info_csv_file.csv

</br>

# Server's info file format
To provide an unlimited list of servers, you should make the list in a csv file format including the following columns:

hostname,ip,ssh_username,ssh_password,ssh_port
some-server,1.1.1.1,root,some-smart-password,22

Notes:
</br> 
1- some commands on the remote machine may require root privilleges, it is recommended to use root as the user
</br>
2- Do not include column names in your CSV info file. You may find a sample file as sample_server_info_file.csv in this repo
</br>
</br>
</br>

# How to Disable DST (if required)
==[ IF DST IS ENABLED there would be 4 records for each year]==
</br>
root@MAHMOUD-TestDeB:~# zdump -v /etc/localtime | grep 2022
</br>
/etc/localtime Mon Mar 21 20:29:59 2022 UT = Mon Mar 21 23:59:59 2022 +0330 isdst=0 gmtoff=12600
</br>
/etc/localtime Mon Mar 21 20:30:00 2022 UT = Tue Mar 22 01:00:00 2022 +0430 isdst=1 gmtoff=16200
</br>
/etc/localtime Wed Sep 21 19:29:59 2022 UT = Wed Sep 21 23:59:59 2022 +0430 isdst=1 gmtoff=16200
</br>
/etc/localtime Wed Sep 21 19:30:00 2022 UT = Wed Sep 21 23:00:00 2022 +0330 isdst=0 gmtoff=12600
</br>
</br>
</br>
</br>


<h3>
To disable DST run the following commands in the target machine
</h3>
</br>
# zic -d . Tehran-dst-disabled-zone-file
</br>
# tree .
</br>
.
</br>
├── Asia
</br>
│  └── Tehran
</br>
└── Tehran-dst-disabled-zone-file
</br>
</br>
# cp /usr/share/zoneinfo/Asia/Tehran /usr/share/zoneinfo/Asia/
Tehran_dst_enabled
</br>
# cp Asia/Tehran /usr/share/zoneinfo/Asia/
</br>
</br>


==[IF DST IS DISABLED - There would be no Result ;) ]==
</br>
#zdump -v /etc/localtime | grep 2022
</br>
#.

# Automated DST Disabler
You can use the automate script "debian_disable_dst.sh" to disable the DST
- #/bin/bash debian_disable_dst.sh