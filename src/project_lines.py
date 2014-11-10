'''
Created on Nov 9, 2014
@author: Mark

Calculates the number of lines of code in a project directory

usage: project_lines.py [-h] [-e EXCLUDED_FILETYPES] [-s] root_path

positional arguments:
  root_path             path to project directory

optional arguments:
  -h, --help            show this help message and exit
  -e EXCLUDED_FILETYPES, --excluded_filetypes EXCLUDED_FILETYPES
                        comma-separated list of filetypes to ignore in project
                        line count, eg ".pyc, .sh"
  -s, --skip_blanks     skip blank lines
  
'''
import os
import argparse

class ProjectLines(object):
    def __init__(self,project_path,exclude_list = None, skip_blank_lines = False):
        self.project_path = project_path
        self.exclude_list = exclude_list
        self.skip_blank_lines = skip_blank_lines
        self.file_types = []
        self.file_type_line_count = {}
        self.num_lines_in_project = 0
        
    def traverse_project(self):
        '''
        recursively iterates through all subdirectories of a project and calls 
        'count_lines' for each file
        '''
        try:
            os.chdir(self.project_path)
        except Exception,e:
            e.args += (self.project_path,)
            raise
        
        
        for subdir,_,files in os.walk(self.project_path):
            #ignore all directories that start with a "dot" and all of its 
            #sub-directories
            if subdir.count('.') > 0:
                continue
            
            for name in files:
                file_ext = os.path.splitext(name)[-1]
                #ignore files whose filetype is in exclude list or if it 
                #doesn't have an extension
                if file_ext in self.exclude_list or file_ext == "":
                    continue
                
                if not file_ext in self.file_types:
                    self.file_types.append(file_ext)
                    self.file_type_line_count[file_ext] = 0
                    
                self.count_lines(subdir,name)
                self.num_lines_in_project += self.line_count
                self.file_type_line_count[file_ext] += self.line_count 
                
                
    def count_lines(self,file_path,file_name):
        '''
        count the number of lines in a file
        '''
        line_count = 0
        try:
            with open(os.path.join(file_path,file_name),'rb') as fh:
                for line in fh:
                    if self.skip_blank_lines and line.strip() == "":
                        continue
                    line_count += 1
        except Exception, e:
            print "can't open file %s" % file_name
        self.line_count = line_count
    
    def check_num_lines(self):
        ''' 
        checks that the number of lines in project adds up to the sum of the number of
        lines for each file type
        '''
        check_lines = 0
        for key in self.file_type_line_count:
            print "file type '%s' has %d lines" % (key, self.file_type_line_count[key])
            check_lines += self.file_type_line_count[key]
        assert(check_lines == self.line_count), "the number of lines doesn't "\
                                                "add up, some files might have "\
                                                "been skipped"
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('root_path', help = "path to project directory")
    parser.add_argument('-e','--excluded_filetypes', 
                        help = "comma-separated list of filetypes to ignore in project "\
                        "line count, eg \".pyc, .sh\"")
    parser.add_argument('-s', '--skip_blanks', help = "don't include blank "\
                                                      "lines in line count", 
                                                      action = "store_true")
    args = parser.parse_args()
    
    excluded_filetypes = map(str.strip,args.excluded_filetypes.split(","))
    
    proj_lines = ProjectLines(args.root_path, exclude_list = excluded_filetypes, 
                              skip_blank_lines = args.skip_blanks)
    proj_lines.traverse_project()
    print "total number of lines in project is %d" % proj_lines.line_count
    proj_lines.check_num_lines()
    
        
