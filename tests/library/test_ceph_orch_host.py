from mock.mock import patch
import pytest
import common
import ceph_orch_host

class TestCephadmBootstrapModule(object):

    @patch('ansible.module_utils.basic.AnsibleModule.exit_json')
    @patch('ansible.module_utils.basic.AnsibleModule.run_command')
    def test_state_absent(self, m_run_command, m_exit_json):
        common.set_module_args({
            'state': 'absent',
            'name': 'ceph-node123'
        })
        m_exit_json.side_effect = common.exit_json
        stdout = "Removed  host 'ceph-node5'"
        stderr = ''
        rc = 0
        m_run_command.return_value = rc, stdout, stderr

        with pytest.raises(common.AnsibleExitJson) as result:
            ceph_orch_host.main()

        result = result.value.args[0]
        assert result['changed']
        assert result['cmd'] == ["cephadm", "shell", "ceph", "orch", "host", "rm", "ceph-node123"]
        assert result['stdout'] == stdout
        assert result['rc'] == 0

    @patch('ansible.module_utils.basic.AnsibleModule.exit_json')
    @patch('ansible.module_utils.basic.AnsibleModule.run_command')
    def test_state_drain(self, m_run_command, m_exit_json):
        common.set_module_args({
            'state': 'drain',
            'name': 'ceph-node123'
        })
        m_exit_json.side_effect = common.exit_json
        stdout = """
Scheduled to remove the following daemons from host 'ceph-node123'
type                 id
-------------------- ---------------
crash                ceph-node5
osd                  3
osd                  5
osd                  7
"""
        stderr = ''
        rc = 0
        m_run_command.return_value = rc, stdout, stderr

        with pytest.raises(common.AnsibleExitJson) as result:
            ceph_orch_host.main()

        result = result.value.args[0]
        assert result['changed']
        assert result['cmd'] == ["cephadm", "shell", "ceph", "orch", "host", "drain", "ceph-node123"]
        assert result['stdout'] == stdout
        assert result['rc'] == 0