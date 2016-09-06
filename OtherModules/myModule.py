'''
This is mymodule module test file
==================================
'''

def main():
    """Script to be run on start up"""
    print dir()
    
def myFunction():
    """This is my function"""
    import sys
    print sys.path

if __name__ == '__main__':
    main()