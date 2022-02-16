#! /usr/bin/env python3
#
# Copyright (C) 2021  Fx Bricks Inc.
# This file is part of the pfxbrick python module.
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# PFx Brick BLE session helpers


import asyncio
import logging
import sys

from bleak import BleakClient, BleakScanner

from pfxbrick import *
from pfxbrick.pfxexceptions import *
from pfxbrick.pfxhelpers import *
from pfxbrick.pfxmsg import *

DEV_INFO_UUID = "%x" % (PFX_BLE_GATT_DEV_INFO_UUID)
DEV_SN_UUID = "%x" % (PFX_BLE_GATT_DEV_SN_UUID)
MAX_RETRIES = 200
RX_RETRY_TIME = 0.05


async def ble_device_scanner(
    scan_time=3.0,
    min_devices=1,
    scan_timeout=30.0,
    filters=None,
    silent=False,
    verbose=False,
):
    """
    Performs a Bluetooth scan for available peripheral devices which advertise
    themselves as PFx Bricks.

    This coroutine will search for the required number of devices in scan_time
    chunks up until the scan_timeout interval has elapsed.

    :param scan_time: :obj:`float` scan time interval to look for devices
    :param min_devices: :obj:`int` minimum number of devices to look for before returning
    :param scan_timeout: :obj:`float` timeout interval for finding the required min_devices
    :param filters: :obj:`list` or `str` optional device name filters, e.g. "16 MB"
    :param silent: :obj:`boolean` a flag to disable printing of status
    :param verbose: :obj:`boolean` a flag to print a verbose list of advertising devices

    :returns: [:obj:`BLEDevice`] a list of PFx Brick device objects described in a Bleak BLEDevice class.
    """

    def _filter_device(dc):
        if filters is not None:
            for f in filters:
                if f in dc.name:
                    return True
            return False
        return True

    pfxdevs = []
    total_scan_time = 0
    if filters is not None:
        if isinstance(filters, str):
            filters = [filters]
    while len(pfxdevs) < min_devices:
        if not silent:
            print("Scanning...")
        async with BleakScanner() as scanner:
            await asyncio.sleep(scan_time)
            total_scan_time += scan_time
            devices = scanner.discovered_devices
        if not silent and len(devices) > 0:
            print("Found %d advertising devices" % (len(devices)))
            if verbose:
                for i, d in enumerate(devices):
                    s = '%2d. UUID=%-36s "%s"' % (i + 1, d.address, d.name)
                    print(s)
        for d in devices:
            if "PFx Brick" in d.name:
                if _filter_device(d):
                    if not silent:
                        print("Found %s UUID=%-36s" % (d.name, d.address))
                    pfxdevs.append(d)
        if total_scan_time > scan_timeout:
            break
    return pfxdevs


async def find_ble_pfxbricks(devices, connect_interval=5.0, timeout=30.0, silent=False):
    """
    Resolves a list of scanned candidate Bluetooth devices into valid PFx Brick devices.

    :param devices: [:obj:`BLEDevice`] a list of candidate PFx Brick device objects
    :param connect_interval: :obj:`float` time interval to wait for connection
    :param timeout: :obj:`float` timeout interval for attempting a device connection
    :param silent: :obj:`boolean` a flag to disable printing of status

    :returns: [:obj:`dict`] a list of dictionary objects for each PFx Brick verified by connection. The dictionary contains keys for "address", "serial_no" and "name".
    """

    async def connect_device(device, connect_timeout):
        async with BleakClient(device.address, timeout=connect_timeout) as client:
            sn = None
            # only continue if we have a connection to the device
            if client.is_connected:
                rssi = device.rssi
                # get all the available services from the device
                services = await client.get_services()
                for service in services:
                    if DEV_INFO_UUID.lower() in service.uuid:
                        for char in service.characteristics:
                            if DEV_SN_UUID in char.uuid:
                                sn = bytes(await client.read_gatt_char(char.uuid))
                                return sn, rssi

    pfxbricks = []
    for d in devices:
        sn = None
        connected = False
        total_connect_time = 0
        while not connected and total_connect_time < timeout:
            try:
                if not silent:
                    print('Discovering device %s "%s"...' % (d.address, d.name))
                sn, rssi = await connect_device(d, connect_timeout=connect_interval)
                connected = True
            except:
                total_connect_time += connect_interval
        if sn is not None:
            if not silent:
                fmt = 'Found "%s" S/N=%s UUID=%s'
                if rssi is not None:
                    fmt = fmt + " RSSI=%d dBm"
                    print(fmt % (d.name, str(sn, encoding="utf8"), d.address, rssi))
                else:
                    print(fmt % (d.name, str(sn, encoding="utf8"), d.address))
            pfxbricks.append({"address": d.address, "serial_no": sn, "name": d.name})

    return pfxbricks


