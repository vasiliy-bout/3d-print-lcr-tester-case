# 3D printed LCR-T4 Mega328 tester case

This repository contains source code for generating a 3D model of a case for
a popular "LCR-T4 Mega328" tester.

Tester PCB design may vary over time, so be sure that your tester PCB has
matching dimensions, SMD components placement, wiring placement, and so on.
I bought my tester device [here on AliExpress](https://www.aliexpress.com/item/32774177793.html).

## Dependencies

Scripts require Python3. Tested with Python 3.8.

[ZenCad library](https://github.com/mirmik/zencad) is used as a SCAD core.

## Usage

You can view 3D model by running:
```
./main.py
```

You can export STL model files with:
```
./main.py --top top.stl --bottom bottom.stl
```

You can see usage information with:
```
./main.py -h
```
