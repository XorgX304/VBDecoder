#!/usr/bin/env python
import re
from collections import Counter
from optparse import OptionParser
import sys

def main(input_file):
    try:
        vbscript_file = open(input_file, 'r')
        vbscript = vbscript_file.read()
        vbscript_file.close()
    except:
        print "\nFailed to open file, ensure path is correct.\n"
        sys.exit()

    ## Output Header
    VBScriptHeader = "-------------\n\nImports System\nimports Microsoft.VisualBasic\nPublic Module Decoder\n"
    print VBScriptHeader

    ## Extract Most Common Function Name
    regex_items = []
    func_name_regex = "[^a-zA-Z0-9]{1,}(.*?)\(\""
    for item in re.findall(func_name_regex, vbscript):
        regex_items = regex_items + re.split(r" |(?<![0-9])[.,](?![0-9])", item)
    func_count = Counter(regex_items)
    func_name = str(func_count.most_common(1)).split("'")[1]

    ## Get AND NOT, ASC and CHR Functions
    function_re = "Function(.*?)End Function"
    for function in re.findall(function_re, str(vbscript), flags=re.IGNORECASE|re.DOTALL):
        strings = ['and not', '=asc', '=chr']
        for string in strings:
            if string in function.lower():
                for line in function.split('\n'):
                    if re.match("^[a-zA-Z0-9]{1,30}=[0-9]{1,5}", line):
                        function = function.replace(line, '')
                print "Function{0}End Function\n".format(function)

    ## Get Main Function
    main_re = "Function {0}(.*?)End Function".format(func_name)
    for main in re.findall(main_re, vbscript, flags=re.IGNORECASE|re.DOTALL):
        for line in main.split('\n'):
            if re.match("^[a-zA-Z0-9]{1,30}=[0-9]{1,5}", line):
                main = main.replace(line, '')
        print "Function {0}{1}End Function\n".format(func_name,main)

    ## Get Decryption Routine Value\Key
    decryption_re = "\(\"(.*?)\)"
    print "Public Sub Main()"
    for value in re.findall(decryption_re, vbscript):
        if "\"" not in value.split(',')[1]:
            variable_re = "{0}=(\".*)".format(value.split(',')[1])
            for var in re.findall(variable_re,vbscript):
                key = value.split(',')[0]
                print "Console.WriteLine({0}(\"{1},{2}))".format(func_name,key, var.strip())
        else:
            pass
            print "Console.WriteLine({0}(\"{1}))".format(func_name, value)

    ## Output Footer
    print "End Sub"
    print "End Module\n\n-------------"
    print "\nNow copy to https://dotnetfiddle.net and create a VB.NET Console project.\n"


if __name__ == "__main__":
    parser = OptionParser(usage='usage: %prog file / dir\n')
    (options, args) = parser.parse_args()
    if len(args) < 1:
        print "No file selected"
        sys.exit()
    input_file = args[0]
    main(input_file)
