"""Only NEW H2AO offline cases. No real Docker, scanner, registry or Cloud calls."""
import copy,io,json,os,sys,tempfile,unittest,urllib.error
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"scripts"))
import step05_h2ao_selective_continuation_once_20261129 as m
import step05_h2ao_oci_identity as i
from step05_h2am_acceptance_support import Result,Session,Store,Stop,sha256
def private(p,data):
    p.write_bytes(data);p.chmod(0o600)
def fixture(role,historical=False,kind="manifest"):
    raw_config=json.dumps({"os":"linux","architecture":"amd64","config":{"User":"65532:65532",
        "WorkingDir":"/app","Entrypoint":["/nodejs/bin/node"],
        "Cmd":["functions/staging-marketplace/four-role/"+role+".mjs"],"Env":["NODE_ENV=production"]},
        "rootfs":{"type":"layers","diff_ids":["sha256:"+"d"*64]}},separators=(",",":")).encode()
    cfg=i.hashed(raw_config)
    raw_manifest=json.dumps({"schemaVersion":2,"mediaType":"application/vnd.oci.image.manifest.v1+json",
        "config":{"mediaType":"application/vnd.oci.image.config.v1+json","digest":cfg,"size":len(raw_config)},
        "layers":[{"mediaType":"application/vnd.oci.image.layer.v1.tar+gzip","digest":"sha256:"+"e"*64,"size":80}]},
        separators=(",",":")).encode()
    child=i.hashed(raw_manifest);ref=m.old.PREFIX+m.PINS[role][0]+"@"+child
    config=json.loads(raw_config)
    local={"Id":child if kind=="manifest" else cfg,"RepoDigests":[ref],"Os":"linux","Architecture":"amd64",
        "Config":config["config"],"RootFS":{"Type":"layers","Layers":config["rootfs"]["diff_ids"]}}
    severities=["High"]*18+["Medium"]*20+["Low"]*6+["Negligible"]*11+["Unknown"]*2 if historical else ["High","Medium"]
    report=json.dumps({"source":{"type":"image","target":{"imageID":cfg,"userInput":ref,"config":raw_config.decode(),
        "manifestDigest":"sha256:"+"f"*64,"manifest":"TRANSFORMED_MANIFEST_NOT_THE_APPROVED_BYTES"}},
        "descriptor":{"version":"TEST_ONLY","db":{"status":{"built":"2026-11-29T00:00:00Z","valid":True}}},
        "matches":[{"vulnerability":{"id":"TEST-"+str(n),"severity":v}} for n,v in enumerate(severities)]}).encode()
    return {"manifest":raw_manifest,"report":report,"row":local,"ref":ref,"config":cfg,"child":child}
class Fake:
    def __init__(self,session,store,data,fail_role=None):
        self.session=session;self.store=store;self.data=data;self.calls=[];self.states={};self.fail_role=fail_role
    def call(self,args,timeout=30,input_bytes=None,stdout_file=None):
        self.session.require();self.calls.append(args)
        if args[0]=="grype":
            role=next(r for r,v in self.data.items() if args[1]=="docker:"+v["ref"])
            if role=="mediator":raise AssertionError("MEDIATOR_SCAN_FORBIDDEN")
            private(Path(stdout_file),self.data[role]["report"]);return Result(0)
        op=args[1]
        if op=="run":
            role=next(r for r,v in self.data.items() if args[-1]==v["ref"]);name=args[args.index("--name")+1]
            cid=str(list(self.data).index(role)+1)*64
            self.states[name]={"Id":cid,"Name":"/"+name,"Image":self.data[role]["config"],
                "Config":{"Labels":{"oldx.h2ao.attempt":self.session.attempt,"oldx.h2ao.role":role}},
                "HostConfig":{"NetworkMode":"none","ReadonlyRootfs":True,"PortBindings":{},"Binds":None,
                    "Memory":768*1024*1024,"NanoCpus":1000000000,"PidsLimit":128,
                    "CapDrop":["ALL"],"SecurityOpt":["no-new-privileges"]},"Mounts":[],
                "State":{"Running":True,"ExitCode":0,"OOMKilled":False,"Pid":99,"Error":""}}
            return Result(0,cid)
        if op=="inspect":
            state=self.states.get(args[2])
            return Result(0,json.dumps([state])) if state else Result(1,stderr="No such container")
        if op=="exec":
            state=next(x for x in self.states.values() if x["Id"]==args[3]);role=state["Config"]["Labels"]["oldx.h2ao.role"]
            if role==self.fail_role:
                state["State"].update(Running=False,ExitCode=1)
                return Result(137,stderr="ORIGINAL_EXEC_FAILURE")
            return Result(0,json.dumps({"health":200,"product":503,"state":"OFF","role":role,"uid":65532,"nodeMajor":24,"error":None}))
        if op=="logs":return Result(0,stderr="RETAINED_ORIGINAL_MAIN_ERROR")
        if op=="stop":
            self.states[args[-1]]["State"].update(Running=False,ExitCode=0);return Result(0,args[-1])
        if op=="rm":
            if self.fail_role and self.states[args[-1]]["Config"]["Labels"]["oldx.h2ao.role"]==self.fail_role:
                return Result(1,stderr="No such container")
            self.states.pop(args[-1]);return Result(0,args[-1])
        raise AssertionError("UNAPPROVED_CALL "+str(args))
