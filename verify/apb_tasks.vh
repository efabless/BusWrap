/*
	Copyright (C) 2020 AUCOH
    
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

task APB_W_WRITE (input [31:0] address, input [31:0] data );
    begin
        @(posedge PCLK);
        PSEL    = 1;
        PWRITE  = 1;
        PWDATA  = data;
        PENABLE = 0;
        PADDR   = address;
        @(posedge PCLK);
        PENABLE = 1;
        @(posedge PCLK);
        PSEL    = 0;
        PWRITE  = 0;
        PENABLE = 0;
    end
endtask
		
task APB_W_READ(input [31:0] address, output [31:0] data );
    begin
        @(posedge PCLK);
        PSEL    = 1;
        PWRITE  = 0;
        PENABLE = 0;
        PADDR   = address;
        @(posedge PCLK);
        PENABLE = 1;
        @(posedge PCLK);
        wait(PREADY == 1)
        data    = PRDATA;
        PSEL    = 0;
        PWRITE  = 0;
        PENABLE = 0;
    end
endtask