# Instrument Controll

One Paragraph of project description goes here

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Package Description: 

* [*pyDecorators*](https://github.com/gregmoille/InstrumentControl/tree/master/pyDecorators): Usefull decorator for instrument control, such as error catching, checking argument type passed, etc ...
* [*pyLaser*](https://github.com/gregmoille/InstrumentControl/tree/master/pyLaser): laser package to controll the different coded laser. 1 file = 1 laser brand. So far the laser that works are *NewFocus 6700*and *Toptics 1060*
* [*pyNiDAQ*](https://github.com/gregmoille/InstrumentControl/tree/master/pyNiDAQ): package to make it more user friendly the use of a National Instrument USB DAQ card
* [*pyPowerMeter*](https://github.com/gregmoille/InstrumentControl/tree/master/pyPowerMeter): pacakge to control the Thorlabs powermeter (PM100D, PM100USB, PM16-XXX)
* [*pyWavemeter*](https://github.com/gregmoille/InstrumentControl/tree/master/pyWavemeter): package to control the Angstrom HighFiness wavemeter. The full software and driver have to be installed as the python script run as a sever

## Sofwate and UI:

* *TranmissionSetup*: python script with UI in order to characterize the optical tranmission of a device, with user choice of calibrating with the wavemeter the wavelength scan, and ftching the transmission losses with the powermeters.

### Prerequisites

* Python >3.4
* Most of the tools only work on **Windows** as the different drivers for the instruments are only provided for this OS. The driver are obvioulsy need to make these package work as we are directly sending commands to the instruments
* _as the setup.py is still a work in progress, you'll probably have to "pip" different python package_

### Installing

_WORK IN PROGRESS_

## Contributing

Please read [CONTRIBUTING.md](https://github.com/gregmoille/InstrumentControl) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

<!-- We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).  -->

## Authors

* **Gregory Moille** - *Initial work* - [NIST](https://www.nist.gov/people/gregory-moille)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
