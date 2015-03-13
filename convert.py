import os
import sys
import signal
import CloudConvert

apikey = open("apikey.txt", "r").read().strip()

process = CloudConvert.ConversionProcess(apikey)

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

task = []
for f in sys.argv[1:]:
    if os.path.exists(f):
        task.append(get_outputformat(f))

for t in task:
    if CloudConvert.CloudConvert.is_possible(t['from'], t['to']):
        inputfile = t['filename']
        outputfile = t['filename'] + "." + t['to']
        process.init(inputfile, outputfile)
        print("start convert - " + inputfile + " to " + outputfile)
        process.start()
        print("waiting...")
        process.wait_for_completion()
        print("Saving")
        process.save()
        print("Open")
        os.system("start " + outputfile)
