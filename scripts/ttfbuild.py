import os, sys, subprocess
import fontforge
from shutil import copyfile

file_list=os.listdir("instances")
lang=sys.argv[1]
family_name=sys.argv[2]
full_font_name=sys.argv[3]
font_name=sys.argv[4]
FEATURES = '''\
table head {
  FontRevision 1.001;
} head;
include (features-'''+lang+'''.fea)\n'''
INFO='''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>unitsPerEm</key>
	<integer>1024</integer>
</dict>
</plist>'''

for file in file_list:
    path='instances/'+file+'/font.ufo'
    print "[INFO] Checking out lines and resetting UFO"
    subprocess.call(['checkOutlinesUFO', '-e', '-all','-wd', path])

    for item in os.listdir(path):
        if os.path.isfile(path+'/'+item) and not item=="lib.plist" and not item=="metainfo.plist":
            os.remove(path+'/'+item)

    with open(path+'/features.fea', 'w') as f:
        f.write(FEATURES)
    with open(path+'/fontinfo.plist', 'w') as f:
        f.write(INFO)

    for item in os.listdir('instances/'+file):
        if os.path.isfile('instances/'+file+'/'+item):
            copyfile('instances/'+file+"/"+item, path+"/"+item)

    copyfile("features/features-"+lang+".fea", path+"/features-"+lang+".fea")
    copyfile("features/tables-"+lang+".fea", path+"/tables-"+lang+".fea")

    try:
       copyfile("features/GENERATED_classes.fea", path+"/GENERATED_classes.fea")
    except:
        print "[INFO] GENERATED_classes.fea not found"


    font = fontforge.open(path)
    font.familyname=family_name
    font.fontname=font_name+"-"+file
    font.fullname=full_font_name+" "+file
    font.version="1.001"
    if not os.path.exists("ttf-build"):
        os.mkdir("ttf-build")
    if lang=="s" and not os.path.exists("ttf-build/Sinhala"):
        os.mkdir("ttf-build/Sinhala")
    elif lang=="t" and not os.path.exists("ttf-build/Tamil"):
        os.mkdir("ttf-build/Tamil")
    print "[INFO] Generating ttf font"
    if lang=="s":
        font.generate("ttf-build/Sinhala/"+full_font_name+"-"+file+".ttf")
    else:
        font.generate("ttf-build/Tamil/"+full_font_name+"-"+file+".ttf")
