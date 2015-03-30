import os
import sys
import CloudConvert

curdir = os.path.abspath(os.path.dirname(sys.argv[0]));

apikey = open(curdir + "/apikey.txt", "r").read().strip()

def get_outputformat(f):
    ext = f.split(".")[-1]
    print("File: " + f)
    print("Extension: " + ext)
    outext = []
    n = 0
    for out in CloudConvert.CloudConvert.conversion_types(ext):
        n += 1
        outext.append(out['outputformat'])
        print("%d - %s - type is %s, note \'%s\'" % (n, out['outputformat'], out['group'], out['shortnote']))
    while True:
        sel = raw_input("Select format (1 - " + str(n) + "): ")
        try:
            sel = int(sel)
        except ValueError:
            print("Enter number")
            continue
        if sel > 0 and sel <= n:
            break
    return {'filename': f, 'from': ext, 'to': outext[sel - 1]}

def convert(apikey, inputfile, outputfile):
    process = CloudConvert.ConversionProcess(apikey)
    process.init(inputfile, outputfile)
    print("start convert - " + inputfile + " to " + outputfile)
    process.start()
    print("waiting...")
    process.wait_for_completion()
    print("Saving " + outputfile)
    process.save()
    print("Open " + outputfile)
    os.system("start " + outputfile)

task = []
for f in sys.argv[1:]:
    if os.path.exists(f):
        task.append(get_outputformat(f))

for t in task:
    if CloudConvert.CloudConvert.is_possible(t['from'], t['to']):
        convert(apikey, t['filename'], t['filename'] + "." + t['to'])