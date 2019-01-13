import sys, os
import xml.etree.ElementTree as ET


valid_screenshot_list = []

def get_all_screeninformation( root):
    sceenshots = []
    for tag in root.iter():
        if 'InformativeScreenshot' in tag.attrib and len( tag.attrib['InformativeScreenshot']) > 0:
            sceenshots.append( tag.attrib['InformativeScreenshot'])
    return sceenshots


def mark_used_screenshots( cur_dir, valid_sreenshot_list):
    files = os.listdir( cur_dir)
    for f in files:
        if not f.startswith('.') and os.path.isdir( f) :
            print('call mark_used_screenshots with folder %s' %(f))
            mark_used_screenshots( cur_dir + os.sep + f, valid_sreenshot_list) # recursive call 
        if '.xaml' in f: # xaml file 
            root = ET.parse( cur_dir + os.sep + f).getroot() # root element 
            screenshots = get_all_screeninformation(root)
            valid_screenshot_list.extend( screenshots)

def print_and_remove_unused_screenshots( cur_dir, valid_sreenshot_list, remove=False):
    sshots = os.listdir( cur_dir + os.sep + '.screenshots')
    print("valid screenshot # %d and .screenshots has # %d" %(len(valid_sreenshot_list), len(sshots)-2))
    for f in sshots:
        if ".png" in f and not f[0: len(f)-4] in valid_sreenshot_list:
            unused_f = '{0}{1}.screenshots{1}{2}'.format( cur_dir, os.sep, f) 
            print('found unused screenshots : %s' %( f))
            #os.system('git rm .screenshots%s%s' %( os.sep, f))
            if remove and os.path.isfile( unused_f) and '.png' in f :
                #os.remove( unused_f)
                print('forced to remove %s' %(unused_f))

if __name__ == '__main__':
    cur_dir = os.getcwd()
    if len(sys.argv) == 2 :
        cur_dir = cur_dir + os.sep + sys.argv[1]
    mark_used_screenshots( cur_dir, valid_screenshot_list)
    print_and_remove_unused_screenshots( cur_dir, valid_screenshot_list, True)
