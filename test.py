import os

validExtensions = [".jpg", ".png", ".jpeg"]
validFiles = []
directory = 'Images'
listImages = os.listdir(directory)


for item in listImages:
    if os.path.splitext(item)[1].casefold() in validExtensions:
        validFiles.append(item)
    else:
        pass

print(validFiles)
for item in validFiles:
    stats = os.stat(os.getcwd() + "\\" + directory + "\\" + item)
    print(f"{item} has size of {stats.st_size / 1000000} MB")

def test():
    value1 =  "hello"
    value2 = 24

    return value1, value2

x,y = test()
print(x)
print(y)