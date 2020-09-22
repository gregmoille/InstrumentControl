Instructions for Thorlabs powermeters using _thorlabspowermeter.py_


- For Windows users:
  1. Using this script requires the PM10xx drivers from Thorlabs
    https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4037&pn=PM100USB
  2. Once the Thorlabs software has been downloaded veryify that you are using the "PM  100D (NI-VISA TM)" drivers.
    - Using the TLPM drivers does not let ResourceManager find the device. (Manually finding the device address and bypassing ResourceManager.list_resources also won't work)
    - Switch back to the TLPM drivers when using the Thorlabs Optical Power Meter software.
    - - Note: The help section of this software has a logfile for troubleshooting
    - Accomplish this step using the Power Meter Driver Switcher software located in '\PowerMeters\Tools\DriverSwitcher' of the program's installation directory
-For Unix users:
  - pyvisa used the option _"@py"_ hence no drivers should be needed to make it work. It works also with ARM based devices, such as raspberry pi computers
