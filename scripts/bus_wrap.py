"""
Copyright (c) 2020 AUCOHL


   Author: Mohamed Shalan (mshalan@aucegypt.edu)
  
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at:


   http://www.apache.org/licenses/LICENSE-2.0


   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
"""
   An automatic wrapper generator for the AMBA Advanced Peripherals Bus (APB) 
   and the Advanced High Performance Bus (AHB) Lite, as well as the Wishbone bus.
   The input is a yaml/json file that contains the IP definition.
"""


import sys
#import os.path
import yaml
import json


IP          = None


# COnfigurations to be loaded from a configuration file
BUS_AW      = 16
INT_REG_OFF = 0x0F00


# Interrupt registers offsets
IC_OFF      = 0x0C + INT_REG_OFF
RIS_OFF     = 0x08 + INT_REG_OFF
IM_OFF      = 0x00 + INT_REG_OFF
MIS_OFF     = 0x04 + INT_REG_OFF


def print_license():
   print(f"/*\n\tCopyright {IP['info']['date'].split('-')[2]} {IP['info']['owner']}\n")
   print(f"\tAuthor: {IP['info']['author']} ({IP['info']['email']})\n")

   if "MIT" in IP['info']['license'].upper():
       print("\tPermission is hereby granted, free of charge, to any person obtaining")
       print("\ta copy of this software and associated documentation files (the")
       print("\t\"Software\"), to deal in the Software without restriction, including")
       print("\twithout limitation the rights to use, copy, modify, merge, publish,")
       print("\tdistribute, sublicense, and/or sell copies of the Software, and to")
       print("\tpermit persons to whom the Software is furnished to do so, subject to")
       print("\tthe following conditions:\n")
       print("\tThe above copyright notice and this permission notice shall be")
       print("\tincluded in all copies or substantial portions of the Software.\n")
       print("\tTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND,")
       print("\tEXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF")
       print("\tMERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND")
       print("\tNONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE")
       print("\tLIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION")
       print("\tOF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION")
       print("\tWITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.")
   
   elif "APACHE 2.0" in IP['info']['license'].upper():
       print("\tLicensed under the Apache License, Version 2.0 (the \"License\");")
       print("\tyou may not use this file except in compliance with the License.")
       print("\tYou may obtain a copy of the License at\n")
       print("\t    http://www.apache.org/licenses/LICENSE-2.0\n")
       print("\tUnless required by applicable law or agreed to in writing, software")
       print("\tdistributed under the License is distributed on an \"AS IS\" BASIS,")
       print("\tWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.")
       print("\tSee the License for the specific language governing permissions and")
       print("\tlimitations under the License.")
   
   elif "BSD" in IP['info']['license'].upper():
       print("\tRedistribution and use in source and binary forms, with or without modification,")
       print("\tare permitted provided that the following conditions are met:\n")
       print("\t1. Redistributions of source code must retain the above copyright notice,")
       print("\tthis list of conditions and the following disclaimer.\n")
       print(f"\tTHIS SOFTWARE IS PROVIDED BY {self.author} \“AS IS\” AND ANY EXPRESS OR ")
       print("\tIMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF ")
       print("\tMERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT ")
       print(f"\tSHALL {self.author} BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, ")
       print("\tSPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, ")
       print("\tPROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; ")
       print("\tOR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER ")
       print("\tIN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING ")
       print("\tIN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF ")
       print("\tSUCH DAMAGE.")
   
   elif "GPL" in IP['info']['license'].upper():
       print("\tThis program is free software; you can redistribute it and/or")
       print("\tmodify it under the terms of the GNU General Public License")
       print("\tversion 2 as published by the Free Software Foundation.\n")
       print("\tThis program is distributed in the hope that it will be useful,")
       print("\tbut WITHOUT ANY WARRANTY; without even the implied warranty of")
       print("\tMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the")
       print("\tGNU General Public License for more details.")
   print("\n*/\n")

def print_header(bus_type):
   """
   Print the header of the generated file.
   """
   print(f"/* THIS FILE IS GENERATED, DO NOT EDIT */\n")
   print(f"`timescale\t\t\t1ns/1ps")
   print(f"`default_nettype\tnone\n")
   print(f"`define\t\t\t\t{bus_type}_AW\t\t{BUS_AW}\n")
   print(f"`include\t\t\t\"{bus_type.lower()}_wrapper.vh\"\n")  


def print_module_header(bus_type):
    """
    Prints the header of the generated file for the specified bus type.

    Parameters:
        bus_type (str): The type of bus (e.g. APB, AHBL, WB).

    Returns:
        None
    """
    # Print module name
    print(f"module {IP['info']['name']}_{bus_type}", end="")

    if "parameters" in IP:
        print(" #( \n\tparameter\t")
        for index, p in enumerate(IP['parameters']):
            print(f"\t\t{p['name']} = {p['default']}", end="")
            if index != len(IP['parameters']) - 1:
                print(",")
        print("\n)", end="")
    print(" (")
    if "external_interface" in IP:
        # Print {bus_type}_SLAVE_PORTS
        print(f"\t`{bus_type}_SLAVE_PORTS,")

        # Print details of each interface
        for index, ifc in enumerate(IP['external_interface']):
            if index != len(IP['external_interface']) - 1:
                # Print interface details with comma
                print(f"\t{ifc['direction']}\t[{ifc['width']-1}:0]\t{ifc['name']},")
            else:
                # Print interface details without comma
                print(f"\t{ifc['direction']}\t[{ifc['width']-1}:0]\t{ifc['name']}")
    else:
        # Print only {bus_type}_SLAVE_PORTS
        print("\t`{bus_type}_SLAVE_PORTS")

    # Print end of module header
    print(");\n")
  
def print_wires(bus_type):
    """
    Print the wire declarations for the given IP.

    This function prints the wire declarations for the clock, reset, and ports of the IP.
    It also includes the `CTRL_SIGNALS` macro.

    Args:
        The bus type (string): APB, AHBL or WB

    Returns:
        None
    """

    if bus_type == "APB" :
        clk_net = "PCLK"
        rst_net = "PRESETn"
    elif bus_type == "AHBL":
        clk_net = "HCLK"
        rst_net = "HRESETn"
    elif bus_type == "WB":
        clk_net = "clk_i"
        rst_net = "(~rst_i)"

    # Print clock wire declaration
    print(f"\twire\t\t{IP['clock']['name']} = {clk_net};")

    # Check if reset is active and set the 'mod' variable accordingly
    if IP['reset']['level'] == 0:
        mod = ""
    else:
        mod = "~"

    # Print reset wire declaration
    print(f"\twire\t\t{IP['reset']['name']} = {mod}{rst_net};\n")

    # Print the needed APB control signals
    print(f"\n\t`{bus_type}_CTRL_SIGNALS\n")

    # Print wire declarations for the IP instance ports
    for i in IP['ports']:
        print(f"\twire [{i['width']}-1:0]\t{i['name']};")

    print("")

    #print("")
  
def print_instance_to_wrap(bus_type):
    """
    Print the instance to wrap by formatting the IP dictionary.

    Args:
        None

    Returns:
        None
    """

    # Generate synchronizers for input interfaces if needed
    if "external_interface" in IP:
        for index, ifc in enumerate(IP['external_interface']):
            if "sync" in ifc:
                if ifc["sync"] == True:
                    if ifc["direction"] != "input":
                        raise sys.exit("You cannot attach a synchronizer to non-input interface")
                    print_synchronizer(bus_type, ifc['name'], ifc['port'], ifc['width'], 2)

    if "parameters" in IP:
        print(f"\t{IP['info']['name']} #(")
        for index, p in enumerate(IP['parameters']):
            print(f"\t\t.{p['name']}({p['name']})", end="")
            if index != len(IP['parameters']) - 1:
                print(",")
        print("\n\t) instance_to_wrap (")
    else:
        print(f"\t{IP['info']['name']} instance_to_wrap (")

    print(f"\t\t.{IP['clock']['name']}({IP['clock']['name']}),")
    print(f"\t\t.{IP['reset']['name']}({IP['reset']['name']}),")
    for index, p in enumerate(IP['ports']):
        if index != len(IP['ports']) - 1 or "external_interface" in IP:
            print(f"\t\t.{p['name']}({p['name']}),")
        else:
            print(f"\t\t.{p['name']}({p['name']})")
    
    if "external_interface" in IP:
        for index, ifc in enumerate(IP['external_interface']):
            port = f"{ifc['name']}"
            if "sync" in ifc:
                if ifc['sync'] == True:
                    port = f"_{ifc['port']}_w_"
            
            if index != len(IP['external_interface']) - 1:
                print(f"\t\t.{ifc['port']}({port}),")
            else:
                print(f"\t\t.{ifc['port']}({port})")
    print("\t);\n")

def print_synchronizer(bus_type, name, port, width, stages):
    if bus_type == "AHBL":
        clk = "HCLK"
        rst = "HRESETn"
        pol = 0
    elif bus_type == "APB":
        clk = "PCLK"
        rst = "PRESETn"
        pol = 0
    elif bus_type == "WB":
        clk = "clk_i"
        rst = "rst_i"
        pol = 1
    
    clock_edge = "posedge" if pol == 1 else "negedge"

    print(f"\treg [{width-1}:0]\t_{name}_reg_[{stages-1}:0];")
    print(f"\twire\t\t_{port}_w_ = _{name}_reg_[{stages-1}];")
    print(f"\talways@(posedge {clk} or {clock_edge} {rst})")
    print(f"\t\tif({rst} == {pol}) begin")
    for i in range(stages):
        print(f"\t\t\t_{name}_reg_[{i}] <= 'b0;")
    print(f"\t\tend")
    print(f"\t\telse begin")
    print(f"\t\t\t_{name}_reg_[0] <= {name};")
    for i in range(stages-1):
        print(f"\t\t\t_{name}_reg_[{i+1}] <= _{name}_reg_[{i}];")
    print(f"\t\tend")
def print_registers(bus_type):
    """
    Print the register declarations for the given IP.

    Args:
        None

    Returns:
        None
    """
    if IP['registers'] is False:
        return
            
    for r in IP['registers']:    
        if r['fifo'] is True:
            print(f"\twire\t[{r['size']}-1:0]\t{r['name']}_WIRE;")
        else:
            if r['mode'] == 'rw':
                # 'rw' registers cannot have field
                print(f"\treg\t[{r['size']}-1:0]\t{r['name']}_REG;")
                print(f"\twire\t[{r['size']}-1:0]\t{r['name']}_WIRE;")
                print(f"\tassign\t{r['name']}_WIRE = {r['read_port']};")
                print(f"\tassign\t{r['write_port']} = {r['name']}_REG;")
                print(f"\t`{bus_type}_REG({r['name']}_REG, 0, 8)")
            elif r['mode'] == 'w':
                print(f"\treg [{r['size']}-1:0]\t{r['name']}_REG;")
                if "fields" in r and "write_port" not in r:
                    for f in r['fields']:
                        if isinstance(f['bit_width'], int):
                            to = f['bit_width'] + f['bit_offset'] - 1
                        else:
                            if f['bit_offset'] == 0:
                                to = f"({f['bit_width']} - 1)"
                            else:
                                to = f"({f['bit_width']} + {f['bit_offset'] - 1})"
                        print(f"\tassign\t{f['write_port']}\t=\t{r['name']}_REG[{to} : {f['bit_offset']}];")
                else:
                    print(f"\tassign\t{r['write_port']} = {r['name']}_REG;")
                print(f"\t`{bus_type}_REG({r['name']}_REG, {r['init'] if 'init' in r else 0}, {r['size']})")
            elif r['mode'] == 'r':
                print(f"\twire [{r['size']}-1:0]\t{r['name']}_WIRE;")
                if "fields" in r:
                    for f in r['fields']:
                        if isinstance(f['bit_width'], int):
                            to = f['bit_width'] + f['bit_offset'] - 1
                        else:
                            if f['bit_offset'] == 0:
                                to = f"({f['bit_width']} - 1)"
                            else:
                                to = f"({f['bit_width']} + {f['bit_offset'] - 1})"
                        print(f"\tassign\t{r['name']}_WIRE[{to} : {f['bit_offset']}] = {f['read_port']};")
                else:
                    print(f"\tassign\t{r['name']}_WIRE = {r['read_port']};")
        
        print()
      
def get_port_width(port):
   """
   Get the width of a port.

   Args:
       port (str): The name of the port.

   Returns:
       int: The width of the port.
   """
   for p in IP['ports']:
       if p['name'] == port:
           return p['width']
   return -1


def get_param_default(param):
   for p in IP['parameters']:
       if p['name'] == param:
           return p['default']
   return -1


def print_ris_register(bus_type):
    """
    Prints the code for generating the RIS register for the specified bus type.

    Parameters:
        bus_type (str): The type of bus (e.g. APB, AHBL, WB).

    Returns:
        None
    """
    # declare wires for the flags if the flag name is different than the port it is connected to
    print()
    for f in IP['flags']:
        if f['name'] != f['port']:
            print(f"\twire [{get_port_width(f['port'])-1}:0] {f['name']} = {f['port']};")
    print()

    # Initialize the loop counter
    print("\n\tinteger _i_;")

    # Check if RIS_REG is accessible, else skip the loop
    print(f"\t`{bus_type}_BLOCK(RIS_REG, 0) else begin")

    # Iterate over each flag in the IP dictionary
    pos = 0
    for f in IP['flags']:
        # Iterate from 0 to the port width of the flag
        print(f"\t\tfor(_i_ = {pos}; _i_ < {get_port_width(f['port'])+pos}; _i_ = _i_ + 1) begin")

        # Update RIS_REG based on the condition
        print(f"\t\t\tif(IC_REG[_i_]) RIS_REG[_i_] <= 1'b0; else if({f['name']}[_i_ - {pos}] == 1'b1) RIS_REG[_i_] <= 1'b1;")

        # End the inner loop
        print("\t\tend")

        pos += get_port_width(f['port'])

    # End the outer loop
    print("\tend")

    # Add a newline for readability
    print()


def print_IRQ_registers(bus_type):
    """
    Print the register declarations for the given IP.

    Args:
        None

    Returns:
        None
    """
    flag_size = 0
    for f in IP['flags']:
        if get_port_width(f['port']) == -1:
            raise Exception(f"Port {f['port']} not found in the IP definition")
        else:
            flag_size += get_port_width(f['port'])
    print(f"\treg [{flag_size-1}:0] IM_REG;")
    print(f"\treg [{flag_size-1}:0] IC_REG;")
    print(f"\treg [{flag_size-1}:0] RIS_REG;\n")
    print(f"\t`{bus_type}_MIS_REG({flag_size})")
    print(f"\t`{bus_type}_REG(IM_REG, 0, {flag_size})")
    print(f"\t`{bus_type}_IC_REG({flag_size})")
    print_ris_register(bus_type)
    print(f"\tassign IRQ = |MIS_REG;")
    print()


def print_registers_offsets(bus_type):
   """
   Print the register offsets for the given IP.


   Args:
       None


   Returns:
       None
   """
   # user defined registers
   for r in IP['registers']:
       print(f"\tlocalparam\t{r['name']}_REG_OFFSET = `{bus_type}_AW'd{r['offset']};")


   # Interrupt registers
   print(f"\tlocalparam\tIM_REG_OFFSET = `{bus_type}_AW'd{IM_OFF};")
   print(f"\tlocalparam\tMIS_REG_OFFSET = `{bus_type}_AW'd{MIS_OFF};")
   print(f"\tlocalparam\tRIS_REG_OFFSET = `{bus_type}_AW'd{RIS_OFF};")
   print(f"\tlocalparam\tIC_REG_OFFSET = `{bus_type}_AW'd{IC_OFF};")
              
   print("")

def print_rdata(bus_type):
    IRQ_REGS = ["IM", "MIS", "RIS", "IC"]
    prefix = "last_H"
    if bus_type == "APB":
        prefix = "P"
        print(f"\tassign\t{prefix}RDATA = ")
    else:
        print(f"\tassign\tHRDATA = ")
    
    for index,r in enumerate(IP['registers']):
        if "r" in r['mode'] or r['fifo'] is True:
            print(f"\t\t\t({prefix}ADDR[`{bus_type}_AW-1:0] == {r['name']}_REG_OFFSET)\t? {r['name']}_WIRE :")
        else:
            print(f"\t\t\t({prefix}ADDR[`{bus_type}_AW-1:0] == {r['name']}_REG_OFFSET)\t? {r['name']}_REG :")
    
    if "flags" in IP:
        for r in IRQ_REGS:
            print(f"\t\t\t({prefix}ADDR[`{bus_type}_AW-1:0] == {r}_REG_OFFSET)\t? {r}_REG :")
    
    print("\t\t\t32'hDEADBEEF;")
    
    if bus_type == "APB":
        print(f"\n\tassign\t{prefix}READY = 1'b1;\n")
    else:
        print(f"\n\tassign\tHREADYOUT = 1'b1;\n")

def print_wb_dat_o(bus_type):
    IRQ_REGS = ["IM", "MIS", "RIS", "IC"]

    print(f"\tassign\tdat_o = ")

    for index,r in enumerate(IP['registers']):
        if "r" in r['mode'] or r['fifo'] is True:
            print(f"\t\t\t(adr_i[`{bus_type}_AW-1:0] == {r['name']}_REG_OFFSET)\t? {r['name']}_WIRE :")
        else:
            print(f"\t\t\t(adr_i[`{bus_type}_AW-1:0] == {r['name']}_REG_OFFSET)\t? {r['name']}_REG :")

    if "flags" in IP:
        for r in IRQ_REGS:
            print(f"\t\t\t(adr_i[`{bus_type}_AW-1:0] == {r}_REG_OFFSET)\t? {r}_REG :")

    print("\t\t\t32'hDEADBEEF;")

    print("\n\talways @ (posedge clk_i or posedge rst_i)")
    print("\t\tif(rst_i)\n\t\t\tack_o <= 1'b0;")
    print("\t\telse if(wb_valid & ~ack_o)")
    print("\t\t\tack_o <= 1'b1;")
    print("\t\telse\n\t\t\tack_o <= 1'b0;")

def print_fifos(bus_type):
    if "fifos" in IP:
        addr = "adr_i"
        data = "dat_i"
        if bus_type == "APB":
            addr = "PADDR"
            data = "PWDATA"
        elif bus_type == "AHBL":
            addr = "last_HADDR"
            data = "HWDATA"
  
        for f in IP["fifos"]:
            if bus_type == "WB":
                rd = f" ack_o & ({bus_type.lower()}_re & ({addr}[`{bus_type}_AW-1:0] == {f['register']}_REG_OFFSET))"
                wr = f"ack_o & ({bus_type.lower()}_we & ({addr}[`{bus_type}_AW-1:0] == {f['register']}_REG_OFFSET))"
            else:
                rd = f"({bus_type.lower()}_re & ({addr}[`{bus_type}_AW-1:0] == {f['register']}_REG_OFFSET))"
                wr = f"({bus_type.lower()}_we & ({addr}[`{bus_type}_AW-1:0] == {f['register']}_REG_OFFSET))"
            if f['type'] == "write":
                print(f"\tassign\t{f['data_port']} = {data};") #{f['register']}_WIRE;")
                print(f"\tassign\t{f['control_port']} = {wr};")
            else:
                print(f"\tassign\t{f['register']}_WIRE = {f['data_port']};")
                print(f"\tassign\t{f['control_port']} = {rd};")

def print_bus_wrapper(bus_type):
    print_license()
    print_header(bus_type)
    print_module_header(bus_type)
    print_registers_offsets(bus_type)
    print_wires(bus_type)
    print_registers(bus_type)
    if "flags" in IP:
        print_IRQ_registers(bus_type)
    print_instance_to_wrap(bus_type)
    if bus_type == "WB":
        print_wb_dat_o(bus_type)
    else:
        print_rdata(bus_type)

    print_fifos(bus_type)
    print("endmodule")


def print_tb_duv(bus_type):
   print(f"\n\t{IP['info']['name']}_{bus_type} DUV (")
   print(f"\t\t`TB_{bus_type}_SLAVE_CONN", end="")
   if IP["external_interface"]:
       print(",")
       for index, ifc in enumerate(IP['external_interface']):
           if index != len(IP['external_interface']) - 1:
               print(f"\t\t.{ifc['name']}({ifc['name']}),")
           else:
               print(f"\t\t.{ifc['name']}({ifc['name']})")


   print("\t);")


def print_tb_reg_offsets(bus_type):
   print(f"\tlocalparam [`{bus_type}_AW-1:0]")
   for i, r in enumerate(IP['registers']):
       print(f"\t\t\t{r['name'].upper()}_REG_OFFSET =\t`{bus_type}_AW'h"+"{0:04x}".format(r['offset'])+",")
   print(f"\t\t\tIM_REG_OFFSET =\t\t`{bus_type}_AW'h" +"{0:04x}".format(IM_OFF)+",")
   print(f"\t\t\tIC_REG_OFFSET =\t\t`{bus_type}_AW'h" +"{0:04x}".format(IC_OFF)+",")
   print(f"\t\t\tRIS_REG_OFFSET =\t`{bus_type}_AW'h"  +"{0:04x}".format(RIS_OFF)+",")
   print(f"\t\t\tMIS_REG_OFFSET =\t`{bus_type}_AW'h"  +"{0:04x}".format(MIS_OFF)+";\n")


def print_tb(bus_type):
    print_license()
    print(f"/* THIS FILE IS GENERATED, edit it to complete the testbench */\n")
    print(f"`timescale\t\t1ns/1ps\n")
    print(f"`default_nettype\tnone\n")
    print(f"`define\t\t\t{bus_type}_AW\t\t\t{BUS_AW}")
    print("`define\t\t\tMS_TB_SIMTIME\t\t1_000_000\n")
    print(f"`include\t\t\"tb_macros.vh\"\n")


    print(f"module {IP['info']['name']}_{bus_type}_tb;\n")


    print("\t// Change the following parameters as desired")
    print("\tparameter real CLOCK_PERIOD = 100.0;")
    print("\tparameter real RESET_DURATION = 999.0;\n")

    print("\t// DON NOT Change the following parameters")
    print_tb_reg_offsets(bus_type)


    print(f"\t`TB_{bus_type}_SIG\n")


    if IP["external_interface"]:
        # Print details of each interface
        for index, ifc in enumerate(IP['external_interface']):
            if(ifc['direction'] == "input"):
                print("\treg\t", end='')
            else:
                print("\twire\t", end='')
            print(f"[{ifc['width']-1}:0]\t{ifc['name']};")

    if bus_type == "AHBL":
        clk = "HCLK"
        rst = "HRESETn"
        rst_pol = "1'b0"
    elif bus_type == "APB":
        clk = "PCLK"
        rst = "PRESETn"
        rst_pol = "1'b0"
    elif bus_type == "WB":
        clk = "clk_i"
        rst = "rst_i"
        rst_pol = "1'b1"

    print(f"\n\t`TB_CLK({clk}, CLOCK_PERIOD)")
    #print(f"\t`TB_SRSTN({'HRESETn' if bus_type == 'AHBL' else 'PRESETn'}, {'HCLK' if bus_type == 'AHBL' else 'PCLK'}, RESET_DURATION)")
    print(f"\t`TB_ESRST({rst}, {rst_pol}, {clk}, RESET_DURATION)")
    print(f"\t`TB_DUMP(\"{bus_type}_{IP['info']['name']}_tb.vcd\", {IP['info']['name']}_{bus_type}_tb, 0)")
    print(f"\t`TB_FINISH(`MS_TB_SIMTIME)")


    print_tb_duv(bus_type)


    print(f"\n\t`include \"{bus_type.lower()}_tasks.vh\"\n")


    print("\t`TB_TEST_EVENT(test1)\n")
    print("\tinitial begin\n"
            "\t\t#999 -> e_assert_reset;\n"
            "\t\t@(e_reset_done);\n\n"
            "\t\t// Perform Test 1\n"
            "\t\t#1000 -> e_test1_start;\n"
            "\t\t@(e_test1_done);\n\n"
            "\t\t// Perform other tests\n\n"
            "\t\t// Finish the simulation\n"
            "\t\t#1000 $finish();\n"         
            "\tend\n\n")
        
    print("\t// Test 1\n"
            "\t`TB_TEST_BEGIN(test1)"
            "\n\t\t// Test 1 code goes here\n"
            "\n\t`TB_TEST_END(test1)")


    print("endmodule")


def print_reg_def():
   ip_name = IP['info']['name'].upper()
   off = 0
   print_license()
   print(f"#ifndef {ip_name}REGS_H")
   print(f"#define {ip_name}REGS_H\n")
   print("#ifndef IO_TYPES")
   print("#define IO_TYPES")
   print("#define   __R     volatile const unsigned int")
   print("#define   __W     volatile       unsigned int")
   print("#define   __RW    volatile       unsigned int")
   print("#endif\n")
  
   for r in IP["registers"]:
       if "fields" in r:
           for f in r["fields"]:
               if not isinstance(f['bit_width'], int):
                   width = get_param_default(f['bit_width'])
               else:
                   width = f['bit_width']
               print(f"#define {ip_name}_{r['name'].upper()}_REG_{f['name'].upper()}_BIT\t{f['bit_offset']}")
               mask = hex((2**width - 1) << f['bit_offset'])
               print(f"#define {ip_name}_{r['name'].upper()}_REG_{f['name'].upper()}_MASK\t{mask}")


   print()   
   # add Int Registers fields
   if "flags" in IP:
       c = 0;
       #fcnt = len(self.ip.data["flags"])
       for flag in IP["flags"]:
           w = get_port_width(flag["port"])
           if isinstance(w, int):
               width = w
           else:
               width = get_param_default(w)
           pattern = (2**width - 1) << c
           print(f"#define {ip_name}_{flag['name'].upper()}_FLAG\t{hex(pattern)}")
           c = c + width


   print()


   print(f"typedef struct _{ip_name}_TYPE_ "+"{")
   for index, r in enumerate(IP["registers"]):
       reg_type = "__RW"
       if r["mode"] == "r":
           reg_type = "__R "
       elif r["mode"] == "w":
           reg_type = "__W "
       print(f"\t{reg_type}\t{r['name']};")
       off = off + 4
   reserved_size = int((INT_REG_OFF - off)/4)
   print(f"\t__R \treserved[{(reserved_size)}];")
   print("\t__RW\tim;")
   print("\t__R \tmis;")
   print("\t__R \tris;")
   print("\t__W \ticr;")
   print("}", end="")
   print(f" {ip_name}_TYPE;")
   print("\n#endif\n")


"""
   Print bitfield JSON for all registers
