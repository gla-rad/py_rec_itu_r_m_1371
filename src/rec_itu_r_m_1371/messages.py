# -*- coding: utf-8 -*-
"""
AIS Messages Module.

This module includes classes for representing AIS messages and functions for
text character encoding and decoding.

The message definitions and algorithms used herein are compliant with Rec.
ITU-R M.1371-5, Annex 8.

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
from bitstring import BitStream, pack

# =============================================================================
# %% Function Definitions
# =============================================================================
def ais_ascii_8b_to_6b(ascii_8b):
    """
    Convert an 8-bit ASCII-encoded string to a 6-bit ASCII encoded bitstream.

    Intended for use in AIS/ASM Message encoding as per Rec. ITU-R M.1371.

    Parameters
    ----------
    ascii_8b : str
        Input string encoded in 8-bit ASCII.

    Returns
    -------
    bs : bitstring.BitStream
        Input string encoded in 6-bit ASCII.

    """
    bs = BitStream()
    ascii_8b = ascii_8b.__str__().upper()
    for c in ascii_8b:
        ascii_ord = ord(c)
        if (ascii_ord >= 32) & (ascii_ord <= 63):
            ais_ord = ascii_ord
            bs.append('uint:6=' + str(ais_ord))
        elif (ascii_ord >= 64) & (ascii_ord <= 95):
            ais_ord = ascii_ord - 64
            bs.append('uint:6=' + str(ais_ord))

    return bs

def ais_ascii_6b_to_8b(bs):
    """
    Convert a 6-bit ASCII-encoded bitstream to an 8-bit ASCII-encoded string.

    Intended for use in AIS/ASM Message decoding as per Rec. ITU-R M.1371.

    Parameters
    ----------
    bs : bitstring.BitStream
        Input string encoded in 6-bit ASCII.

    Returns
    -------
    ascii_8b : str
        Input string encoded in 8-bit ASCII.

    """
    # TODO: Add some input testing to see if the bitstream len is divisible by 6

    n_char = len(bs) // 6
    char_lst = bs.readlist(n_char*'uint:6, ')

    char_lst[:] = [char + 64 if char < 32 else char for char in char_lst]

    return "".join(map(chr, char_lst))


# =============================================================================
# %% Class Definitions
# =============================================================================
class AISMessage8:
    """
    AIS Message 8: Binary broadcast message, as per Rec. ITU-R M.1371-5.

    Parameters
    ----------
    source_id : int
        Source ID. The MMSI number of the source station.
    payload : vdes.ais.application_layer.asm_payloads.*
        ASM payload (the Binary Data portion of the ASM).

    """
    msg_id = 8
    repeat_indicator = 0
    msg_type_str = "AIS Binary broadcast message"

    # Message format string
    fmt = '\
        uint:6=msg_id, \
        uint:2=repeat_indicator, \
        uint:30=source_id, \
        pad:2'

    def __init__(self, source_id, payload):
        self.source_id = source_id
        self.payload = payload

    @classmethod
    def from_vdes_asm(cls, vdes_asm):
        """
        Initialise message from a VDES ASM.
        (vdes.asm.application_layer.messages.ApplicationLayerMsg<1..7>).

        Intended for use where VDES ASMs need to be output as AIS-style ASMs,
        e.g. for presentation purposes.

        Note: The 2 MSBs of the Source ID are set to zero.

        """
        # FIX: Fix the message type in the docstring.

        # Mask away the extra two bits of the 32-bit VDES Source ID
        source_id = 0x3FFFFFFF & vdes_asm.source_id

        return cls(source_id, vdes_asm.asm_payload)

    @property
    def bitstream(self):
        """
        Return the message bitstream, formatted as per ITU-R M.1371-5

        """
        # Construct the field name: value dictionary for the bit packing
        d = {'msg_id': self.msg_id,
             'repeat_indicator': self.repeat_indicator,
             'source_id': self.source_id}

        # Create a bitstream using the message format and name: value dict.
        bs = pack(self.fmt, **d)

        # Append the payload bitstream
        bs += self.payload.bitstream

        return bs

    def __str__(self):
        s = """

    AIS Message 8: Binary Broadcast Message
    ---------------------------------------
    Source ID: {:d}
    Binary Data: 0x{:s}""".format(self.source_id, self.payload.bitstream.hex)

        return s


class AISMessage21:
    """
    AIS Message 21: AtoN report, as per Rec. ITU-R M.1371-4?5.

    TODO: Input parameter checking.

    TODO: AtoN Name Extension field.

    Parameters
    ----------
    source_id : int
        Source ID. The MMSI of the sending station.
    aton_type : int
        Type of AtoN (0-31).
    aton_name : str
        Name of AtoN (up to 20 characters).
    pos_accuracy : int
        Position accuracy (0-1).
    lon : float
        Longitude.
    lat : float
        Latitude.
    dimension : list
        Dimension / reference point for position; [A, B, C, D].
    epf_device_type : int
        Type of electronic position fixing device (0-15).
    time_stamp : int
        Time stamp (0-63).
    off_position : int
        Off-position indicator (0-1).
    aton_status : int
        AtoN status (0-255).
    raim_fl : int
        RAIM flag (0-1).
    vaton_fl : int
        Virtual AtoN flag (0-1).
    assigned_mode_fl : int
        Assigned mode flag (0-1).
    aton_name_extension : str, optional
        Name of AtoN extension. The default is "".

    """
    msg_id = 21
    repeat_indicator = 0
    msg_type_str = "Aids-to-navigation report"

    # Message format string
    fmt = '\
        uint:6=msg_id, \
        uint:2=repeat_indicator, \
        uint:30=source_id, \
        uint:5=aton_type, \
        bits:120=aton_name, \
        uint:1=pos_accuracy, \
        int:28=lon, \
        int:27=lat, \
        uint:9=dimension_A, \
        uint:9=dimension_B, \
        uint:6=dimension_C, \
        uint:6=dimension_D, \
        uint:4=epf_device_type, \
        uint:6=time_stamp, \
        uint:1=off_position, \
        uint:8=aton_status, \
        uint:1=raim_fl, \
        uint:1=vaton_fl, \
        uint:1=assigned_mode_fl, \
        pad:1'

    def __init__(
            self,
            source_id,
            aton_type,
            aton_name,
            pos_accuracy,
            lon,
            lat,
            dimension,
            epf_device_type,
            time_stamp,
            off_position,
            aton_status,
            raim_fl,
            vaton_fl,
            assigned_mode_fl,
            aton_name_extension=""):

        self.source_id = source_id
        self.aton_type = aton_type
        self.aton_name = aton_name
        self.pos_accuracy = pos_accuracy
        self.lon = lon
        self.lat = lat
        self.dimension = dimension  # To be specified as [A, B, C, D]
        self.epf_device_type = epf_device_type
        self.time_stamp = time_stamp
        self.off_position = off_position
        self.aton_status = aton_status
        self.raim_fl = raim_fl
        self.vaton_fl = vaton_fl
        self.assigned_mode_fl = assigned_mode_fl
        self.aton_name_extension = aton_name_extension

    @classmethod
    def from_bitstream(cls, bs):
        """
        Initialise an AISMessage21 object from a bitstream.

        Parameters
        ----------
        bs : bitstring.BitStream
            Message bitstream.

        Returns
        -------
        AISMessage21
            AIS Message 21 object.

        """
        # Unpack the bitstream using the class' format string
        msg_id, repeat_indicator, source_id, aton_type, aton_name, pos_accuracy, \
        lon, lat, dimension_A, dimension_B, dimension_C, dimension_D, \
        epf_device_type, time_stamp, off_position, aton_status, raim_fl, \
        vaton_fl, assigned_mode_fl = bs.unpack(cls.fmt)

        # Pre-process any input variables as required
        aton_name = ais_ascii_6b_to_8b(aton_name)
        aton_name_extension = ""
        lon = lon / 600000.0
        lat = lat / 600000.0

        return cls(
            source_id,
            aton_type,
            aton_name,
            pos_accuracy,
            lon,
            lat,
            [dimension_A, dimension_B, dimension_C, dimension_D],
            epf_device_type,
            time_stamp,
            off_position,
            aton_status,
            raim_fl,
            vaton_fl,
            assigned_mode_fl,
            aton_name_extension)

    @property
    def bitstream(self):
        """
        Returns
        -------
        bs : bitstring.BitStream
            Message bitstream, formatted as per Rec. ITU-R M.1371-4?5

        """
        # Pre-process any member variables as required
        aton_name = self.aton_name.__str__().ljust(20, '@')

        # Construct the field name: value dictionary for the bit packing
        d = {'msg_id': self.msg_id,
             'repeat_indicator': self.repeat_indicator,
             'source_id': self.source_id,
             'aton_type': self.aton_type,
             'aton_name': ais_ascii_8b_to_6b(aton_name),
             'pos_accuracy': self.pos_accuracy,
             'lon': int(round(self.lon*600000)),
             'lat': int(round(self.lat*600000)),
             'dimension_A': self.dimension[0],
             'dimension_B': self.dimension[1],
             'dimension_C': self.dimension[2],
             'dimension_D': self.dimension[3],
             'epf_device_type': self.epf_device_type,
             'time_stamp': self.time_stamp,
             'off_position': self.off_position,
             'aton_status': self.aton_status,
             'raim_fl': self.raim_fl,
             'vaton_fl': self.vaton_fl,
             'assigned_mode_fl': self.assigned_mode_fl}

        # Create a bitstream using the message format string and name: value
        # dict.
        bs = pack(self.fmt, **d)

        return bs

    def __str__(self):
        s = """

    AIS Message 21: Aids-to-navigation Report
    -----------------------------------------
    Source ID: {0:d}
    AtoN type: {1:d}
    AtoN name: {2}
    Position accuracy: {3:d}
    Latitude (deg): {4:f}
    Longitude (deg): {5:f}
    Dimension A (m): {6:d}
    Dimension B (m): {7:d}
    Dimension C (m): {8:d}
    Dimension D (m): {9:d}
    EPF device type: {10:d}
    Timestamp (s): {11:d}
    Off-position flag: {12:d}
    AtoN status bits: {13:b}
    RAIM flag: {14:d}
    Virtual flag: {15:d}
    Assigned mode flag: {16:d}\n""".format(
        self.source_id,
        self.aton_type,
        self.aton_name,
        self.pos_accuracy,
        self.lat,
        self.lon,
        self.dimension[0],
        self.dimension[1],
        self.dimension[2],
        self.dimension[3],
        self.epf_device_type,
        self.time_stamp,
        self.off_position,
        self.aton_status,
        self.raim_fl,
        self.vaton_fl,
        self.assigned_mode_fl)

        return s

# =============================================================================
# %% Quick & Dirty Testing
# =============================================================================
# For additional tests, see the 'tests' directory
if __name__=='__main__':
    from asm_payloads import SampleASMPayload1

    # Test the 8-bit/6-bit ASCII conversions
    ascii_8b_str = "Beam me up, Scotty!"
    ascii_6b_bs = ais_ascii_8b_to_6b(ascii_8b_str)

    # Create an AIS Message 8 (Broadcast Binary Msg.)
    ais_msg_8 = AISMessage8(
        source_id=123456789,
        payload=SampleASMPayload1(n_app_data_bytes=2))

    print(ais_msg_8)

    # Create an AIS Message 21 (AtoN Report)
    ais_msg_21 = AISMessage21(
        source_id=992356001,
        aton_type=30,
        aton_name="Jan's Virtual AtoN",
        pos_accuracy=1,
        lon=1.34,
        lat=51.92,
        dimension=[1,2,3,4],
        epf_device_type=0,
        time_stamp=60,
        off_position=0,
        aton_status=0,
        raim_fl=0,
        vaton_fl=1,
        assigned_mode_fl=0,
        aton_name_extension="")

    print(ais_msg_21)

    # Test conversion to/from a bitstream
    ais_msg_21_from_bs = AISMessage21.from_bitstream(ais_msg_21.bitstream)

    print(ais_msg_21_from_bs)
