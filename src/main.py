import sys
from textnode import *
from htmlnode import *
from helper_functions import *
from os import listdir, mkdir
from os.path import exists, isfile, join
from shutil import rmtree, copy

def main():
    base_path = sys.argv[1] if len(sys.argv[1]) == 2 else "/"
    copy_source_to_destination()
    # generate_page("./content/index.md", "./template.html", "./public/index.html")
    generate_pages_recursive("./content", "./template.html", "./docs", base_path)

# delete everything in public dir
# copy all files/directories from static to public 
# log src and dest file paths while copying
def copy_source_to_destination(src="static",dst="docs"):
    # delete public and its contents
    if exists(dst):
        print(f"deleting {dst} and its contents")
        rmtree(dst)
    
    # create public dir if does not exist
    if not exists(dst):
        print(f"creating {dst}")
        mkdir(dst)
    
    # iterate all entities in dir and either copy to dst or recurse
    for entity in listdir(src):
        srcPath = join(src, entity)
        dstPath = join(dst, entity)
        if isfile(srcPath):
            # copy to dst
            print(f"copying {srcPath} to {dst}")
            copy(srcPath, dst)
        else:
            # recurse
            copy_source_to_destination(srcPath, dstPath)
    return True


main()

