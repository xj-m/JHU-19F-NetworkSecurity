from .NetworkManager import NetworkManager
from .StatusOutputProcessor import DeviceStatusOutputProcessor, RoutesStatusOutputProcessor

### We need to import these class to register them (via metaclass) ###
from .SwitchDevice import SwitchDevice
from .UnreliableSwitchDevice import UnreliableSwitchDevice
from .VnicDevice import VnicDevice
###