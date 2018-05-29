import sys
import pywifi
import time
from pywifi import const
wifi = pywifi.PyWiFi()
ifaces = wifi.interfaces()[0]
ifaces.disconnect()
profile = pywifi.Profile()
profile.ssid = sys.argv[1]
profile.auth = const.AUTH_ALG_OPEN
profile.akm.append(const.AKM_TYPE_WPA2PSK)
profile.cipher = const.CIPHER_TYPE_CCMP
profile.key = sys.argv[2]
ifaces.remove_all_network_profiles()
tmp_profile = ifaces.add_network_profile(profile)
ifaces.connect(tmp_profile)
time.sleep(5)
if ifaces.status() == const.IFACE_CONNECTED:
    print("password {0} is collect".format(profile.key))
    exit(0)
else:
    print(ifaces.status())
    print("password {0} is not collect".format(profile.key))

# In [14]: profile.key="86525542"
#
# In [15]: ifaces.remove_all_network_profiles()
#
# In [16]: tmp_profile = ifaces.add_network_profile(profile)
#
# In [17]: ifaces.connect(tmp_profile)
#
# In [18]: ifaces.status()
# Out[18]: 4
#
# In [19]: const.IFACE_CONNECTED
# Out[19]: 4
#
# In [20]: ifaces.disconnect()
#
# In [21]: tmp_profile = ifaces.add_network_profile(profile)
#
#
#














