import time
from typing import Optional

import broadlink

from homecontrol.broadlink.structs import BroadlinkConnectionInfo


class BroadlinkDevice:
    """Wrapper for broadlink devices"""

    # Max time we expect learning an IR packet to take (seconds)
    LEARNING_TIMEOUT = 10

    # Minimum time between querying if anything has been learnt yet (seconds)
    LEARNING_CHECK_TIME = 1

    _connection_info: BroadlinkConnectionInfo
    _device: broadlink.Device

    def __init__(self, connection_info: BroadlinkConnectionInfo) -> None:
        """Creates and authenticates the broadlink device"""
        self._connection_info = connection_info
        self._device = broadlink.hello(self._connection_info.ip_address)
        self._device.auth()

    def get_ir_packet(self) -> Optional[bytes]:
        """Puts the device in learning mode and waits until an IR packet is
        returned or we reach a timeout in which case this returns None

        Returns:
            Optional[bytes]: The IR packet, or None if the timeout was reached
        """

        # Start learning mode
        self._device.enter_learning()

        # Current packet
        packet = None

        # Start, elapsed and elapsed time that we last did a check for any
        # IR packet
        start_time = time.time()
        current_elapsed_time = 0
        last_check_time = 0

        # Keep checking for packets until we reach the timeout
        while current_elapsed_time < self.LEARNING_TIMEOUT:
            current_elapsed_time = time.time() - start_time

            # Due a check?
            if current_elapsed_time - last_check_time > self.LEARNING_CHECK_TIME:
                last_check_time = current_elapsed_time

                # Attempt to get a packet, but ignore errors if nothing found
                try:
                    packet = self._device.check_data()
                    return packet
                except broadlink.exceptions.ReadError:
                    pass

        return None

    def send_ir_packet(self, packet: bytes):
        """
        Sends an IR packet to the device
        """
        self._device.send_data(packet)
