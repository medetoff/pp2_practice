#Delete File
#To delete a file, you must import the OS module,and run its os.remove() function:
#1 Remove the file "demofile.txt":

import os
os.remove("demofile.txt")

#2 Check if File exist:
import os
if os.path.exists("demofile.txt"):
  os.remove("demofile.txt")
else:
  print("The file does not exist")
  
#3 Delete folder
import os
os.rmdir("myfolder")

#4 Copy a file
import shutil
# Copy file from source to destination
shutil.copy("source.txt", "destination.txt")  
# Copies the file content and permissions

#5 Safe delete with existence check
import os
file_path = "example.txt"
if os.path.exists(file_path):
    os.remove(file_path)
    print("File deleted")
else:
    print("File does not exist")