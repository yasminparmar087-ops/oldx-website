"""NEW H2AM OFFLINE tests. Every Docker/Grype/process call is a test double."""
import copy
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"scripts"))
import step05_h2am_selective_acceptance_once_20261128 as m
import step05_h2am_acceptance_support as s

IDS={r:"sha256:"+c*64 for r,c in zip(m.PINS,"abcd")}
def report(role,historical=False):
    severities=(["High"]*18+["Medium"]*20+["Low"]*6+["Negligible"]*11+["Unknown"]*2) if historical else ["High","Medium","High"]
    return json.dumps({"source":{"type":"image","target":{"imageID":IDS[role],"userInput":m.REFS[role],
        "manifestDigest":"sha256:"+m.PINS[role][1]}},
        "descriptor":{"version":"TEST_ONLY_GRYPE","db":{"built":"2026-11-28T00:00:00Z","checksum":"f"*64,"schemaVersion":6}},
        "matches":[{"vulnerability":{"id":"TEST-HIST-"+str(i),"severity":v}} for i,v in enumerate(severities)]}).encode()
def private(path,data):
    path.write_bytes(data);path.chmod(0o600)
class Fake:
    def __init__(self,session,store,fail_role=None,mode=None):
        self.session=session;self.store=store;self.calls=[];self.containers={};self.fail_role=fail_role;self.mode=mode
        self.before_cleanup=[]
    def call(self,args,timeout=30,input_bytes=None,stdout_file=None):
        self.session.require();self.calls.append(list(args))
        if args[:3]==["docker","image","inspect"]:
            role=next(r for r in m.PINS if m.REFS[r]==args[3])
            data=[{"Id":IDS[role],"RepoDigests":[m.REFS[role]],"Os":"linux","Architecture":"amd64",
             "Config":{"User":"65532:65532","WorkingDir":"/app","Entrypoint":["/nodejs/bin/node"],
             "Cmd":["functions/staging-marketplace/four-role/"+role+".mjs"],"Env":["NODE_ENV=production"]}}]
            return s.Result(0,json.dumps(data))
        if args[0]=="grype":
            role=next(r for r in m.PINS if args[1]=="docker:"+IDS[r])
            if role=="mediator":raise AssertionError("MEDIATOR_MUST_NEVER_SCAN")
            private(Path(stdout_file),report(role));return s.Result(0)
        op=args[1]
        if op=="run":
            name=args[args.index("--name")+1];role=name.split("-")[2]
            labels={"oldx.h2am.attempt":self.session.attempt,"oldx.h2am.role":role}
            state={"Id":("1" if role=="mediator" else "2")*64,"Name":"/"+name,"Image":IDS[role],
             "Config":{"Labels":labels},"HostConfig":{"NetworkMode":"none","ReadonlyRootfs":True,"PortBindings":{},
             "Binds":None,"Memory":768*1024*1024,"NanoCpus":1_000_000_000,"PidsLimit":128,
             "CapDrop":["ALL"],"SecurityOpt":["no-new-privileges"]},"Mounts":[],
             "State":{"Running":True,"ExitCode":0,"OOMKilled":False,"Error":"","Pid":123}}
            if role==self.fail_role and self.mode=="startup":
                state["State"].update(Running=False,ExitCode=1)
            self.containers[name]=state;return s.Result(0,state["Id"])
        if op=="inspect":
            name=args[2];state=self.containers.get(name)
            if not state:return s.Result(1,stderr="Error: No such container: "+name)
            return s.Result(0,json.dumps([state]))
        if op=="exec":
            name=next(k for k,v in self.containers.items() if v["Id"]==args[3]);role=name.split("-")[2]
            if role==self.fail_role:
                self.containers[name]["State"].update(Running=self.mode=="cleanup",ExitCode=1,OOMKilled=self.mode=="oom")
                return s.Result(137,stdout="first probe output",stderr="FIRST_EXEC_FAILURE")
            return s.Result(0,json.dumps({"health":200,"product":503,"state":"OFF","role":role,"uid":65532,"nodeMajor":24,"error":None}))
        if op=="logs":
            return s.Result(0,stderr="Error [ERR_MODULE_NOT_FOUND]: /app/scripts/missing.mjs\n"+(
                "Authorization: Bearer private_token_must_not_escape" if self.mode=="startup" else ""))
        if op in ("stop","rm"):
            name=args[-1];role=name.split("-")[2]
            saved=self.store.get(role+"-runtime.json");self.before_cleanup.append(saved)
            if role==self.fail_role and self.mode=="cleanup":
                return s.Result(1,stderr="daemon unavailable cleanup")
            if op=="stop":
                self.containers[name]["State"].update(Running=False,ExitCode=0);return s.Result(0,name)
            if role==self.fail_role and self.mode=="notfound":
                self.containers.pop(name,None);return s.Result(1,stderr="No such container")
            self.containers.pop(name,None);return s.Result(0,name)
        raise AssertionError("UNEXPECTED_OPERATION "+str(args))
