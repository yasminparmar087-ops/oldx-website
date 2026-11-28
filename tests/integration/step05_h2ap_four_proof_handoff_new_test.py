"""NEW H2AP OFFLINE tests only. Registry/SDK/H2AO processes are all doubles."""
import base64,copy,datetime,io,json,os,shutil,sys,tempfile,time,types,unittest,urllib.error
from pathlib import Path
from unittest.mock import patch
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE/"scripts"))
import step05_h2ap_four_manifest_proofs_then_h2ao_once_20261129 as m
import step05_h2ap_cached_owner_token as tk
import step05_h2ao_oci_identity as ident
def make(role):
    config={"os":"linux","architecture":"amd64","config":{"User":"65532:65532","WorkingDir":"/app",
        "Entrypoint":["/nodejs/bin/node"],"Cmd":["functions/staging-marketplace/four-role/"+role+".mjs"],
        "Env":["NODE_ENV=production"]},"rootfs":{"type":"layers","diff_ids":["sha256:"+"d"*64]}}
    raw=json.dumps(config,separators=(",",":")).encode();raw+=b" "*(32372-len(raw));cfg=ident.hashed(raw)
    manifest=json.dumps({"schemaVersion":2,"mediaType":"application/vnd.oci.image.manifest.v1+json",
        "config":{"mediaType":"application/vnd.oci.image.config.v1+json","digest":cfg,"size":len(raw)},
        "layers":[{"mediaType":"application/vnd.oci.image.layer.v1.tar+gzip","digest":"sha256:"+"e"*64,"size":10}]}).encode()
    ref=m.PREFIX+m.PINS[role][0]+"@"+ident.hashed(manifest)
    sev=["High"]*18+["Medium"]*20+["Low"]*6+["Negligible"]*11+["Unknown"]*2
    report=json.dumps({"source":{"type":"image","target":{"imageID":cfg,"userInput":ref,
        "config":base64.b64encode(raw).decode()}},"matches":[{"vulnerability":{"severity":v,"id":"TEST-"+str(n)}} for n,v in enumerate(sev)]}).encode()
    return {"raw":manifest,"ref":ref,"cfg":cfg,"report":report}
class Response(io.BytesIO):
    def __init__(self,raw,status=200,headers=None):
        super().__init__(raw);self.status=status;self.headers=headers or {"Content-Type":"application/vnd.oci.image.manifest.v1+json"}
