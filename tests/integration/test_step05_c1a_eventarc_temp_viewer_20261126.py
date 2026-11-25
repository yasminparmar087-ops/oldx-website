import importlib.util
import unittest
import subprocess
import sys
from pathlib import Path
src=Path(__file__).resolve().parents[2]/'scripts/step05_c1a_eventarc_temporary_viewer_read_revoke_once_20261126.py'
s=importlib.util.spec_from_file_location('s',src)
m=importlib.util.module_from_spec(s)
s.loader.exec_module(m)
class Offline(unittest.TestCase):
 def test_empty_all_locations(self):
  self.assertEqual(m.trigger_inspection([])[0],'NO_C1A_TRIGGER_IN_SUCCESSFUL_ALL_LOCATION_LIST_WITH_LIMITS')
 def test_unrelated(self):
  self.assertEqual(m.trigger_inspection([{'name':'projects/oldx-staging/locations/global/triggers/z','destination':{'cloudRun':{'service':'other'}}}])[0],'NO_C1A_TRIGGER_IN_SUCCESSFUL_ALL_LOCATION_LIST_WITH_LIMITS')
 def test_exact_dependency(self):
  self.assertEqual(m.trigger_inspection([{'name':'projects/oldx-staging/locations/us-east1/triggers/z','destination':{'cloudRun':{'service':'oldx-step05-gateway'}}}])[0],'C1A_DEPENDENCY_EXISTS_STOP')
 def test_full_path_dependency(self):
  self.assertEqual(m.trigger_inspection([{'name':'projects/oldx-staging/locations/global/triggers/z','destination':{'cloudRun':{'service':'projects/oldx-staging/locations/asia-south1/services/oldx-step05-gateway'}}}])[0],'C1A_DEPENDENCY_EXISTS_STOP')
 def test_unresolved_destination(self):
  with self.assertRaises(m.Halt):m.trigger_inspection([{'name':'projects/oldx-staging/locations/global/triggers/z','destination':{}}])
 def test_wrong_project(self):
  with self.assertRaises(m.Halt):m.trigger_inspection([{'name':'projects/other/locations/global/triggers/z','destination':{'workflow':'w'}}])
 def test_workflow(self):
  self.assertEqual(m.trigger_inspection([{'name':'projects/oldx-staging/locations/global/triggers/z','destination':{'workflow':'w'}}])[0],'NO_C1A_TRIGGER_IN_SUCCESSFUL_ALL_LOCATION_LIST_WITH_LIMITS')
 def test_exact_scoped_iam_binding(self):
  binding={'role':m.ROLE,'members':[m.MEMBER],'condition':{'title':'T','expression':'E'}}
  self.assertEqual(m.precise_binding({'bindings':[binding]},'T','E'),[binding])
 def test_existing_role_guard(self):
  self.assertEqual(len(m.own_bindings({'bindings':[{'role':m.ROLE,'members':[m.MEMBER]}]})),1)
 def test_wrong_owner(self):
  with self.assertRaises(m.Halt):m.assert_owner([{'status':'ACTIVE','account':'other@example.com'}])
 def test_no_flag_executes_no_cloud(self):
  p=subprocess.run([sys.executable,str(src)],capture_output=True,text=True)
  self.assertEqual(p.returncode,2)
  self.assertIn('STOP_FLAG_REQUIRED',p.stdout)
if __name__=='__main__':unittest.main(verbosity=2)