"""
def print_bf():
   for r in IP["registers"]:
       print(f"\n{r['name']}.json")
       print("<img src=\"https://svg.wavedrom.com/{reg:[", end="")
       if not "fields" in r:
           if isinstance(r["size"], int):
               size = int(r["size"])
           else:
               size = get_param_default(r["size"])
           print(f"{{name:'{r['name']}', bits:{size}}},", end="")
           print(f"{{bits: {32-size}}}" , end="")
       else:
           l = 0
           for f in r["fields"]:
               if f["bit_offset"] > l:
                   print(f"{{bits: {f['bit_offset']-l}}},", end="")
                   l = f["bit_offset"]
               if isinstance(f["bit_width"], int):
                   size = int(f["bit_width"])
               else:
                   size = get_param_default(f["bit_width"])
               l = l + size
               print(f"{{name:'{f['name']}', bits:{size}}},", end="")
           print(f"{{bits: {32-l}}}", end="")
       #print("], config: {hspace: width, lanes: 2, hflip: true}}")
       print("], config: {lanes: 2, hflip: true}} \"/>")


def print_reg_bf(r):
   print("<img src=\"https://svg.wavedrom.com/{reg:[", end="")
   if not "fields" in r:
       if isinstance(r["size"], int):
           size = int(r["size"])
       else:
           size = get_param_default(r["size"])
       print(f"{{name:'{r['name']}', bits:{size}}},", end="")
       print(f"{{bits: {32-size}}}" , end="")
   else:
       l = 0
       for f in r["fields"]:
           if f["bit_offset"] > l:
               print(f"{{bits: {f['bit_offset']-l}}},", end="")
               l = f["bit_offset"]
           if isinstance(f["bit_width"], int):
               size = int(f["bit_width"])
           else:
               size = get_param_default(f["bit_width"])
           l = l + size
           print(f"{{name:'{f['name']}', bits:{size}}},", end="")
       print(f"{{bits: {32-l}}}", end="")
       #print("], config: {hspace: width, lanes: 2, hflip: true}}")
   print("], config: {lanes: 2, hflip: true}} \"/>")


def print_md_tables():
   # Description
   # The Wrapped IP
   # Implementation Example
   # Programing Interface
   #   Registers
   #   Interrupt Flags 
   #   Interface
   #       Module Parameters
   #       Ports
   #   APIs
   # F/W Usage Guidelines
   # Installation
   # Simulation

   print(f"# {IP['info']['name']}\n")
   print(f"{IP['info']['description']}")
   print("## The wrapped IP\n")    
   if (IP['info']['bus'][0]=='generic'):
        print("\n APB, AHBL, and Wishbone wrappers, generated by the [BusWrap](https://github.com/efabless/BusWrap/tree/main) `bus_wrap.py` utility, are provided. All wrappers provide the same programmer's interface as outlined in the following sections.")
        print("\n### Wrapped IP System Integration\n")
        print("Based on your use case, use one of the provided wrappers or create a wrapper for your system bus type. For an example of how to integrate the APB wrapper:")
        print("```verilog")
        print(f"{IP['info']['name']}_APB INST (")
        print("\t`TB_APB_SLAVE_CONN,")
        if "external_interface" in IP:
            for ei in IP["external_interface"]:
                print(f"\t.{ei['name']}({ei['name']})")
        print(");")
        print("```")
        #The port `ext_in` must be connected to an input I/O pad.
        print("> **_NOTE:_** `TB_APB_SLAVE_CONN is a convenient macro provided by [BusWrap](https://github.com/efabless/BusWrap/tree/main).")
   elif (IP['info']['bus'][0]=='APB'):
        print("\n The IP comes with an APB Wrapper")
        print("\n### Wrapped IP System Integration\n")
        print("```verilog")
        print(f"{IP['info']['name']}_APB INST (")
        print("\t`TB_APB_SLAVE_CONN,")
        if "external_interface" in IP:
            for ei in IP["external_interface"]:
                print(f"\t.{ei['name']}({ei['name']})")
        print(");")
        print("```")
        print("> **_NOTE:_** `TB_APB_SLAVE_CONN is a convenient macro provided by [BusWrap](https://github.com/efabless/BusWrap/tree/main).")
   elif (IP['info']['bus'][0]=='AHBL'):
        print("\n The IP comes with an AHBL Wrapper")
        print("\n### Wrapped IP System Integration\n")
        print("```verilog")
        print(f"{IP['info']['name']}_APB INST (")
        print("\t`TB_AHBL_SLAVE_CONN,")
        if "external_interface" in IP:
            for ei in IP["external_interface"]:
                print(f"\t.{ei['name']}({ei['name']})")
        print(");")
        print("```")
        print("> **_NOTE:_** `TB_APB_SLAVE_CONN is a convenient macro provided by [BusWrap](https://github.com/efabless/BusWrap/tree/main).")
   
   print("\n## Implementation example  \n")
   print(f"The following table is the result for implementing the {IP['info']['name']} IP with different wrappers using Sky130 PDK and [OpenLane2](https://github.com/efabless/openlane2) flow.")
   print("|Module | Number of cells | Max. freq |")
   print("|---|---|---|")
   if (IP['info']['bus'][0]=='generic'):
        print(f"|{IP['info']['name']}|{IP['info']['cell_count'][0]['IP']}| {IP['info']['clock_freq_mhz'][0]['IP']} |")
        print(f"|{IP['info']['name']}_APB|{IP['info']['cell_count'][1]['APB']}|{IP['info']['clock_freq_mhz'][1]['APB']}|")
        print(f"|{IP['info']['name']}_AHBL|{IP['info']['cell_count'][2]['AHBL']}|{IP['info']['clock_freq_mhz'][2]['AHBL']}|")
        print(f"|{IP['info']['name']}_WB|{IP['info']['cell_count'][3]['WB']}|{IP['info']['clock_freq_mhz'][3]['WB']}|")
   elif (IP['info']['bus'][0]=='APB'):
        print(f"|{IP['info']['name']}|{IP['info']['cell_count'][0]['IP']}| {IP['info']['clock_freq_mhz'][0]['IP']} |")
        print(f"|{IP['info']['name']}_APB|{IP['info']['cell_count'][1]['APB']}|{IP['info']['clock_freq_mhz'][1]['APB']}|")
   elif (IP['info']['bus'][0]=='AHBL'):
        print(f"|{IP['info']['name']}|{IP['info']['cell_count'][0]['IP']}| {IP['info']['clock_freq_mhz'][0]['IP']} |")
        print(f"|{IP['info']['name']}_AHBL|{IP['info']['cell_count'][1]['AHBL']}|{IP['info']['clock_freq_mhz'][1]['AHBL']}|")
   elif (IP['info']['bus'][0]=='WB'):
        print(f"|{IP['info']['name']}|{IP['info']['cell_count'][0]['IP']}| {IP['info']['clock_freq_mhz'][0]['IP']} |")
        print(f"|{IP['info']['name']}_WB|{IP['info']['cell_count'][1]['WB']}|{IP['info']['clock_freq_mhz'][1]['WB']}|")
  
   if "registers" in IP:

        print("## The Programming Interface\n")
        print("\n### Registers\n")

        print("|Name|Offset|Reset Value|Access Mode|Description|")
        print("|---|---|---|---|---|")
        for r in IP["registers"]:
            if isinstance(r["size"], int):
                size = int(r["size"])
            else:
                size = get_param_default(r["size"])
            if "init" in r:
                reset_value = '0x' + r["init"].strip("'h?").zfill(8)
            else:
                reset_value = "0x00000000"
            print("|{0}|{1}|{2}|{3}|{4}|".format(r["name"], hex(r["offset"])[2:].zfill(4), reset_value, r["mode"], r["description"]))
   if "flags" in IP:
       print("|{0}|{1}|{2}|{3}|{4}|".format("IM", hex(IM_OFF)[2:].zfill(4), "0x00000000", "w", "Interrupt Mask Register; write 1/0 to enable/disable interrupts; check the interrupt flags table for more details"))
       print("|{0}|{1}|{2}|{3}|{4}|".format("RIS", hex(RIS_OFF)[2:].zfill(4), "0x00000000", "w", "Raw Interrupt Status; reflects the current interrupts status;check the interrupt flags table for more details"))
       print("|{0}|{1}|{2}|{3}|{4}|".format("MIS", hex(MIS_OFF)[2:].zfill(4), "0x00000000", "w", "Masked Interrupt Status; On a read, this register gives the current masked status value of the corresponding interrupt. A write has no effect; check the interrupt flags table for more details"))
       print("|{0}|{1}|{2}|{3}|{4}|".format("IC", hex(IC_OFF)[2:].zfill(4), "0x00000000", "w", "Interrupt Clear Register; On a write of 1, the corresponding interrupt (both raw interrupt and masked interrupt, if enabled) is cleared; check the interrupt flags table for more details"))


   if "registers" in IP:
        for r in IP["registers"]:
            print(f"\n### {r['name']} Register [Offset: {hex(r['offset'])}, mode: {r['mode']}]")
            print(f"\n{r['description']}")
            print_reg_bf(r)
            if "fields" in r:
                print("\n|bit|field name|width|description|")
                print("|---|---|---|---|")
                for f in r["fields"]:
                    if isinstance(f["bit_width"], int):
                        width = int(f["bit_width"])
                    else:
                        width = get_param_default(f["bit_width"])
                    print("|{0}|{1}|{2}|{3}|".format(f["bit_offset"], f["name"], width, f["description"]))
            print()
      
   if "flags" in IP:
       c = 0;
       print("\n### Interrupt Flags\n")
       print("The wrapped IP provides four registers to deal with interrupts: IM, RIS, MIS and IC. These registers exist for all wrapper types generated by the [BusWrap](https://github.com/efabless/BusWrap/tree/main) `bus_wrap.py` utility. \n\nEach register has a group of bits for the interrupt sources/flags.")
       print("- `IM`: is used to enable/disable interrupt sources.\n")
       print("- `RIS`: has the current interrupt status (interrupt flags) whether they are enabled or disabled.\n")
       print("- `MIS`: is the result of masking (ANDing) RIS by IM.\n")
       print("- `IC`: is used to clear an interrupt flag.\n")
       print("\nThe following are the bit definitions for the interrupt registers:\n")
       print("|Bit|Flag|Width|Description|")
       print("|---|---|---|---|")
       for flag in IP["flags"]:
           width = get_port_width(flag["port"])
           if isinstance(width, int):
               w = width
           else:
               w = get_param_default(width)
           print(f"|{c}|{flag['name'].upper()}|{w}|{flag['description']}|")
           c += w


   print("\n### The Interface \n")
  
   if "parameters" in IP:
       print("\n#### Module Parameters \n")
       print("|Parameter|Description|Default Value|")
       print("|---|---|---|")      
       for parameter in IP["parameters"]:
           print(f"|{parameter['name']}|{parameter['description']}|{parameter['default']}|")
  
   print("\n#### Ports \n")
   print("|Port|Direction|Width|Description|")
   print("|---|---|---|---|")
   for port in IP["external_interface"]:
       print(f"|{port['name']}|{port['direction']}|{port['width']}|{port['description']}|")      
   for port in IP["ports"]:
       print(f"|{port['name']}|{port['direction']}|{port['width']}|{port['description']}|")
  
   print ("## F/W Usage Guidelines:")

   print ("## Installation:")
   print ("You can either clone repo or use [IPM](https://github.com/efabless/IPM) which is an open-source IPs Package Manager")
   print ("* To clone repo:")
   print(f"```git clone https://{IP['info']['repo']}```")
   print("* To download via IPM , follow installation guides [here](https://github.com/efabless/IPM/blob/main/README.md) then run ")
   print(f"```ipm install {IP['info']['name']}```")

    # print ("## Simulation:")
    # print ("### Run Verilog Testbench:")
    # print ("1. Clone [IP_Utilities](https://github.com/shalan/IP_Utilities) repo in the same directory as the IP")
    # print (f"2. In the directory ``{IP['info']['name']}/verify/utb/`` run ``make APB-RTL`` to run testbench for APB or ``make AHBL-RTL`` to run testbench for AHBL")
   print ("### Run cocotb UVM Testbench:")
   print ("In IP directory run:")
   print (" ```shell")
   print (" cd verify/uvm-python/")
   print (" ```")
   print (" ##### To run testbench for design with APB ")
   print (" To run all tests:")
   print (" ```shell")
   print (" make run_all_tests BUS_TYPE=APB")                    
   print (" ```")
   print (" To run a certain test:")
   print (" ```shell")
   print (" make run_<test_name> BUS_TYPE=APB")
   print (" ```")
   print (" To run all tests with a tag: ")
   print (" ```shell")
   print (" make run_all_tests TAG=<new_tag> BUS_TYPE=APB")
   print (" ```")
   print (" ##### To run testbench for design with APB") 
   print (" To run all tests:")
   print (" ```shell")
   print (" make run_all_tests BUS_TYPE=AHB")                    
   print (" ```")
   print (" To run a certain test:")
   print (" ```shell")
   print (" make run_<test_name> BUS_TYPE=AHB")
   print (" ```")
   print (" To run all tests with a tag: ")
   print (" ```shell")
   print (" make run_all_tests TAG=<new_tag> BUS_TYPE=AHB")
   print ("```")
          
      
def print_help():
   print(f"Usage: {sys.argv[0]} ip.yml|ip.json -apb|-ahbl|-wb -tb|-ch|-md")
   print("Options:")
   print("\t-apb : generate APB wrapper")
   print("\t-ahbl: generate AHBL wrapper")
   print("\t-tb  : generate a Verilog testbench for the generated bus wrapper")
   print("\t-ch  : generate a C header file containing the register definitions")
   print("Arguments:")
   print("\tip.yml: A YAML file that contains the IP definition")


def exit_with_message(msg):
   print(msg)
   sys.exit(f"Usage: {sys.argv[0]} ip.yml|ip.json -apb|-ahbl|-wb -tb|-ch|-md")   


def main():
    global IP

    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

    if "--help" in opts:
        print_help()
        sys.exit(0)

    if "-apb" in opts:
        bus_type = "APB"
    elif "-ahbl" in opts:   
        bus_type = "AHBL"
    elif "-wb" in opts:   
        bus_type = "WB"
        
    else:
        exit_with_message("You must specify a bus type using -apb or -ahbl option.")

    if ".yaml" not in args[0] and ".yml" not in args[0] and ".json" not in args[0]:
        exit_with_message("First argument must be an IP description file in YAML or JSON format.")
    
    if ".json" in args[0]:
        with open(args[0], "r") as jfile:
            try:
                IP = json.load(jfile)
            except Exception:
                raise sys.exit("Error loading the JSON file! Please check the file for syntax errors; you may use jsonlint for this.")
    else:   
        with open(args[0], "r") as stream:
            try:
                IP=yaml.safe_load(stream)
            except Exception:
                raise sys.exit("Error loading the YAML file! Please check the file for syntax errors; you may use yamllint for this.")

    if "-tb" in opts:
        print_tb(bus_type)
    elif "-ch" in opts:
        print_reg_def()
    elif "-md" in opts:
        print_md_tables()
        #print_bf()
    else:
        print_bus_wrapper(bus_type)
  
if __name__ == '__main__':
   main()
