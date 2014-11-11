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
        self.__file_types = []
        self.__file_type_line_count = {}
        self.__num_lines_in_project = 0
    
    def get_filetypes(self):
        return self.__file_types
    
    def set_filetypes(self, file_ext):
        if isinstance(file_ext,basestring):
            self.__file_types.append(file_ext)
        else:
            print "filetype is not a string!"
    
    def get_file_type_line_count(self,file_ext):
        if file_ext in self.get_filetypes():
            return self.__file_type_line_count[file_ext]
        else:
            print "filetype is not in list of valid types!"
    
    def set_file_type_line_count(self,file_ext,line_count):
        if file_ext in self.get_filetypes() and isinstance(line_count,int):
            self.__file_type_line_count[file_ext] += line_count
        else:
            print "either filetype isn't right or line count isn't an integer"
        
    def set_project_line_count(self,line_count):
        if isinstance(line_count, int):
            self.__num_lines_in_project += line_count
        else:
            print "line count is not an integer!"
        
    def get_project_line_count(self):
        return self.__num_lines_in_project
    
    def init_file_type(self,file_ext):
        if isinstance(file_ext, basestring):
            self.__file_type_line_count[file_ext] = 0
        else:
            print "not a valid type!"
    
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
                if file_ext == "" or (self.exclude_list and file_ext in self.exclude_list):
                    continue
                
                if not file_ext in self.get_filetypes():
                    self.set_filetypes(file_ext)
                    self.init_file_type(file_ext)
                    
                line_count = self.count_lines(subdir,name)
                self.set_project_line_count(line_count)
                self.set_file_type_line_count(file_ext, line_count)
                 
                
                
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
        return(line_count)
    
    
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
    
    if args.excluded_filetypes == None:
        excluded_filetypes = None
    else:
        excluded_filetypes = map(str.strip,args.excluded_filetypes.split(","))
    
    proj_lines = ProjectLines(args.root_path, exclude_list = excluded_filetypes, 
                              skip_blank_lines = args.skip_blanks)
    proj_lines.traverse_project()
    print "total number of lines in project is %d" % proj_lines.get_project_line_count()
    
        
