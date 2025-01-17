#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2017-2019 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

from litex.build.generic_platform import *
from litex.build.xilinx import Xilinx7SeriesPlatform, VivadoProgrammer

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Clk / Rst
    ("clk125", 0,
        Subsignal("p", Pins("G10"), IOStandard("LVDS")),
        Subsignal("n", Pins("F10"), IOStandard("LVDS"))
    ),

    ("clk300", 0,
        Subsignal("p", Pins("AK17"), IOStandard("DIFF_SSTL12")),
        Subsignal("n", Pins("AK16"), IOStandard("DIFF_SSTL12"))
    ),
    ("cpu_reset", 0, Pins("AN8"), IOStandard("LVCMOS18")),

    # Leds
    ("user_led", 0, Pins("AP8"), IOStandard("LVCMOS18")),
    ("user_led", 1, Pins("H23"), IOStandard("LVCMOS18")),
    ("user_led", 2, Pins("P20"), IOStandard("LVCMOS18")),
    ("user_led", 3, Pins("P21"), IOStandard("LVCMOS18")),
    ("user_led", 4, Pins("N22"), IOStandard("LVCMOS18")),
    ("user_led", 5, Pins("M22"), IOStandard("LVCMOS18")),
    ("user_led", 6, Pins("R23"), IOStandard("LVCMOS18")),
    ("user_led", 7, Pins("P23"), IOStandard("LVCMOS18")),

    # Buttons
    ("user_btn_c", 0, Pins("AE10"), IOStandard("LVCMOS18")),
    ("user_btn_n", 0, Pins("AD10"), IOStandard("LVCMOS18")),
    ("user_btn_s", 0, Pins("AF8"),  IOStandard("LVCMOS18")),
    ("user_btn_w", 0, Pins("AF9"),  IOStandard("LVCMOS18")),
    ("user_btn_e", 0, Pins("AE8"),  IOStandard("LVCMOS18")),

    # Switches
    ("user_dip_btn", 0, Pins("AN16"), IOStandard("LVCMOS12")),
    ("user_dip_btn", 1, Pins("AN19"), IOStandard("LVCMOS12")),
    ("user_dip_btn", 2, Pins("AP18"), IOStandard("LVCMOS12")),
    ("user_dip_btn", 3, Pins("AN14"), IOStandard("LVCMOS12")),

    # SMA
    ("user_sma_clock", 0,
        Subsignal("p", Pins("D23"), IOStandard("LVDS")),
        Subsignal("n", Pins("C23"), IOStandard("LVDS"))
    ),
    ("user_sma_clock_p", 0, Pins("D23"), IOStandard("LVCMOS18")),
    ("user_sma_clock_n", 0, Pins("C23"), IOStandard("LVCMOS18")),
    ("user_sma_gpio", 0,
        Subsignal("p", Pins("H27"), IOStandard("LVDS")),
        Subsignal("n", Pins("G27"), IOStandard("LVDS"))
    ),
    ("user_sma_gpio_p", 0, Pins("H27"), IOStandard("LVCMOS18")),
    ("user_sma_gpio_n", 0, Pins("G27"), IOStandard("LVCMOS18")),

    # I2C
    ("i2c", 0,
        Subsignal("scl", Pins("J24")),
        Subsignal("sda", Pins("J25")),
        IOStandard("LVCMOS18")
    ),

    # Serial
    ("serial", 0,
        Subsignal("cts", Pins("L23")),
        Subsignal("rts", Pins("K27")),
        Subsignal("tx",  Pins("K26")),
        Subsignal("rx",  Pins("G25")),
        IOStandard("LVCMOS18")
    ),

    # SPIFlash
    ("spiflash", 0,  # clock needs to be accessed through primitive
        Subsignal("cs_n", Pins("U7")),
        Subsignal("dq",   Pins("AC7 AB7 AA7 Y7")),
        IOStandard("LVCMOS18")
    ),
    ("spiflash", 1,  # clock needs to be accessed through primitive
        Subsignal("cs_n", Pins("G26")),
        Subsignal("dq",   Pins("M20 L20 R21 R22")),
        IOStandard("LVCMOS18")
    ),

    # SDCard
    ("spisdcard", 0,
        Subsignal("clk",  Pins("AL10")),
        Subsignal("cs_n", Pins("AH8")),
        Subsignal("mosi", Pins("AD9"), Misc("PULLUP")),
        Subsignal("miso", Pins("AP9"), Misc("PULLUP")),
        Misc("SLEW=FAST"),
        IOStandard("LVCMOS18")
    ),
    ("sdcard", 0,
        Subsignal("clk", Pins("AL10")),
        Subsignal("cmd", Pins("AD9"), Misc("PULLUP True")),
        Subsignal("data", Pins("AP9 AN9 AH9 AH8"), Misc("PULLUP True")),
        Misc("SLEW=FAST"),
        IOStandard("LVCMOS18")
    ),

    # Rotary Encoder
    ("rotary", 0,
        Subsignal("a",    Pins("Y21")),
        Subsignal("b",    Pins("AD26")),
        Subsignal("push", Pins("AF28")),
        IOStandard("LVCMOS18")
    ),

    # HDMI
    ("hdmi", 0,
        Subsignal("d", Pins(
            "AK11 AP11 AP13 AN13 AN11 AM11 AN12 AM12",
            "AL12 AK12 AL13 AK13 AD11 AH12 AG12 AJ11",
            "AG10 AK8")),
        Subsignal("de",        Pins("AE11")),
        Subsignal("clk",       Pins("AF13")),
        Subsignal("vsync",     Pins("AH13")),
        Subsignal("hsync",     Pins("AE13")),
        Subsignal("spdif",     Pins("AE12")),
        Subsignal("spdif_out", Pins("AF12")),
        IOStandard("LVCMOS18")
    ),

    # DDR4 SDRAM
    ("ddram", 0,
        Subsignal("a", Pins(
            "AE17 AH17 AE18 AJ15 AG16 AL17 AK18 AG17",
            "AF18 AH19 AF15 AD19 AJ14 AG19"),
            IOStandard("SSTL12_DCI")),
        Subsignal("ba",      Pins("AF17 AL15"), IOStandard("SSTL12_DCI")),
        Subsignal("bg",      Pins("AG15"), IOStandard("SSTL12_DCI")),
        Subsignal("ras_n",   Pins("AF14"), IOStandard("SSTL12_DCI")), # A16
        Subsignal("cas_n",   Pins("AG14"), IOStandard("SSTL12_DCI")), # A15
        Subsignal("we_n",    Pins("AD16"), IOStandard("SSTL12_DCI")), # A14
        Subsignal("cs_n",    Pins("AL19"), IOStandard("SSTL12_DCI")),
        Subsignal("act_n",   Pins("AH14"), IOStandard("SSTL12_DCI")),
        #Subsignal("ten",     Pins("AH16"), IOStandard("SSTL12_DCI")),
        #Subsignal("alert_n", Pins("AJ16"), IOStandard("SSTL12_DCI")),
        #Subsignal("par",     Pins("AD18"), IOStandard("SSTL12_DCI")),
        Subsignal("dm",      Pins("AD21 AE25 AJ21 AM21 AH26 AN26 AJ29 AL32"),
            IOStandard("POD12_DCI")),
        Subsignal("dq",      Pins(
            "AE23 AG20 AF22 AF20 AE22 AD20 AG22 AE20",
            "AJ24 AG24 AJ23 AF23 AH23 AF24 AH22 AG25",
            "AL22 AL25 AM20 AK23 AK22 AL24 AL20 AL23",
            "AM24 AN23 AN24 AP23 AP25 AN22 AP24 AM22",
            "AH28 AK26 AK28 AM27 AJ28 AH27 AK27 AM26",
            "AL30 AP29 AM30 AN28 AL29 AP28 AM29 AN27",
            "AH31 AH32 AJ34 AK31 AJ31 AJ30 AH34 AK32",
            "AN33 AP33 AM34 AP31 AM32 AN31 AL34 AN32"),
            IOStandard("POD12_DCI"),
            Misc("PRE_EMPHASIS=RDRV_240"),
            Misc("EQUALIZATION=EQ_LEVEL2")),
        Subsignal("dqs_p",   Pins("AG21 AH24 AJ20 AP20 AL27 AN29 AH33 AN34"),
            IOStandard("DIFF_POD12_DCI"),
            Misc("PRE_EMPHASIS=RDRV_240"),
            Misc("EQUALIZATION=EQ_LEVEL2")),
        Subsignal("dqs_n",   Pins("AH21 AJ25 AK20 AP21 AL28 AP30 AJ33 AP34"),
            IOStandard("DIFF_POD12_DCI"),
            Misc("PRE_EMPHASIS=RDRV_240"),
            Misc("EQUALIZATION=EQ_LEVEL2")),
        Subsignal("clk_p",   Pins("AE16"), IOStandard("DIFF_SSTL12_DCI")),
        Subsignal("clk_n",   Pins("AE15"), IOStandard("DIFF_SSTL12_DCI")),
        Subsignal("cke",     Pins("AD15"), IOStandard("SSTL12_DCI")),
        Subsignal("odt",     Pins("AJ18"), IOStandard("SSTL12_DCI")),
        Subsignal("reset_n", Pins("AL18"), IOStandard("LVCMOS12")),
        Misc("SLEW=FAST"),
    ),

    # PCIe
    ("pcie_x1", 0,
        Subsignal("rst_n", Pins("K22"), IOStandard("LVCMOS18")),
        Subsignal("clk_p", Pins("AB6")),
        Subsignal("clk_n", Pins("AB5")),
        Subsignal("rx_p",  Pins("AB2")),
        Subsignal("rx_n",  Pins("AB1")),
        Subsignal("tx_p",  Pins("AC4")),
        Subsignal("tx_n",  Pins("AC3"))
    ),
    ("pcie_x2", 0,
        Subsignal("rst_n", Pins("K22"), IOStandard("LVCMOS18")),
        Subsignal("clk_p", Pins("AB6")),
        Subsignal("clk_n", Pins("AB5")),
        Subsignal("rx_p",  Pins("AB2 AD2")),
        Subsignal("rx_n",  Pins("AB1 AD1")),
        Subsignal("tx_p",  Pins("AC4 AE4")),
        Subsignal("tx_n",  Pins("AC3 AE3"))
    ),
    ("pcie_x4", 0,
        Subsignal("rst_n", Pins("K22"), IOStandard("LVCMOS18")),
        Subsignal("clk_p", Pins("AB6")),
        Subsignal("clk_n", Pins("AB5")),
        Subsignal("rx_p",  Pins("AB2 AD2 AF2 AH2")),
        Subsignal("rx_n",  Pins("AB1 AD1 AF1 AH1")),
        Subsignal("tx_p",  Pins("AC4 AE4 AG4 AH6")),
        Subsignal("tx_n",  Pins("AC3 AE3 AG3 AH5"))
    ),
    ("pcie_x8", 0,
        Subsignal("rst_n", Pins("K22"), IOStandard("LVCMOS18")),
        Subsignal("clk_p", Pins("AB6")),
        Subsignal("clk_n", Pins("AB5")),
        Subsignal("rx_p",  Pins("AB2 AD2 AF2 AH2 AJ4 AK2 AM2 AP2")),
        Subsignal("rx_n",  Pins("AB1 AD1 AF1 AH1 AJ3 AK1 AM1 AP1")),
        Subsignal("tx_p",  Pins("AC4 AE4 AG4 AH6 AK6 AL4 AM6 AN4")),
        Subsignal("tx_n",  Pins("AC3 AE3 AG3 AH5 AK5 AL3 AM5 AN3"))
    ),

    # SGMII Clk
    ("sgmii_clock", 0,
        Subsignal("p", Pins("P26"), IOStandard("LVDS_25")),
        Subsignal("n", Pins("N26"), IOStandard("LVDS_25"))
    ),

    # SI570
    ("si570_refclk", 0,
        Subsignal("p", Pins("P6")),
        Subsignal("n", Pins("P5"))
    ),

    # SMA
    ("user_sma_mgt_refclk", 0,
        Subsignal("p", Pins("V6")),
        Subsignal("n", Pins("V5"))
    ),
    ("user_sma_mgt_tx", 0,
        Subsignal("p", Pins("R4")),
        Subsignal("n", Pins("R3"))
    ),
    ("user_sma_mgt_rx", 0,
        Subsignal("p", Pins("P2")),
        Subsignal("n", Pins("P1"))
    ),

    # SFP
    ("sfp", 0,
        Subsignal("txp", Pins("U4")),
        Subsignal("txn", Pins("U3")),
        Subsignal("rxp", Pins("T2")),
        Subsignal("rxn", Pins("T1"))
    ),
    ("sfp_tx", 0,
        Subsignal("p", Pins("U4")),
        Subsignal("n", Pins("U3")),
    ),
    ("sfp_rx", 0,
        Subsignal("p", Pins("T2")),
        Subsignal("n", Pins("T1")),
    ),
    ("sfp_tx_disable_n", 0, Pins("AL8"), IOStandard("LVCMOS18")),

    ("sfp", 1,
        Subsignal("txp", Pins("W4")),
        Subsignal("txn", Pins("W3")),
        Subsignal("rxp", Pins("V2")),
        Subsignal("rxn", Pins("V1"))
    ),
    ("sfp_tx", 1,
        Subsignal("p", Pins("W4")),
        Subsignal("n", Pins("W3")),
    ),
    ("sfp_rx", 1,
        Subsignal("p", Pins("V2")),
        Subsignal("n", Pins("V1")),
    ),
    ("sfp_tx_disable_n", 1, Pins("D28"), IOStandard("LVCMOS18")),
]

