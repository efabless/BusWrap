/*
	Copyright (C) 2020 AUCOHL
    
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

`define     TB_CLK(clk, period)                 reg clk=0; always #(period/2) clk = !clk;
`define     TB_SRSTN(rstn, clk, duration)       reg rstn=0; initial begin #duration; @(posedge clk) rstn = 1; end
`define     TB_ESRST(rst, pol, clk, duration)   reg rst=1'bx;\ 
                                                event e_assert_reset, e_reset_done; \
                                                initial forever begin \
                                                    @(e_assert_reset); \
                                                    rst = pol; \
                                                    #duration; \
                                                    @(posedge clk) rst = ~pol; \
                                                    -> e_reset_done; \
                                                end
`define     TB_DUMP(file, mod, level)           initial begin $dumpfile(file); $dumpvars(level, mod); end
`define     TB_FINISH(length)                   initial begin #``length``; $display("Verification Failed: Timeout");$finish; end
`define     TB_WAIT_FOR_CLOCK_CYC(clk, count)   repeat(count) begin @(posedge clk) end
`define     TB_TEST_EVENT(name)                 event e_``name``_start, e_``name``_done;
`define     TB_TEST_BEGIN(name)                 initial  begin : name \
                                                @(e_``name``_start);
`define     TB_TEST_END(name)                   -> e_``name``_done; \
                                                end 
`define     TB_APB_SIG                          reg PWRITE, PENABLE, PSEL; reg [31:0] PWDATA, PADDR; wire PREADY; wire [31:0] PRDATA; wire IRQ;
`define     TB_AHBL_SIG                          reg HWRITE, HSEL; reg [2:0] HSIZE; reg [1:0] HTRANS; reg [31:0] HWDATA, HADDR; reg HREADY; wire HREADYOUT; wire [31:0] HRDATA; wire IRQ;
`define     TB_WB_SIG                           reg cyc_i, stb_i, we_i; reg [3:0] sel_i; reg [31:0] adr_i, dat_i; wire ack_o; wire[31:0]  dat_o; wire IRQ;
`define     TB_AHBL_SLAVE_CONN                   .HCLK(HCLK),\
                                                .HRESETn(HRESETn),\
                                                .HSEL(HSEL),\
                                                .HADDR(HADDR),\
                                                .HTRANS(HTRANS),\
                                                .HWDATA(HWDATA),\
                                                .HWRITE(HWRITE),\
                                                .HREADY(HREADY),\
                                                .HREADYOUT(HREADYOUT),\
                                                .HRDATA(HRDATA),\
                                                .IRQ(IRQ)
`define     TB_APB_SLAVE_CONN                   .PCLK(PCLK),\
                                                .PRESETn(PRESETn),\
                                                .PWRITE(PWRITE),\
                                                .PWDATA(PWDATA),\
                                                .PADDR(PADDR),\
                                                .PENABLE(PENABLE),\
                                                .PSEL(PSEL),\
                                                .PREADY(PREADY),\
                                                .PRDATA(PRDATA),\
                                                .IRQ(IRQ)

`define     TB_WB_SLAVE_CONN                    .clk_i(clk_i), \
                                                .rst_i(rst_i), \
                                                .cyc_i(cyc_i), \
                                                .stb_i(stb_i), \
                                                .we_i(we_i), \ 
                                                .sel_i(sel_i), \ 
                                                .adr_i(adr_i), \ 
                                                .dat_i(dat_i), \ 
                                                .ack_o(ack_o), \ 
                                                .dat_o(dat_o), \
                                                .IRQ(IRQ)
                                                


