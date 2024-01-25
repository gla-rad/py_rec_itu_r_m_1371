# -*- coding: utf-8 -*-
"""
ASM Payloads Module.

This module contains classes for representing the "payload" (the Binary Data
portion) of ASM messages.

These payloads can be embedded either in AIS ASM or VDES-ASM messages.

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
from bitstring import pack
from bitstring import BitStream

# =============================================================================
# %% Function Definitions
# =============================================================================


# =============================================================================
# %% Class Definitions
# =============================================================================
class SampleASMPayload1:
    """
    Sample ASM payload - type 1.

    Parameters
    ----------
    n_app_data_bytes : int, optional
        Size of the Application Data portion of the ASM (bytes).
        Application Data is initialised to all 0s.
        Maximum Application Data sizes:
            - Single-line VDM sentence carrying an AIS Message 8: 38;
            - 3-slot AIS Message 8: 66;
            - 3-slot VDES-ASM broadcast w/o FEC: 157 (158 according to
              the VDES1000 datasheet);
            - 3-slot VDES-ASM broadcast with FEC: 114 (according to the
              datasheet; not yet tested);
        The default is 10.

    """
    # Designated area code
    dac = 0
    # Function identifier
    fi = 1

    application_str = "Sample ASM 1"

    fmt = '\
        uint:10=dac, \
        uint:6=fi'

    def __init__(self, n_app_data_bytes=10):
        # Note that Rec. ITU-R M.1371 requires the data output to the VDL to be
        # byte-aligned.
        self.n_app_data_bytes = n_app_data_bytes

    @classmethod
    def from_bitstream(cls, bs):
        """
        Initialise a TestASMPayload1 object from a bitstream object.

        Parameters
        ----------
        bs : bitstring.BitStream
            Bitstream representing a TestASMPayload1 object.

        Raises
        ------
        ValueError
            When an invalid DAC or FI are provided or the Application Data
            portion of the bitstream is not byte-aligned.

        Returns
        -------
        TestASMPayload1
            Test ASM Payload type 1 object.

        """
        dac, fi, app_data_bs = bs.unpack(cls.fmt + ', bits')

        if (dac != cls.dac) or (fi != cls.fi):
            raise ValueError("Invalid Application Identifier!")

        if (len(app_data_bs) % 8) != 0:
            raise ValueError("Application Data is not byte-aligned!")

        n_app_data_bytes = len(app_data_bs) // 8

        return cls(n_app_data_bytes)

    @property
    def bitstream(self):
        """
        Returns
        -------
        bs : bitstring.BitStream
            A payload bitstream formatted according to ITU-R M.1371.
            The Application Data portion of the payload does not conform to
            any particular standard; a sequence of all zeros is used
            for testing purposes.

        """
        # Construct the field name: value dictionary for the bit packing
        d = {'dac': self.dac,
             'fi': self.fi}

        # Create a bitstream using the message format and name: value dict
        bs = pack(self.fmt, **d)

        # Append the required number of zero bytes (the Application Data)
        bs.append(BitStream(self.n_app_data_bytes * 8))

        return bs

# =============================================================================
# %% Quick & Dirty Testing
# =============================================================================
if __name__ == "__main__":

    # Initialise a test ASM payload
    asm_payload_1 = SampleASMPayload1(n_app_data_bytes=2)

    print(asm_payload_1.bitstream)

    # See if we can recover the payload object from a bitstream
    asm_payload_2 = SampleASMPayload1.from_bitstream(asm_payload_1.bitstream)

    print(asm_payload_2.bitstream)
