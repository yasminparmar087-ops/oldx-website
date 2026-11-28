#!/usr/bin/env python3
"""NEW H2AG focused offline-only tests. Never create OAuth credentials or call APIs."""
from __future__ import annotations
import importlib.util
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

SCRIPT=Path(__file__).resolve().parents[2]/'scripts/step05_h2ag_exact_reader_sa_two_key_roles_once_20261128.py'
spec=importlib.util.spec_from_file_location('h2ag_once',SCRIPT)
h=importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)

class H2AGTests(unittest.TestCase):
    def signer(self,version=3):
        return {'version':version,'etag':'BwYAAAABAA==',
                'bindings':[{'role':'roles/cloudkms.signer','members':[h.SIGNER_MEMBER]}]}
    def reader(self,uid='123456789012345678901'):
        return {'email':h.READER,'uniqueId':uid,'name':'projects/'+h.PROJECT+'/serviceAccounts/'+h.READER,
                'projectId':h.PROJECT} # disabled false omitted (ProtoJSON)
    def test_01_exact_preimage_and_version_allowed(self):
        for version in (1,3):
            self.assertEqual(h.exact_policy(self.signer(version)), 'BwYAAAABAA==')
    def test_02_existing_role_or_conditional_policy_drift_stops(self):
        for change in ('extra','condition','public'):
            p=self.signer()
            if change=='extra':p['bindings'].append({'role':'roles/owner','members':['user:x@example.com']})
            elif change=='condition':p['bindings'][0]['condition']={'expression':'true'}
            else:p['bindings'][0]['members']=['allUsers']
            with self.assertRaises(h.Stop):h.exact_policy(p)
    def test_03_key_only_reader_roles_preserve_signer(self):
        p=h.payload_set(self.signer())
        self.assertEqual(p['updateMask'],'bindings,etag')
        self.assertEqual([b['role'] for b in p['policy']['bindings']],
          ['roles/cloudkms.signer','roles/cloudkms.viewer','roles/cloudkms.publicKeyViewer'])
        self.assertEqual([b['members'] for b in p['policy']['bindings']],
          [[h.SIGNER_MEMBER],[h.READER_MEMBER],[h.READER_MEMBER]])
        self.assertEqual(h.exact_policy(p['policy'],include_reader=True),'BwYAAAABAA==')
    def test_04_sa_omitted_default_false_correct_uid_and_reject_wrong(self):
        good=self.reader()
        self.assertEqual(h.identity(good),'123456789012345678901')
        for bad in [dict(good,uniqueId=h.GATEWAY_UID),dict(good,disabled=True),
                    dict(good,disabled=None),dict(good,email=h.SIGNER)]:
            with self.assertRaises(h.Stop):h.identity(bad)
    def test_05_outside_scope_api_rejected_without_network(self):
        with patch.object(h.OPENER,'open',side_effect=AssertionError('NETWORK MUST NOT START')):
            for method,url,body in [
             ('DELETE',h.IAM_ROOT+'/'+h.READER,None),
             ('POST','https://cloudkms.googleapis.com/v1/'+h.KEY+':asymmetricSign',{}),
             ('POST',h.POLICY_SET,{'policy':{'etag':'hack'},'updateMask':'bindings,etag'}),
             ('GET','https://iam.googleapis.com/v1/projects/oldx-staging/serviceAccounts',None),
            ]:
                with self.assertRaises(h.Stop):h.api(method,url,'fake-no-real-token',body)
    def test_06_real_one_shot_flow_mocked_create_then_exact_key_set(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            uid='123456789012345678901'
            p=self.signer()
            end={**h.payload_set(p)['policy'],'etag':'BwYAAAABBB=='}
            called=[]
            responses=[(404,{}),(200,p),(200,self.reader(uid)),(200,self.reader(uid)),
                       (200,p),(200,end),(200,end)]
            def fake_api(method,url,token,body=None,allowed_numeric_uid=None):
                called.append((method,url,body))
                return responses.pop(0)
            with patch.object(h,'ROOT',root),patch.object(h,'MARK',root/'marker'),\
                 patch.object(h,'owner_token',return_value='test-owner-token'),\
                 patch.object(h,'api',side_effect=fake_api),redirect_stdout(StringIO()) as output:
                self.assertEqual(h.main(),0)
                self.assertEqual([x[0] for x in called],['GET','GET','POST','GET','GET','POST','GET'])
                self.assertEqual(sum(m=='POST' and u==h.IAM_ROOT for m,u,_ in called),1)
                self.assertEqual(sum(m=='POST' and u==h.POLICY_SET for m,u,_ in called),1)
                self.assertIn('H2AG_RESULT=ONE_READER_SA_TWO_KEY_READ_ONLY_ROLES_PASS',output.getvalue())
                self.assertTrue((root/'marker').exists())
                self.assertEqual(responses,[])
    def test_07_create_error_stop_consumed_no_key_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            p=self.signer()
            responses=[(404,{}),(200,p),(409,{})]
            called=[]
            def fake(method,url,token,body=None,allowed_numeric_uid=None):
                called.append((method,url))
                return responses.pop(0)
            with patch.object(h,'ROOT',root),patch.object(h,'MARK',root/'marker'),\
                 patch.object(h,'owner_token',return_value='test-owner-token'),\
                 patch.object(h,'api',side_effect=fake),redirect_stdout(StringIO()) as output:
                self.assertEqual(h.main(),2)
                self.assertTrue((root/'marker').exists())
                self.assertEqual(called,[('GET',h.SA_URL),('GET',h.POLICY_GET),('POST',h.IAM_ROOT)])
                self.assertIn('H2AG_RESULT=STOP_AFTER_MARKER_POSSIBLE_PARTIAL_CLOUD_WRITE',output.getvalue())

if __name__=='__main__':unittest.main(verbosity=2)