class H2AM(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.global_dir=self.root/"global";self.global_dir.mkdir(mode=0o700)
        self.counter=0
    def tearDown(self):self.tmp.cleanup()
    def engine(self,**kwargs):
        self.counter+=1;folder=self.root/("evidence"+str(self.counter));folder.mkdir(mode=0o700)
        store=s.Store(folder);session=s.Session.consume(self.root/("attempt"+str(self.counter)),str(self.counter)*32,m.plan_digest())
        fake=Fake(session,store,**kwargs);return m.Acceptance(store,session,fake,self.global_dir),fake,store
    def historic(self):return report("mediator",True),s.scan_report(report("mediator",True),m.REFS["mediator"],historical=True)
    def test_01_default_flags_never_invoke_process_or_read_old_evidence(self):
        with patch.object(s.subprocess,"Popen",side_effect=AssertionError("NO PROCESS")),patch.object(m,"prerequisites",side_effect=AssertionError("NO PRIVATE READ")):
            for args in ([],["--execute-h2am-once"],["--owner-approved-selective-off-only"]):
                with patch("sys.stdout",new=io.StringIO()):self.assertEqual(m.cli(args),0)
        marker=self.root/"taken";s.Session.consume(marker,"x",m.plan_digest())
        with self.assertRaises(FileExistsError):s.Session.consume(marker,"x",m.plan_digest())
    def test_02_historic_counts_are_exact_imported_and_mediator_never_scanned(self):
        a,f,store=self.engine();raw,h=self.historic();result=a.run(raw,h)
        self.assertEqual(result["outcome"],"COMPLETE_OFF_EVIDENCE_SECURITY_REVIEW_REQUIRED")
        self.assertEqual(store.get("mediator-scan.json")["severity"],s.HISTORIC_COUNTS)
        self.assertEqual(store.get("mediator-scan.json")["matches"],57)
        self.assertEqual((store.path/"mediator-historic-grype.json").read_bytes(),raw)
        self.assertEqual([next(r for r in m.PINS if x[1]=="docker:"+IDS[r]) for x in f.calls if x[0]=="grype"],["gateway","backend","reader"])
        with self.assertRaisesRegex(s.Stop,"MEDIATOR_RESCAN_FORBIDDEN"):a.scan("mediator",IDS["mediator"])
    def test_03_scan_metadata_is_durable_before_runtime_and_kept_on_failure(self):
        a,f,store=self.engine(fail_role="gateway",mode="exec")
        raw,h=self.historic();out=a.run(raw,h)
        self.assertEqual(out["outcome"],"STOP_PARTIAL_NO_AUTOMATIC_RETRY")
        self.assertEqual(store.get("gateway-scan.json")["status"],"COMPLETE")
        self.assertEqual(store.get("gateway-scan.json")["database"]["checksum"],"f"*64)
        self.assertEqual(store.get("gateway-runtime.json")["primaryFailure"]["detail"]["exitCode"],137)
        self.assertFalse((store.path/"backend-scan.json").exists())
        plan=m.inspect_resume(store.path,self.global_dir)
        self.assertEqual(plan["status"],"BLOCKED_NO_EXECUTION")
        f.calls.clear();again=a.run(raw,h)
        self.assertEqual(f.calls,[]);self.assertEqual(again["outcome"],"STOP_PARTIAL_NO_AUTOMATIC_RETRY")
    def test_04_startup_exit_one_no_exec_logs_kept_before_cleanup(self):
        a,f,store=self.engine(fail_role="mediator",mode="startup")
        raw,h=self.historic();a.run(raw,h)
        r=store.get("mediator-runtime.json")
        self.assertEqual(r["primaryFailure"]["code"],"MAIN_EXIT_BEFORE_PROBE")
        self.assertEqual(r["state"]["ExitCode"],1)
        self.assertIn("ERR_MODULE_NOT_FOUND",r["logs"]["stderr"])
        self.assertNotIn("private_token_must_not_escape",json.dumps(r))
        self.assertFalse(any(x[1]=="exec" for x in f.calls))
        self.assertTrue(f.before_cleanup[0]["primaryFailure"])
    def test_05_exec_137_is_not_oom_and_notfound_cleanup_preserves_first_failure(self):
        a,f,store=self.engine(fail_role="mediator",mode="notfound")
        raw,h=self.historic();a.run(raw,h);r=store.get("mediator-runtime.json")
        self.assertEqual(r["primaryFailure"]["detail"]["exitCode"],137)
        self.assertEqual(r["state"]["ExitCode"],1);self.assertEqual(r["oomEvidence"],"DOCKER_STATE_FALSE")
        self.assertEqual(r["cleanup"]["status"],"UNKNOWN")
        self.assertEqual(len([x for x in f.calls if x[1]=="rm"]),1)
        self.assertEqual(len([x for x in f.calls if x[1]=="stop"]),0)
    def test_06_oom_requires_true_docker_field(self):
        self.assertEqual(s.classify_oom({"ExitCode":137}),"UNKNOWN")
        self.assertEqual(s.classify_oom({"ExitCode":137,"OOMKilled":False}),"DOCKER_STATE_FALSE")
        a,f,store=self.engine(fail_role="mediator",mode="oom");raw,h=self.historic();a.run(raw,h)
        self.assertEqual(store.get("mediator-runtime.json")["oomEvidence"],"DOCKER_STATE_TRUE")
    def test_07_ambiguous_cleanup_stops_without_second_stop_or_delete(self):
        a,f,store=self.engine(fail_role="mediator",mode="cleanup");raw,h=self.historic();a.run(raw,h)
        r=store.get("mediator-runtime.json")
        self.assertEqual(r["primaryFailure"]["detail"]["exitCode"],137)
        self.assertEqual(r["cleanup"]["status"],"UNKNOWN")
        self.assertEqual(len([x for x in f.calls if x[1]=="stop"]),1)
        self.assertFalse(any(x[1]=="rm" for x in f.calls))
        self.assertEqual(len([x for x in f.calls if x[1]=="run"]),1)
    def test_08_one_explicit_esm_probe_network_none_no_rm_or_ports(self):
        a,f,store=self.engine();raw,h=self.historic();a.run(raw,h)
        for args in [x for x in f.calls if x[1]=="run"]:
            self.assertNotIn("--rm",args);self.assertNotIn("-p",args);self.assertNotIn("--publish",args)
            self.assertEqual(args[args.index("--network")+1],"none")
            self.assertEqual(args[args.index("--pull=never")],"--pull=never")
            self.assertIn("OLDX_H2AH_ENABLED=false",args)
        self.assertEqual(len([x for x in f.calls if x[1]=="exec"]),4)
        for args in [x for x in f.calls if x[1]=="exec"]:self.assertIn("--input-type=module",args)
        self.assertIn("127.0.0.1",m.PROBE);self.assertNotIn("metadata.google",m.PROBE)
    def test_09_resume_only_unattempted_stages_never_rechecks_completed_roles_or_scans(self):
        a,f,store=self.engine();raw,h=self.historic()
        private(store.path/"mediator-historic-grype.json",raw)
        a.save_stage("mediator","scan",{**h,"rawFile":"mediator-historic-grype.json"})
        a.runtime("mediator",IDS["mediator"]);a.scan("gateway",IDS["gateway"])
        store.put("summary.json",{"scope":m.SCOPE,"planDigest":m.plan_digest(),"outcome":"INTERRUPTED_BETWEEN_STAGES"})
        plan=m.inspect_resume(store.path,self.global_dir)
        self.assertFalse(plan["blocked"]);self.assertNotIn({"role":"gateway","stage":"scan"},plan["unattemptedOnly"])
        b,g,new=self.engine();out=b.run(raw,h)
        self.assertEqual(out["outcome"],"COMPLETE_OFF_EVIDENCE_SECURITY_REVIEW_REQUIRED")
        self.assertEqual([x[1] for x in g.calls if x[0]=="grype"],["docker:"+IDS["backend"],"docker:"+IDS["reader"]])
        self.assertFalse(any(m.REFS["mediator"] in x for x in g.calls))
    def test_10_unknown_digest_sa_and_report_binding_refuse(self):
        frozen=(ROOT/"deployment/four-role/h2aj-four-immutable-images-pinned-proposal.json").read_bytes()
        self.assertEqual(m.proposal_check(frozen)["roles"]["reader"]["serviceAccountUid"],m.PINS["reader"][3])
        for key,value in (("image","UNKNOWN"),("serviceAccountUid","wrong")):
            changed=json.loads(frozen);changed["roles"]["reader"][key]=value
            with self.assertRaises(s.Stop):m.proposal_check(json.dumps(changed).encode())
        raw,h=self.historic()
        changed=json.loads(raw);changed["source"]["target"]["imageID"]="sha256:"+"0"*64
        with self.assertRaises(s.Stop):s.scan_report(json.dumps(changed).encode(),m.REFS["mediator"],image_id=IDS["mediator"],historical=True)
        with self.assertRaises(s.Stop):s.scan_report(b"[]",m.REFS["mediator"])
    def test_11_old_markers_untouched_and_historical_evidence_validated(self):
        old_a=self.root/"h2aj";old_k=self.root/"h2ak";old_scan=self.root/"mediator-grype.json"
        a="RESULT=PASS_FOUR_NEW_PRIVATE_OFF_IMAGES\n"+"".join("ROLE="+r+" REGISTRY_INDEX=sha256:"+"e"*64+" AMD64_CHILD=sha256:"+p[1]+"\n" for r,p in m.PINS.items())
        k="ROLE=mediator ABOUT_TO_CHECK\nRESULT=STOP_PARTIAL_LOCAL_READ_ONLY_ACCEPTANCE\n"
        private(old_a,a.encode());private(old_k,k.encode());private(old_scan,report("mediator",True))
        before=[x.read_bytes() for x in (old_a,old_k,old_scan)]
        with patch.object(m,"HISTORIC_RAW_SHA256",s.sha256(before[2])):
            m.prerequisites(self.root,old_a,old_k,old_scan)
        self.assertEqual(before,[x.read_bytes() for x in (old_a,old_k,old_scan)])
        changed=json.loads(before[2]);changed["matches"].pop()
        private(old_scan,json.dumps(changed).encode())
        with patch.object(m,"HISTORIC_RAW_SHA256",s.sha256(before[2])):
            with self.assertRaisesRegex(s.Stop,"CHECKSUM_DRIFT_NO_RESCAN"):m.prerequisites(self.root,old_a,old_k,old_scan)
        with self.assertRaisesRegex(s.Stop,"COUNTS_MISMATCH"):s.scan_report(json.dumps(changed).encode(),m.REFS["mediator"],historical=True)
    def test_12_completed_scan_missing_or_changed_is_blocker_not_rescan(self):
        a,f,store=self.engine();a.scan("gateway",IDS["gateway"])
        private(store.path/"gateway-grype.json",b"{}");f.calls.clear()
        with self.assertRaisesRegex(s.Stop,"CHANGED_NO_RESCAN"):a.scan("gateway",IDS["gateway"])
        self.assertFalse(f.calls)
    def test_13_sanitizer_preserves_app_import_error_not_credentials_or_signed_config(self):
        text="ERR_MODULE_NOT_FOUND /app/scripts/missing.mjs\nAuthorization: Bearer opaque-secret\n"+(
            "-----BEGIN PRIVATE KEY-----\nPRIVATEBYTES\n-----END PRIVATE KEY-----\n")+'{"Env":["PASSWORD=keep-private"]}\n'+(
            "signedPayload="+"x"*300+"\n/root/private/credential.json")
        output=s.sanitized(text)
        self.assertIn("/app/scripts/missing.mjs",output)
        for value in ("opaque-secret","PRIVATEBYTES","keep-private","x"*100,"/root/private"):self.assertNotIn(value,output)
    def test_14_bounded_command_timeout_preserves_exact_code_and_partial_stderr_without_real_process(self):
        a,f,store=self.engine();killed=[]
        class Process:
            def __init__(self,*args,**kwargs):
                self.stdout=io.BytesIO(b"partial stdout");self.stderr=io.BytesIO(b"FIRST ERROR\nAuthorization: Bearer hidden-token")
                self.stdin=None;self.returncode=None
            def poll(self):return self.returncode
            def kill(self):killed.append(True);self.returncode=-9
            def wait(self,timeout=None):return self.returncode
        commands=s.Commands(a.session,store,{})
        with patch.object(s.subprocess,"Popen",Process):
            result=commands.call(["docker","exec","test"],timeout=0)
        self.assertEqual(result.code,-9);self.assertTrue(result.timed_out);self.assertEqual(killed,[True])
        saved=store.get("command-0001.json")
        self.assertIn("FIRST ERROR",saved["stderr"]);self.assertNotIn("hidden-token",json.dumps(saved))
    def test_15_unknown_container_ownership_never_stopped_or_removed(self):
        a,f,store=self.engine();original=f.call
        def call(args,**kw):
            result=original(args,**kw)
            if args[:2]==["docker","inspect"] and result.code==0:
                state=json.loads(result.stdout);state[0]["Config"]["Labels"]={}
                return s.Result(0,json.dumps(state))
            return result
        f.call=call;raw,h=self.historic();a.run(raw,h)
        self.assertFalse(any(x[1] in ("stop","rm") for x in f.calls))
        self.assertEqual(store.get("mediator-runtime.json")["cleanup"]["status"],"UNKNOWN")
    def test_16_primary_receipt_failure_retains_container_instead_of_destroying_evidence(self):
        a,f,store=self.engine(fail_role="mediator",mode="exec");original=store.put
        def put(name,data):
            if name=="mediator-runtime.json" and data.get("primaryFailure"):raise OSError("simulated full evidence disk")
            return original(name,data)
        with patch.object(store,"put",side_effect=put):
            raw,h=self.historic();out=a.run(raw,h)
        self.assertFalse(any(x[1] in ("stop","rm") for x in f.calls))
        self.assertEqual(out["failure"]["detail"]["primaryFailure"]["detail"]["exitCode"],137)
    def test_17_missing_or_truncated_logs_retain_container_and_first_error(self):
        for logs_result in (s.Result(1,stderr="logs transport unknown"),s.Result(0,stdout="partial",truncated=True)):
            a,f,store=self.engine(fail_role="mediator",mode="exec");original=f.call
            def call(args,**kw):
                if args[:2]==["docker","logs"]:
                    f.calls.append(args);return logs_result
                return original(args,**kw)
            f.call=call;raw,h=self.historic();a.run(raw,h)
            receipt=store.get("mediator-runtime.json")
            self.assertEqual(receipt["primaryFailure"]["detail"]["exitCode"],137)
            self.assertEqual(receipt["cleanup"]["reason"],"DIAGNOSTICS_INCOMPLETE_CONTAINER_RETAINED")
            self.assertFalse(any(x[1] in ("stop","rm") for x in f.calls))
            # Separate isolated test state, not a production ledger reset.
            self.global_dir=self.root/("global"+str(self.counter));self.global_dir.mkdir(mode=0o700)
    def test_18_historical_import_is_durable_before_any_command(self):
        a,f,store=self.engine();raw,h=self.historic();a.import_historic(raw,h)
        self.assertFalse(f.calls)
        self.assertEqual(store.get("mediator-scan.json")["rawSha256"],s.sha256(raw))
        self.assertEqual(json.loads(s.read_private(a.claim_path("mediator","scan")))["status"],"COMPLETE")


    def test_19_actual_grype_nested_db_schema_and_explicit_child_binding(self):
        value=json.loads(report("mediator",True))
        value["source"]["target"]["manifestDigest"]="sha256:"+"e"*64
        value["descriptor"]={"version":"0.122.1","configuration":{"secret":"NEVER_COPY"},
            "db":{"providers":[],"status":{"built":"2026-11-28T00:00:00Z","schemaVersion":"6.1.3",
                "valid":True,"path":"/root/PRIVATE_DB","from":"PRIVATE_SOURCE"}}}
        receipt=s.scan_report(json.dumps(value).encode(),m.REFS["mediator"],historical=True)
        self.assertEqual(receipt["matches"],57)
        self.assertEqual(receipt["database"],{"built":"2026-11-28T00:00:00Z","schemaVersion":"6.1.3","valid":True})
        self.assertNotIn("PRIVATE",json.dumps(receipt))
        value["source"]["type"]="directory"
        with self.assertRaises(s.Stop):s.scan_report(json.dumps(value).encode(),m.REFS["mediator"],historical=True)
if __name__=="__main__":unittest.main()
