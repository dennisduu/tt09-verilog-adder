# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
import random

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Apply reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)  # Keep reset active for a few cycles
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 5)  # Wait for a few cycles after releasing reset

    dut._log.info("Test project behavior")

    for i in range(1000):
        # Generate random values for a and b in the range of 0 to 15 (4-bit inputs)
        a = random.randint(0, 15)
        b = random.randint(0, 15)

        # Assign random values to inputs
        dut.ui_in.value = (b << 4) | a  # Assign 4 bits of `b` to upper 4 bits, `a` to lower 4 bits

        # Wait for 10 clock cycles to settle
        await ClockCycles(dut.clk, 10)

        # Expected values for sum and carry_out
        expected_sum = (a + b) & 0xF  # Lower 4 bits of the sum
        expected_carry_out = (a + b) >> 4  # Carry-out from the addition

        dut._log.info(f"Test {i + 1}: a={a}, b={b}, sum={dut.uo_out[3:0].value}, carry_out={dut.uo_out[4].value}")

        # Check if the sum and carry_out match the expected values
        assert dut.uo_out[3:0].value == expected_sum, f"Test failed for a={a}, b={b}: expected sum={expected_sum}, got {dut.uo_out[3:0].value}"
        assert dut.uo_out[4].value == expected_carry_out, f"Test failed for a={a}, b={b}: expected carry_out={expected_carry_out}, got {dut.uo_out[4].value}"

    dut._log.info("All 1000 test cases passed.")



    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
    
