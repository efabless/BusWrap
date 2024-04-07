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

`define		AHBL_BLOCK(name, init)		always @(posedge HCLK or negedge HRESETn) if(~HRESETn) name <= init;

`define     AHBL_CTRL_SIGNALS           reg  last_HSEL, last_HWRITE; reg [31:0] last_HADDR; reg [1:0] last_HTRANS;\
                                        always@ (posedge HCLK) begin \
                                            if(HREADY) begin\
                                                last_HSEL       <= HSEL;\
                                                last_HADDR      <= HADDR;\
                                                last_HWRITE     <= HWRITE;\
                                                last_HTRANS     <= HTRANS;\
                                            end\
                                        end\
                                        wire    ahbl_valid	= last_HSEL & last_HTRANS[1];\
	                                    wire	ahbl_we	= last_HWRITE & ahbl_valid;\
	                                    wire	ahbl_re	= ~last_HWRITE & ahbl_valid;

`define		AHBL_REG(name, init, size)	`AHBL_BLOCK(name, init)\
                                        else if(ahbl_we & (last_HADDR[`AHBL_AW-1:0]==``name``_OFFSET)) \
                                            name <= HWDATA[``size``-1:0];

`define		AHBL_IC_REG(size)			`AHBL_BLOCK(IC_REG, ``size``'b0)\ 
                                        else if(ahbl_we & (last_HADDR[`AHBL_AW-1:0]==IC_REG_OFFSET)) \
                                            IC_REG <= HWDATA[``size``-1:0]; \
                                        else IC_REG <= ``size``'d0;

`define     AHBL_SLAVE_PORTS            input wire          HCLK,\
                                        input wire          HRESETn,\
                                        input wire          HWRITE,\
                                        input wire [31:0]   HWDATA,\
                                        input wire [31:0]   HADDR,\
                                        input wire [1:0]    HTRANS,\
                                        input wire          HSEL,\
                                        input wire          HREADY,\
                                        output wire         HREADYOUT,\
                                        output wire [31:0]  HRDATA,\
                                        output wire         IRQ\

`define     AHBL_MIS_REG(size)          wire[size-1:0]      MIS_REG	= RIS_REG & IM_REG;
