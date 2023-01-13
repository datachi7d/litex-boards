#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2019-2020 Florent Kermarrec <florent@enjoy-digital.fr>
# Copyright (c) 2021 Dhiru Kholia <dhiru.kholia@gmail.com>
# SPDX-License-Identifier: BSD-2-Clause

from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform, VivadoProgrammer
from litex.build.xilinx.programmer import XC3SProg

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Clk / Rst
    ("clk33_333", 0, Pins("N18"), IOStandard("LVCMOS33")),
    ("clk25", 0, Pins("U18"), IOStandard("LVCMOS33")),

    # Leds
    ("user_led", 0, Pins("W14"), IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("W13"), IOStandard("LVCMOS33")),

    # Serial
    ("serial", 0,
        Subsignal("tx", Pins("B20")),
        Subsignal("rx", Pins("B19")),
        IOStandard("LVCMOS33")
    ),

    # PS7
    ("ps7_clk",   0, Pins("E7")),
    ("ps7_porb",  0, Pins("C7")),
    ("ps7_srstb", 0, Pins("B10")),
    ("ps7_mio",   0, Pins("E6 A7 B8 D6 B7 A6 A5 D8 D5 B5 E9 C6 D9 E8 C5 C8 A19 E14 B18 D10 A17 F14 B17 D11 A16 F15 A15 D13 C16 C13 C15 E16 A14 D15 A12 F12 A11 A10 E13 C18 D14 C17 E12 A9 F13 B15 D16 B14 B12 C12 B13 B9 C10 C11"), IOStandard("LVCMOS33")),
    ("ps7_ddram", 0,
        Subsignal("addr",    Pins("N2 K2 M3 K3 M4 L1 L4 K4 K1 J4 F5 G4 E4 D4 F4")),
        Subsignal("ba",      Pins("L5 R4 J5")),
        Subsignal("cas_n",   Pins("P5")),
        Subsignal("ck_n",    Pins("M2")),
        Subsignal("ck_p",    Pins("L2")),
        Subsignal("cke",     Pins("N3")),
        Subsignal("cs_n",    Pins("N1")),
        Subsignal("dm",      Pins("A1 F1 T1 Y1")),
        Subsignal("dq",      Pins("C3 A2 A4 D3 D1 C1 E1 E2 E3 G3 H3 J3 H2 H1 J1"
                                   "P1 P3 R3 R1 T4 U4 U2 U3 V1 Y3 W1 W3 V2 V3")),
        Subsignal("dqs_n",   Pins("B2 F2 T2 W4")),
        Subsignal("dqs_p",   Pins("C2 G2 R2 W5")),
        Subsignal("odt",     Pins("N5")),
        Subsignal("ras_n",   Pins("P4")),
        Subsignal("reset_n", Pins("B4")),
        Subsignal("we_n",    Pins("M5")),
        Subsignal("vrn",     Pins("G5")),
        Subsignal("vrp",     Pins("H5")),
    ),

    ("ps7_enet0_mdio", 0,
        Subsignal("mdc",  Pins("W15")),
        Subsignal("i",    Pins(1)),
        Subsignal("o",    Pins(1)),
        Subsignal("t",    Pins(1)),
        IOStandard("LVCMOS33"),
    ),
    ("ps7_enet0", 0,
        Subsignal("tx_en",  Pins("W19")),
        Subsignal("tx_er",  Pins(1)),
        Subsignal("txd",    Pins("W18 Y18 V18 Y19")),
        Subsignal("col",    Pins(1)),
        Subsignal("crs",    Pins(1)),
        Subsignal("rx_clk", Pins("U14")),
        Subsignal("rx_dv",  Pins("W16")),
        Subsignal("rx_er",  Pins(1)),
        Subsignal("tx_clk", Pins("U15")),
        Subsignal("rxd",    Pins("Y16 V16 V17 Y17")),
        IOStandard("LVCMOS33")
    ),
]

# Connectors ---------------------------------------------------------------------------------------

_connectors = [
]

# Platform -----------------------------------------------------------------------------------------

class Platform(XilinxPlatform):
    default_clk_name   = "clk25"
    default_clk_period = 1e9/25e6

    def __init__(self, toolchain="vivado"):
        XilinxPlatform.__init__(self, "xc7z010-clg400-1", _io,  _connectors, toolchain=toolchain)

    def create_programmer(self):
        return VivadoProgrammer()

    """
    # We will like to use this later - Vivado is slow!
    def create_programmer(self):
        return XC3SProg(cable="ftdi")
    """

    def do_finalize(self, fragment):
        XilinxPlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk33_333", loose=True), 1e9/33.333e6)
        self.add_period_constraint(self.lookup_request("cl25", loose=True), 1e9/25e6)
