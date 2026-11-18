"""Mocked only: never connects to Google Cloud, never calls gcloud."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SRC = Path(__file__).resolve().parents[2] / 'scripts' / 'step04-g4-one-doc-proof.py'
spec = importlib.util.spec_from_file_location('g4_probe', SRC)
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)

class FakeAPI:
    def __init__(self, *, runtime_delete_status=403, owner_cleanup_status=200,
                 block_create=False, block_update=False):
        self.doc = None
        self.ct = '2026-11-18T13:00:00.000000Z'
        self.ut = self.ct
        self.calls = []
        self.delete_status = runtime_delete_status
        self.cleanup_status = owner_cleanup_status
        self.block_create = block_create
        self.block_update = block_update

    def __call__(self, method, url, token, payload=None):
        self.calls.append((method, url, token))
        if method == 'GET':
            return p.HttpResult(200, dict(self.doc)) if self.doc else p.HttpResult(404, {'error':{'status':'NOT_FOUND'}})
        if method == 'POST' and 'documentId=' in url:
            if self.block_create: return p.HttpResult(403, {'error':{'status':'PERMISSION_DENIED'}})
            docid = url.split('documentId=')[1]
            self.doc = {'name':p.DB_ROOT+'/documents/'+p.COLLECTION+'/'+docid,
                        'fields':payload['fields'],'createTime':self.ct,'updateTime':self.ct}
            return p.HttpResult(200, dict(self.doc))
        if method == 'PATCH':
            if self.block_update: return p.HttpResult(403, {'error':{'status':'PERMISSION_DENIED'}})
            self.doc['fields']['revision'] = {'integerValue':'2'}
            self.doc['updateTime'] = '2026-11-18T13:00:00.100000Z'
            return p.HttpResult(200, dict(self.doc))
        if method == 'DELETE' and token == 'a' * 42:
            if self.delete_status == 403:
                return p.HttpResult(403, {'error':{'status':'PERMISSION_DENIED'}})
            self.doc = None
            return p.HttpResult(self.delete_status,{})
        if method == 'DELETE' and token == 'b' * 42:
            if self.cleanup_status in (200,204): self.doc = None
            return p.HttpResult(self.cleanup_status, {} if self.cleanup_status < 400 else {'error':{'status':'PERMISSION_DENIED'}})
        self.fail('Unexpected API call')

class ProofTests(unittest.TestCase):
    def do_test(self, api, expected=None):
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(p.Path, 'home', return_value=Path(temp)),\
                 patch.object(p, 'guard_operator', return_value='b'*42),\
                 patch.object(p, 'runtime_credential', return_value='a'*42),\
                 patch.object(p, 'request', side_effect=api):
                if expected:
                    with self.assertRaises(p.Stop) as e:p.run_once()
                    self.assertEqual(e.exception.code,expected)
                else:p.run_once()
                journal=Path(temp)/p.JOURNAL_DIRNAME/'journal.json'
                self.assertTrue(journal.exists())
                self.assertEqual(journal.stat().st_mode & 0o777,0o600)
                self.assertEqual(journal.parent.stat().st_mode & 0o777,0o700)
                import json
                status=json.loads(journal.read_text())['state']
                return status

    def test_success_one_doc_exact_cleanup(self):
        api=FakeAPI()
        status=self.do_test(api)
        self.assertEqual(status,'CLEANUP_VERIFIED')
        self.assertIsNone(api.doc)
        self.assertEqual([x[0] for x in api.calls],['GET','GET','POST','PATCH','DELETE','GET','DELETE','GET'])
    def test_create_403_no_cleanup_no_retry(self):
        api=FakeAPI(block_create=True)
        self.assertEqual(self.do_test(api,'CREATE_DENIED_OR_FAILED'),'CREATE_UNKNOWN')
        self.assertEqual(sum(x[0]=='POST' for x in api.calls),1)
        self.assertIsNone(api.doc)
    def test_runtime_delete_succeeds_unexpectedly_stops(self):
        api=FakeAPI(runtime_delete_status=200)
        self.assertEqual(self.do_test(api,'RUNTIME_DELETE_NOT_PROVEN_DENIED'),'RUNTIME_DELETE_UNEXPECTED')
        self.assertIsNone(api.doc)
        self.assertEqual(sum(x[0]=='DELETE' for x in api.calls),1)
    def test_operator_cleanup_denied_maintain_journal(self):
        api=FakeAPI(owner_cleanup_status=403)
        self.assertEqual(self.do_test(api,'OPERATOR_CLEANUP_FAILED'),'OPERATOR_CLEANUP_OUTCOME_UNKNOWN')
        self.assertIsNotNone(api.doc)
        self.assertEqual(sum(x[0]=='DELETE' for x in api.calls),2)
    def test_journal_blocks_repeat(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(p.Path,'home',return_value=Path(temp)):
            (Path(temp)/p.JOURNAL_DIRNAME).mkdir()
            with self.assertRaises(p.Stop) as e:p.run_once()
            self.assertEqual(e.exception.code,'EXISTING_JOURNAL_REQUIRES_REVIEW')

    def test_resume_after_initialized_cli_timeout_reuses_exact_document(self):
        import json
        api = FakeAPI()
        with tempfile.TemporaryDirectory() as temp, patch.object(p.Path, 'home', return_value=Path(temp)):
            with patch.object(p, 'guard_operator', side_effect=p.Stop('GCLOUD_UNAVAILABLE')):
                with self.assertRaises(p.Stop) as caught:
                    p.run_once()
                self.assertEqual(caught.exception.code, 'GCLOUD_UNAVAILABLE')
            journal = Path(temp) / p.JOURNAL_DIRNAME / 'journal.json'
            before = json.loads(journal.read_text())
            self.assertEqual(before['state'], 'INITIALIZED')
            self.assertEqual(api.calls, [])
            with patch.object(p, 'guard_operator', return_value='b'*42), \
                 patch.object(p, 'runtime_credential', return_value='a'*42), \
                 patch.object(p, 'request', side_effect=api):
                p.run_once(resume_initialized=True)
            after = json.loads(journal.read_text())
            self.assertEqual(after['document'], before['document'])
            self.assertEqual(after['marker'], before['marker'])
            self.assertEqual(after['state'], 'CLEANUP_VERIFIED')
            self.assertIsNone(api.doc)
            self.assertEqual([x[0] for x in api.calls],
                ['GET','GET','POST','PATCH','DELETE','GET','DELETE','GET'])
            with self.assertRaises(p.Stop) as again:
                p.run_once(resume_initialized=True)
            self.assertEqual(again.exception.code, 'JOURNAL_NOT_EXACT_PRIVATE_INITIALIZED')

    def test_resume_rejects_drifted_initial_state_without_cloud(self):
        import json
        with tempfile.TemporaryDirectory() as temp, patch.object(p.Path,'home',return_value=Path(temp)):
            with patch.object(p, 'guard_operator', side_effect=p.Stop('GCLOUD_UNAVAILABLE')):
                with self.assertRaises(p.Stop): p.run_once()
            directory = Path(temp) / p.JOURNAL_DIRNAME
            journal = directory / 'journal.json'
            original = json.loads(journal.read_text())
            for change in [
                {'state':'CREATE_UNKNOWN'}, {'marker':'ff'},
                {'document':p.COLLECTION+'/another-document'},
                {'project':'oldx-1c983'}, {'createTime':'2026-11-18T12:00:00Z'}
            ]:
                obj = {**original, **change}
                p.durable_record(directory, obj)
                with patch.object(p, 'guard_operator', side_effect=AssertionError('should not call gcloud')):
                    with self.assertRaises(p.Stop) as denied:
                        p.run_once(resume_initialized=True)
                    self.assertEqual(denied.exception.code,'JOURNAL_NOT_EXACT_PRIVATE_INITIALIZED')
            p.durable_record(directory, original)
            journal.chmod(0o644)
            with self.assertRaises(p.Stop) as denied:
                p.run_once(resume_initialized=True)
            self.assertEqual(denied.exception.code,'JOURNAL_NOT_EXACT_PRIVATE_INITIALIZED')

    def test_bad_scope_and_marker_rejected(self):
        with self.assertRaises(p.Stop):
            p.valid_document({'name':'wrong','fields':p.fields('abc',1),'createTime':'2026-11-18T13:00:00Z','updateTime':'2026-11-18T13:00:00Z'},'right','abc',1)
    def test_http_url_allowlist_rejects_non_firestorm(self):
        with self.assertRaises(p.Stop) as e:p.request('GET','https://example.com','a'*42)
        self.assertEqual(e.exception.code,'UNEXPECTED_ENDPOINT')

if __name__ == '__main__':unittest.main()
