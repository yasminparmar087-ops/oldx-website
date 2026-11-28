"""H2AO pure OCI identities. No Docker/network/filesystem activity at import."""
from __future__ import annotations
import base64,hashlib,json,re
from step05_h2am_acceptance_support import Stop,digest,scan_report

TYPES={"application/vnd.oci.image.manifest.v1+json":"application/vnd.oci.image.config.v1+json",
 "application/vnd.docker.distribution.manifest.v2+json":"application/vnd.docker.container.image.v1+json"}
def need(ok,code):
    if not ok:raise Stop(code)
def hashed(raw):return "sha256:"+hashlib.sha256(raw).hexdigest()
def object_json(raw):
    def pairs(items):
        obj={}
        for k,v in items:
            if k in obj:raise Stop("DUPLICATE_JSON_KEY")
            obj[k]=v
        return obj
    try:
        x=json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in ()).throw(Stop("NONFINITE_JSON")))
    except (ValueError,UnicodeError,TypeError):raise Stop("INVALID_IDENTITY_JSON") from None
    need(isinstance(x,dict),"IDENTITY_OBJECT_REQUIRED");return x
def manifest_config(raw,ref):
    need(isinstance(raw,bytes) and 0<len(raw)<=524288,"CHILD_MANIFEST_BYTES_MISSING")
    need(hashed(raw)==ref.rsplit("@",1)[-1],"PINNED_CHILD_MANIFEST_HASH_MISMATCH")
    m=object_json(raw);typ=m.get("mediaType")
    need(m.get("schemaVersion")==2 and typ in TYPES and "manifests" not in m and
         not m.get("artifactType") and not m.get("subject"),"RUNNABLE_CHILD_MANIFEST_REQUIRED_NOT_INDEX")
    c=m.get("config");layers=m.get("layers")
    need(isinstance(c,dict) and c.get("mediaType")==TYPES[typ] and digest(c.get("digest")) and
         type(c.get("size")) is int and 0<c["size"]<=1048576,"CONFIG_DESCRIPTOR_INVALID")
    need(isinstance(layers,list) and 0<len(layers)<=128,"IMAGE_LAYERS_REQUIRED")
    for layer in layers:
        need(isinstance(layer,dict) and digest(layer.get("digest")) and type(layer.get("size")) is int and
             layer["size"]>=0 and not layer.get("urls") and
             layer.get("mediaType") in ("application/vnd.oci.image.layer.v1.tar+gzip",
              "application/vnd.oci.image.layer.v1.tar+zstd","application/vnd.oci.image.layer.v1.tar",
              "application/vnd.docker.image.rootfs.diff.tar.gzip"),"LOCAL_IMAGE_LAYER_DESCRIPTOR_INVALID")
    return m
def config_bytes(report):
    source=report.get("source");need(isinstance(source,dict),"GRYPE_IMAGE_SOURCE_REQUIRED")
    target=source.get("target");need(isinstance(target,dict),"GRYPE_IMAGE_TARGET_REQUIRED")
    raw=target.get("config")
    need(isinstance(raw,str) and 0<len(raw)<=1398104,"GRYPE_RAW_CONFIG_BYTES_REQUIRED")
    # Syft/Grype Go []byte fields use base64; older fixtures may carry literal JSON.
    if raw.lstrip().startswith("{"):data=raw.encode("utf8")
    else:
        try:data=base64.b64decode(raw,validate=True)
        except (ValueError,UnicodeError):raise Stop("GRYPE_CONFIG_ENCODING_INVALID") from None
    need(0<len(data)<=1048576,"GRYPE_CONFIG_BYTES_LIMIT")
    return data
def config_contract(raw,role):
    c=object_json(raw);conf=c.get("config",{});root=c.get("rootfs",{})
    need(isinstance(conf,dict) and isinstance(root,dict),"CONFIG_OBJECTS_REQUIRED")
    need(c.get("os")=="linux" and c.get("architecture")=="amd64" and
         c.get("variant") in (None,""),"CONFIG_PLATFORM_DRIFT")
    need(isinstance(conf,dict) and conf.get("User")=="65532:65532" and conf.get("WorkingDir")=="/app" and
         conf.get("Entrypoint")==["/nodejs/bin/node"] and
         conf.get("Cmd")==["functions/staging-marketplace/four-role/"+role+".mjs"] and
         not conf.get("Volumes"),"CONFIG_ROLE_NONROOT_ENTRYPOINT_DRIFT")
    env=conf.get("Env",[])
    need(isinstance(env,list) and all(isinstance(v,str) for v in env) and
         not any(v.startswith("OLDX_") and v.endswith("=true") for v in env),"CONFIG_ENABLED_OR_ENV_INVALID")
    diff=root.get("diff_ids")
    need(root.get("type")=="layers" and isinstance(diff,list) and 0<len(diff)<=128 and
         all(digest(v) for v in diff),"CONFIG_ROOTFS_DIFFIDS_REQUIRED")
    return c
