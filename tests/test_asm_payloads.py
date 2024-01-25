# -*- coding: utf-8 -*-
"""
Test ASM Payloads Module.

This module contains test cases for the asm_payloads.py Module.

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
from rec_itu_r_m_1371.asm_payloads import SampleASMPayload1

# =============================================================================
# %% Sample Data
# =============================================================================


# =============================================================================
# %% Test Cases
# =============================================================================
def test_sample_asm_payload_1_creation():
    # Test creating a SampleASMPayload1 object with default parameters
    asm_payload = SampleASMPayload1()
    assert asm_payload.n_app_data_bytes == 10
    assert asm_payload.application_str == "Sample ASM 1"

    # Test creating a SampleASMPayload1 object with a specified number of
    # application data bytes
    asm_payload_custom_size = SampleASMPayload1(n_app_data_bytes=2)
    assert asm_payload_custom_size.n_app_data_bytes == 2

def test_sample_asm_payload_1_from_bitstream():
    # Test creating a SampleASMPayload1 object from a bitstream
    # Sample bitstream
    bs = BitStream("0x00010000")
    asm_payload = SampleASMPayload1.from_bitstream(bs)

    # Check if the created object has the correct properties
    assert asm_payload.n_app_data_bytes == 2

    # Test with an invalid bitstream
    # Invalid DAC
    invalid_bs = BitStream("0x01E10000")
    with pytest.raises(ValueError, match="Invalid Application Identifier!"):
        SampleASMPayload1.from_bitstream(invalid_bs)

    # Invalid FI
    invalid_bs = BitStream("0x03E10000")
    with pytest.raises(ValueError, match="Invalid Application Identifier!"):
        SampleASMPayload1.from_bitstream(invalid_bs)

    # Bitstream not byte-aligned
    invalid_bs = BitStream("0x00010")
    with pytest.raises(ValueError, match="Application Data is not byte-aligned!"):
        SampleASMPayload1.from_bitstream(invalid_bs)

def test_sample_asm_payload_1_bitstream():
    # Test getting the bitstream representation of a SampleASMPayload1 object
    n_app_data_bytes = 7
    asm_payload = SampleASMPayload1(n_app_data_bytes=n_app_data_bytes)
    bs = asm_payload.bitstream

    # Check if the bitstream has the correct length
    assert len(bs) == 16 + n_app_data_bytes * 8

    # Check if the DAC and FI values are correct
    bs.pos = 0
    assert bs.read('uint:10') == 0
    assert bs.read('uint:6') == 1

    # Check if the Application Data portion is byte-aligned
    assert bs.read('bits') == '0b00000000' * n_app_data_bytes

# =============================================================================
# %% Main Function
# =============================================================================
if __name__ == '__main__':
    pytest.main()
