Ansible Role: osm_alertmanager
==============================

>Alertmanager is tool that handles alerts sent by Prometheus. It gets the alert from Prometheus server and make groups of alerts on the basis of labels and after that it will forward the alert to different reciever such as Email, PagerDuty, Slack.

>Alertmanager is configured via using command-line flags and a configuration while. While command line configure system parameters, the configuration file contains the information like recievers and routing.

**This ansible role will install and configure alertmanager with Prometheus.**

Version History
---------------

|**Date**| **Version**| **Description**| **Changed By** |
|----------|---------|---------------|-----------------|
|**June '15** | v.1.0 | Initial Draft | Sudipt Sharma |

Supported OS
------------
  * CentOS:7
  * CentOS:6
  * Ubuntu:xenial
  * Ubuntu:trusty

Dependencies
------------
- prometheus-server
- libselinux-python

Requirements
------------
- libselinux-python and we have included that as well.
- 9093 port should be open in your server

Directory Structure of Role
---------------------------
This is the directory structure of role:-
```bash
osm_alertmanager
├── defaults
│   └── main.yml
├── files
│   ├── alertmanager.init
│   └── email.tmpl
├── handlers
│   └── main.yml
├── README.md
├── site.yml
├── tasks
│   ├── debian.yml
│   ├── main.yml
│   └── redhat.yml
└── templates
    ├── alertmanager.service.j2
    └── alertmanager.yml.j2
```

Role Variables
--------------

|**Variable**| **Default Value**| **Description**|
|---------|------------|-----------|
|alertmanager_version| "0.15.1"| The version of alertmanager version, this variable you have to give because it will download alertmanager from github releases|
|sender_email| "send.test@example.com"| The email id you want to send alerts||
|alertmanager_email| "alertmanager.test@example.com" | The email id from which you want to send mail to recievers|
|smtp_server | "smtp.gmail.com:587" | smtp server host name|

Inventory
----------
An inventory should look like this:-
```ini
[alertmanager]                 
192.168.1.198    ansible_user=ubuntu   
192.168.3.201    ansible_user=opstree 
```

Example Playbook
----------------
* Here is an example playbook:-
```yaml
---
- hosts: alertmanager
  become: true
  roles:
    -  alertmanager
```
* ansible-playbook -i inventory alrtmanager.yml

**After successful installation of alertmanager, you can browse through the alertmanager url and see the web interface**
![web](./media/alertmanager_ui.png)

License
-------
BSD

References
----------
- **[software](https://prometheus.io/docs/alerting/alertmanager/)**

Author Information
------------------
This role is written and maintained by [Abhishek Dubey](https://gitlab.com/abhishek-dubey). If you have any queries and sugesstion, please feel free to reach.

Email ID:- [abhishek.dubey@opstree.com]()
