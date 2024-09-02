# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: MIT
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")
    # Set the clock period to 20 ns ( 50 MHz)
    clock = Clock(dut.clk, 20, units="ns")
    cocotb.start_soon(clock.start())
	
    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    dut._log.info("Test project behavior")
	
    # uio_in[7:0] = [wr_en,   sel,     0, out_en, in[11], in[10], in[9], in[8]] 
    # ui_in [7:0] = [in[7], in[6], in[5],  in[4],  in[3],  in[2], in[1], in[0]]
    # uo_out[0]   = pwm_out
	
#----------- TEST1 ---------------

    # Set the input values for duty cycles
    dut.ui_in.value = 50	# duty 50%
    dut.uio_in.value = 160	# uio_in = [1, 0, 1, 0, 0, 0, 0, 0]
	
    # Wait for one clock cycle to see the output values
    await ClockCycles(dut.clk, 2)
    duty = int(dut.ui_in.value)	# store duty cycle value 
    # Set the input values for period
	
    dut.ui_in.value = 4 	# period = 4 ==> fq = 12.5MHz
    dut.uio_in.value = 224	# uio_in = [1, 1, 1, 0, 0, 0, 0, 0]
    await ClockCycles(dut.clk, 2)
    period = int(dut.ui_in.value)
    await ClockCycles(dut.clk, dut.ui_in.value)
	
    t_on = int((duty*period)/100)
	
    val = []
	
    for i in range(dut.ui_in.value):
        await ClockCycles(dut.clk, 1)
#       dut._log.info("pwm_out : %s",dut.uo_out.value); 
        val.append(int(dut.uo_out.value))
		
#    if val.count(1) == t_on:
#       print("\n		TEST TRECUT")
#    else: 
#        print("\n		TEST PICAT")
    #val.reverse()
#    print(val)

    assert val.count(1) == t_on
	
#------------ TEST2 ----------------

    # Set the input values for duty cycles
    dut.ui_in.value = 30	# duty 30%
    dut.uio_in.value = 160	# uio_in = [1, 0, 1, 0, 0, 0, 0, 0]
	
    await ClockCycles(dut.clk, 2)
    duty = int(dut.ui_in.value)	# store duty cycle value 
	
    # Set the input values for period
    dut.ui_in.value = 144 	# period = 100 ==> fq = 5MHz
    dut.uio_in.value = 224	# uio_in = [1, 1, 1, 0, 0, 0, 0, 0]
	
    await ClockCycles(dut.clk, 2)
    period = int(dut.ui_in.value)
	
    await ClockCycles(dut.clk, dut.ui_in.value)
	
    t_on = int((duty*period)/100)
	
    val = []
    for i in range(dut.ui_in.value):
        await ClockCycles(dut.clk, 1)
        # dut._log.info("pwm_out : %s",dut.uo_out.value); 
        val.append(int(dut.uo_out.value))
		
    assert val.count(1) == t_on
