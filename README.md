# Ansible Role for Alertmanager

Alertmanager is tool that handles alerts sent by Prometheus. It gets the alert from Prometheus server and make groups of alerts on the basis of labels and after that it will forward the alert to different reciever such as Email, PagerDuty, Slack.

Alertmanager is configured via using command-line flags and a configuration while. While command line configure system parameters, the configuration file contains the information like recievers and routing.

## Requirements

There is no particular requirment for running this role. As this role is platform independent for centos 6 or 7 and ubuntu 14 or 16. The only dependency for centos 6 is libselinux-python and we have included that as well.
The basic requirments are:-
- Centos/Ubuntu Server
- Python should be installed on the target server
- 9093 port should be open in your server

## Role Variables
The role variables are defined in the [vars](https://gitlab.com/oosm/osm_alertmanager/tree/master/defaults). Here is the list of variables that is used in this role

```yaml
# vars file for grafana
alertmanager_version: "0.15.1"
sender_email: "send.test@example.com"
alertmanager_email: "alertmanager.test@example.com"
smtp_server: "smtp.gmail.com:587"
```

|Variable | Description|
|---------|------------|
|alertmanager_version| The version of alertmanager version, this variable you have to give because it will download alertmanager from github releases|
|sender_email| The email id you want to send alerts||
|alertmanager_email| The email id from which you want to send mail to recievers|
|smtp_server | smtp server host name|

## Dependencies

Here is the dependency for this role:-
- prometheus-server
- libselinux-python

## Example Playbook

Here is an example for the main playbook

```yaml
---
- hosts: alertmanager
  roles:
    -  alertmanager
```
Here We are using root as an user but you can use different user, For that you just have to make become value true. Something like this:-
```yaml
---
- hosts: alertmanager
  become: true
  roles:
    -  alertmanager
```

For inventory you can create a host file in which you can define your server ip, For example:-

```
[alertmanager]
10.1.1.100
```

You can simply use this role by using this command
```shell
ansible-playbook -i hosts site.yml
```

## Directory Structure of Role
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
## License

BSD

## Author Information

This role is written and maintained by [Abhishek Dubey](https://gitlab.com/abhishek-dubey). If you have any queries and sugesstion, please feel free to reach.

Email ID:- [abhishek.dubey@opstree.com]()
