import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_alertmanager_is_installed(host):
    alertmanager = host.package("alertmanager")
    assert alertmanager.is_installed


def test_config_file(host):
    f = host.file('/etc/alertmanager/alertmanager.yml')
    assert f.exists
    assert f.is_file


def test_template_file(host):
    f = host.file('/etc/alertmanager/email.tmpl')
    assert f.exists
    assert f.is_file


def test_alertmanager_log_dir(host):
    d = host.file('/var/lib/alertmanager')
    assert d.exists
    assert d.is_directory
    assert d.owner == "alertmanager"
    assert d.group == "alertmanager"


def test_grafana_running_and_enabled(host):
    os = host.system_info.distribution
    if os == '16':
        alertmanager = host.service("alertmanager")
        assert alertmanager.is_running
        assert alertmanager.is_enabled
    if os == '7':
        alertmanager = host.service("alertmanager")
        assert alertmanager.is_running
        assert alertmanager.is_enabled