class PFxBrickBLE(PFxBrick):
    """
    Inherited sub-class of a :obj:`PFxBrick` object class.

    This sub-class of :obj:`PFxBrick` is necessary for communicating with a
    PFx Brick via Bluetooth LE.  Since the Bluetooth communication stack is
    based on the Bleak python module, it runs in an asynchronous context using
    python's async/await mechanisms.  Since this requires co-routines instead
    of conventional function methods, this sub-class reimplements many of
    the parent :obj:`PFxBrick` class methods as asyncronous co-routines.

    Almost all class functionality is more or less the same as the USB based
    PFxBrick class and fortunately some of the utility methods can be
    reused.

    You can initialize a `PFxBrickBLE` object instance with either a dictionary
    or a UUID string that specifies which PFx Brick to connect with.

    The dictionary describing the desired PFx Brick peripheral device
    is as follows:

    "address":  hardware address of the PFx Brick obtained by a Bluetooth device scan
    "serial_no":  optional serial number of the PFx Brick obtained by a device scan
    "name": optional name of the PFx Brick device obtained by a device scan

    Only the "address" key is mandatory, the other keys are provided if desired.

    Alternatively, you can simply initialize the PFxBrickBLE class using a
    UUID string like the following example:

    brick = PFxBrickBLE(uuid="059930E2-BE75-48A4-B193-3AD3F67246E4")

    Unless the Bluetooth hardware address of the PFx Brick is known in advance,
    then it must be obtained by performing a Bluetooth peripheral device scan to
    see which Bluetooth devices are currently advertising availability.  The
    Bluetooth hardware address is operating system dependent and must be provided
    in a UUID form that is compatible with your OS.

    for Windows and Linux this is typically in the form of "24:71:89:cc:09:05"
    and on macOS it is in the form of "B9EA5233-37EF-4DD6-87A8-2A875E821C46"

    Attributes:
        dev (:obj:`device`): a device handle which is reference to self

        is_open (:obj:`boolean`): a flag indicating connected session status

        client (:obj:`BleakClient`): Bleak BLE client object reference

        callback_audio_done (:obj:`func`): a function callback reference in response to a `PFX_NOTIFICATION_AUDIO_PLAY_DONE` notification. Must have the call signature `func(fileid, filename)`

        callback_audio_play (:obj:`func`): a function callback reference in response to a `PFX_NOTIFICATION_AUDIO_PLAY` notification. Must have the call signature `func(fileid, filename)`

        callback_motora_stop (:obj:`func`): a function callback reference in response to a `PFX_NOTIFICATION_MOTORA_STOP` notification. Must have the call signature `func()`

        callback_motora_speed (:obj:`func`): a function callback reference in response to a `PFX_NOTIFICATION_MOTORA_CURR_SPD` notification. Must have the call signature `func(speed)`

        callback_motorb_stop (:obj:`func`): a function callback reference in response to a `PFX_NOTIFICATION_MOTORB_STOP` notification. Must have the call signature `func()`

        callback_motorb_speed (:obj:`func`): a function callback reference in response to a `PFX_NOTIFICATION_MOTORB_CURR_SPD` notification. Must have the call signature `func(speed)`

    :param dev_dict: :obj:`dict` a dictionary describing the PFx Brick device to connect. Must have the key "address" with the Bluetooth MAC address of the PFx Brick. Optional keys "name" and "serial_no" can be provided.
    :param uuid: :obj:`str` a string representing the UUID/address of the PFx Brick device. This is an alternative to using the `dev_dict` argument to specify the PFx Brick.
    :param debug: :obj:`boolean` a flag to enable low level debug logging of Bluetooth session activity
    """

    def __init__(self, dev_dict=None, uuid=None, debug=False):
        super().__init__()
        if dev_dict is not None:
            if "address" not in dev_dict:
                raise BLEDeviceMissingAddressException()
            else:
                self.ble_address = dev_dict["address"]
            if "serial_no" in dev_dict:
                self.serial_no = dev_dict["serial_no"]
            if "name" in dev_dict:
                self.usb_prod_str = dev_dict["name"]
        elif uuid is not None:
            self.ble_address = uuid
        else:
            raise BLEDeviceMissingAddressException()
        self.client = None
        self.is_open = False
        self.dev = None
        self.callback_audio_done = None
        self.callback_audio_play = None
        self.callback_motora_stop = None
        self.callback_motora_speed = None
        self.callback_motorb_stop = None
        self.callback_motorb_speed = None
        self._disconnect_flag = False
        self._rxbuff = None
        self._log = logging.getLogger(str(self.__class__))
        if debug:
            self._log.setLevel(logging.DEBUG)
            h = logging.StreamHandler(sys.stdout)
            h.setLevel(logging.DEBUG)
            self._log.addHandler(h)

    async def open(self, timeout=10):
        """
        Opens a BLE communication session with a PFx Brick.

        This method is called after this instance has been initialized with a valid
        Bluetooth address.

        :param timeout: :obj:`float` timeout interval (seconds) to wait for an open connection
        """
        self.client = BleakClient(
            self.ble_address, disconnected_callback=self._disconnected_callback
        )
        self.is_open = await self.client.connect(timeout=timeout)
        if self.is_open:
            self._log.info("Connected to PFx Brick %s" % (self.ble_address))
            await self.client.start_notify(PFX_BLE_GATT_UART_RX_UUID, self._rx_callback)
            self.dev = self
            self.usb_manu_str = "Fx Bricks"
        else:
            self._log.error("Timeout connecting to %s" % (self.ble_address))
            raise BLEConnectTimeoutException()

    async def close(self):
        """
        Closes a BLE communication session with a PFx Brick.
        """
        if self.is_open and self.client is not None:
            self._disconnect_flag = True
            await self.client.disconnect()
            self._log.info("Connection closed with PFx Brick %s" % (self.ble_address))

    async def get_rssi(self):
        """
        Get a recent measurement of RSSI (received signal strength)

        :returns: :obj:`int` or None of signal strength in dBm
        """
        rssi = None
        if self.is_open:
            rssi = await self.client.get_rssi()
        return rssi

    def _disconnected_callback(self, client):
        """
        BLE disconnection event handler.
        This is always called by the Bleak BLE API since this callback is registered
        in the :obj:`open` method.
        """
        if not self._disconnect_flag:
            self._log.warning(
                "Unexpected disconnection from PFx Brick %s" % (self.ble_address)
            )
            raise BLEDeviceDisconnectedException()

    def _process_notification(self, msg):
        if msg[0] == PFX_MSG_NOTIFICATION:
            if msg[1] == PFX_NOTIFICATION_AUDIO_PLAY_DONE:
                if self.callback_audio_done is not None:
                    fn = self.filedir.get_file_dir_entry(msg[2])
                    self.callback_audio_done(msg[2], fn.name)
            if msg[1] == PFX_NOTIFICATION_AUDIO_PLAY:
                if self.callback_audio_play is not None:
                    fn = self.filedir.get_file_dir_entry(msg[2])
                    self.callback_audio_play(msg[2], fn.name)
            if msg[1] == PFX_NOTIFICATION_MOTORA_CURR_SPD:
                if self.callback_motora_speed is not None:
                    self.callback_motora_speed(int8_toint(msg[2]))
            if msg[1] == PFX_NOTIFICATION_MOTORA_STOP:
                if self.callback_motora_stop is not None:
                    self.callback_motora_stop()
            if msg[1] == PFX_NOTIFICATION_MOTORB_CURR_SPD:
                if self.callback_motorb_speed is not None:
                    self.callback_motorb_speed(int8_toint(msg[2]))
            if msg[1] == PFX_NOTIFICATION_MOTORB_STOP:
                if self.callback_motorb_stop is not None:
                    self.callback_motorb_stop()

    def _rx_callback(self, sender, data):
        self._log.info("Rx Data: %s" % (data))
        self._rxbuff = data
        # look for notificaitons in the received buffer
        # and activate callbacks if required
        last_idx = -3
        for i, b in enumerate(self._rxbuff):
            if b == PFX_MSG_NOTIFICATION and i > last_idx + 2:
                if (i + 2) < len(self._rxbuff):
                    self._process_notification(self._rxbuff[i : i + 3])
                    last_idx = i

    async def _tx_msg(self, msg):
        self._rxbuff = []
        msg_type = int(0x80 | msg[3])
        chunks = [msg[i : i + 20] for i in range(0, len(msg), 20)]
        for chunk in chunks:
            await self.client.write_gatt_char(PFX_BLE_GATT_UART_TX_UUID, chunk)
            self._log.info("Tx Data: %s" % (chunk))
        retries = 0
        while len(self._rxbuff) == 0 and retries < MAX_RETRIES:
            await asyncio.sleep(RX_RETRY_TIME)
            retries += 1
        if retries >= MAX_RETRIES:
            self._log.error(
                "Timeout waiting for response from PFx Brick %s" % (self.ble_address)
            )
            await self.close()
            raise ResponseTimeoutException()
        if len(self._rxbuff) > 0:
            if self._rxbuff[0] != msg_type and self._rxbuff[0] != PFX_MSG_NOTIFICATION:
                self._log.error(
                    "Invalid response from PFx Brick %s" % (self.ble_address)
                )
                await self.close()
                raise InvalidResponseException()

    async def ble_transaction(self, msg):
        """
        Wraps and sends an ICD message via Bluetooth and waits for and returns a
        corresponding response from the PFx Brick.

        :param msg: [:obj:`int`] ICD message to send as an integeter list of bytes
        :returns: [:obj:`int`] returned message in a byte array list
        """
        tx = bytearray()
        # wrap the message with the required prefix/suffix delimiters [[[ ]]]
        tx.extend([0x5B, 0x5B, 0x5B])
        tx.extend(msg)
        tx.extend([0x5D, 0x5D, 0x5D])
        await self._tx_msg(tx)
        return self._rxbuff

    async def get_icd_rev(self, silent=False):
        """
        Requests the version of Interface Control Document (ICD)
        the connected PFx Brick supports using the `PFX_CMD_GET_ICD_REV`
        ICD message.  The resulting version number is stored in
        this class and also returned.

        :param boolean silent: flag to optionally silence the status LED blink

        :returns: :obj:`str` ICD version, e.g. "3.38"
        """
        res = await cmd_get_icd_rev(self.dev, silent)
        self.icd_rev = uint16_tover(res[1], res[2])
        self.config.icd_rev = self.icd_rev
        return self.icd_rev

    async def get_status(self):
        """
        Requests the top level operational status of the PFx Brick
        using the `PFX_CMD_GET_STATUS ICD` message.  The resulting
        status data is stored in this class and can be queried
        with typical class member access methods or the print_status method.
        """
        res = await cmd_get_status(self.dev)
        if res:
            self.status = res[1]
            self.error = res[2]
            self.product_id = uint16_tostr(res[7], res[8])
            self.serial_no = uint32_tostr(res[9], res[10], res[11], res[12])
            self.product_desc = bytes(res[13:37]).decode("utf-8")
            self.firmware_ver = uint16_tover(res[37], res[38])
            self.firmware_build = uint16_tostr(res[39], res[40])

    async def get_config(self):
        """
        Retrieves configuration settings from the PFx Brick using
        the `PFX_CMD_GET_CONFIG ICD` message. The configuration data
        is stored in the :obj:`PFxBrick.config` class member variable.
        """
        res = await cmd_get_config(self.dev)
        if res:
            self.config.from_bytes(res)

    async def set_config(self):
        """
        Writes the contents of the PFxConfig data structure class to
        the PFx Brick using the `PFX_CMD_SET_CONFIG` ICD message.

        It is recommended that the configuration be read from the
        PFx Brick (using get_config) before any changes are made to
        the configuration and written back. This ensures that any
        configuration settings which are not desired to be changed
        are left in the same state.
        """
        res = await cmd_set_config(self.dev, self.config.to_bytes())

    async def reset_factory_config(self):
        """
        Resets the PFx Brick configuration settings to factory defaults.
        """
        res = await cmd_set_factory_defaults(self.dev)

    async def get_name(self):
        """
        Retrieves the user defined name of the PFx Brick using
        the `PFX_CMD_GET_NAME ICD` message. The name is stored in
        the name class variable as a UTF-8 string.

        :returns: :obj:`str` user defined name
        """
        res = await cmd_get_name(self.dev)
        if res:
            self.name = safe_unicode_str(res[1:25])
        return self.name

    async def set_name(self, name):
        """
        Sets the user defined name of the PFx Brick using the
        `PFX_CMD_SET_NAME` ICD message.

        :param name: :obj:`str` new name to set (up to 24 character bytes, UTF-8)
        """
        res = await cmd_set_name(self.dev, name)

    async def get_action_by_address(self, address):
        """
        Retrieves a stored action indexed by address rather than a
        combination of eventID and IR channel.  The address is converted into a
        [eventID, IR channel] pair and the get_action method is
        called with this function as a convenient wrapper.

        :param address: :obj:`int` event/action LUT address (0 - 0x7F)
        :returns: :obj:`PFxAction` class filled with retrieved LUT data
        """
        if address > EVT_LUT_MAX:
            self._log.warning(
                "Requested action at address %02X is out of range" % (address)
            )
            return None
        else:
            evt, ch = address_to_evtch(address)
            a = await self.get_action(evt, ch)
            return a

    async def get_action(self, evtID, ch):
        """
        Retrieves the stored action associated with a particular
        [eventID / IR channel] event. The eventID and channel value
        form a composite address pointer into the event/action LUT
        in the PFx Brick. The address to the LUT is formed as:

        Address[5:2] = event ID
        Address[1:0] = channel

        :param evtID: :obj:`int` event ID LUT address component (0 - 0x20)
        :param channel: :obj:`int` channel index LUT address component (0 - 3)
        :returns: :obj:`PFxAction` class filled with retrieved LUT data
        """
        if ch > 3 or evtID > EVT_ID_MAX:
            self._log.warning(
                "Requested action (id=%02X, ch=%02X) is out of range" % (evtID, ch)
            )
            return None
        else:
            res = await cmd_get_event_action(self.dev, evtID, ch)
            action = PFxAction()
            if res:
                action.from_bytes(res)
            return action

    async def set_action_by_address(self, address, action):
        """
        Sets a new stored action in the event/action LUT at the
        address specified. The address is converted into a
        [eventID, IR channel] pair and the set_action method is
        called with this function as a convenient wrapper.

        :param address: :obj:`int` event/action LUT address (0 - 0x7F)
        :param action: :obj:`PFxAction` action data structure class
        """
        if address > EVT_LUT_MAX:
            self._log.warning(
                "Requested action at address %02X is out of range" % (address)
            )
            return None
        else:
            evt, ch = address_to_evtch(address)
            await self.set_action(evt, ch, action)

    async def set_action(self, evtID, ch, action):
        """
        Sets a new stored action associated with a particular
        [eventID / IR channel] event. The eventID and channel value
        form a composite address pointer into the event/action LUT
        in the PFx Brick. The address to the LUT is formed as:

        Address[5:2] = event ID
        Address[1:0] = channel

        :param evtID: :obj:`int` event ID LUT address component (0 - 0x20)
        :param ch: :obj:`int` channel index LUT address component (0 - 3)
        :param action: :obj:`PFxAction` action data structure class
        """
        if ch > 3 or evtID > EVT_ID_MAX:
            self._log.warning(
                "Requested action (id=%02X, ch=%02X) is out of range" % (evtID, ch)
            )
            return None
        else:
            res = await cmd_set_event_action(self.dev, evtID, ch, action.to_bytes())

    async def test_action(self, action):
        """
        Executes a passed action data structure. This function is
        used to "test" actions to see how they behave. The passed
        action is not stored in the event/action LUT.

        :param action: :obj:`PFxAction` action data structure class
        """
        res = await cmd_test_action(self.dev, action.to_bytes())

    async def clear_action_by_address(self, address):
        """
        Clears a stored action in the event/action LUT at the
        address specified. The address is converted into a
        [eventID, IR channel] pair and the set_action method is
        called with this function as a convenient wrapper.

        :param address: :obj:`int` event/action LUT address (0 - 0x7F)
                        :obj:`list,tuple,range` specify a list or range of addresses
        """
        if isinstance(address, (list, tuple)):
            addresses = address
        elif isinstance(address, range):
            addresses = [x for x in range]
        else:
            addresses = [address]
        for a in addresses:
            if a > EVT_LUT_MAX:
                print("Requested action at address %02X is out of range" % (a))
                return None
            else:
                evt, ch = address_to_evtch(a)
                await self.clear_action(evt, ch)

    async def clear_action(self, evtID, ch):
        """
        Clears a stored action associated with a particular
        [eventID / IR channel] event. The eventID and channel value
        form a composite address pointer into the event/action LUT
        in the PFx Brick. The address to the LUT is formed as:

        Address[5:2] = event ID
        Address[1:0] = channel

        :param evtID: :obj:`int` event ID LUT address component (0 - 0x20)
        :param ch: :obj:`int` channel index LUT address component (0 - 3)
        """
        if ch > 3 or evtID > EVT_ID_MAX:
            print("Requested action (id=%02X, ch=%02X) is out of range" % (evtID, ch))
            return None
        else:
            # set to an empty PFxAction to clear
            res = await cmd_set_event_action(
                self.dev, evtID, ch, PFxAction().to_bytes()
            )

    async def find_startup_action(self, lightfx=None, soundfx=None, motorfx=None):
        raise NotImplementedError("PFx Brick method not supported over Bluetooth")

    async def set_motor_speed(self, ch, speed, duration=None):
        """
        A convenience wrapper for `PFxAction().set_motor_speed`

        :param ch: [:obj:`int`] a list of motor channels (1-4)
        :param speed: :obj:`int` desired motor speed (-100 to +100)
        :param duration: :obj:`float` optional duration (in seconds) to run motor, runs indefinitely if not specified

        If the duration value is specified, it represents the desired motor
        run time in seconds. Note that this value will be rounded to the
        nearest fixed interval of the DURATION parameter as defined in the ICD
        ranging between 16 fixed values from 0.5 sec to 5 min.
        """
        await self.test_action(
            PFxAction().set_motor_speed(ch, speed, duration=duration)
        )

    async def stop_motor(self, ch):
        """
        A convenience wrapper for `PFxAction().stop_motor`

        :param ch: [:obj:`int`] a list of motor channels (1-4)
        """
        await self.test_action(PFxAction().stop_motor(ch))

    async def light_on(self, ch):
        """
        A convenience wrapper for `PFxAction().light_on`

        :param ch: [:obj:`int`] a list of light channels (1-8)
        """
        await self.test_action(PFxAction().light_on(ch))

    async def light_off(self, ch):
        """
        A convenience wrapper for `PFxAction().light_off`

        :param ch: [:obj:`int`] a list of light channels (1-8)
        """
        await self.test_action(PFxAction().light_off(ch))

    async def light_toggle(self, ch):
        """
        A convenience wrapper `for PFxAction().light_toggle`

        :param ch: [:obj:`int`] a list of light channels (1-8)
        """
        await self.test_action(PFxAction().light_toggle(ch))

    async def set_brightness(self, ch, brightness):
        """
        A convenience wrapper for `PFxAction().set_brightness`

        :param ch: [:obj:`int`] a list of light channels (1-8)
        :param brightness: :obj:`int` brightness (0 - 255 max)
        """
        await self.test_action(PFxAction().set_brightness(ch, brightness))

    async def combo_light_fx(self, fx, param=[0, 0, 0, 0, 0]):
        """
        A convenience wrapper for `PFxAction().combo_light_fx`

        :param fx: :obj:`int` desired light effect
        :param param: [:obj:`int`] a list of up to 5 light parameters
        """
        await self.test_action(PFxAction().combo_light_fx(fx, param=param))

    async def light_fx(self, ch, fx, param=[0, 0, 0, 0, 0]):
        """
        A convenience wrapper for `PFxAction().light_fx`

        :param ch: [:obj:`int`] a list of light channels (1-8)
        :param fx: :obj:`int` desired light effect
        :param param: [:obj:`int`] a list of up to 5 light parameters
        """
        await self.test_action(PFxAction().light_fx(ch, fx, param=param))

    async def sound_fx(self, fx, param=[0, 0], fileID=None):
        """
        A convenience wrapper for `PFxAction().sound_fx`

        :param fx: :obj:`int` desired sound action
        :param param: [:obj:`int`] a list of up to 2 sound parameters
        :param fileID: :obj:`int` file ID of an audio file in the file system
        """
        if fileID is not None:
            fileID = await self.file_id_from_str_or_int(fileID)
        await self.test_action(PFxAction().sound_fx(fx, param=param, fileID=fileID))

    async def play_audio_file(self, fileID):
        """
        A convenience wrapper for `PFxAction().sound_fx`

        :param fileID: :obj:`int` or :obj:`str` file ID or filename of an audio file in the file system
        """
        fileID = await self.file_id_from_str_or_int(fileID)
        await self.test_action(PFxAction().play_audio_file(fileID=fileID))

    async def stop_audio_file(self, fileID):
        """
        A convenience wrapper for `PFxAction().stop_audio_file`

        :param fileID: :obj:`int` or :obj:`str` file ID or filename of an audio file in the file system
        """
        fileID = await self.file_id_from_str_or_int(fileID)
        await self.test_action(PFxAction().stop_audio_file(fileID=fileID))

    async def repeat_audio_file(self, fileID):
        """
        A convenience wrapper for `PFxAction().repeat_audio_file`

        :param fileID: :obj:`int` or :obj:`str` file ID or filename of an audio file in the file system
        """
        fileID = await self.file_id_from_str_or_int(fileID)
        await self.test_action(PFxAction().repeat_audio_file(fileID=fileID))

    async def set_volume(self, volume):
        """
        A convenience wrapper for `PFxAction().set_volume`

        :param volume: :obj:`int` desired audio volume (0 - 100%)
        """
        await self.test_action(PFxAction().set_volume(volume))

    async def refresh_file_dir(self):
        """
        Reads the PFx Brick file system directory. This includes
        the total storage used as well as the remaining capacity.
        Individual file directory entries are stored in the
        :obj:`PFxBrick.filedir.files` class variable.
        """
        res = await cmd_get_free_space(self.dev)
        if res:
            self.filedir.bytesLeft = uint32_toint(res[3:7])
            capacity = uint32_toint(res[7:11])
            self.filedir.bytesUsed = capacity - self.filedir.bytesLeft
        res = await cmd_get_num_files(self.dev)
        if res:
            self.filedir.files = []
            self.filedir.numFiles = uint16_toint(res[3:5])
            file_count = 0
            for i in range(PFX_AUDIO_FILES_MAX):
                res = await cmd_get_dir_entry(self.dev, i + 1)
                d = PFxFile()
                d.from_bytes(res)
                if d.id < 0xFF:
                    self.filedir.files.append(d)
                    file_count += 1
                if file_count >= self.filedir.numFiles:
                    break

    async def put_file(self, fileID, fn, show_progress=True):
        """
        PFx Brick file system operations not supported over Bluetooth
        raises :obj:`NotImplementedError`
        """
        raise NotImplementedError(
            "PFx Brick file system operations not supported over Bluetooth"
        )

    async def get_file(self, fileID, fn=None, show_progress=True):
        """
        PFx Brick file system operations not supported over Bluetooth
        raises :obj:`NotImplementedError`
        """
        raise NotImplementedError(
            "PFx Brick file system operations not supported over Bluetooth"
        )

    async def remove_file(self, fileID):
        """
        PFx Brick file system operations not supported over Bluetooth
        raises :obj:`NotImplementedError`
        """
        raise NotImplementedError(
            "PFx Brick file system operations not supported over Bluetooth"
        )

    async def format_fs(self, quick=False):
        """
        PFx Brick file system operations not supported over Bluetooth
        raises :obj:`NotImplementedError`
        """
        raise NotImplementedError(
            "PFx Brick file system operations not supported over Bluetooth"
        )

    async def set_file_attributes(self, fileID, attr, mask=0x7C):
        """
        PFx Brick file system operations not supported over Bluetooth
        raises :obj:`NotImplementedError`
        """
        raise NotImplementedError(
            "PFx Brick file system operations not supported over Bluetooth"
        )

    async def rename_file(self, fileID, new_name):
        """
        PFx Brick file system operations not supported over Bluetooth
        raises :obj:`NotImplementedError`
        """
        raise NotImplementedError(
            "PFx Brick file system operations not supported over Bluetooth"
        )

    async def stop_script(self):
        """
        Stops all script execution.
        """
        res = await cmd_run_script(self.dev, 0xFF)

    async def run_script(self, scriptfile):
        """
        Runs a specified script file on the PFx Brick filesystem.

        A file is identified either by its numeric file ID (0 - 254) or alphanumeric
        filename as a string.

        :param scriptfile: :obj:`int` or :obj:`str` file ID or file name string
        """
        fileid = await self.file_id_from_str_or_int(scriptfile)
        res = await cmd_run_script(self.dev, fileid)

    async def file_id_from_str_or_int(self, filespec):
        """
        Returns a numeric file ID from either a string filename or integer file ID.

        A file is identified on the PFx Brick filesystem primarily by its numeric
        file ID (0 - 254).  A file ID of 255 is an invalid or non-existant file.
        A numeric file ID can be queried using its alphanumeric filename in the
        filesystem directory.  This function performs this lookup if necessary,
        i.e. if a string filename is provided.

        :param filespec: :obj:`int` or :obj:`str` file ID or file name string
        :returns: :obj:`int` numeric file ID from PFx Brick filesystem, or 0xFF if not found
        """
        if isinstance(filespec, int):
            return filespec
        elif isinstance(filespec, str):
            fileid = 0xFF
            fb = bytes(filespec, "utf-8")
            p = [len(fb)]
            p.extend(fb)
            res = await cmd_file_dir(self.dev, PFX_DIR_REQ_GET_NAMED_FILE_ID, p)
            if len(res) >= 3 and not res[2] == PFX_ERR_FILE_NOT_FOUND:
                fileid = int(res[2])
            return fileid
        return 0xFF

    async def get_current_state(self):
        """
        Returns the current state of the PFx Brick operating parameters.

        :returns: :obj:`PFxState` a dataclass container with state information
        """
        res = await cmd_get_current_state(self.dev)
        self.state.from_bytes(res)
        return self.state

    async def get_fs_state(self):
        """
        PFx Brick operation not supported over Bluetooth
        raises :obj:`NotImplementedError`
        """
        raise NotImplementedError("PFx Brick method not supported over Bluetooth")

    async def get_bt_state(self):
        """
        PFx Brick operation not supported over Bluetooth
        raises :obj:`NotImplementedError`
        """
        raise NotImplementedError("PFx Brick method not supported over Bluetooth")

    async def send_raw_icd_command(self, msg):
        """
        Sends a raw ICD command message represented as a list of bytes.

        :returns: :obj:`bytes` response from the PFx Brick
        """
        res = await cmd_raw(self.dev, msg)
        return res

    async def set_notifications(self, events):
        """
        Enables user selected notifications to be sent asynchronously from the PFx Brick.

        :param events: :obj:`int` a bitwise OR of notification flags:

        - :obj:`PFX_NOTIFICATION_AUDIO_PLAY_DONE = 0x01`
        - :obj:`PFX_NOTIFICATION_AUDIO_PLAY = 0x02`
        - :obj:`PFX_NOTIFICATION_MOTORA_CURR_SPD = 0x04`
        - :obj:`PFX_NOTIFICATION_MOTORA_STOP = 0x08`
        - :obj:`PFX_NOTIFICATION_MOTORB_CURR_SPD = 0x10`
        - :obj:`PFX_NOTIFICATION_MOTORB_STOP = 0x20`
        - :obj:`PFX_NOTIFICATION_TO_USB = 0x80`
        - :obj:`PFX_NOTIFICATION_TO_BLE = 0x40`

        Note that :obj:`PFX_NOTIFICATION_TO_BLE` is automatically set and does not need to be specified.
        """

        # if notifications are configured for audio events, refresh file directory
        # so that we can resolve file ID numbers to filenames
        if (
            events & PFX_NOTIFICATION_AUDIO_PLAY
            or events & PFX_NOTIFICATION_AUDIO_PLAY_DONE
        ):
            await self.refresh_file_dir()
        res = await cmd_set_notifications(self.dev, PFX_NOTIFICATION_TO_BLE | events)

    async def disable_notifications(self):
        """
        Disables asynchronous notifications sent from the PFx Brick.
        """
        res = await cmd_set_notifications(self.dev, 0)