# Connectors ---------------------------------------------------------------------------------------

_connectors = [
    ("HPC", {
        "DP0_C2M_P"     : "F6",
        "DP0_C2M_N"     : "F5",
        "DP0_M2C_P"     : "E4",
        "DP0_M2C_N"     : "E3",
        "DP1_C2M_P"     : "D6",
        "DP1_C2M_N"     : "D5",
        "DP1_M2C_P"     : "D2",
        "DP1_M2C_N"     : "D1",
        "DP2_C2M_P"     : "C4",
        "DP2_C2M_N"     : "C3",
        "DP2_M2C_P"     : "B2",
        "DP2_M2C_N"     : "B1",
        "DP3_C2M_P"     : "B6",
        "DP3_C2M_N"     : "B5",
        "DP3_M2C_P"     : "A4",
        "DP3_M2C_N"     : "A3",
        "DP4_C2M_P"     : "N4",
        "DP4_C2M_N"     : "N3",
        "DP4_M2C_P"     : "M2",
        "DP4_M2C_N"     : "M1",
        "DP5_C2M_P"     : "J4",
        "DP5_C2M_N"     : "J3",
        "DP5_M2C_P"     : "H2",
        "DP5_M2C_N"     : "H1",
        "DP6_C2M_P"     : "L4",
        "DP6_C2M_N"     : "L3",
        "DP6_M2C_P"     : "K2",
        "DP6_M2C_N"     : "K1",
        "DP7_C2M_P"     : "G4",
        "DP7_C2M_N"     : "G3",
        "DP7_M2C_P"     : "F2",
        "DP7_M2C_N"     : "F1",
        "LA06_P"        : "D13",
        "LA06_N"        : "C13",
        "LA10_P"        : "L8",
        "LA10_N"        : "K8",
        "LA14_P"        : "B10",
        "LA14_N"        : "A10",
        "LA18_CC_P"     : "E22",
        "LA18_CC_N"     : "E23",
        "LA27_P"        : "H21",
        "LA27_N"        : "G21",
        "HA01_CC_P"     : "E16",
        "HA01_CC_N"     : "D16",
        "HA05_P"        : "J15",
        "HA05_N"        : "J14",
        "HA09_P"        : "F18",
        "HA09_N"        : "F17",
        "HA13_P"        : "B14",
        "HA13_N"        : "A14",
        "HA16_P"        : "A19",
        "HA16_N"        : "A18",
        "HA20_P"        : "C19",
        "HA20_N"        : "B19",
        "CLK1_M2C_P"    : "E25",
        "CLK1_M2C_N"    : "D25",
        "LA00_CC_P"     : "H11",
        "LA00_CC_N"     : "G11",
        "LA03_P"        : "A13",
        "LA03_N"        : "A12",
        "LA08_P"        : "J8",
        "LA08_N"        : "H8",
        "LA12_P"        : "E10",
        "LA12_N"        : "D10",
        "LA16_P"        : "B9",
        "LA16_N"        : "A9",
        "LA20_P"        : "B24",
        "LA20_N"        : "A24",
        "LA22_P"        : "G24",
        "LA22_N"        : "F25",
        "LA25_P"        : "D20",
        "LA25_N"        : "D21",
        "LA29_P"        : "B20",
        "LA29_N"        : "A20",
        "LA31_P"        : "B25",
        "LA31_N"        : "A25",
        "LA33_P"        : "A27",
        "LA33_N"        : "A28",
        "HA03_P"        : "G15",
        "HA03_N"        : "G14",
        "HA07_P"        : "L19",
        "HA07_N"        : "L18",
        "HA11_P"        : "J19",
        "HA11_N"        : "J18",
        "HA14_P"        : "F15",
        "HA14_N"        : "F14",
        "HA18_P"        : "B17",
        "HA18_N"        : "B16",
        "HA22_P"        : "C18",
        "HA22_N"        : "C17",
        "GBTCLK1_M2C_P" : "H6",
        "GBTCLK1_M2C_N" : "H5",
        "GBTCLK0_M2C_P" : "K6",
        "GBTCLK0_M2C_N" : "K5",
        "LA01_CC_P"     : "G9",
        "LA01_CC_N"     : "F9",
        "LA05_P"        : "L13",
        "LA05_N"        : "K13",
        "LA09_P"        : "J9",
        "LA09_N"        : "H9",
        "LA13_P"        : "D9",
        "LA13_N"        : "C9",
        "LA17_CC_P"     : "D24",
        "LA17_CC_N"     : "C24",
        "LA23_P"        : "G22",
        "LA23_N"        : "F22",
        "LA26_P"        : "G20",
        "LA26_N"        : "F20",
        "PG_M2C"        : "L27",
        "HA00_CC_P"     : "G17",
        "HA00_CC_N"     : "G16",
        "HA04_P"        : "G19",
        "HA04_N"        : "F19",
        "HA08_P"        : "K18",
        "HA08_N"        : "K17",
        "HA12_P"        : "K16",
        "HA12_N"        : "J16",
        "HA15_P"        : "D14",
        "HA15_N"        : "C14",
        "HA19_P"        : "D19",
        "HA19_N"        : "D18",
        "PRSNT_M2C_B"   : "H24",
        "CLK0_M2C_P"    : "H12",
        "CLK0_M2C_N"    : "G12",
        "LA02_P"        : "K10",
        "LA02_N"        : "J10",
        "LA04_P"        : "L12",
        "LA04_N"        : "K12",
        "LA07_P"        : "F8",
        "LA07_N"        : "E8",
        "LA11_P"        : "K11",
        "LA11_N"        : "J11",
        "LA15_P"        : "D8",
        "LA15_N"        : "C8",
        "LA19_P"        : "C21",
        "LA19_N"        : "C22",
        "LA21_P"        : "F23",
        "LA21_N"        : "F24",
        "LA24_P"        : "E20",
        "LA24_N"        : "E21",
        "LA28_P"        : "B21",
        "LA28_N"        : "B22",
        "LA30_P"        : "C26",
        "LA30_N"        : "B26",
        "LA32_P"        : "E26",
        "LA32_N"        : "D26",
        "HA02_P"        : "H19",
        "HA02_N"        : "H18",
        "HA06_P"        : "L15",
        "HA06_N"        : "K15",
        "HA10_P"        : "H17",
        "HA10_N"        : "H16",
        "HA17_CC_P"     : "E18",
        "HA17_CC_N"     : "E17",
        "HA21_P"        : "E15",
        "HA21_N"        : "D15",
        "HA23_P"        : "B15",
        "HA23_N"        : "A15",
        }
    ),
    ("LPC", {
        "GBTCLK0_M2C_P" : "AA24",
        "GBTCLK0_M2C_N" : "AA25",
        "LA01_CC_P"     : "W25",
        "LA01_CC_N"     : "Y25",
        "LA05_P"        : "V27",
        "LA05_N"        : "V28",
        "LA09_P"        : "V26",
        "LA09_N"        : "W26",
        "LA13_P"        : "AA20",
        "LA13_N"        : "AB20",
        "LA17_CC_P"     : "AA32",
        "LA17_CC_N"     : "AB32",
        "LA23_P"        : "AD30",
        "LA23_N"        : "AD31",
        "LA26_P"        : "AF33",
        "LA26_N"        : "AG34",
        "CLK0_M2C_P"    : "AA24",
        "CLK0_M2C_N"    : "AA25",
        "LA02_P"        : "AA22",
        "LA02_N"        : "AB22",
        "LA04_P"        : "U26",
        "LA04_N"        : "U27",
        "LA07_P"        : "V22",
        "LA07_N"        : "V23",
        "LA11_P"        : "V21",
        "LA11_N"        : "W21",
        "LA15_P"        : "AB25",
        "LA15_N"        : "AB26",
        "LA19_P"        : "AA29",
        "LA19_N"        : "AB29",
        "LA21_P"        : "AC33",
        "LA21_N"        : "AD33",
        "LA24_P"        : "AE32",
        "LA24_N"        : "AF32",
        "LA28_P"        : "V31",
        "LA28_N"        : "W31",
        "LA30_P"        : "Y31",
        "LA30_N"        : "Y32",
        "LA32_P"        : "W30",
        "LA32_N"        : "Y30",
        "LA06_P"        : "V29",
        "LA06_N"        : "W29",
        "LA10_P"        : "T22",
        "LA10_N"        : "T23",
        "LA14_P"        : "U21",
        "LA14_N"        : "U22",
        "LA18_CC_P"     : "AB30",
        "LA18_CC_N"     : "AB31",
        "LA27_P"        : "AG31",
        "LA27_N"        : "AG32",
        "CLK1_M2C_P"    : "AC31",
        "CLK1_M2C_N"    : "AC32",
        "LA00_CC_P"     : "W23",
        "LA00_CC_N"     : "W24",
        "LA03_P"        : "W28",
        "LA03_N"        : "Y28",
        "LA08_P"        : "U24",
        "LA08_N"        : "U25",
        "LA12_P"        : "AC22",
        "LA12_N"        : "AC23",
        "LA16_P"        : "AB21",
        "LA16_N"        : "AC21",
        "LA20_P"        : "AA34",
        "LA20_N"        : "AB34",
        "LA22_P"        : "AC34",
        "LA22_N"        : "AD34",
        "LA25_P"        : "AE33",
        "LA25_N"        : "AF34",
        "LA29_P"        : "U34",
        "LA29_N"        : "V34",
        "LA31_P"        : "V33",
        "LA31_N"        : "W34",
        "LA33_P"        : "W33",
        "LA33_N"        : "Y33",
        }
    ),
    ("pmod0", "AK25 AN21 AH18 AM19 AE26 AF25 AE21 AM17"),
    ("pmod1", "AL14 AM14 AP16 AP15 AM16 AM15 AN18 AN17"),
]

# Platform -----------------------------------------------------------------------------------------

class Platform(Xilinx7SeriesPlatform):
    default_clk_name   = "clk125"
    default_clk_period = 1e9/125e6

    def __init__(self, toolchain="vivado"):
        Xilinx7SeriesPlatform.__init__(self, "xcku040-ffva1156-2-e", _io, _connectors, toolchain=toolchain)

    def create_programmer(self):
        return VivadoProgrammer()

    def do_finalize(self, fragment):
        Xilinx7SeriesPlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk125", loose=True), 1e9/125e6)
        self.add_period_constraint(self.lookup_request("clk300", loose=True), 1e9/300e6)
        self.add_platform_command("set_property INTERNAL_VREF 0.84 [get_iobanks 44]")
        self.add_platform_command("set_property INTERNAL_VREF 0.84 [get_iobanks 45]")
        self.add_platform_command("set_property INTERNAL_VREF 0.84 [get_iobanks 46]")
