import json

with open("data.json", "r") as file:
    data = json.load(file)

print("Interface Status")
print("=" * 102)
print(f"{'DN':<55} {'Description':<10} {'Speed':<7} {'MTU':<5}")
print("-" * 102)

for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]
    dn = attributes["dn"]
    speed = attributes["speed"]
    mtu = attributes["mtu"]
    description = "inherit"
    if dn in [
        "topology/pod-1/node-201/sys/phys-[eth1/33]",
        "topology/pod-1/node-201/sys/phys-[eth1/34]",
        "topology/pod-1/node-201/sys/phys-[eth1/35]"
    ]:
        print(f"{dn:<55} {description:<10} {speed:<7} {mtu:<5}")
