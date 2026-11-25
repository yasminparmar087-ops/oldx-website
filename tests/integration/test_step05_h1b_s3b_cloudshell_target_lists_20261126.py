import importlib.util
import json
import pathlib
import unittest
import tempfile
import os
from unittest.mock import patch

SRC = pathlib.Path(__file__).resolve().parents[2] / 'scripts/step05_h1b_s3b_cloudshell_exact_target_lists_once_20261126.py'
spec = importlib.util.spec_from_file_location('s3b', SRC)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class S3BTests(unittest.TestCase):
    def service(self, data, code=0, stderr=''):
        return m.classify_listing('service',code,json.dumps(data),stderr)
    def sa(self, data, code=0, stderr=''):
        return m.classify_listing('sa',code,json.dumps(data),stderr)
    def test_empty_service_list_absent(self):
        self.assertEqual(self.service([]), 'ABSENT_FROM_SUCCESSFUL_LIST_WITH_LIMITS')
    def test_empty_sa_list_absent(self):
        self.assertEqual(self.sa([]), 'ABSENT_FROM_SUCCESSFUL_LIST_WITH_LIMITS')
    def test_other_services_absent(self):
        self.assertEqual(self.service([{'metadata':{'name':'oldx-owner-read'}},{'name':'projects/oldx-staging/locations/asia-south1/services/oldx-step05-gateway'}]),'ABSENT_FROM_SUCCESSFUL_LIST_WITH_LIMITS')
    def test_exact_service_collision(self):
        self.assertEqual(self.service([{'metadata':{'name':m.NEW_SERVICE}}]), 'EXISTS_COLLISION_STOP')
    def test_v2_service_collision(self):
        self.assertEqual(self.service([{'name':f'projects/{m.PROJECT}/locations/{m.REGION}/services/{m.NEW_SERVICE}'}]), 'EXISTS_COLLISION_STOP')
    def test_exact_sa_collision(self):
        self.assertEqual(self.sa([{'email':m.NEW_SA}]), 'EXISTS_COLLISION_STOP')
    def test_other_sa_absent(self):
        self.assertEqual(self.sa([{'email':'oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com'}]), 'ABSENT_FROM_SUCCESSFUL_LIST_WITH_LIMITS')
    def test_403_failclosed(self):
        self.assertEqual(self.service([],code=1,stderr='PERMISSION_DENIED 403'), 'UNRESOLVED_CLI_NONZERO')
    def test_success_with_error_warning_failclosed(self):
        self.assertEqual(self.service([],stderr='WARNING: partial permissions'), 'UNRESOLVED_WARNING')
    def test_invalid_json_failclosed(self):
        self.assertEqual(m.classify_listing('service',0,'not json',''), 'UNRESOLVED_JSON')
    def test_invalid_schema_failclosed(self):
        self.assertEqual(m.classify_listing('sa',0,'{}',''), 'UNRESOLVED_LIST_SCHEMA')
    def test_missing_name_failclosed(self):
        self.assertEqual(self.service([{'metadata':{}}]), 'UNRESOLVED_ITEM_SCHEMA')
    def test_missing_email_failclosed(self):
        self.assertEqual(self.sa([{'displayName':'x'}]), 'UNRESOLVED_ITEM_SCHEMA')
    def test_invalid_kind(self):
        self.assertEqual(m.classify_listing('other',0,'[{}]',''), 'INVALID_LIST_KIND')
    def _prior_fixture(self, root, bad_owner=False, bad_project=False):
        d=pathlib.Path(root)/'oldx-h1b-s3-cloudshell-readonly-20261125T213000Z'
        d.mkdir()
        (pathlib.Path(root)/m.S3_MARKER).write_text('S3_ATTEMPT_CONSUMED\nEVIDENCE='+str(d)+'\nRESULT=STOP\nREASON=TARGET_STATUS_UNRESOLVED_STOP\n')
        (d/'owner.stdout').write_text(json.dumps([{'status':'ACTIVE','account': 'wrong@example.com' if bad_owner else m.OWNER}]))
        (d/'project.stdout').write_text(json.dumps({'projectId':m.PROJECT,'projectNumber':'1' if bad_project else m.PROJECT_NUMBER,'lifecycleState':'ACTIVE'}))
        (d/'registry.stdout').write_text(json.dumps({'name':'projects/oldx-staging/locations/asia-south1/repositories/oldx-staging-images','format':'DOCKER'}))
        (d/'summary.json').write_text(json.dumps({'result':'STOP','reason':'TARGET_STATUS_UNRESOLVED_STOP','project':m.PROJECT,'region':m.REGION}))
        return d
    def test_prior_evidence_read_only_accepts_expected_state(self):
        with tempfile.TemporaryDirectory() as root:
            target=self._prior_fixture(root)
            self.assertEqual(m.verify_prior_evidence(pathlib.Path(root)), target)
    def test_wrong_past_owner_denied(self):
        with tempfile.TemporaryDirectory() as root:
            self._prior_fixture(root,bad_owner=True)
            with self.assertRaises(m.Stop):m.verify_prior_evidence(pathlib.Path(root))
    def test_wrong_past_project_denied(self):
        with tempfile.TemporaryDirectory() as root:
            self._prior_fixture(root,bad_project=True)
            with self.assertRaises(m.Stop):m.verify_prior_evidence(pathlib.Path(root))
    def test_prior_evidence_symlink_denied(self):
        with tempfile.TemporaryDirectory() as root:
            self._prior_fixture(root)
            p=pathlib.Path(root)/m.S3_MARKER
            actual=pathlib.Path(root)/'marker_real'
            p.rename(actual);p.symlink_to(actual)
            with self.assertRaises(m.Stop):m.verify_prior_evidence(pathlib.Path(root))
    def test_exact_bounded_list_invocation_with_fake_cli(self):
        with tempfile.TemporaryDirectory() as root:
            r=pathlib.Path(root)
            cli=r/'fake-gcloud'
            cli.write_text('#!/bin/sh\nprintf "%s\\n" "$@" >"$OLDX_ARG_LOG"\necho "[]"\n')
            cli.chmod(0o700)
            env=dict(os.environ,OLDX_ARG_LOG=str(r/'args'))
            state=m.run_list(str(cli),['run','services','list','--region='+m.REGION],r,'service',env)
            self.assertEqual(state,'ABSENT_FROM_SUCCESSFUL_LIST_WITH_LIMITS')
            args=(r/'args').read_text()
            self.assertIn('--account='+m.OWNER,args)
            self.assertIn('--project='+m.PROJECT,args)
            self.assertIn('--region='+m.REGION,args)
            self.assertIn('--format=json',args)
            self.assertNotIn('deploy',args)
    def test_no_flags_failclosed(self):
        import subprocess,sys
        r=subprocess.run([sys.executable, str(SRC)],capture_output=True,text=True)
        self.assertEqual(r.returncode,2)
        self.assertIn('STOP_FLAG_REQUIRED',r.stdout)

if __name__=='__main__':
    unittest.main(verbosity=2)
