/*
	Copyright 2020 AUCOHL

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
*/

`define     WB_BLOCK(name, init)        always @(posedge clk_i or posedge rst_i) if(rst_i) name <= init;

`define     WB_REG(name, init, size)    `WB_BLOCK(name, init) else if(wb_we & (adr_i[`WB_AW-1:0]==``name``_OFFSET)) name <= dat_i[size-1:0];

`define     WB_REG_AC(name, init, size, pat)    `WB_BLOCK(name, init) else if(wb_we & (adr_i[`WB_AW-1:0]==``name``_OFFSET)) name <= dat_i[size-1:0]; else name <= pat & name;

`define     WB_AUTO_CLR_REG(name, init, size)    `WB_BLOCK(name, init) else if(wb_we & (adr_i[`WB_AW-1:0]==``name``_OFFSET)) name <= dat_i[size-1:0]; else name <= 'b0;

`define     WB_CTRL_SIGNALS             wire            wb_valid    = cyc_i & stb_i;\
                                        wire            wb_we       = we_i & wb_valid;\
                                        wire            wb_re       = ~we_i & wb_valid;\
                                        wire[3:0]       wb_byte_sel = sel_i & {4{wb_we}};

`define     WB_IC_REG(sz)               `WB_BLOCK(IC_REG, sz'b0) \
                                        else if(wb_we & (adr_i[`WB_AW-1:0]==IC_REG_OFFSET)) \
                                            IC_REG <= dat_i[``sz``-1:0]; \
                                        else \ 
                                            IC_REG <= sz'd0;

`define     WB_SLAVE_PORTS              input   wire            ext_clk,\
                                        input   wire            clk_i,\
                                        input   wire            rst_i,\
                                        input   wire [31:0]     adr_i,\
                                        input   wire [31:0]     dat_i,\
                                        output  wire [31:0]     dat_o,\
                                        input   wire [3:0]      sel_i,\
                                        input   wire            cyc_i,\
                                        input   wire            stb_i,\
                                        output  reg             ack_o,\
                                        input   wire            we_i,\
                                        output  wire            IRQ
                                        
`define     WB_MIS_REG(size)           wire[size-1:0]      MIS_REG	= RIS_REG & IM_REG;