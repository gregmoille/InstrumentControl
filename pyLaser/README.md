# pyLaser

Control of different type and brand of laser through python

## Getting Started

### Prerequisites

* Python >3.4
* Windows is needed for NewFocus lasers as driver are needed and has to be installed
* For laser connected in Ethernet, any OS are supported
* _as the setup.py is still a work in progress, you'll probably have to "pip" different python package_

### Creating a New Laser

* One good example (first one coded and the most commented script) is [newfocus.py](https://github.com/gregmoille/InstrumentControl/pyLaser/newfocus.py)
* A good rule of thumb is such that create only a new file if the brand of the laser change. Create a new class for each type of laser. 
* The laser class must has:
    - methods:
        + self.Querry: method which send the command word for the action to performed and read the response and/or buffer
    - properties:
        + identity <str>
        + connected <bool>
        + output - output.setter <bool>
        + lbd - lbd.setter <float>
        + current - current.setter <float>
        + scan_limit - scan_limit.setter <list>
        + scan_speed - scan_speed.setter <float>
        + scan - scan.setter <bool>
        + error <str>
        + has_error <bool>
* The laser might has the following depending on the model:
    - properties:
        + pzt - pzt.setter <float>
        + beep - beep.setter <bool>


### Installing

_WORK IN PROGRESS_

## Contributing

Please read [CONTRIBUTING.md](https://github.com/gregmoille/InstrumentControl) for details on our code of conduct, and the process for submitting pull requests to us.


## Authors

* **Gregory Moille** - *Initial work* - [NIST](https://www.nist.gov/people/gregory-moille)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
