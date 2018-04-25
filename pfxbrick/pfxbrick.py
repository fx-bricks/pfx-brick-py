#! /usr/bin/env python3

# PFx Brick python API

import hid
from pfxbrick.pfx import *
from pfxbrick.pfxconfig import PFxConfig
from pfxbrick.pfxaction import PFxAction
from pfxbrick.pfxfiles import PFxDir, PFxFile
from pfxbrick.pfxmsg import *
from pfxbrick.pfxhelpers import *


class PFxBrick:
    """
    Top level PFx Brick object class.
    
    This class is used to initialize and maintain a communication session
    with a USB connected PFx Brick.
    """
    def __init__(self):
        self.product_id = ""
        self.serial_no = ""
        self.product_desc = ""
        self.firmware_ver = ""
        self.firmware_build = ""
        self.icd_rev = ""
        self.status = 0
        self.error = 0
        self.hid = ''
        self.usb_vid = PFX_USB_VENDOR_ID
        self.usb_pid = PFX_USB_PRODUCT_ID
        self.usb_manu_str = ''
        self.usb_prod_str = ''
        self.usb_serno_str = ''
        self.is_open = False    
        self.name = ''
        
        self.config = PFxConfig()
        self.filedir = PFxDir()

    def find_bricks(self, show_list=False):
        """
        Enumerate and optionally print a list PFx Bricks currently connected to the USB bus.

        :param boolean show_list: optionally print a list of enumerated PFx Bricks
        :returns: the number of bricks discovered
        """
        numBricks = 0
        serials = []
        if not self.is_open:
            for dev in hid.enumerate():
                if dev['vendor_id'] == PFX_USB_VENDOR_ID and dev['product_id'] == PFX_USB_PRODUCT_ID:
                    if dev['serial_number'] not in serials:
                        numBricks += 1
                        serials.append(dev['serial_number'])
                        self.hid = hid.device()
                        self.hid.open(PFX_USB_VENDOR_ID, PFX_USB_PRODUCT_ID, dev['serial_number'])
                        self.usb_manu_str = self.hid.get_manufacturer_string()
                        self.usb_prod_str = self.hid.get_product_string()
                        self.usb_serno_str = self.hid.get_serial_number_string()
                        if show_list == True:
                            print('%d. %s, Serial No: %s' % (numBricks, self.usb_prod_str, self.usb_serno_str))
                        self.hid.close()
        else:
            print("A PFx Brick session is currently open. Close the session before enumerating new PFx Bricks.")
        return numBricks                

        
    def open(self, ser_no=None):
        """
        Opens a USB communication session with a PFx Brick. If multiple PFx Bricks are
        connected, then a serial number must be specified to connect to a unique PFx Brick.

        :param ser_no: optional serial number to specify a particular PFx Brick if multiple connected
        :returns: boolean indicating open session result
        """
        if not self.is_open:
            numBricks = 0
            serials = []
            for dev in hid.enumerate():
                if dev['vendor_id'] == PFX_USB_VENDOR_ID and dev['product_id'] == PFX_USB_PRODUCT_ID:
                    if dev['serial_number'] not in serials:
                        numBricks += 1
                        serials.append(dev['serial_number'])
            if ser_no is not None and ser_no not in serials:
                print("The PFx Brick with serial number %s was not found." % (ser_no))
            else:
                if numBricks == 0:
                    print("No PFx Bricks are currently connected.")
                elif numBricks > 1 and ser_no is None:
                    print("There are multiple PFx Bricks connected. Therefore a serial number is required to specify which PFx Brick to connect to.")
                else:
                    self.hid = hid.device()
                    self.hid.open(PFX_USB_VENDOR_ID, PFX_USB_PRODUCT_ID, ser_no)
                    self.usb_manu_str = self.hid.get_manufacturer_string()
                    self.usb_prod_str = self.hid.get_product_string()
                    self.usb_serno_str = self.hid.get_serial_number_string()
                    self.is_open = True
        return self.is_open
            
    def close(self):
        """
        Closes a USB communication session with a PFx Brick.
        """
        if self.is_open:
            self.hid.close()
        
    def get_icd_rev(self, silent=False):
        """
        Requests the version of Interface Control Document (ICD)
        the connected PFx Brick supports using the CMD_PFX_GET_ICD_REV
        ICD message.  The resulting version number is stored in
        this class and also returned.
        
        :param boolean silent: flag to optionally silence the status LED blink
        """    
        res = cmd_get_icd_rev(self.hid, silent)
        self.icd_rev = uint16_tover(res[1], res[2])
        return self.icd_rev
        
    def get_status(self):
        """
        Requests the top level operational status of the PFx Brick
        using the CMD_PFX_GET_STATUS ICD message.  The resulting
        status data is stored in this class and can be queried
        with typical class member access methods or the print_status method.
        """
        res = cmd_get_status(self.hid)
        if res:
            self.status = res[1]
            self.error = res[2]
            self.product_id = uint16_tostr(res[7], res[8])
            self.serial_no = uint32_tostr(res[9], res[10], res[11], res[12])
            self.product_desc = bytes(res[13:37]).decode("utf-8")
            self.firmware_ver = uint16_tover(res[37], res[38])
            self.firmware_build = uint16_tostr(res[39], res[40])
                     
    def print_status(self):
        """
        Prints the top level operational status information retrieved
        by a previous call to the get_status method.
        """
        print("USB vendor ID         : %04X" % (self.usb_vid))
        print("USB product ID        : %04X" % (self.usb_pid))
        print("USB product desc      : %s" % (self.usb_prod_str))
        print("USB manufacturer      : %s" % (self.usb_manu_str))
        print("PFx Brick product ID  : %s, %s" %(self.product_id, self.product_desc))
        print("Serial number         : %s" % (self.serial_no))
        print("Firmware version      : %s build %s" % (self.firmware_ver, self.firmware_build))
        print("Status                : %02X %s" %(self.status, get_status_str(self.status)))
        print("Errors                : %02X %s" %(self.error, get_error_str(self.error)))    
        
    def get_config(self):
        """
        Retrieves configuration settings from the PFx Brick using 
        the PFX_CMD_GET_CONFIG ICD message. The configuration data
        is stored in the PFxConfig class member variable config.
        """
        res = cmd_get_config(self.hid)
        if res:
            self.config.read_from_brick(res)
    
    def print_config(self):
        """
        Prints a summary representation of the PFx Brick configuration
        settings which were retrieved by a previous call to get_config.
        """
        print(str(self.config))
        
    def get_name(self):
        """
        Retrieves the user defined name of the PFx Brick using 
        the PFX_CMD_GET_NAME ICD message. The name is stored in
        the name class variable as a UTF-8 string.
        """
        res = cmd_get_name(self.hid)
        if res:
            self.name = bytes(res[1:25]).decode("utf-8")
            
    def set_name(self, name):
        """
        Sets the user defined name of the PFx Brick using the
        PFX_CMD_SET_NAME ICD message.
        
        :param str name: new name to set
        """
        res = cmd_set_name(self.hid, name)
            
    def get_action(self, evtID, ch):
        """
        Retrieves the stored action associated with a particular
        [eventID / IR] channel event. The eventID and channel value
        form a composite address pointer into the event/action LUT
        in the PFx Brick. The address to the LUT is formed as:
        
        Address[5:2] = event ID
        Address[1:0] = channel
        
        :param int evtID: event ID LUT address component (0 - 0x20)
        :param int channel: channel index LUT address component (0 - 3)
        :returns: a PFxAction class filled with retrieved LUT data
        """
        if ch > 3 or evtID > EVT_ID_MAX:
            print("Requested action (id=%02X, ch=%02X) is out of range" % (evtID, ch))
            return None
        else:
            res = cmd_get_event_action(self.hid, evtID, ch)
            action = PFxAction()
            if res:
                action.read_from_brick(res)
            return action
        
    def set_action(self, evtID, ch, action):
        """
        Sets a new stored action associated with a particular
        [eventID / IR] channel event. The eventID and channel value
        form a composite address pointer into the event/action LUT
        in the PFx Brick. The address to the LUT is formed as:
        
        Address[5:2] = event ID
        Address[1:0] = channel
        
        :param int evtID: event ID LUT address component (0 - 0x20)
        :param int ch: channel index LUT address component (0 - 3)
        :param PFxAction action: action data structure class
        """
        if ch > 3 or evtID > EVT_ID_MAX:
            print("Requested action (id=%02X, ch=%02X) is out of range" % (evtID, ch))
            return None
        else:
            res = cmd_set_event_action(self.hid, evtID, ch, action)

    def test_action(self, action):
        """
        Executes a passed action data structure. This function is
        used to "test" actions to see how they behave. The passed
        action is not stored in the event/action LUT.
        
        :param PFxAction action: action data structure class
        """
        res = cmd_test_action(self.hid, action.to_bytes())                            
    
    def refresh_file_dir(self):
        """
        Reads the PFx Brick file system directory. This includes
        the total storage used as well as the remaining capacity.
        Individual file directory entries are stored in the
        filedir.files data class.
        """
        res = cmd_get_free_space(self.hid)
        if res:
            self.filedir.bytesLeft = uint32_toint(res[3:7])
            capacity = uint32_toint(res[7:11])
            self.filedir.bytesUsed = capacity - self.filedir.bytesLeft
        res = cmd_get_num_files(self.hid)
        if res:
            self.filedir.files = []
            self.filedir.numFiles = uint16_toint(res[3:5])
            for i in range(self.filedir.numFiles):
                res = cmd_get_dir_entry(self.hid, i+1)
                d = PFxFile()
                d.read_from_brick(res)
                self.filedir.files.append(d)

    def reset_factory_config(self):
        """
        Resets the PFx Brick configuration settings to factory defaults.
        """
        res = cmd_set_factory_defaults(self.hid)
        
        