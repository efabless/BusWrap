import sys
import yaml
from svmodule.moddict import ModDict
from svmodule.printer import Printer
from datetime import datetime

now = datetime.now() # current date and time

opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

if len(args) < 2:
    sys.exit(f"Usage: {sys.argv[0]} <module file> <module name>") 

module_str = ""

try:
    file = open(args[0], "r")
except:
    sys.exit(f"Could not open {args[0]}")

lines = file.readlines()
flag = 0
for line in lines:
    if flag == 1:
        #print(line, end="")
        module_str += line
        if "endmodule" in line:
            flag = 0
    elif "module" in line:
        if "endmodule" in line:
            continue
        tokens = line.split()
        if tokens[1] == args[1]:
            flag = 1
            #print(line, end="")
            module_str += line

m = ModDict()
m.parse(module_str)

print(f"""info:
  name: {m.parsed_module['name']}
  description: <Add the description here>
  repo: <repo>
  owner: <owner>
  license: <MIT|APACHE 2.0|GPL|BSD>
  author: <author>
  email: <email>
  version: <version>
  date: {now.strftime('%d-%m-%Y')}
  category: <digital|analog>
  tags:
    - <a tag>
    - <another tag>
  bus:
    - <generic|ahb|apb|wb>
  type: <soft|hard|firm>
  status: <verified|fpga|silicon>
  qualification: <Comm|Ind|Automotive|Mil>
  cell_count: "<count>
  width: <width>
  height: <height>
  technology: <tech>
  clock_freq_mhz: <frequency in MHz>
  digital_supply_voltage: <DVDD>
  analog_supply_voltage: <AVCC>
""")

print("parameters:")
for p in m.parsed_module['parameters']:
    print(f"- name: {p['name']}\n  default: {p['value']}")

print("\n# Remove the clock, reset and external interface ports from the following list\nports:")
for p in m.parsed_module['ports']:
    #print(p)
    if p['packed'] == "":
        width = 1
    else:
        ft = p["packed"].split(":")
        f = ft[1]
        t = ft[0]
        try:
            width = int(t.split("[")[1])
            width = width - int(f.split("]")[0]) + 1
        except ValueError:
            width = t.split("[")[1].split("-")[0]

    print(f" - name: {p['name']}\n   width: {width}\n   direction: {p['direction']}\n   description: ")

print("\nclock:\n  name: <clk_name>")
print("\nreset:\n  name: <rst_name>\n  level: 0/1")
print("\nexternal_interface:")
print("- name: \n  port: \n  direction: \n  width: \n  description: ")
print("\nregisters: \n- name: \n  size: \n  mode: r/w/rw\n  fifo: no/yes\n  offset: \n  bit_access: no/yes\n  description: ")
print("  fields:\n  - name: \n    bit_offset: \n    bit_width: \n    write_port: \n    description: ")
print("\nflags:\n- name: \n  port: \n  description: ")
