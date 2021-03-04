import os

listImages = os.listdir('Images')
print(type(listImages[1]))


print(os.getcwd() + '\\' + listImages[1])
print(listImages)
