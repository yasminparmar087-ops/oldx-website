// BAJUTO/OLDX Step05 — source-only, NO IAM SDK/network or changes.
// Build a non-executable proposed EXACT CryptoKey-level policy change for a
// dedicated metadata/public-key reader. Never give Gateway read or Reader sign.
// Google predefined KMS Viewer allows CryptoKeyVersion.get; PublicKeyViewer
// allows viewPublicKey. Both require narrowly scoped bindings on this Key.
export const C2_H2_READER_KEY = 'projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256';
export const C2_H2_READER_EMAIL = 'oldx-c2-kms-reader@oldx-staging.iam.gserviceaccount.com';
export const C2_H2_SIGNER_EMAIL = 'oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com';
export const C2_H2_READER_ROLES = Object.freeze(['roles/cloudkms.viewer', 'roles/cloudkms.publicKeyViewer']);
const KEY = C2_H2_READER_KEY;
const R = 'serviceAccount:' + C2_H2_READER_EMAIL;
const S = 'serviceAccount:' + C2_H2_SIGNER_EMAIL;
const ok = v => v !== null && typeof v === 'object' && !Array.isArray(v) && Object.getPrototypeOf(v) === Object.prototype &&
  Reflect.ownKeys(v).every(k => typeof k === 'string' && Object.hasOwn(Object.getOwnPropertyDescriptor(v,k),'value'));
const disabled = reason => Object.freeze({reviewReady:false,cloudWriteAuthorized:false,reason});
const UID = /^\d{1,32}$/;
const ETAG = /^[A-Za-z0-9+/=]{4,200}$/;
// A fresh, already-read getIamPolicy preimage must have been supplied to a
// privileged owner-only operator. Do not fetch, re-fetch or set policies here.
// For any unexpected other binding or conditional policy: fail closed; do NOT
// replace/remove someone else's IAM grant to make this work.
export function proposeC2H2DedicatedReaderKeyPolicy({enabled=false,key=KEY,
 readerEmail=C2_H2_READER_EMAIL,readerUid,readerDisabled,preimage}={}) {
 if(enabled!==true || key!==KEY || readerEmail!==C2_H2_READER_EMAIL ||
   typeof readerUid!=='string' || !UID.test(readerUid) ||
   readerDisabled!==false || !ok(preimage) ||
   typeof preimage.etag!=='string' || !ETAG.test(preimage.etag) ||
   !Array.isArray(preimage.bindings) || preimage.bindings.length!==1 ||
   !ok(preimage.bindings[0]) || preimage.version!==1)return disabled('EXACT_PRINCIPAL_OR_POLICY_PREIMAGE_REQUIRED');
 const base=preimage.bindings[0];
 if(Reflect.ownKeys(base).length!==2 || base.role!=='roles/cloudkms.signer' ||
    !Array.isArray(base.members) || base.members.length!==1 || base.members[0]!==S)
   return disabled('SIGNER_PREIMAGE_DRIFT');
 // Note: the Cloud-side operation must use the same ETag and must independently
 // validate SA email + immutable numeric uniqueId via a fresh IAM readback.
 const bindings=[{role:'roles/cloudkms.signer',members:[S]},
  {role:C2_H2_READER_ROLES[0],members:[R]},
  {role:C2_H2_READER_ROLES[1],members:[R]}];
 const intent=Object.freeze({
  cryptoKey:KEY,readerEmail:C2_H2_READER_EMAIL,readerUid,
  roles:C2_H2_READER_ROLES,
  preservesSigner:C2_H2_SIGNER_EMAIL,
  keyPolicy:Object.freeze({version:1,etag:preimage.etag,
   bindings:Object.freeze(bindings.map(b=>Object.freeze({role:b.role,members:Object.freeze([...b.members])})))}),
  requiredCloudPreflight:Object.freeze([
   'OWNER_PRINCIPAL_AND_PROJECT_FROZEN','READER_EMAIL_UNIQUE_ID_AND_ENABLED_CONFIRMED',
   'EXACT_CRYPTOKEY_GET_IAM_POLICY_UNCHANGED_ETAG',
   'INHERITED_GROUP_AND_DENY_PERMISSIONS_NOT_PROVEN_BY_DIRECT_POLICY',
   'ONE_KEY_ONLY_SET_IAM_POLICY_AND_READBACK_NEEDS_OWNER_APPROVAL',
  ])
 });
 return Object.freeze({reviewReady:true,cloudWriteAuthorized:false,
  reason:'SOURCE_ONLY_EXPECT_EXACT_OWNER_CONSENT',intent});
}
