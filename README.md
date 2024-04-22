# python_term_mon

to use:

cd src

-make sure you install netmiko (pip install netmiko)
-copy config.json.sample to config.json and update config items as needed
- run: python main.py
- to end press {crtl c}

This is a re-write of my other repository python_term_mon

main.py is somewhat tested and adds a few things functionally:
-moves class DeviceMonitor out of the main file into a class file
-moves deduplication of messages based on regex into RegexMessageTracker class file
-creates a thread safe singleton like based logger with only 1 instanace for each ip address
-creates a singleton config loader class with only on instance for the entire running processes
-moves devices and configurable items into config.json
-sets output directory for log files and is configurable in config.json
-adds date/timestamp to debug log filenames
-info logs to file and warning logs to console and file
-handles case where user leaves __commments__ from config.json.sample in config.json

monitor python sessions 

- this script logs into cisco device/s 
- logs all output to a log file and prints specificly configured alert_strings on the local terminal window of the machine they are run from
- it will deduplicate certain messages based on a provided regular expression for messages produced by debug but have no value to the troubleshooting

In short:

login to each deivce in config.json
issue terminal monitor command
issue any debug commands
read the output 
print to local terminal for items in config.json alert_strings
write all terminal output to per device log file
issue undebug all on shutdown.

You need to install netmiko for yourself.

"pip install netmiko"

No other dependancies.

Copy ./config/config.json.sample to ./config/config.json and update information in config.json to match the devices you want to monitor.


    # Define class-level attribute for debug commands
    debug_list = [
        'debug wgb uplink event',
        'debug wgb uplink scan info',  # Add additional default debug commands as needed
    ]

Every debug command in this list will be executed afer a connection is made and terminal monitor mode is set.


    # Define a class-level attribute for the filter list
    alert_list = [
        "[DOT11_UPLINK_CONNECTED]",
        "Aux roam switch radio role",
        "[DOT11_UPLINK_FT_AUTHENTICATING]",
        "target channel",
        "DOT11-UPLINK_ESTABLISHED",
        "Peer assoc event received from driver"
    ]

Anything in the alert list prints to the local console and the local log file.  If nothing in the list matches then it only prints to the log file.

This helps you look for specfic messages on the console while reducing the clutter of messages you are less intersted in.

While at the same time everything is in the local log file for later analysis.

The initial list are things related to a roaming event on an IW9165 or (WGB).

