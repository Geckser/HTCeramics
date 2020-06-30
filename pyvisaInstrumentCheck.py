import pyvisa as visa

print("Resource Manager has identified the following instruments.")
print(visa.ResourceManager.list_resources())
