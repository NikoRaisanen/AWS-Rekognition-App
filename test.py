import os
import shutil

listImages = os.listdir()
print(type(listImages[1]))
print(os.getcwd())
print(listImages)

source = os.getcwd() + '\\' + 'linkedInpfp.jpg'
destination = os.getcwd() + '\\' + 'testFolder' + '\\' + 'linkedincopy.jpg'

dest = shutil.copyfile(source, destination)

print(dest)