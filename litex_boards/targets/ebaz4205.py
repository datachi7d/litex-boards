#!/usr/bin/env python3

#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2019-2020 Florent Kermarrec <florent@enjoy-digital.fr>,
# Copyright (c) 2021 Dhiru Kholia <dhiru.kholia@gmail.com>,
# SPDX-License-Identifier: BSD-2-Clause

from migen import *

from litex_boards.platforms import ebaz4205
from litex.build.xilinx.vivado import vivado_build_args, vivado_build_argdict

from litex.soc.interconnect import axi
from litex.soc.interconnect import wishbone

from litex.soc.cores.clock import *
from litex.soc.integration.soc_core import *
from litex.soc.integration.soc import SoCRegion
from litex.soc.integration.builder import *
from litex.soc.cores.led import LedChaser

# CRG ----------------------------------------------------------------------------------------------

class _CRG(Module):
    def __init__(self, platform, sys_clk_freq, use_ps7_clk=False):
        self.rst = Signal()
        self.clock_domains.cd_sys = ClockDomain()

        # # #

        if use_ps7_clk:
            assert sys_clk_freq == 100e6
            self.comb += ClockSignal("sys").eq(ClockSignal("ps7"))
            self.comb += ResetSignal("sys").eq(ResetSignal("ps7") | self.rst)
        else:
            self.submodules.pll = pll = S7PLL(speedgrade=-1)
            self.comb += pll.reset.eq(self.rst)
            pll.register_clkin(platform.request("clk25"), 25e6)
            pll.create_clkout(self.cd_sys, sys_clk_freq)

# BaseSoC ------------------------------------------------------------------------------------------

