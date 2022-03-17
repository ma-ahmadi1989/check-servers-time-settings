import sys
from datetime import datetime, timezone
import csv

import paramiko


def convert_machine_info_str_to_dict(machine_info: str):
    machine_info_dict = {}
    machine_info_dict['hostname'] = machine_info.split(',')[0]
    machine_info_dict['host'] = machine_info.split(',')[1]
    machine_info_dict['username'] = machine_info.split(',')[2]
    machine_info_dict['password'] = machine_info.split(',')[3]
    machine_info_dict['ssh_port'] = machine_info.split(',')[4]
    return machine_info_dict


def get_remote_machine_time_settings(machine: str):
    machine_info = convert_machine_info_str_to_dict(machine)
    time_setting = {}

    print("Checking " + machine_info['hostname'] +
          " at " + machine_info['host'] + ":" + machine_info['ssh_port'])

    time_setting['hostname'] = machine_info['hostname']
    time_setting['host ip'] = machine_info['host']

    utc_dt = datetime.now(timezone.utc)
    time_setting['execution_datetime'] = utc_dt.astimezone()

    time_setting['date'] = get_remote_machine_date(machine_info)
    time_setting['ntp_servers'] = get_remote_machine_ntp_servers_list(
        machine_info)
    timectl = get_remote_machine_timectl_settings(
        machine_info)
    time_setting['timectl_local_time'] = timectl['timectl_local_time']
    time_setting['timectl_Universal_time'] = timectl['timectl_Universal_time']
    time_setting['timectl_rtc_time'] = timectl['timectl_rtc_time']
    time_setting['timectl_time_zone'] = timectl['timectl_time_zone']
    time_setting['timectl_network_time_on'] = timectl['timectl_network_time_on']
    time_setting['timectl_ntp_synchronized'] = timectl['timectl_ntp_synchronized']
    time_setting['timectl_rtc_in_local'] = timectl['timectl_rtc_in_local']

    time_setting['vmware_sync_stat'] = get_remote_machine_vmware_time_sync_status(
        machine_info)
    time_setting['daylight_saving_time_status'] = get_remote_machine_daylight_saving_time_status(
        machine_info)

    return time_setting


def get_remote_machine_daylight_saving_time_status(machine_info: dict):
    command_result = "Error - Check the server manually!"
    try:
        remote_command = "zdump -v /etc/localtime | grep -i 2022 | wc -l"
        command_result = run_command_on_remote_machine(
            machine_info=machine_info, remote_command=remote_command).rstrip()
        if int(command_result.strip()) == 4:
            command_result = "Enabled"
        elif int(command_result.strip()) == 0:
            command_result = "Disabled"

    except Exception as error:
        print(error)
    return command_result


def get_remote_machine_ntp_servers_list(machine_info: dict):
    command_result = "ntpq is not installed!"
    try:
        remote_command = "ntpq  -pn | awk '{print $1}' | grep -v 'remote\|='"
        command_result = run_command_on_remote_machine(
            machine_info=machine_info, remote_command=remote_command).rstrip()
    except Exception as error:
        print(error)
    return command_result


def get_remote_machine_timectl_settings(machine_info: dict):
    timectl = {}
    timectl['timectl_local_time'] = ""
    timectl['timectl_Universal_time'] = ""
    timectl['timectl_rtc_time'] = ""
    timectl['timectl_time_zone'] = ""
    timectl['timectl_network_time_on'] = ""
    timectl['timectl_ntp_synchronized'] = ""
    timectl['timectl_rtc_in_local'] = ""
    try:
        remote_command = 'timedatectl'
        command_result = run_command_on_remote_machine(
            machine_info=machine_info, remote_command=remote_command)

        timectl['timectl_local_time'] = "".join(command_result.split("\n")[
            0].split(":")[1:]).lstrip()
        timectl['timectl_Universal_time'] = "".join(command_result.split("\n")[
            1].split(":")[1:]).lstrip()
        timectl['timectl_rtc_time'] = "".join(
            command_result.split("\n")[2].split(":")[1:]).lstrip()
        timectl['timectl_time_zone'] = "".join(
            command_result.split("\n")[3].split(":")[1:]).lstrip()
        timectl['timectl_network_time_on'] = "".join(command_result.split("\n")[
            4].split(":")[1:]).lstrip()
        timectl['timectl_ntp_synchronized'] = "".join(command_result.split("\n")[
            5].split(":")[1:]).lstrip()
        timectl['timectl_rtc_in_local'] = "".join(command_result.split("\n")[
            6].split(":")[1:]).lstrip()
    except Exception as error:
        print(error)

    return timectl


def get_remote_machine_vmware_time_sync_status(machine_info: dict):
    command_result = "VMWare tools is not installed!"
    try:
        remote_command = 'vmware-toolbox-cmd timesync status'
        command_result = run_command_on_remote_machine(
            machine_info=machine_info, remote_command=remote_command)
    except Exception as error:
        print(error)
    return command_result.strip()


def get_remote_machine_date(machine_info: dict):
    command_result = "date is not installed!"
    try:
        remote_command = 'date'
        command_result = run_command_on_remote_machine(
            machine_info=machine_info, remote_command=remote_command)
    except Exception as error:
        print(error)
    return command_result


def run_command_on_remote_machine(machine_info: dict, remote_command: str):
    command_result = ''
    try:
        remote_machine = paramiko.SSHClient()
        remote_machine.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote_machine.connect(machine_info['host'], username=machine_info['username'],
                               password=machine_info['password'], port=int(machine_info['ssh_port']), timeout=5)
        ssh_stdin, ssh_stdout, ssh_stderr = remote_machine.exec_command(
            remote_command)
        # if ssh_stderr:
        #     print(ssh_stderr)
        command_result = ssh_stdout.readlines()
        command_result = "".join(command_result)
        ssh_stdin.close()
    except Exception as error:
        print(error)

    return command_result


def save_result_in_csv(time_settings: dict):
    with open("result.csv", "w") as file:
        csv_file = csv.writer(file)
        csv_file.writerow([
            'hostname',
            'host ip',
            'execution_datetime',
            'date',
            'ntp_servers',
            'timectl_local_time',
            'timectl_Universal_time',
            'timectl_rtc_time',
            'timectl_time_zone',
            'timectl_network_time_on',
            'timectl_ntp_synchronized',
            'timectl_rtc_in_local',
            'vmware_sync_stat',
            'daylight_saving_time_status']
        )
        for item in time_settings:

            csv_file.writerow([
                item['hostname'],
                item['host ip'],
                item['execution_datetime'],
                item['date'],
                item['ntp_servers'],
                item['timectl_local_time'],
                item['timectl_Universal_time'],
                item['timectl_rtc_time'],
                item['timectl_time_zone'],
                item['timectl_network_time_on'],
                item['timectl_ntp_synchronized'],
                item['timectl_rtc_in_local'],
                item['vmware_sync_stat'],
                item['daylight_saving_time_status']
            ])


time_settings = []

with open(sys.argv[1], 'r') as machine_list:
    machines = machine_list.readlines()
    for machine in machines:
        time_settings.append(get_remote_machine_time_settings(machine.strip()))

    save_result_in_csv(time_settings)
    print("==[Result saved as result.csv in current dir!")
