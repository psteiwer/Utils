import os

def findFile(path, filename):
    result = []
    for root, dirs, files in os.walk(path):
        if filename in files:
            result.append(os.path.join(root, filename))
    return result

def isSameSize(file1,file2):
    return file1.st_size==file2.st_size

def moveToSafe(sourceDirectory,searchDirectory):
    pathOld=sourceDirectory
    pathNew=searchDirectory

    oldDirectory = os.fsencode(pathOld)
    newDirectory = os.fsencode(pathNew)
    sizearray=[]
    count=0
    duplicatesizecount=0
    maxdsize=0
    skiplist=[]
    safeList=[]
    for file in os.listdir(oldDirectory):
        filename = os.fsdecode(file)
        if filename in skiplist:
            continue
        # Check if file exists in new
        if not os.path.isfile(pathNew+"\\"+filename):
            #os.rename(pathOld+"\\"+filename, pathNew+"\\"+filename)
            continue
        oldFileInfo=os.stat(pathOld+"\\"+filename)
        newFileInfo=os.stat(pathNew+"\\"+filename)


        if oldFileInfo.st_size in sizearray:
            if oldFileInfo.st_size>maxdsize:
                maxdsize=oldFileInfo.st_size
            duplicatesizecount=duplicatesizecount+1
            #continue
        else:
            sizearray.append(oldFileInfo.st_size)

        if isSameSize(oldFileInfo,newFileInfo):
            safeList.append(filename)
            os.rename(pathOld+"\\"+filename, pathOld+" safe\\"+filename)
            count=count+1


def isDuplicate(filepath,directory):
    origFileStat=os.stat(filepath)
    filename=filepath.split("\\")
    filename=filename[len(filename)-1]
    duplicates=findFile(directory,filename)
    if len(duplicates)>0:
        for duplicate in duplicates:
            if filepath==duplicate:
                continue
            if isSameSize(origFileStat,os.stat(duplicate)):
                print("Duplicate found: "+filepath+" duplicate of "+duplicate)
                return True

def findDuplicates(sourceDirectory,searchDirectory):
    duplicateList = []
    for root, dirs, files in os.walk(sourceDirectory):
        for file in files:
            if isDuplicate(os.path.join(root, file),searchDirectory):
                duplicateList.append(os.path.join(root, file))
    return duplicateList

def deleteDuplicates(sourceDirectory,searchDirectory):
    duplicates=findDuplicates(sourceDirectory,searchDirectory)
    for duplicate in duplicates:
        os.remove(duplicate)

deleteDuplicates("F:\\Lightroom\\Lightroom CC\\50a52b6f144647768510f6178babfb69\\originals\\","F:\\")