class H2AP(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.data={r:make(r) for r in m.PINS};self.count=0
        self.refs={r:v["ref"] for r,v in self.data.items()};self.token="UNIT_ONLY_"+"t"*80
        self.patches=[patch.object(m,"REFS",self.refs),patch.object(m,"REPORT_SHA",m.sha(self.data["mediator"]["report"])),
            patch.object(m,"MED_CONFIG",self.data["mediator"]["cfg"])]
        for p in self.patches:p.start()
    def tearDown(self):
        for p in reversed(self.patches):p.stop()
        self.tmp.cleanup()
    def workflow(self,fail_role=None,error=None):
        self.count+=1;p=self.root/("evidence"+str(self.count));p.mkdir(mode=0o700);calls=[];mark=self.root/("marker"+str(self.count))
        def fetch(role,token):
            self.assertEqual(token,self.token);self.assertTrue(mark.is_file());calls.append(role)
            self.assertEqual(json.loads((p/(role+"-receipt.json")).read_bytes())["status"],"ATTEMPTED")
            if role==fail_role:raise error or m.Stop("HTTP_ERROR_NO_RETRY",401)
            return self.data[role]["raw"],{"status":200,"type":"application/vnd.oci.image.manifest.v1+json",
                "digest":self.refs[role].rsplit("@",1)[1]}
        return m.Workflow(p,mark,ident,self.data["mediator"]["report"],fetch=fetch),calls
    def bundle(self):
        self.count+=1;root=self.root/("source"+str(self.count));root.mkdir(mode=0o700)
        for path in m.FROZEN:
            p=root/path;p.parent.mkdir(mode=0o700,parents=True,exist_ok=True);m.write_new(p,(BASE/path).read_bytes())
        return root
    def test_01_default_off_requires_both_future_approvals(self):
        with patch.object(m,"prepare_bundle",side_effect=AssertionError("NO_IO")),patch.object(m,"get_manifest",side_effect=AssertionError("NO_GET")),patch.object(m,"load_token",side_effect=AssertionError("NO_SDK")):
            self.assertEqual(m.cli([]),0)
            self.assertEqual(m.cli(["--owner-approved-four-manifest-gets-once"]),0)
    def test_02_four_proofs_raw_bytes_private_modes_and_historical_config_binding(self):
        w,calls=self.workflow();w.acquire(self.token);w.verify_proofs()
        self.assertEqual(calls,list(m.PINS));self.assertEqual(w.summary["outcome"],"FOUR_PROOFS_COMPLETE")
        self.assertEqual(w.proofs.stat().st_mode&0o777,0o700)
        for role in m.PINS:
            f=w.proofs/(role+"-child-manifest.json")
            self.assertEqual(f.read_bytes(),self.data[role]["raw"]);self.assertEqual(f.stat().st_mode&0o777,0o600)
            self.assertEqual(w.summary["roles"][role]["status"],"COMPLETE")
        self.assertNotIn(self.token,json.dumps(w.summary)+w.marker.read_text())
    def test_03_partial_failure_at_each_role_stops_without_retry_and_retains_prior(self):
        for role in m.PINS:
            w,calls=self.workflow(role)
            with self.assertRaises(m.Stop):w.acquire(self.token)
            self.assertEqual(calls,list(m.PINS)[:list(m.PINS).index(role)+1])
            self.assertTrue(w.marker.exists());self.assertEqual(w.summary["roles"][role]["httpStatus"],401)
            for prior in calls[:-1]:self.assertTrue((w.proofs/(prior+"-child-manifest.json")).exists())
            self.assertEqual(w.summary["handoff"]["status"],"NOT_ATTEMPTED")
    def test_04_marker_consumed_cannot_start_a_second_request(self):
        w,calls=self.workflow();m.write_new(w.marker,b"consumed")
        with self.assertRaises(FileExistsError):w.acquire(self.token)
        self.assertFalse(calls);self.assertEqual(w.marker.read_bytes(),b"consumed")
    def test_05_http_fixed_urls_one_get_and_auth_header_removed_after_call(self):
        requests=[]
        class Opener:
            def open(_self,req,timeout):
                requests.append(req);return Response(b"RAW")
        with patch.object(m,"opener",return_value=Opener()):
            for role in m.PINS:self.assertEqual(m.get_manifest(role,self.token)[0],b"RAW")
            with self.assertRaises(m.Stop):m.get_manifest("arbitrary",self.token)
        self.assertEqual([r.full_url for r in requests],list(m.URLS.values()))
        self.assertTrue(all(r.get_method()=="GET" and r.get_header("Authorization") is None for r in requests))
        self.assertTrue(all("@sha" not in r.full_url and "/manifests/sha256:" in r.full_url for r in requests))
    def test_06_401_dns_tls_timeout_have_one_request_no_error_body_or_token_leak(self):
        for error in (urllib.error.HTTPError("https://TEST",401,self.token,{},None),
            urllib.error.URLError(self.token),TimeoutError(self.token)):
            class Opener:
                count=0
                def open(_self,*a,**k):_self.count+=1;raise error
            op=Opener()
            with patch.object(m,"opener",return_value=op),self.assertRaises(m.Stop) as caught:m.get_manifest("mediator",self.token)
            self.assertEqual(op.count,1);self.assertNotIn(self.token,str(caught.exception))
    def test_07_redirect_handler_never_follows_to_other_host(self):
        with self.assertRaisesRegex(m.Stop,"REDIRECT"):
            m.NoRedirect().redirect_request(None,None,302,"",{},"https://UNAPPROVED")
    def test_08_wrong_encoding_and_body_oversize_stop_before_proof(self):
        for response in (Response(b"x",headers={"Content-Encoding":"gzip"}),Response(b"x"*524289)):
            class Opener:
                def open(_self,*a,**k):return response
            with patch.object(m,"opener",return_value=Opener()),self.assertRaises(m.Stop) as caught:m.get_manifest("mediator",self.token)
            self.assertEqual(caught.exception.status,200)
    def test_09_false_media_and_digest_headers_reject_and_keep_private_raw(self):
        for headers in ({"status":200,"type":"text/html","digest":None},
            {"status":200,"type":"application/vnd.oci.image.manifest.v1+json","digest":"sha256:"+"0"*64}):
            w,calls=self.workflow();w.fetch=lambda role,token:(self.data[role]["raw"],headers)
            with self.assertRaises(m.Stop):w.acquire(self.token)
            self.assertEqual(w.summary["roles"]["mediator"]["status"],"FAILED")
            self.assertTrue((w.proofs/"mediator-child-manifest.json").exists())
    def test_10_wrong_raw_hash_and_malformed_or_index_manifest_cannot_handoff(self):
        w,_=self.workflow();w.fetch=lambda role,token:(b"tampered",{"status":200,"type":"application/vnd.oci.image.manifest.v1+json","digest":None})
        with self.assertRaises(ident.Stop):w.acquire(self.token)
        self.assertEqual(w.summary["handoff"]["status"],"NOT_ATTEMPTED")
        for raw in (b'{"schemaVersion":2,"manifests":[]}',b'{"config":',b'{"schemaVersion":2}'):
            with self.assertRaises(ident.Stop):ident.manifest_config(raw,"x@"+ident.hashed(raw))
    def test_11_mediator_config_digest_size_or_historical_hash_mismatch_stops(self):
        raw=self.data["mediator"]["report"];manifest=json.loads(self.data["mediator"]["raw"])
        for key,value in (("digest","sha256:"+"0"*64),("size",32371)):
            bad=copy.deepcopy(manifest);bad["config"][key]=value
            with self.assertRaisesRegex(m.Stop,"CONFIG_MISMATCH"):m.mediator_config(raw,bad,ident)
        with self.assertRaisesRegex(m.Stop,"REPORT_SHA"):m.mediator_config(raw+b" ",manifest,ident)
    def test_12_four_complete_rehashed_proofs_and_separate_approval_before_one_handoff(self):
        w,_=self.workflow();bundle=self.bundle();calls=[]
        with self.assertRaises(m.Stop):w.handoff(bundle,True,lambda *a:calls.append(a))
        w.acquire(self.token)
        with self.assertRaisesRegex(m.Stop,"SEPARATE"):w.handoff(bundle,False,lambda *a:calls.append(a))
        def invoke(*args):
            calls.append(args);return {"status":"COMPLETE","exitCode":0,"outcome":"COMPLETE_OFF_EVIDENCE_SECURITY_REVIEW_REQUIRED"}
        w.handoff(bundle,True,invoke)
        self.assertEqual(len(calls),1)
        with self.assertRaisesRegex(m.Stop,"ALREADY_ATTEMPTED"):w.handoff(bundle,True,invoke)
        self.assertEqual(len(calls),1);self.assertEqual(w.summary["outcome"],"PROOFS_AND_OFF_EVIDENCE_COMPLETE_SECURITY_HOLD")
    def test_13_changed_proof_or_frozen_source_refuses_handoff(self):
        w,_=self.workflow();w.acquire(self.token);bundle=self.bundle()
        (w.proofs/"reader-child-manifest.json").write_bytes(b"tampered")
        with self.assertRaisesRegex(m.Stop,"PROOF_CHANGED"):w.handoff(bundle,True,lambda *a:self.fail("NO_HANDOFF"))
        p=bundle/"scripts/step05_h2ao_oci_identity.py";p.write_bytes(b"tampered")
        with self.assertRaisesRegex(m.Stop,"SOURCE_DRIFT"):m.verify_bundle(bundle)
    def test_14_h2ao_stop_preserves_completed_proofs_and_no_second_call(self):
        w,_=self.workflow();w.acquire(self.token);bundle=self.bundle();calls=[]
        def invoke(*args):calls.append(args);return {"status":"STOP","exitCode":2,"outcome":"UNKNOWN"}
        with self.assertRaisesRegex(m.Stop,"H2AO_STOP"):w.handoff(bundle,True,invoke)
        self.assertEqual(len(calls),1);self.assertEqual(w.summary["handoff"]["exitCode"],2)
        w.verify_proofs()
        with self.assertRaisesRegex(m.Stop,"ALREADY_ATTEMPTED"):w.handoff(bundle,True,invoke)
        self.assertEqual(len(calls),1)
    def test_15_token_loader_captures_only_memory_and_never_puts_token_in_env_or_argv(self):
        sdk=self.root/"sdk";native=sdk/"python";sdk.mkdir();m.write_new(native,bytes([127])+b"ELF");native.chmod(0o700)
        helper=BASE/"scripts/step05_h2ap_cached_owner_token.py";calls=[]
        def run(argv,**kw):
            calls.append((argv,kw));return types.SimpleNamespace(returncode=0,stdout=json.dumps({"token":self.token,"expiresAt":int(time.time())+600}).encode())
        with patch.multiple(m,SDK=sdk,SDK_PY=native),patch.object(m.subprocess,"run",side_effect=run):
            self.assertEqual(m.load_token(helper),self.token)
        self.assertEqual(len(calls),1);argv,kw=calls[0]
        self.assertNotIn(self.token,str(argv)+str(kw["env"]))
        self.assertEqual(kw["stderr"],m.subprocess.PIPE)
    def test_16_cached_token_expiry_and_service_account_fail_closed_no_refresh(self):
        class User:pass
        google=types.ModuleType("google.oauth2.credentials");google.Credentials=User
        now=datetime.datetime.now(datetime.timezone.utc)
        with patch.dict(sys.modules,{"google.oauth2.credentials":google}):
            for seconds in (-10,60,4000):
                credential=User();credential.token=self.token;credential.expiry=now+datetime.timedelta(seconds=seconds)
                with self.assertRaises(tk.Stop):tk.validate_cached(credential,now)
            with self.assertRaises(tk.Stop):tk.validate_cached(object(),now)
            credential=User();credential.token=self.token;credential.expiry=now+datetime.timedelta(seconds=600)
            self.assertEqual(tk.validate_cached(credential,now)["token"],self.token)
    def test_17_sdk_sandbox_forces_readonly_sqlite_and_denies_network_or_writes(self):
        config=self.root/"config";config.mkdir()
        for name in ("credentials.db","access_tokens.db"):m.write_new(config/name,b"TEST_NO_CREDENTIALS")
        hooks=[];connections=[]
        def connect(database,*a,**kw):connections.append((database,kw));return "READONLY"
        with patch.object(tk.sys,"addaudithook",side_effect=hooks.append),patch.object(tk.sqlite3,"connect",side_effect=connect):
            tk.sandbox(config)
            self.assertEqual(tk.sqlite3.connect(config/"credentials.db"),"READONLY")
            self.assertTrue(connections[0][0].endswith("?mode=ro&immutable=1"))
            with self.assertRaises(tk.Stop):tk.sqlite3.connect(config/"UNAPPROVED.db")
        for event,args in (("socket.connect",()),("subprocess.Popen",()),("open",("file","w",os.O_WRONLY)),("os.remove",("x",))):
            with self.assertRaises(tk.Stop):hooks[0](event,args)
    def test_18_old_and_h2ao_markers_preserved_before_any_new_attempt(self):
        ao=types.SimpleNamespace(MARKER=self.root/"ao",PREFLIGHT_MARKER=self.root/"pref",GET_MARKER=self.root/"get",GLOBAL=self.root/"global")
        mark=self.root/"ap"
        with patch.object(m,"MARKER",mark):
            m.assert_fresh(ao)
            m.write_new(ao.MARKER,b"old-consumed")
            with self.assertRaisesRegex(m.Stop,"NO_REPLAY"):m.assert_fresh(ao)
            self.assertEqual(ao.MARKER.read_bytes(),b"old-consumed");self.assertFalse(mark.exists())
    def test_19_full_new_cli_token_before_marker_and_handoff_only_after_four_proofs(self):
        bundle=self.bundle();old=self.root/"old-marker";m.write_new(old,b"consumed-KEEP")
        snapshots={str(old):m.sha(old.read_bytes())};db=self.root/"db";db.mkdir(mode=0o700)
        native=self.root/"fake-elf";m.write_new(native,bytes([127])+b"ELF");native.chmod(0o700)
        ao=types.SimpleNamespace(MARKER=self.root/"ao",PREFLIGHT_MARKER=self.root/"pref",GET_MARKER=self.root/"get",
            GLOBAL=self.root/"aoglobal",DB=db,GRYPE=native,REFS=self.refs,owner_scope=lambda:None,
            history=lambda:(self.data["mediator"]["report"],{},snapshots),private_dir=lambda p:None,
            old=types.SimpleNamespace(proposal_check=lambda raw:None))
        mark=self.root/"ap";gets=[];handoffs=[]
        def token(helper):self.assertFalse(mark.exists());return self.token
        def fetch(role,token):
            self.assertTrue(mark.exists());gets.append(role)
            return self.data[role]["raw"],{"status":200,"type":"application/vnd.oci.image.manifest.v1+json","digest":None}
        def invoke(b,p,e):
            self.assertEqual(gets,list(m.PINS));self.assertTrue(all((p/(r+"-child-manifest.json")).exists() for r in m.PINS))
            handoffs.append(True);return {"exitCode":0,"outcome":"COMPLETE_OFF_EVIDENCE_SECURITY_REVIEW_REQUIRED"}
        with patch.multiple(m,ROOT=self.root,MARKER=mark),patch("platform.system",return_value="Linux"),patch("platform.release",return_value="microsoft"),patch.object(m,"prepare_bundle",return_value=bundle),patch.object(m.importlib,"import_module",side_effect=lambda n:ao if n.endswith("20261129") else ident),patch.object(m.shutil,"which",return_value=str(native)),patch.object(m.shutil,"disk_usage",return_value=types.SimpleNamespace(free=8*1024**3)),patch.object(m,"load_token",side_effect=token),patch.object(m,"get_manifest",side_effect=fetch),patch.object(m,"invoke_h2ao",side_effect=invoke):
            self.assertEqual(m.cli(["--owner-approved-four-manifest-gets-once","--owner-approved-h2ao-selective-once"]),0)
        self.assertEqual(len(handoffs),1);self.assertEqual(old.read_bytes(),b"consumed-KEEP")
    def test_20_receipt_write_failure_stops_before_next_role_or_handoff(self):
        w,calls=self.workflow();original=m.receipt
        def write(path,value):
            if Path(path).name=="mediator-receipt.json" and value.get("status")=="COMPLETE":raise OSError("TEST_DISK_FULL")
            return original(path,value)
        with patch.object(m,"receipt",side_effect=write),self.assertRaises(OSError):w.acquire(self.token)
        self.assertEqual(calls,["mediator"]);self.assertTrue((w.proofs/"mediator-child-manifest.json").exists())
        self.assertEqual(w.summary["handoff"]["status"],"NOT_ATTEMPTED")

    def test_21_token_failure_reports_only_allowlisted_code_never_captured_secret(self):
        sdk=self.root/"sdk";native=sdk/"python";sdk.mkdir();m.write_new(native,bytes([127])+b"ELF");native.chmod(0o700)
        helper=BASE/"scripts/step05_h2ap_cached_owner_token.py"
        for stderr,expected in ((b"H2AP_TOKEN_STOP=SDK_WRITE_FORBIDDEN","OWNER_TOKEN_SDK_WRITE_FORBIDDEN"),
            (self.token.encode(),"CACHED_OWNER_TOKEN_UNAVAILABLE_NO_REFRESH")):
            result=types.SimpleNamespace(returncode=2,stdout=self.token.encode(),stderr=stderr)
            with patch.multiple(m,SDK=sdk,SDK_PY=native),patch.object(m.subprocess,"run",return_value=result),self.assertRaises(m.Stop) as caught:m.load_token(helper)
            self.assertEqual(caught.exception.code,expected)
            self.assertNotIn(self.token,str(caught.exception))
if __name__=="__main__":unittest.main()
