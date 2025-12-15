import os

path = "haier/881311_20250618095635252.wav"
filename = os.path.splitext(os.path.basename(path))[0]
print(filename)
