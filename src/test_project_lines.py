'''
Created on Nov 10, 2014

@author: mark
'''
import unittest
import os
import shutil
import project_lines
from os.path import expanduser

class project_lines_Test(unittest.TestCase):


    def setUp(self):
        self.num_levels = 5
        self.num_files = 10
        self.num_lines_per_file = 50
        self.num_blanks = 0
        self.file_types = ['.pyc','.py','.sh','.java','.sql']
        test_root_dir = os.path.join(expanduser("~"),'test_dir')
        self.root_dir = test_root_dir
        if not os.path.exists(self.root_dir):
                os.mkdir(self.root_dir)
        for level in range(self.num_levels):
            new_dir = os.path.join(self.root_dir,'level_'+str(level))
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            for file_num in range(self.num_files):
                file_name = os.path.join(new_dir,'file_'+str(file_num)+self.file_types[int(file_num % self.num_files/(self.num_files/len(self.file_types)))])
                try: 
                    with open(file_name,'w') as fh:
                        for line_num in range(self.num_lines_per_file):
                            fh.write('line %d\n' % line_num)
                except Exception,e:
                    e.args += (file_name,)
                    raise
        

    def tearDown(self):
        try:
            shutil.rmtree(self.root_dir)
        except OSError, e:
            print ("Error: %s - %s." % (e.filename,e.strerror))
       

    def testLineCount(self):
        pl = project_lines.ProjectLines(os.path.join(expanduser("~"),'test_dir'))
        line_count = pl.count_lines(os.path.join(self.root_dir,'level_0'), 'file_2.py')
        self.assertEqual(line_count,self.num_lines_per_file)
    
    def testFiletypeLinecount(self):
        pl = project_lines.ProjectLines(os.path.join(expanduser("~"),'test_dir'))
        pl.traverse_project()
        self.assertEqual(pl.get_file_type_line_count('.py'),self.num_levels * self.num_files/len(self.file_types) * self.num_lines_per_file)
    
    def testProjectLines(self): 
        pl = project_lines.ProjectLines(os.path.join(expanduser("~"),'test_dir'))
        pl.traverse_project()
        self.assertEqual(pl.get_project_line_count(),self.num_levels * self.num_files * self.num_lines_per_file)
    
    def testExludeFiletypes(self): 
        excluded_filetypes = ['.pyc','.sh']       
        pl = project_lines.ProjectLines(os.path.join(expanduser("~"),'test_dir'),excluded_filetypes)
        self.assertListEqual(pl.exclude_list, excluded_filetypes, 'lists not equal')
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    
    unittest.main()
    newSuite = unittest.makeSuite(project_lines_Test)
    newSuite.addTest(project_lines_Test("testLineCount"))
    newSuite.addTest(project_lines_Test("testFiletypeLinecount"))
    newSuite.addTest(project_lines_Test("testProjectLines"))
    newSuite.addTest(project_lines_Test("testExcludeFiletypes"))
    