def local_contract(row,role,ref):
    need(isinstance(row,dict) and digest(row.get("Id")) and isinstance(row.get("RepoDigests"),list) and
         ref in row["RepoDigests"],"LOCAL_PIN_NOT_PRESENT")
    c=row.get("Config",{})
    need(row.get("Os")=="linux" and row.get("Architecture")=="amd64" and
         isinstance(c,dict) and c.get("User")=="65532:65532" and c.get("WorkingDir")=="/app" and
         c.get("Entrypoint")==["/nodejs/bin/node"] and
         c.get("Cmd")==["functions/staging-marketplace/four-role/"+role+".mjs"] and not c.get("Volumes"),
         "LOCAL_PLATFORM_NONROOT_ROLE_DRIFT")
    env=c.get("Env",[])
    need(isinstance(env,list) and all(isinstance(v,str) for v in env) and
         not any(v.startswith("OLDX_") and v.endswith("=true") for v in env),"LOCAL_ENABLED_OR_ENV_INVALID")
    return row
def bind(raw_manifest,raw_report,row,role,ref,*,historical=False,raw_report_sha=None):
    # The approved child hash is the trust anchor; registry headers/labels are not proof.
    if historical:need(hashlib.sha256(raw_report).hexdigest()==raw_report_sha,"HISTORICAL_SCAN_SHA_MISMATCH_NO_RESCAN")
    report=object_json(raw_report);source=report.get("source")
    need(isinstance(source,dict) and source.get("type")=="image","GRYPE_IMAGE_SOURCE_REQUIRED")
    target=source.get("target");need(isinstance(target,dict),"GRYPE_IMAGE_TARGET_REQUIRED")
    need(target.get("userInput") in (ref,"docker:"+ref),"GRYPE_EXACT_ROLE_REF_REQUIRED")
    m=manifest_config(raw_manifest,ref);raw_config=config_bytes(report)
    need(hashed(raw_config)==m["config"]["digest"] and len(raw_config)==m["config"]["size"],
         "MANIFEST_CONFIG_BYTES_MISMATCH")
    config=config_contract(raw_config,role);local_contract(row,role,ref)
    need(target.get("imageID")==m["config"]["digest"],"GRYPE_CONFIG_ID_UNBOUND")
    need(len(m["layers"])==len(config["rootfs"]["diff_ids"]),"LAYER_CONFIG_COUNT_DRIFT")
    need(isinstance(row.get("RootFS"),dict) and row["RootFS"].get("Type")=="layers" and
         row["RootFS"].get("Layers")==config["rootfs"]["diff_ids"],"LOCAL_ROOTFS_CONFIG_DRIFT")
    for key in ("User","WorkingDir","Entrypoint","Cmd","Env"):
        need(row["Config"].get(key)==config["config"].get(key),"LOCAL_CONFIG_FIELD_DRIFT")
    child=ref.rsplit("@",1)[-1];cfg=m["config"]["digest"];engine=row["Id"]
    need(engine in (child,cfg),"DOCKER_ID_NEITHER_VERIFIED_MANIFEST_NOR_CONFIG")
    receipt=scan_report(raw_report,ref,image_id=cfg,historical=historical)
    # Deliberately distinct: do NOT normalize/change raw Grype or Docker IDs.
    return {**receipt,"scope":"oldx.h2ao.identity.v1","role":role,"approvedChildManifestDigest":child,
        "canonicalConfigDigest":cfg,"dockerImageId":engine,
        "dockerIdKind":"CHILD_MANIFEST" if engine==child else "CONFIG",
        "grypeImageId":target["imageID"],"grypeRecordedManifestDigest":target.get("manifestDigest"),
        "rawChildSha256":hashlib.sha256(raw_manifest).hexdigest(),"rawConfigSha256":cfg[7:],
        "identity":"CRYPTOGRAPHIC_CHILD_CONFIG_SCAN_LOCAL_BINDING","securityDisposition":"HOLD_NOT_ACCEPTED"}
