---
layout: default
title: Tuning and Calibration Overview
has_children: true
nav_order: 8
---

# Tuning and Calibration Overview
{: .no_toc}

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

## General Resources
- The best tuning resource there is: [Ellis' Print Tuning Guide](https://ellis3dp.com/Print-Tuning-Guide/articles/index_tuning.html)
- Minimal 3DP's Basic Klipper Configuration Checks Procedure
	- [Klipper Basic Configuration Checks - Google Sheets](https://docs.google.com/spreadsheets/d/1CwccwL21RJTX0NQu1DDUu3yGtK1RVByJQGIV45AjyNA/edit?gid=0#gid=0)
- OrcaSlicer's Calibration Info: [Calibration · SoftFever/OrcaSlicer Wiki · GitHub](https://github.com/SoftFever/OrcaSlicer/wiki/Calibration)

Prioritize the following items, IN ORDER:
 1. [Extruder Calibration](https://ellis3dp.com/Print-Tuning-Guide/articles/extruder_calibration.html) (*100mm requested = 100mm extruded*)
 2. Bed Leveling / Bed Mesh (*this will vary depending on your chosen sensor*)
 3. [First Layer Squish](https://ellis3dp.com/Print-Tuning-Guide/articles/first_layer_squish.html)
 4. [Pressure Advance](https://ellis3dp.com/Print-Tuning-Guide/articles/pressure_linear_advance/introduction.html)
	Use the [Pattern Method](https://ellis3dp.com/Print-Tuning-Guide/articles/pressure_linear_advance/pattern_method.html) via [OrcaSlicer's Built-in Calibration Tools](https://github.com/OrcaSlicer/OrcaSlicer/wiki/pressure-advance-calib)
 5. [Extrusion Multipler](https://ellis3dp.com/Print-Tuning-Guide/articles/extrusion_multiplier.html)
 6. [Flow Rate (YOLO method is recommended)](https://github.com/OrcaSlicer/OrcaSlicer/wiki/flow-rate-calib)
 7. [Retraction](https://github.com/OrcaSlicer/OrcaSlicer/wiki/retraction-calib)
 8. [Cornering](https://github.com/OrcaSlicer/OrcaSlicer/wiki/cornering-calib)


- Minimal 3DP's Klipper Calibrations Spreadsheet (*this can be useful for helping calculate much of the above*)
	- [Klipper Calibrations - Google Sheets](https://docs.google.com/spreadsheets/d/1LlSHsa86RuT_btswmDsmQp0LrTJ9U0HJcRhorsqz1ug/edit?gid=1017893331#gid=1017893331)
		- Run Current
			- *particularly if using the BTT SKR Mini E3 V3.0 which can handle higher currents than the Einsey RAMbo...*

## Input Shaping
There's too much here to exhaustively detail, but you'll need an input shaper sensor (ADXL etc) which you may or may not have on your toolhead.  Remember, Prusawire is a bed slinger and you will want to input shape Y axis as well!  The on-toolhead sensors will not detect Y axis.

[Klipper Shake&Tune](https://github.com/Frix-x/klippain-shaketune) works well.

## Skew / Scaling Correction
Some filament shrinks noticably (ABS/ASA espesically).  Prusawire and Voron-adjacent printers are designed with ABS shrinkage in mind and require no scaling.  Not all projects do this!

[Califlower MK2](https://vector3d.shop/products/califlower-calibration-tool-mk2) is an excellent tool to compensate for material shrinkage AND skew.  It is, however, a paid model.

A great free/open source option is Calistar: [Printables](https://www.printables.com/model/778188-calistar-parametric-open-source-alternative-to-cal) and [GitHub](https://github.com/dirtdigger/fleur_de_cali).

## Miscellaneous Notes
- Ella suggests that if using SKR Mini, motor currents can increase over the values provided for the slower Rambo board.  See Run Current above.
