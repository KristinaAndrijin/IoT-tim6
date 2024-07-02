import time

n = time.ctime()[11:13] + time.ctime()[14:16]
s = str(n).rjust(4)
n4 = " "*4

print(n)
print(s)
print("fuf"+n4+"fuf")
kek = str(n4).rjust(4)
print("fuf"+kek+"fuf")