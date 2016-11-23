import subprocess

p = subprocess.Popen(["ls", "/proc"], stdout=subprocess.PIPE, shell=False, universal_newlines=True)
(output, err) = p.communicate()
arr = output.split('\n')
outArr = [];
for element in arr:
    if(element.isdigit()):
        cmdString = "/proc/" + element + "/status"
        p2 = subprocess.Popen(["cat", cmdString], stdout=subprocess.PIPE, shell=False, universal_newlines=True)
        (output2, err) = p2.communicate()
        arr2 = output2.split('\n')
        for element2 in arr2:
            if((element2) and (element2[0] == 'N') and (element2[1] == 'a')):
                element = element.strip(" ")
                element2 = element2.strip("Name:")
                element2 = element2.strip(" ")
                element2 = element2.strip('\t')
                outArr.append([element, element2])

for element in outArr:
    print(element)

#subprocess.call(["cat", "/proc/meminfo"])