class H2AO(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.data={r:fixture(r,r=="mediator") for r in m.PINS}
        self.refs={r:v["ref"] for r,v in self.data.items()}
        self.patch=patch.object(m,"REFS",self.refs);self.patch.start()
    def tearDown(self):self.patch.stop();self.tmp.cleanup()
    def binding(self,role="mediator",**kw):
        f=self.data[role]
        return i.bind(f["manifest"],f["report"],f["row"],role,f["ref"],
            historical=role=="mediator",raw_report_sha=sha256(f["report"]),**kw)
    def engine(self,fail_role=None):
        evidence=self.root/"evidence";evidence.mkdir(mode=0o700)
        global_dir=self.root/"global";global_dir.mkdir(mode=0o700)
        store=Store(evidence);session=Session.consume(self.root/"ao-marker","a"*32,"TEST")
        fake=Fake(session,store,self.data,fail_role)
        a=m.Acceptance(store,session,fake,global_dir,{r:v["row"] for r,v in self.data.items()},self.binding(),
            {r:v["manifest"] for r,v in self.data.items()})
        return a,fake,store
    def test_01_containerd_manifest_id_and_grype_config_id_bound_without_conflation(self):
        r=self.binding()
        self.assertEqual(r["dockerIdKind"],"CHILD_MANIFEST")
        self.assertNotEqual(r["dockerImageId"],r["grypeImageId"])
        self.assertEqual(r["canonicalConfigDigest"],r["grypeImageId"])
        self.assertEqual(r["matches"],57);self.assertEqual(r["severity"]["High"],18)
        self.assertEqual(r["securityDisposition"],"HOLD_NOT_ACCEPTED")
    def test_02_legacy_config_id_uses_same_cryptographic_chain(self):
        self.data["mediator"]["row"]["Id"]=self.data["mediator"]["config"]
        self.assertEqual(self.binding()["dockerIdKind"],"CONFIG")
    def test_03_wrong_child_bytes_or_index_and_duplicate_json_fail_closed(self):
        f=self.data["mediator"]
        with self.assertRaisesRegex(Stop,"HASH_MISMATCH"):i.manifest_config(f["manifest"]+b" ",f["ref"])
        raw=b'{"schemaVersion":2,"manifests":[]}'
        with self.assertRaisesRegex(Stop,"NOT_INDEX"):i.manifest_config(raw,"x@"+i.hashed(raw))
        with self.assertRaisesRegex(Stop,"DUPLICATE"):i.object_json(b'{"x":1,"x":2}')
    def test_04_wrong_config_hash_size_and_missing_raw_config_fail(self):
        f=self.data["mediator"];v=json.loads(f["report"])
        for change in ("wrong","missing"):
            t=copy.deepcopy(v)
            if change=="wrong":t["source"]["target"]["config"]+=" "
            else:t["source"]["target"].pop("config")
            with self.assertRaises(Stop):i.bind(f["manifest"],json.dumps(t).encode(),f["row"],"mediator",f["ref"])
    def test_05_wrong_historical_scan_hash_and_grype_exact_ref_fail(self):
        f=self.data["mediator"]
        with self.assertRaisesRegex(Stop,"SCAN_SHA"):i.bind(f["manifest"],f["report"],f["row"],"mediator",f["ref"],
            historical=True,raw_report_sha="0"*64)
        t=json.loads(f["report"]);t["source"]["target"]["userInput"]=self.refs["gateway"]
        with self.assertRaisesRegex(Stop,"EXACT_ROLE_REF"):i.bind(f["manifest"],json.dumps(t).encode(),f["row"],"mediator",f["ref"])
    def test_06_wrong_engine_id_platform_nonroot_and_cross_role_reject(self):
        f=self.data["mediator"]
        for field,value in (("Id","sha256:"+"0"*64),("Architecture","arm64")):
            row=copy.deepcopy(f["row"]);row[field]=value
            with self.assertRaises(Stop):i.bind(f["manifest"],f["report"],row,"mediator",f["ref"])
        row=copy.deepcopy(f["row"]);row["Config"]["User"]="0:0"
        with self.assertRaises(Stop):i.bind(f["manifest"],f["report"],row,"mediator",f["ref"])
        with self.assertRaises(Stop):i.bind(f["manifest"],f["report"],f["row"],"gateway",f["ref"])
    def test_07_rootfs_diffids_and_config_runtime_env_must_match(self):
        f=self.data["mediator"]
        for key,value in (("RootFS",{"Type":"layers","Layers":["sha256:"+"0"*64]}),
            ("Config",{**f["row"]["Config"],"Env":["OLDX_H2AH_ENABLED=true"]})):
            row=copy.deepcopy(f["row"]);row[key]=value
            with self.assertRaises(Stop):i.bind(f["manifest"],f["report"],row,"mediator",f["ref"])
    def test_08_missing_oci_proof_never_accepts_distinct_labels(self):
        f=self.data["mediator"]
        with self.assertRaisesRegex(Stop,"BYTES_MISSING"):i.bind(b"",f["report"],f["row"],"mediator",f["ref"])
        row=copy.deepcopy(f["row"]);row["Id"]="sha256:"+"f"*64
        with self.assertRaisesRegex(Stop,"NEITHER"):i.bind(f["manifest"],f["report"],row,"mediator",f["ref"])
    def test_09_default_off_never_calls_old_cli_or_any_preflight(self):
        with patch.object(m,"history",side_effect=AssertionError("NO_HISTORY")),patch.object(m.old,"cli",side_effect=AssertionError("NO_OLD_RUN")),patch.object(m.Commands,"call",side_effect=AssertionError("NO_DOCKER")):
            self.assertEqual(m.cli([]),0)
            self.assertEqual(m.cli(["--execute-h2ao-once"]),0)
    def test_10_mediator_import_then_only_three_exact_ref_scans_and_four_runtime(self):
        a,f,s=self.engine();out=a.run(self.data["mediator"]["report"],self.binding())
        self.assertEqual(out["outcome"],"COMPLETE_OFF_EVIDENCE_SECURITY_REVIEW_REQUIRED")
        scans=[x[1] for x in f.calls if x[0]=="grype"]
        self.assertEqual(scans,["docker:"+self.refs[r] for r in ("gateway","backend","reader")])
        runs=[x for x in f.calls if x[:2]==["docker","run"]]
        self.assertEqual(len(runs),4)
        self.assertTrue(all("--rm" not in x and "--pull=never" in x and x[-1] in self.refs.values() for x in runs))
        self.assertEqual(s.get("mediator-scan.json")["rawSha256"],sha256(self.data["mediator"]["report"]))
    def test_11_mediator_runtime_failure_stops_before_all_new_scans_and_keeps_first_error(self):
        a,f,s=self.engine("mediator");out=a.run(self.data["mediator"]["report"],self.binding())
        self.assertEqual(out["outcome"],"STOP_PARTIAL_NO_AUTOMATIC_RETRY")
        self.assertFalse(any(x[0]=="grype" for x in f.calls))
        r=s.get("mediator-runtime.json")
        self.assertEqual(r["primaryFailure"]["detail"]["exitCode"],137)
        self.assertEqual(r["oomEvidence"],"DOCKER_STATE_FALSE")
        self.assertEqual(r["state"]["ExitCode"],1)
        self.assertIn("ORIGINAL_MAIN",r["logs"]["stderr"])
        self.assertEqual(r["cleanup"]["status"],"UNKNOWN")
    def test_12_completed_new_scan_is_durable_before_failed_runtime_no_replay(self):
        a,f,s=self.engine("gateway");a.run(self.data["mediator"]["report"],self.binding())
        self.assertEqual(s.get("gateway-scan.json")["status"],"COMPLETE")
        before=len(f.calls)
        with self.assertRaises(FileExistsError):a.scan("gateway")
        self.assertEqual(before,len(f.calls))
    def test_13_missing_other_child_proof_stops_before_spending_scan(self):
        a,f,s=self.engine();a.manifests.pop("gateway")
        with self.assertRaisesRegex(Stop,"BEFORE_NEW_SCAN"):a.scan("gateway")
        self.assertFalse(f.calls);self.assertFalse(a.claim_path("gateway","scan").exists())
    def test_14_container_inspect_image_may_be_verified_config_or_child_only(self):
        b=self.binding();name="oldx-h2ao-mediator-"+"a"*16
        for image in (b["canonicalConfigDigest"],b["approvedChildManifestDigest"]):
            x={"Name":"/"+name,"Image":image,"Config":{"Labels":{"oldx.h2ao.attempt":"a"*32,"oldx.h2ao.role":"mediator"}}}
            self.assertEqual(m.state_info(Result(0,json.dumps([x])),name,b,"a"*32,"mediator")["Image"],image)
        x["Image"]=self.data["gateway"]["config"]
        with self.assertRaisesRegex(Stop,"NO_CLEANUP"):m.state_info(Result(0,json.dumps([x])),name,b,"a"*32,"mediator")
    def prior_fixture(self):
        am=self.root/"am";am.mkdir(mode=0o700);glob=self.root/"amglobal";glob.mkdir(mode=0o700)
        raw=self.data["mediator"]["report"];h=self.binding();h["imageId"]=h["canonicalConfigDigest"]
        summary={"scope":m.old.SCOPE,"planDigest":m.old.plan_digest(),"outcome":"STOP_PARTIAL_NO_AUTOMATIC_RETRY",
            "failure":{"code":"MEDIATOR_HISTORIC_LOCAL_CONFIG_MISMATCH"},"roles":{"mediator":{"stage":"IMAGE_BINDING"}}}
        private(am/"summary.json",json.dumps(summary).encode());marker=self.root/"ammarker"
        private(marker,json.dumps({"started":True,"scope":m.old.plan_digest(),"attempt":"b"*32}).encode())
        receipt={**h,"scope":m.old.SCOPE,"role":"mediator","ref":self.refs["mediator"],"rawFile":"old.json",
            "evidence":str(am),"attempt":"b"*32}
        private(am/"mediator-scan.json",json.dumps(receipt).encode());private(am/"old.json",raw)
        private(glob/(m.PINS["mediator"][1]+"-scan.json"),json.dumps(receipt).encode())
        an=self.root/"an";private(an,("ATTEMPT_CONSUMED=TRUE\nSOURCE=8f5df51075d6cc42f0d32ad0c730b14611c03f87\nALL_FOUR_CHILDREN_VERIFIED\n"+
            "".join("ROLE="+r+" PULL_ATTEMPT_STARTED\nROLE="+r+" VERIFIED_IMAGE_ID="+self.data[r]["row"]["Id"]+"\n" for r in ("gateway","backend","reader"))).encode())
        report=self.root/"historic";private(report,raw);aj=self.root/"aj";ak=self.root/"ak";private(aj,b"old");private(ak,b"old")
        return am,glob,an,marker,report,aj,ak,raw,h
    def test_15_exact_prior_failure_consumed_markers_preserved_and_tamper_rejected(self):
        am,glob,an,mark,rep,aj,ak,raw,h=self.prior_fixture()
        with patch.multiple(m,AM_EVIDENCE=am,AM_GLOBAL=glob,AN_MARKER=an,AM_SUMMARY_SHA=sha256((am/"summary.json").read_bytes())),patch.multiple(m.old,MARKER=mark,HISTORIC=rep,H2AJ=aj,H2AK=ak,HISTORIC_RAW_SHA256=sha256(raw)),patch.object(m.old,"prerequisites",return_value=(raw,h)):
            before={p:p.read_bytes() for p in (an,mark,rep,aj,ak)}
            self.assertEqual(m.history()[0],raw)
            self.assertEqual(before,{p:p.read_bytes() for p in before})
            private(am/"summary.json",b"{}")
            with self.assertRaisesRegex(Stop,"SUMMARY_SHA_DRIFT"):m.history()
    def test_16_any_prior_runtime_or_other_scan_attempt_blocks_continuation(self):
        am,glob,an,mark,rep,aj,ak,raw,h=self.prior_fixture()
        with patch.multiple(m,AM_EVIDENCE=am,AM_GLOBAL=glob,AN_MARKER=an,AM_SUMMARY_SHA=sha256((am/"summary.json").read_bytes())),patch.multiple(m.old,MARKER=mark,HISTORIC=rep,H2AJ=aj,H2AK=ak,HISTORIC_RAW_SHA256=sha256(raw)),patch.object(m.old,"prerequisites",return_value=(raw,h)):
            private(am/"mediator-runtime.json",b"{}")
            with self.assertRaisesRegex(Stop,"ALREADY_ATTEMPTED"):m.history()
    def test_17_new_scan_wrong_config_keeps_raw_without_claiming_complete(self):
        a,f,s=self.engine();v=json.loads(self.data["gateway"]["report"]);v["source"]["target"]["imageID"]="sha256:"+"0"*64
        self.data["gateway"]["report"]=json.dumps(v).encode()
        with self.assertRaisesRegex(Stop,"CONFIG_ID_UNBOUND"):a.scan("gateway")
        self.assertEqual(s.get("gateway-scan.json")["status"],"CAPTURED_IDENTITY_PENDING")
        self.assertTrue((s.path/"gateway-grype.json").exists())
        self.assertEqual(len([x for x in f.calls if x[0]=="grype"]),1)
    def test_18_single_authenticated_manifest_get_mocked_and_marker_never_reset(self):
        f=self.data["mediator"];dest=self.root/"saved.json";mark=self.root/"getmarker"
        response=io.BytesIO(f["manifest"]);response.status=200
        response.headers={"Content-Type":"application/vnd.oci.image.manifest.v1+json","Docker-Content-Digest":f["child"]}
        class Opener:
            calls=0
            def open(self,request,timeout):
                self.calls+=1
                self_request=request
                return response
        opener=Opener();rd,wr=os.pipe();os.write(wr,b"TEST_ONLY_"+"x".encode()*80);os.close(wr)
        try:
            with patch("urllib.request.build_opener",return_value=opener):
                raw=m.fetch_one_mediator_manifest(rd,dest,mark)
            self.assertEqual(raw,f["manifest"]);self.assertEqual(opener.calls,1)
            with self.assertRaisesRegex(Stop,"ALREADY_CONSUMED"):m.fetch_one_mediator_manifest(rd,dest,mark)
            self.assertNotIn(b"TEST_ONLY",mark.read_bytes())
        finally:os.close(rd)
    def test_19_http_401_stops_one_request_no_saved_token_or_retry(self):
        mark=self.root/"getmarker";dest=self.root/"raw"
        class Opener:
            calls=0
            def open(self,*args,**kwargs):
                self.calls+=1;raise urllib.error.HTTPError("https://TEST",401,"UNAUTHORIZED",{},None)
        opener=Opener();rd,wr=os.pipe();os.write(wr,b"TEST_ONLY_"+"x".encode()*80);os.close(wr)
        try:
            with patch("urllib.request.build_opener",return_value=opener),self.assertRaisesRegex(Stop,"AUTH_TLS_FAILURE"):
                m.fetch_one_mediator_manifest(rd,dest,mark)
            self.assertEqual(opener.calls,1);self.assertTrue(mark.exists());self.assertFalse(dest.exists())
        finally:os.close(rd)

    def test_20_consumed_h2ao_marker_stops_before_any_command(self):
        mark=self.root/"consumed";private(mark,b"consumed")
        with patch.multiple(m,MARKER=mark,PREFLIGHT_MARKER=self.root/"pref"),patch("platform.system",return_value="Linux"),patch("platform.release",return_value="microsoft"),patch.object(m,"history",side_effect=AssertionError("NO_OLD_REPLAY")),patch.object(m.Commands,"call",side_effect=AssertionError("NO_COMMAND")):
            with self.assertRaisesRegex(Stop,"ALREADY_CONSUMED"):
                m.cli(["--execute-h2ao-once","--owner-approved-selective-off-only"])
        self.assertEqual(mark.read_bytes(),b"consumed")
    def cli_preflight(self,missing_role=None,wrong_config=False):
        from types import SimpleNamespace
        elf=self.root/"fake-native";private(elf,bytes([127])+b"ELF_TEST_ONLY");elf.chmod(0o700)
        db=self.root/"db";db.mkdir(mode=0o700)
        directory=self.root/"manifests";directory.mkdir(mode=0o700)
        for role,f in self.data.items():
            if role!=missing_role:private(directory/(role+"-child-manifest.json"),f["manifest"])
        h=self.binding()
        if wrong_config:h["imageId"]="sha256:"+"0"*64
        marker=self.root/"runtime";pref=self.root/"preflight"
        with patch.multiple(m,ROOT=self.root,MARKER=marker,PREFLIGHT_MARKER=pref,GLOBAL=self.root/"ledger",GRYPE=elf,DB=db),patch("platform.system",return_value="Linux"),patch("platform.release",return_value="microsoft"),patch.object(m,"history",return_value=(self.data["mediator"]["report"],h,{})),patch.object(m,"owner_scope",return_value={"project":"oldx-staging"}),patch("shutil.which",return_value=str(elf)),patch("shutil.disk_usage",return_value=SimpleNamespace(free=8*1024**3)),patch.object(m.Commands,"call",side_effect=AssertionError("NO_EXTERNAL_COMMAND")):
            with self.assertRaises(Stop) as error:
                m.cli(["--execute-h2ao-once","--owner-approved-selective-off-only","--manifest-directory",str(directory)])
        self.assertFalse(marker.exists());self.assertFalse(pref.exists())
        return error.exception.code
    def test_21_missing_other_saved_manifest_blocks_before_any_marker_or_scan(self):
        self.assertIn("SAVED_GATEWAY",self.cli_preflight(missing_role="gateway"))
    def test_22_wrong_historical_config_blocks_before_runtime_or_docker_preflight(self):
        self.assertEqual(self.cli_preflight(wrong_config=True),"MEDIATOR_OCI_CONFIG_UNBOUND_BEFORE_RUNTIME_MARKER")
    def test_23_get_hash_mismatch_keeps_private_raw_and_failure_receipt_no_retry(self):
        dest=self.root/"bad-raw";mark=self.root/"getmarker"
        response=io.BytesIO(b'{"not":"the approved manifest"}');response.status=200
        response.headers={"Content-Type":"application/vnd.oci.image.manifest.v1+json"}
        class Opener:
            def open(self,*args,**kwargs):return response
        rd,wr=os.pipe();os.write(wr,b"TEST_ONLY_"+"x".encode()*80);os.close(wr)
        try:
            with patch("urllib.request.build_opener",return_value=Opener()),self.assertRaisesRegex(Stop,"HASH_MISMATCH"):
                m.fetch_one_mediator_manifest(rd,dest,mark)
            receipt=json.loads((self.root/"mediator-manifest-get-receipt.json").read_bytes())
            self.assertEqual(receipt["status"],"FAILED");self.assertEqual(receipt["httpStatus"],200)
            self.assertEqual(receipt["rawSha256"],sha256(dest.read_bytes()))
            self.assertNotIn("TEST_ONLY",json.dumps(receipt))
        finally:os.close(rd)

    def test_24_actual_grype_base64_config_bytes_match_manifest_descriptor(self):
        import base64
        f=self.data["mediator"];v=json.loads(f["report"])
        raw=v["source"]["target"]["config"].encode()
        v["source"]["target"]["config"]=base64.b64encode(raw).decode()
        encoded=json.dumps(v).encode()
        receipt=i.bind(f["manifest"],encoded,f["row"],"mediator",f["ref"],
            historical=True,raw_report_sha=sha256(encoded))
        self.assertEqual(receipt["canonicalConfigDigest"],f["config"])
        self.assertEqual(receipt["matches"],57)
        v["source"]["target"]["config"]="INVALID_BASE64!"
        with self.assertRaisesRegex(Stop,"ENCODING_INVALID"):
            i.bind(f["manifest"],json.dumps(v).encode(),f["row"],"mediator",f["ref"])

    def test_25_malformed_source_and_truncated_inspect_are_explicit_stops(self):
        f=self.data["mediator"]
        for source in (None,[],{"type":"image","target":None}):
            v=json.loads(f["report"]);v["source"]=source
            with self.assertRaises(Stop):i.bind(f["manifest"],json.dumps(v).encode(),f["row"],"mediator",f["ref"])
        with self.assertRaisesRegex(Stop,"COMMAND_FAILED"):
            m.state_info(Result(0,"[]",truncated=True),"unused",self.binding(),"a"*32,"mediator")

    def test_26_unbound_local_engine_id_stops_in_readonly_preflight_before_runtime_marker(self):
        from types import SimpleNamespace
        elf=self.root/"native";private(elf,bytes([127])+b"ELF_TEST");elf.chmod(0o700)
        db=self.root/"db";db.mkdir(mode=0o700)
        directory=self.root/"proofs";directory.mkdir(mode=0o700)
        for role,f in self.data.items():private(directory/(role+"-child-manifest.json"),f["manifest"])
        marker=self.root/"runtime";pref=self.root/"pref";calls=[]
        def command(_self,args,**kw):
            calls.append(args)
            if args[:2]==["docker","info"]:return Result(0,"linux")
            if args[:3]==["grype","db","status"]:return Result(0,'{"valid":true}')
            if args[:3]==["docker","image","inspect"]:
                role=next(r for r,v in self.data.items() if args[3]==v["ref"])
                row=copy.deepcopy(self.data[role]["row"])
                if role=="gateway":row["Id"]="sha256:"+"0"*64
                return Result(0,json.dumps([row]))
            raise AssertionError("RUNTIME_OR_SCAN_BEFORE_IDENTITY")
        with patch.multiple(m,ROOT=self.root,MARKER=marker,PREFLIGHT_MARKER=pref,GLOBAL=self.root/"ledger",GRYPE=elf,DB=db),patch("platform.system",return_value="Linux"),patch("platform.release",return_value="microsoft"),patch.object(m,"history",return_value=(self.data["mediator"]["report"],self.binding(),{})),patch.object(m,"owner_scope",return_value={"project":"oldx-staging"}),patch("shutil.which",return_value=str(elf)),patch("shutil.disk_usage",return_value=SimpleNamespace(free=8*1024**3)),patch.object(m.Commands,"call",new=command):
            self.assertEqual(m.cli(["--execute-h2ao-once","--owner-approved-selective-off-only","--manifest-directory",str(directory)]),2)
        self.assertTrue(pref.exists());self.assertFalse(marker.exists())
        summary=json.loads(next(self.root.glob("oldx-h2ao-selective-*/summary.json")).read_bytes())
        self.assertEqual(summary["failure"]["code"],"LOCAL_DOCKER_ID_UNBOUND_TO_VERIFIED_CHILD_CONFIG")
        self.assertFalse(any(x[:2]==["docker","run"] or x[:2]==["grype","docker:"] for x in calls))
if __name__=="__main__":unittest.main()
