# LUX2EV

A very easy-to-use small software that uses the lux value measured by the illuminance meter to calculate the shutter speed under different ISO and aperture, and assist photography.


## Prerequisites

- Python 3.9+
- PyQt6

## Installation

```Bash
pip install pyqt6
pip install lux2ev
python -c "import lux2ev;lux2ev.main()"
```

OR 

```Bash
git clone https://github.com/EasyCam/LUX2EV/
cd LUX2EV/lux2ev
pip install pyqt6
python __init__.py
```

## Usage

Just input the Lux value and select an ISO, and the software will calculate the shutter speed under different aperture.
![](./images/Screenshot.png)