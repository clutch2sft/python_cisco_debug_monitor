from netmiko.ssh_dispatcher import CLASS_MAPPER_BASE

# Print all available device types
for device_type in CLASS_MAPPER_BASE.keys():
    print(device_type)
