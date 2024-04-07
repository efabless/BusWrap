task send_serial_8N1(   input real bit_duration, 
                        input [7:0] data); 
    begin : send_serial_8N1_body
        integer i;
        vip_tx = 1'b0;
        #bit_duration;
        for(i=0; i<8; i=i+1) begin
            vip_tx = data[i];
            #bit_duration;
        end
        vip_tx = 1'b1;
        #bit_duration;
    end
endtask