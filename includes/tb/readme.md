# Verification Macros and Tasks

A set of Verilog tasks and macros that makes it easy to develop testbenches for IPs and their generated wrappers.

## ahbl_tasks.vh

Contains two tasks to simulate an AHB Lite master reading and writing a 32-bit data word from/to the bus. 

- `AHBL_W_READ (input [31:0] addr, output [31:0] data)`
- `AHBL_W_WRITE (input [31:0] addr, output [31:0] data)`

## apb_tasks.vh

Contains two tasks to simulate an APB master reading and writing a 32-bit data word from/to the bus.

- `APB_W_READ (input [31:0] addr, output [31:0] data)`
- `APB_W_WRITE (input [31:0] addr, output [31:0] data)`

## tb_macros.vh

Contains a set of convenience macros that provides the testbench infrastructure. 

- `TB_CLK(clk, period)` : Creates a clock with the given period.
- `TB_SRSTN(rstn, clk, duration)` : Create a synchronous active low reset signal for a certain duration.
- `TB_ESRST(rst, pol, clk, duration)` : Generates a synchronous reset signal with a certain polarization for a certain duration of time. The rest is asserted upon firing the vent `e_assert_reset`. Once the reset is done, the event `e_reset_done` will be fired to notify the testbench.
- `TB_DUMP(file, mod, level)` : Dump VCD file for a certain module and hierarchy level.
- `TB_FINISH(length) ` : Ends the simulation after some amount of time. 
- `TB_WAIT_FOR_CLOCK_CYC(clk, count)` : Waits for a number of clock ccycles.
- `TB_TEST_EVENT(name)` : Declares a test related event objects.
- `TB_TEST_BEGIN(name)` : Starts a test definition.
- `TB_TEST_END(name)` : Ends the test definition.
- `TB_APB_SIG` : APB Signals needed to connect a slave to the APB.
- `TB_AHBL_SIG` : AHBL Signals needed to connect a slave to a AHB lite bus.
- `TB_WB_SIG` : Wishbone Bus (WB) Signals needed to connect a slave to a AHB lite bus.
- `TB_AHBL_SLAVE_CONN` : The AHBL slave instance port connections to the bus.
- `TB_APB_SLAVE_CONN` : The APB slave instance port connections to the bus.