class BaseSoC(SoCCore):
    def __init__(self, sys_clk_freq=int(100e6), with_led_chaser=True, toolchain="vivado", variant="z7-10", **kwargs):
        platform = ebaz4205.Platform()

        # CRG --------------------------------------------------------------------------------------
        self.submodules.crg = _CRG(platform, sys_clk_freq, True)

        # SoCCore ----------------------------------------------------------------------------------
        if kwargs.get("cpu_type", None) == "zynq7000":
            kwargs["integrated_sram_size"] = 0

            self.mem_map = {
                'csr': 0x43c0_0000,  # Zynq GP0 default
            }

        SoCCore.__init__(self, platform, sys_clk_freq, ident="LiteX SoC on EBAZ4205", **kwargs)

        # Zynq7000 Integration ---------------------------------------------------------------------
        if kwargs.get("cpu_type", None) == "zynq7000":
            assert toolchain == "vivado", ' not tested / specific vivado cmds'
            del self.cpu.cpu_params['i_USB0_VBUS_PWRFAULT']

            del self.cpu.cpu_params['i_ENET0_MDIO_I']
            del self.cpu.cpu_params['o_ENET0_MDIO_O']
            del self.cpu.cpu_params['o_ENET0_MDIO_T']

            del self.cpu.cpu_params['o_ENET0_GMII_TX_ER']
            del self.cpu.cpu_params['i_ENET0_GMII_COL']
            del self.cpu.cpu_params['i_ENET0_GMII_CRS']
            del self.cpu.cpu_params['i_ENET0_GMII_RX_ER']

            self.cpu.set_ps7(name="ebaz",
                             config={
                                 "PCW_UART0_BASEADDR": "0xE0000000",
                                 "PCW_UART0_HIGHADDR": "0xE0000FFF",
                                 "PCW_ENET0_BASEADDR": "0xE000B000",
                                 "PCW_ENET0_HIGHADDR": "0xE000BFFF",
                                 "PCW_ACT_APU_PERIPHERAL_FREQMHZ": "666.666687",
                                 "PCW_ACT_CAN_PERIPHERAL_FREQMHZ": "10.000000",
                                 "PCW_ACT_DCI_PERIPHERAL_FREQMHZ": "10.158730",
                                 "PCW_ACT_ENET0_PERIPHERAL_FREQMHZ": "25.000000",
                                 "PCW_ACT_ENET1_PERIPHERAL_FREQMHZ": "10.000000",
                                 "PCW_ACT_FPGA0_PERIPHERAL_FREQMHZ": "50.000000",
                                 "PCW_ACT_FPGA1_PERIPHERAL_FREQMHZ": "10.000000",
                                 "PCW_ACT_FPGA2_PERIPHERAL_FREQMHZ": "10.000000",
                                 "PCW_ACT_FPGA3_PERIPHERAL_FREQMHZ": "25.000000",
                                 "PCW_ACT_PCAP_PERIPHERAL_FREQMHZ": "200.000000",
                                 "PCW_ACT_QSPI_PERIPHERAL_FREQMHZ": "10.000000",
                                 "PCW_ACT_SDIO_PERIPHERAL_FREQMHZ": "25.000000",
                                 "PCW_ACT_SMC_PERIPHERAL_FREQMHZ": "100.000000",
                                 "PCW_ACT_SPI_PERIPHERAL_FREQMHZ": "10.000000",
                                 "PCW_ACT_TPIU_PERIPHERAL_FREQMHZ": "200.000000",
                                 "PCW_ACT_TTC0_CLK0_PERIPHERAL_FREQMHZ": "111.111115",
                                 "PCW_ACT_TTC0_CLK1_PERIPHERAL_FREQMHZ": "111.111115",
                                 "PCW_ACT_TTC0_CLK2_PERIPHERAL_FREQMHZ": "111.111115",
                                 "PCW_ACT_TTC1_CLK0_PERIPHERAL_FREQMHZ": "111.111115",
                                 "PCW_ACT_TTC1_CLK1_PERIPHERAL_FREQMHZ": "111.111115",
                                 "PCW_ACT_TTC1_CLK2_PERIPHERAL_FREQMHZ": "111.111115",
                                 "PCW_ACT_UART_PERIPHERAL_FREQMHZ": "100.000000",
                                 "PCW_ACT_WDT_PERIPHERAL_FREQMHZ": "111.111115",
                                 "PCW_ARMPLL_CTRL_FBDIV": "40",
                                 "PCW_CAN_PERIPHERAL_DIVISOR0": "1",
                                 "PCW_CAN_PERIPHERAL_DIVISOR1": "1",
                                 "PCW_CLK0_FREQ": "50000000",
                                 "PCW_CLK1_FREQ": "10000000",
                                 "PCW_CLK2_FREQ": "10000000",
                                 "PCW_CLK3_FREQ": "25000000",
                                 "PCW_CPU_CPU_PLL_FREQMHZ": "1333.333",
                                 "PCW_CPU_PERIPHERAL_DIVISOR0": "2",
                                 "PCW_DCI_PERIPHERAL_DIVISOR0": "15",
                                 "PCW_DCI_PERIPHERAL_DIVISOR1": "7",
                                 "PCW_DDRPLL_CTRL_FBDIV": "32",
                                 "PCW_DDR_DDR_PLL_FREQMHZ": "1066.667",
                                 "PCW_DDR_PERIPHERAL_DIVISOR0": "2",
                                 "PCW_DDR_RAM_HIGHADDR": "0x0FFFFFFF",
                                 "PCW_ENET0_ENET0_IO": "EMIO",
                                 "PCW_ENET0_GRP_MDIO_ENABLE": "1",
                                 "PCW_ENET0_GRP_MDIO_IO": "EMIO",
                                 "PCW_ENET0_PERIPHERAL_CLKSRC": "External",
                                 "PCW_ENET0_PERIPHERAL_DIVISOR0": "1",
                                 "PCW_ENET0_PERIPHERAL_DIVISOR1": "5",
                                 "PCW_ENET0_PERIPHERAL_ENABLE": "1",
                                 "PCW_ENET0_PERIPHERAL_FREQMHZ": "100 Mbps",
                                 "PCW_ENET0_RESET_ENABLE": "0",
                                 "PCW_ENET1_PERIPHERAL_DIVISOR0": "1",
                                 "PCW_ENET1_PERIPHERAL_DIVISOR1": "1",
                                 "PCW_ENET1_RESET_ENABLE": "0",
                                 "PCW_ENET_RESET_ENABLE": "1",
                                 "PCW_ENET_RESET_SELECT": "Share reset pin",
                                 "PCW_EN_CLK3_PORT": "1",
                                 "PCW_EN_EMIO_CD_SDIO0": "0",
                                 "PCW_EN_EMIO_ENET0": "1",
                                 "PCW_EN_EMIO_GPIO": "1",
                                 "PCW_EN_ENET0": "1",
                                 "PCW_EN_GPIO": "1",
                                 "PCW_EN_SDIO0": "1",
                                 "PCW_EN_SMC": "1",
                                 "PCW_EN_UART1": "1",
                                 "PCW_FCLK0_PERIPHERAL_DIVISOR0": "7",
                                 "PCW_FCLK0_PERIPHERAL_DIVISOR1": "4",
                                 "PCW_FCLK1_PERIPHERAL_DIVISOR0": "1",
                                 "PCW_FCLK1_PERIPHERAL_DIVISOR1": "1",
                                 "PCW_FCLK2_PERIPHERAL_DIVISOR0": "1",
                                 "PCW_FCLK2_PERIPHERAL_DIVISOR1": "1",
                                 "PCW_FCLK3_PERIPHERAL_DIVISOR0": "8",
                                 "PCW_FCLK3_PERIPHERAL_DIVISOR1": "7",
                                 "PCW_FCLK_CLK3_BUF": "TRUE",
                                 "PCW_FPGA3_PERIPHERAL_FREQMHZ": "25",
                                 "PCW_FPGA_FCLK0_ENABLE": "1",
                                 "PCW_FPGA_FCLK1_ENABLE": "0",
                                 "PCW_FPGA_FCLK2_ENABLE": "0",
                                 "PCW_FPGA_FCLK3_ENABLE": "1",
                                 "PCW_GPIO_EMIO_GPIO_ENABLE": "1",
                                 "PCW_GPIO_EMIO_GPIO_IO": "64",
                                 "PCW_GPIO_EMIO_GPIO_WIDTH": "64",
                                 "PCW_GPIO_MIO_GPIO_ENABLE": "1",
                                 "PCW_GPIO_MIO_GPIO_IO": "MIO",
                                 "PCW_I2C0_RESET_ENABLE": "0",
                                 "PCW_I2C1_RESET_ENABLE": "0",
                                 "PCW_I2C_PERIPHERAL_FREQMHZ": "25",
                                 "PCW_I2C_RESET_ENABLE": "1",
                                 "PCW_IOPLL_CTRL_FBDIV": "42",
                                 "PCW_IO_IO_PLL_FREQMHZ": "1400.000",
                                 "PCW_MIO_0_DIRECTION": "out",
                                 "PCW_MIO_0_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_0_PULLUP": "disabled",
                                 "PCW_MIO_0_SLEW": "slow",
                                 "PCW_MIO_10_DIRECTION": "inout",
                                 "PCW_MIO_10_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_10_PULLUP": "enabled",
                                 "PCW_MIO_10_SLEW": "slow",
                                 "PCW_MIO_11_DIRECTION": "inout",
                                 "PCW_MIO_11_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_11_PULLUP": "enabled",
                                 "PCW_MIO_11_SLEW": "slow",
                                 "PCW_MIO_12_DIRECTION": "inout",
                                 "PCW_MIO_12_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_12_PULLUP": "enabled",
                                 "PCW_MIO_12_SLEW": "slow",
                                 "PCW_MIO_13_DIRECTION": "inout",
                                 "PCW_MIO_13_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_13_PULLUP": "enabled",
                                 "PCW_MIO_13_SLEW": "slow",
                                 "PCW_MIO_14_DIRECTION": "in",
                                 "PCW_MIO_14_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_14_PULLUP": "disabled",
                                 "PCW_MIO_14_SLEW": "slow",
                                 "PCW_MIO_15_DIRECTION": "inout",
                                 "PCW_MIO_15_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_15_PULLUP": "enabled",
                                 "PCW_MIO_15_SLEW": "slow",
                                 "PCW_MIO_16_DIRECTION": "inout",
                                 "PCW_MIO_16_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_16_PULLUP": "enabled",
                                 "PCW_MIO_16_SLEW": "slow",
                                 "PCW_MIO_17_DIRECTION": "inout",
                                 "PCW_MIO_17_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_17_PULLUP": "enabled",
                                 "PCW_MIO_17_SLEW": "slow",
                                 "PCW_MIO_18_DIRECTION": "inout",
                                 "PCW_MIO_18_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_18_PULLUP": "enabled",
                                 "PCW_MIO_18_SLEW": "slow",
                                 "PCW_MIO_19_DIRECTION": "inout",
                                 "PCW_MIO_19_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_19_PULLUP": "enabled",
                                 "PCW_MIO_19_SLEW": "slow",
                                 "PCW_MIO_1_DIRECTION": "inout",
                                 "PCW_MIO_1_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_1_PULLUP": "enabled",
                                 "PCW_MIO_1_SLEW": "slow",
                                 "PCW_MIO_20_DIRECTION": "inout",
                                 "PCW_MIO_20_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_20_PULLUP": "enabled",
                                 "PCW_MIO_20_SLEW": "slow",
                                 "PCW_MIO_21_DIRECTION": "inout",
                                 "PCW_MIO_21_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_21_PULLUP": "enabled",
                                 "PCW_MIO_21_SLEW": "slow",
                                 "PCW_MIO_22_DIRECTION": "inout",
                                 "PCW_MIO_22_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_22_PULLUP": "enabled",
                                 "PCW_MIO_22_SLEW": "slow",
                                 "PCW_MIO_23_DIRECTION": "inout",
                                 "PCW_MIO_23_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_23_PULLUP": "enabled",
                                 "PCW_MIO_23_SLEW": "slow",
                                 "PCW_MIO_24_DIRECTION": "out",
                                 "PCW_MIO_24_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_24_PULLUP": "enabled",
                                 "PCW_MIO_24_SLEW": "slow",
                                 "PCW_MIO_25_DIRECTION": "in",
                                 "PCW_MIO_25_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_25_PULLUP": "enabled",
                                 "PCW_MIO_25_SLEW": "slow",
                                 "PCW_MIO_26_DIRECTION": "inout",
                                 "PCW_MIO_26_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_26_PULLUP": "enabled",
                                 "PCW_MIO_26_SLEW": "slow",
                                 "PCW_MIO_27_DIRECTION": "inout",
                                 "PCW_MIO_27_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_27_PULLUP": "enabled",
                                 "PCW_MIO_27_SLEW": "slow",
                                 "PCW_MIO_28_DIRECTION": "inout",
                                 "PCW_MIO_28_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_28_PULLUP": "enabled",
                                 "PCW_MIO_28_SLEW": "slow",
                                 "PCW_MIO_29_DIRECTION": "inout",
                                 "PCW_MIO_29_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_29_PULLUP": "enabled",
                                 "PCW_MIO_29_SLEW": "slow",
                                 "PCW_MIO_2_DIRECTION": "out",
                                 "PCW_MIO_2_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_2_PULLUP": "disabled",
                                 "PCW_MIO_2_SLEW": "slow",
                                 "PCW_MIO_30_DIRECTION": "inout",
                                 "PCW_MIO_30_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_30_PULLUP": "enabled",
                                 "PCW_MIO_30_SLEW": "slow",
                                 "PCW_MIO_31_DIRECTION": "inout",
                                 "PCW_MIO_31_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_31_PULLUP": "enabled",
                                 "PCW_MIO_31_SLEW": "slow",
                                 "PCW_MIO_32_DIRECTION": "inout",
                                 "PCW_MIO_32_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_32_PULLUP": "enabled",
                                 "PCW_MIO_32_SLEW": "slow",
                                 "PCW_MIO_33_DIRECTION": "inout",
                                 "PCW_MIO_33_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_33_PULLUP": "enabled",
                                 "PCW_MIO_33_SLEW": "slow",
                                 "PCW_MIO_34_DIRECTION": "in",
                                 "PCW_MIO_34_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_34_PULLUP": "enabled",
                                 "PCW_MIO_34_SLEW": "slow",
                                 "PCW_MIO_35_DIRECTION": "inout",
                                 "PCW_MIO_35_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_35_PULLUP": "enabled",
                                 "PCW_MIO_35_SLEW": "slow",
                                 "PCW_MIO_36_DIRECTION": "inout",
                                 "PCW_MIO_36_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_36_PULLUP": "enabled",
                                 "PCW_MIO_36_SLEW": "slow",
                                 "PCW_MIO_37_DIRECTION": "inout",
                                 "PCW_MIO_37_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_37_PULLUP": "enabled",
                                 "PCW_MIO_37_SLEW": "slow",
                                 "PCW_MIO_38_DIRECTION": "inout",
                                 "PCW_MIO_38_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_38_PULLUP": "enabled",
                                 "PCW_MIO_38_SLEW": "slow",
                                 "PCW_MIO_39_DIRECTION": "inout",
                                 "PCW_MIO_39_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_39_PULLUP": "enabled",
                                 "PCW_MIO_39_SLEW": "slow",
                                 "PCW_MIO_3_DIRECTION": "out",
                                 "PCW_MIO_3_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_3_PULLUP": "disabled",
                                 "PCW_MIO_3_SLEW": "slow",
                                 "PCW_MIO_40_DIRECTION": "inout",
                                 "PCW_MIO_40_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_40_PULLUP": "enabled",
                                 "PCW_MIO_40_SLEW": "slow",
                                 "PCW_MIO_41_DIRECTION": "inout",
                                 "PCW_MIO_41_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_41_PULLUP": "enabled",
                                 "PCW_MIO_41_SLEW": "slow",
                                 "PCW_MIO_42_DIRECTION": "inout",
                                 "PCW_MIO_42_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_42_PULLUP": "enabled",
                                 "PCW_MIO_42_SLEW": "slow",
                                 "PCW_MIO_43_DIRECTION": "inout",
                                 "PCW_MIO_43_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_43_PULLUP": "enabled",
                                 "PCW_MIO_43_SLEW": "slow",
                                 "PCW_MIO_44_DIRECTION": "inout",
                                 "PCW_MIO_44_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_44_PULLUP": "enabled",
                                 "PCW_MIO_44_SLEW": "slow",
                                 "PCW_MIO_45_DIRECTION": "inout",
                                 "PCW_MIO_45_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_45_PULLUP": "enabled",
                                 "PCW_MIO_45_SLEW": "slow",
                                 "PCW_MIO_46_DIRECTION": "inout",
                                 "PCW_MIO_46_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_46_PULLUP": "enabled",
                                 "PCW_MIO_46_SLEW": "slow",
                                 "PCW_MIO_47_DIRECTION": "inout",
                                 "PCW_MIO_47_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_47_PULLUP": "enabled",
                                 "PCW_MIO_47_SLEW": "slow",
                                 "PCW_MIO_48_DIRECTION": "inout",
                                 "PCW_MIO_48_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_48_PULLUP": "enabled",
                                 "PCW_MIO_48_SLEW": "slow",
                                 "PCW_MIO_49_DIRECTION": "inout",
                                 "PCW_MIO_49_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_49_PULLUP": "enabled",
                                 "PCW_MIO_49_SLEW": "slow",
                                 "PCW_MIO_4_DIRECTION": "inout",
                                 "PCW_MIO_4_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_4_PULLUP": "disabled",
                                 "PCW_MIO_4_SLEW": "slow",
                                 "PCW_MIO_50_DIRECTION": "inout",
                                 "PCW_MIO_50_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_50_PULLUP": "enabled",
                                 "PCW_MIO_50_SLEW": "slow",
                                 "PCW_MIO_51_DIRECTION": "inout",
                                 "PCW_MIO_51_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_51_PULLUP": "enabled",
                                 "PCW_MIO_51_SLEW": "slow",
                                 "PCW_MIO_52_DIRECTION": "inout",
                                 "PCW_MIO_52_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_52_PULLUP": "enabled",
                                 "PCW_MIO_52_SLEW": "slow",
                                 "PCW_MIO_53_DIRECTION": "inout",
                                 "PCW_MIO_53_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_53_PULLUP": "enabled",
                                 "PCW_MIO_53_SLEW": "slow",
                                 "PCW_MIO_5_DIRECTION": "inout",
                                 "PCW_MIO_5_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_5_PULLUP": "disabled",
                                 "PCW_MIO_5_SLEW": "slow",
                                 "PCW_MIO_6_DIRECTION": "inout",
                                 "PCW_MIO_6_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_6_PULLUP": "disabled",
                                 "PCW_MIO_6_SLEW": "slow",
                                 "PCW_MIO_7_DIRECTION": "out",
                                 "PCW_MIO_7_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_7_PULLUP": "disabled",
                                 "PCW_MIO_7_SLEW": "slow",
                                 "PCW_MIO_8_DIRECTION": "out",
                                 "PCW_MIO_8_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_8_PULLUP": "disabled",
                                 "PCW_MIO_8_SLEW": "slow",
                                 "PCW_MIO_9_DIRECTION": "inout",
                                 "PCW_MIO_9_IOTYPE": "LVCMOS 3.3V",
                                 "PCW_MIO_9_PULLUP": "enabled",
                                 "PCW_MIO_9_SLEW": "slow",
                                 "PCW_MIO_TREE_PERIPHERALS": "NAND Flash#GPIO#NAND Flash#NAND Flash#NAND Flash#NAND Flash#NAND Flash#NAND Flash#NAND Flash#NAND Flash#NAND Flash#NAND Flash#NAND Flash#NAND Flash#NAND Flash#GPIO#GPIO#GPIO#GPIO#GPIO#GPIO#GPIO#GPIO#GPIO#UART 1#UART 1#GPIO#GPIO#GPIO#GPIO#GPIO#GPIO#GPIO#GPIO#SD 0#GPIO#GPIO#GPIO#GPIO#GPIO#SD 0#SD 0#SD 0#SD 0#SD 0#SD 0#GPIO#GPIO#GPIO#GPIO#GPIO#GPIO#GPIO#GPIO",
                                 "PCW_MIO_TREE_SIGNALS": "cs#gpio[1]#ale#we_b#data[2]#data[0]#data[1]#cle#re_b#data[4]#data[5]#data[6]#data[7]#data[3]#busy#gpio[15]#gpio[16]#gpio[17]#gpio[18]#gpio[19]#gpio[20]#gpio[21]#gpio[22]#gpio[23]#tx#rx#gpio[26]#gpio[27]#gpio[28]#gpio[29]#gpio[30]#gpio[31]#gpio[32]#gpio[33]#cd#gpio[35]#gpio[36]#gpio[37]#gpio[38]#gpio[39]#clk#cmd#data[0]#data[1]#data[2]#data[3]#gpio[46]#gpio[47]#gpio[48]#gpio[49]#gpio[50]#gpio[51]#gpio[52]#gpio[53]",
                                 "PCW_NAND_CYCLES_T_AR": "10",
                                 "PCW_NAND_CYCLES_T_CLR": "20",
                                 "PCW_NAND_CYCLES_T_RC": "50",
                                 "PCW_NAND_CYCLES_T_REA": "20",
                                 "PCW_NAND_CYCLES_T_RR": "20",
                                 "PCW_NAND_CYCLES_T_WC": "50",
                                 "PCW_NAND_CYCLES_T_WP": "25",
                                 "PCW_NAND_GRP_D8_ENABLE": "0",
                                 "PCW_NAND_NAND_IO": "MIO 0 2.. 14",
                                 "PCW_NAND_PERIPHERAL_ENABLE": "1",
                                 "PCW_NOR_GRP_A25_ENABLE": "0",
                                 "PCW_NOR_GRP_CS0_ENABLE": "0",
                                 "PCW_NOR_GRP_CS1_ENABLE": "0",
                                 "PCW_NOR_GRP_SRAM_CS0_ENABLE": "0",
                                 "PCW_NOR_GRP_SRAM_CS1_ENABLE": "0",
                                 "PCW_NOR_GRP_SRAM_INT_ENABLE": "0",
                                 "PCW_NOR_PERIPHERAL_ENABLE": "0",
                                 "PCW_PCAP_PERIPHERAL_DIVISOR0": "7",
                                 "PCW_QSPI_GRP_FBCLK_ENABLE": "0",
                                 "PCW_QSPI_GRP_IO1_ENABLE": "0",
                                 "PCW_QSPI_GRP_SINGLE_SS_ENABLE": "0",
                                 "PCW_QSPI_GRP_SS1_ENABLE": "0",
                                 "PCW_QSPI_PERIPHERAL_DIVISOR0": "1",
                                 "PCW_QSPI_PERIPHERAL_ENABLE": "0",
                                 "PCW_QSPI_PERIPHERAL_FREQMHZ": "200",
                                 "PCW_SD0_GRP_CD_ENABLE": "1",
                                 "PCW_SD0_GRP_CD_IO": "MIO 34",
                                 "PCW_SD0_GRP_POW_ENABLE": "0",
                                 "PCW_SD0_GRP_WP_ENABLE": "0",
                                 "PCW_SD0_PERIPHERAL_ENABLE": "1",
                                 "PCW_SD0_SD0_IO": "MIO 40 .. 45",
                                 "PCW_SDIO_PERIPHERAL_DIVISOR0": "56",
                                 "PCW_SDIO_PERIPHERAL_FREQMHZ": "25",
                                 "PCW_SDIO_PERIPHERAL_VALID": "1",
                                 "PCW_SMC_PERIPHERAL_DIVISOR0": "14",
                                 "PCW_SMC_PERIPHERAL_FREQMHZ": "100",
                                 "PCW_SMC_PERIPHERAL_VALID": "1",
                                 "PCW_SPI_PERIPHERAL_DIVISOR0": "1",
                                 "PCW_TPIU_PERIPHERAL_DIVISOR0": "1",
                                 "PCW_UART1_GRP_FULL_ENABLE": "0",
                                 "PCW_UART1_PERIPHERAL_ENABLE": "1",
                                 "PCW_UART1_UART1_IO": "MIO 24 .. 25",
                                 "PCW_UART_PERIPHERAL_DIVISOR0": "14",
                                 "PCW_UART_PERIPHERAL_FREQMHZ": "100",
                                 "PCW_UART_PERIPHERAL_VALID": "1",
                                 "PCW_UIPARAM_ACT_DDR_FREQ_MHZ": "533.333374",
                                 "PCW_UIPARAM_DDR_BANK_ADDR_COUNT": "3",
                                 "PCW_UIPARAM_DDR_BUS_WIDTH": "16 Bit",
                                 "PCW_UIPARAM_DDR_CL": "7",
                                 "PCW_UIPARAM_DDR_COL_ADDR_COUNT": "10",
                                 "PCW_UIPARAM_DDR_CWL": "6",
                                 "PCW_UIPARAM_DDR_DEVICE_CAPACITY": "2048 MBits",
                                 "PCW_UIPARAM_DDR_DRAM_WIDTH": "16 Bits",
                                 "PCW_UIPARAM_DDR_ECC": "Disabled",
                                 "PCW_UIPARAM_DDR_PARTNO": "MT41K128M16 JT-125",
                                 "PCW_UIPARAM_DDR_ROW_ADDR_COUNT": "14",
                                 "PCW_UIPARAM_DDR_SPEED_BIN": "DDR3_1066F",
                                 "PCW_UIPARAM_DDR_T_FAW": "40.0",
                                 "PCW_UIPARAM_DDR_T_RAS_MIN": "35.0",
                                 "PCW_UIPARAM_DDR_T_RC": "48.75",
                                 "PCW_UIPARAM_DDR_T_RCD": "7",
                                 "PCW_UIPARAM_DDR_T_RP": "7",
                                 "PCW_USB0_RESET_ENABLE": "0",
                                 "PCW_USB1_RESET_ENABLE": "0",
                                 "PCW_USB_RESET_ENABLE": "0",
                                 "PCW_USE_M_AXI_GP0": "1",
                                 "PCW_M_AXI_GP0_ID_WIDTH": "12",
                                 "PCW_M_AXI_GP0_ENABLE_STATIC_REMAP": "0",
                                 "PCW_M_AXI_GP0_SUPPORT_NARROW_BURST": "0",
                                 "PCW_M_AXI_GP0_THREAD_ID_WIDTH": "12",
                                 "PCW_S_AXI_GP0_ID_WIDTH" : "6",
                             })
            
            self.platform.toolchain.additional_commands.append("open_checkpoint ebaz4205_route.dcp")
            self.platform.toolchain.additional_commands.append("write_hw_platform -hw -fixed -force -file ebaz4205.xsa")

            # Connect AXI GP0 to the SoC
            wb_gp0 = wishbone.Interface()
            self.submodules += axi.AXI2Wishbone(
                axi          = self.cpu.add_axi_gp_master(),
                wishbone     = wb_gp0,
                base_address = self.mem_map["csr"])
            self.bus.add_master(master=wb_gp0)

            self.bus.add_region("sram", SoCRegion(
                origin = self.cpu.mem_map["sram"],
                size   = 512 * 1024 * 1024 - self.cpu.mem_map["sram"])
            )

            self.bus.add_region("rom", SoCRegion(
                origin = self.cpu.mem_map["rom"],
                size   = 256 * 1024 * 1024 // 8,
                linker = True)
            )


        # Leds -------------------------------------------------------------------------------------
        if with_led_chaser:
            self.submodules.leds = LedChaser(
                pads         = platform.request_all("user_led"),
                sys_clk_freq = sys_clk_freq)


    def finalize(self, *args, **kwargs):
        super(BaseSoC, self).finalize(*args, **kwargs)
        if self.cpu_type != "zynq7000":
            return

        libxil_path = os.path.join(self.builder.software_dir, 'libxil')
        os.makedirs(os.path.realpath(libxil_path), exist_ok=True)
        lib = os.path.join(libxil_path, 'embeddedsw')
        if not os.path.exists(lib):
            os.system("git clone --depth 1 https://github.com/Xilinx/embeddedsw {}".format(lib))

        os.makedirs(os.path.realpath(self.builder.include_dir), exist_ok=True)
        for header in [
            'XilinxProcessorIPLib/drivers/uartps/src/xuartps_hw.h',
            'lib/bsp/standalone/src/common/xil_types.h',
            'lib/bsp/standalone/src/common/xil_assert.h',
            'lib/bsp/standalone/src/common/xil_io.h',
            'lib/bsp/standalone/src/common/xil_printf.h',
            'lib/bsp/standalone/src/common/xstatus.h',
            'lib/bsp/standalone/src/common/xdebug.h',
            'lib/bsp/standalone/src/arm/cortexa9/xpseudo_asm.h',
            'lib/bsp/standalone/src/arm/cortexa9/xreg_cortexa9.h',
            'lib/bsp/standalone/src/arm/cortexa9/xil_cache.h',
            'lib/bsp/standalone/src/arm/cortexa9/xparameters_ps.h',
            'lib/bsp/standalone/src/arm/cortexa9/xil_errata.h',
            'lib/bsp/standalone/src/arm/cortexa9/xtime_l.h',
            'lib/bsp/standalone/src/arm/common/xil_exception.h',
            'lib/bsp/standalone/src/arm/common/gcc/xpseudo_asm_gcc.h',
        ]:
            shutil.copy(os.path.join(lib, header), self.builder.include_dir)
        write_to_file(os.path.join(self.builder.include_dir, 'bspconfig.h'),
                      '#define FPU_HARD_FLOAT_ABI_ENABLED 1')
        write_to_file(os.path.join(self.builder.include_dir, 'xparameters.h'), '''
#ifndef __XPARAMETERS_H
#define __XPARAMETERS_H

#include "xparameters_ps.h"

#define STDOUT_BASEADDRESS 0xE0001000
#define XPAR_PS7_DDR_0_S_AXI_BASEADDR 0x00100000
#define XPAR_PS7_DDR_0_S_AXI_HIGHADDR 0x3FFFFFFF

#endif
''')





