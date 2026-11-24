import unittest
import importlib.util
from pathlib import Path
p=Path(__file__).parents[2]/'scripts/step05_h1b_s3_cloudshell_readonly_once_20261125.py'
spec=importlib.util.spec_from_file_location('s3',p)
s3=importlib.util.module_from_spec(spec)
spec.loader.exec_module(s3)
class S3Tests(unittest.TestCase):
 def test_correct_owner(self): self.assertTrue(s3.active_owner([{'status':'ACTIVE','account':'yasminparmar087@gmail.com'}]))
 def test_wrong_owner_denied(self):
  with self.assertRaises(s3.Stop): s3.active_owner([{'status':'ACTIVE','account':'wrong@example.com'}])
 def test_multiple_active_denied(self):
  with self.assertRaises(s3.Stop):s3.active_owner([{'status':'ACTIVE','account':'yasminparmar087@gmail.com'},{'status':'ACTIVE','account':'other@example.com'}])
 def test_project_number(self):self.assertTrue(s3.project_valid({'projectId':'oldx-staging','projectNumber':'38472235077','lifecycleState':'ACTIVE'}))
 def test_wrong_project(self):
  with self.assertRaises(s3.Stop):s3.project_valid({'projectId':'oldx-staging','projectNumber':'1','lifecycleState':'ACTIVE'})
 def test_registry(self):self.assertTrue(s3.registry_valid({'format':'DOCKER','name':'projects/oldx-staging/locations/asia-south1/repositories/oldx-staging-images'}))
 def test_403_not_absent(self):self.assertEqual(s3.target_state(1,'ERROR 403 PERMISSION_DENIED NOT_FOUND','', 'service'),'UNRESOLVED_ERROR_NOT_PROVEN_ABSENT')
 def test_404_reported_review(self):self.assertEqual(s3.target_state(1,'NOT_FOUND: service does not exist','', 'service'),'API_NOT_FOUND_REPORTED_REVIEW_REQUIRED')
 def test_absent_response_unknown(self):self.assertEqual(s3.target_state(1,'transient','', 'service'),'UNRESOLVED_ERROR_NOT_PROVEN_ABSENT')
 def test_existing_service(self):self.assertEqual(s3.target_state(0,'','{"metadata":{"name":"oldx-c2-website-mediator"}}','service'),'EXISTS_COLLISION_STOP')
 def test_existing_sa(self):self.assertEqual(s3.target_state(0,'','{"email":"oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com"}','sa'),'EXISTS_COLLISION_STOP')
if __name__ == '__main__':unittest.main(verbosity=2)
