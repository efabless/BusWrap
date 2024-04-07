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

task WB_W_WRITE(input [31:0] addr, input [31:0] data);
    begin : task_body
        @(posedge clk_i);
        #1;
        cyc_i   = 1;
        stb_i   = 1;
        we_i    = 1;
        adr_i   = addr;
        dat_i   = data;
        sel_i   = 4'hF;
        wait (ack_o == 1);
        @(posedge clk_i);
        cyc_i   = 0;
        stb_i   = 0;
    end
endtask

task WB_W_READ(input [31:0] addr, output [31:0] data);
    begin : task_body
        @(posedge clk_i);
        #1;
        cyc_i   = 1;
        stb_i   = 1;
        we_i    = 0;
        adr_i   = addr;
        dat_i   = 0;
        sel_i   = 4'hF;
        wait (ack_o == 1);
        @(posedge clk_i);
        data    = dat_o;
        cyc_i   = 0;
        stb_i   = 0;
    end
endtask