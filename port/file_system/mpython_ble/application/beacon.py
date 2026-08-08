import bluetooth
from bluetooth import UUID
import struct
from ..const import ADType
from ..advertising import advertising_payload, AD_Structure


class iBeacon:
    """ iBeacon """

    def __init__(self, proximity_uuid, major, minor, company_id=0x004C, tx_power=0xC5):
        self.ibeacon = bluetooth.BLE()
        self.ibeacon.active(True)
        print("BLE: activated!")
        # iBeacon frame
        assert isinstance(proximity_uuid, UUID), TypeError("proximity uuid must be type of UUID")
        proximity_uuid = list(bytes(proximity_uuid))
        proximity_uuid.reverse()
        proximity_uuid = bytes(proximity_uuid)
        ibeacon_type = 0x02
        adv_data_length = 0x15
        manuf_specific_data = struct.pack('<H2B', company_id, ibeacon_type, adv_data_length)
        manuf_specific_data += proximity_uuid
        manuf_specific_data += struct.pack(">2HB", major, minor, tx_power)
        manuf_specific = AD_Structure(ad_type=ADType.AD_TYPE_MANUFACTURER_SPECIFIC_DATA, ad_data=manuf_specific_data)
        self._adv_payload = advertising_payload(ad_structure=[manuf_specific])

    def advertise(self, toggle=True, interval_us=500000):
        if toggle:
            self.ibeacon.gap_advertise(interval_us, adv_data=self._adv_payload, connectable=False)
        else:
            self.ibeacon.gap_advertise(interval_us=None)
