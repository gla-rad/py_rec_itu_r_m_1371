# -*- coding: utf-8 -*-
"""
Test Messages Module.

This module contains test cases for the messages.py Module.

@author: Jan Safar

Copyright 2024 GLA Research and Development Directorate

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
# =============================================================================
# %% Import Statements
# =============================================================================
# Built-in Modules ------------------------------------------------------------

# Third-party Modules ---------------------------------------------------------
import pytest
from bitstring import BitStream

# Local Modules ---------------------------------------------------------------
from rec_itu_r_m_1371.messages import (
    ais_ascii_8b_to_6b,
    ais_ascii_6b_to_8b,
    AISMessage8,
    AISMessage21
)

from rec_itu_r_m_1371.asm_payloads import SampleASMPayload1

# =============================================================================
# %% Sample Data
# =============================================================================
ascii_8b_str = "BEAM ME UP, SCOTTY!"
ascii_6b_bs = BitStream("0b00001000010100000100110110000000110100010110000001 \
                        01010100001011001000000100110000110011110101000101000 \
                        11001100001")

# =============================================================================
# %% Test Cases
# =============================================================================
def test_ais_ascii_8b_to_6b():
    result = ais_ascii_8b_to_6b(ascii_8b_str)
    assert result == ascii_6b_bs

def test_ais_ascii_6b_to_8b():
    result = ais_ascii_6b_to_8b(ascii_6b_bs)
    assert result == ascii_8b_str

def test_ais_message8():
    #### Sample Data
    source_id = 123456789
    payload = SampleASMPayload1(n_app_data_bytes=2)

    ais_msg_8_bs = BitStream("0x201d6f345400010000")

    ais_msg_8_str = """

    AIS Message 8: Binary Broadcast Message
    ---------------------------------------
    Source ID: 123456789
    Binary Data: 0x00010000"""

    #### Testing
    ais_msg_8 = AISMessage8(source_id, payload)

    #### Result Checks
    assert ais_msg_8.source_id == source_id
    assert ais_msg_8.payload == payload

    assert ais_msg_8.bitstream == ais_msg_8_bs

    assert str(ais_msg_8) == ais_msg_8_str

    # TODO: Add a test for from_vdes_asm()

def test_ais_message21():
    #### Sample Data
    source_id=992356001
    aton_type=30
    aton_name="JAN'S VIRTUAL ATON"
    pos_accuracy=1
    lon=1.34
    lat=51.92
    dimension=[1,2,3,4]
    epf_device_type=0
    time_stamp=60
    off_position=0
    aton_status=0
    raim_fl=0
    vaton_fl=1
    assigned_mode_fl=0
    aton_name_extension=""

    ais_msg_bs = BitStream(
        """0x54ec989a87c50274e9c0b12928a826400a879c00100c44a03b6af0001010620780
        04""")

    ais_msg_21_str = """

    AIS Message 21: Aids-to-navigation Report
    -----------------------------------------
    Source ID: 992356001
    AtoN type: 30
    AtoN name: JAN'S VIRTUAL ATON
    Position accuracy: 1
    Latitude (deg): 51.920000
    Longitude (deg): 1.340000
    Dimension A (m): 1
    Dimension B (m): 2
    Dimension C (m): 3
    Dimension D (m): 4
    EPF device type: 0
    Timestamp (s): 60
    Off-position flag: 0
    AtoN status bits: 0
    RAIM flag: 0
    Virtual flag: 1
    Assigned mode flag: 0
"""

    #### Testing
    # Create a message 21 using the constructor
    ais_msg_21 = AISMessage21(
        source_id, aton_type, aton_name, pos_accuracy, lon, lat, dimension,
        epf_device_type, time_stamp, off_position, aton_status, raim_fl,
        vaton_fl, assigned_mode_fl)

    # Create a message 21 from a bitstream
    ais_msg_21_from_bs = AISMessage21.from_bitstream(ais_msg_bs)

    #### Result Checks
    assert ais_msg_21.source_id == source_id
    assert ais_msg_21.aton_type == aton_type
    assert ais_msg_21.aton_name == aton_name
    assert ais_msg_21.pos_accuracy == pos_accuracy
    assert ais_msg_21.lon == lon
    assert ais_msg_21.lat == lat
    assert ais_msg_21.dimension == dimension
    assert ais_msg_21.epf_device_type == epf_device_type
    assert ais_msg_21.time_stamp == time_stamp
    assert ais_msg_21.off_position == off_position
    assert ais_msg_21.aton_status == aton_status
    assert ais_msg_21.raim_fl == raim_fl
    assert ais_msg_21.vaton_fl == vaton_fl
    assert ais_msg_21.assigned_mode_fl == assigned_mode_fl
    assert ais_msg_21.aton_name_extension == aton_name_extension

    assert ais_msg_21.bitstream == ais_msg_bs

    assert str(ais_msg_21) == ais_msg_21_str

    assert ais_msg_21_from_bs.source_id == source_id
    assert ais_msg_21_from_bs.aton_type == aton_type
    assert ais_msg_21_from_bs.aton_name == aton_name + "@@"
    assert ais_msg_21_from_bs.pos_accuracy == pos_accuracy
    assert ais_msg_21_from_bs.lon == lon
    assert ais_msg_21_from_bs.lat == lat
    assert ais_msg_21_from_bs.dimension == dimension
    assert ais_msg_21_from_bs.epf_device_type == epf_device_type
    assert ais_msg_21_from_bs.time_stamp == time_stamp
    assert ais_msg_21_from_bs.off_position == off_position
    assert ais_msg_21_from_bs.aton_status == aton_status
    assert ais_msg_21_from_bs.raim_fl == raim_fl
    assert ais_msg_21_from_bs.vaton_fl == vaton_fl
    assert ais_msg_21_from_bs.assigned_mode_fl == assigned_mode_fl
    assert ais_msg_21_from_bs.aton_name_extension == aton_name_extension

# =============================================================================
# %% Main Function
# =============================================================================
if __name__ == '__main__':
    pytest.main()