# Build --------------------------------------------------------------------------------------------

def main():
    from litex.soc.integration.soc import LiteXSoCArgumentParser
    parser = LiteXSoCArgumentParser(description="LiteX SoC on EBAZ4205")
    target_group = parser.add_argument_group(title="Target options")
    target_group.add_argument("--toolchain",    default="vivado",    help="FPGA toolchain (vivado, symbiflow or yosys+nextpnr).")
    target_group.add_argument("--build",        action="store_true", help="Build bitstream.")
    target_group.add_argument("--load",         action="store_true", help="Load bitstream.")
    target_group.add_argument("--sys-clk-freq", default=100e6,       help="System clock frequency.")
    builder_args(parser)
    soc_core_args(parser)
    vivado_build_args(parser)
    parser.set_defaults(cpu_type="zynq7000")
    parser.set_defaults(no_uart=True)
    args = parser.parse_args()

    soc = BaseSoC(
        sys_clk_freq = int(float(args.sys_clk_freq)),
        **soc_core_argdict(args)
    )
    builder = Builder(soc, **builder_argdict(args))
    if args.cpu_type == "zynq7000":
        soc.builder = builder
        builder.add_software_package('libxil')
        builder.add_software_library('libxil')
        #builder.additional_commands.append("write_hw_platform -fixed -force -file ebaz4205.xsa")

    builder.build(**vivado_build_argdict(args), run=args.build)

    if args.load:
        prog = soc.platform.create_programmer()
        prog.load_bitstream(builder.get_bitstream_filename(mode="sram"), device=1)

if __name__ == "__main__":
    main()
