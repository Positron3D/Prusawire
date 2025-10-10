# Prusawire 2025.B1

![Render](Assets/render.png)

A wholly unofficial Prusa MK3 and MK4 total conversion mod, from Positron's April Fools of 2025.


## About

Nomad of Positron3D came up with this idea shortly after completing their Switchwire build. The idea started as a quick design exercise, to try and convert a Prusa MK4S frame into a Switchwire, using everything left over from a CORE One Upgrade.

As the first iteration wrapped up, I took interest in the project, and decided to take this April Fools joke one step further and build it into a reliable machine.

After months of hard work, please enjoy the build ❤

## Who This Printer is For

Pick one of the following:

 - You have an old MK3, MK3S, or MK3S+, and you want to teach an old dog new tricks and are on a budget
 - You upgraded from MK4S to a Core ONE, and have a leftover frame. You are okay spending money on building a new printer with that hardware.

Additionally, the following says this printer is for you: 

 - You want to take your first steps into RepRap beyond Prusa, and Voron is an exciting route.
 - You are comfortable working from a CAD file as your build guide
 - You respect the Frankenstein-y nature of this April Fools joke printer

## Want to Support the Project?

First of all, thank you! Development costs have been mostly self-funded, with filament sponsored by Levendigs, and LDO Motors for providing the funds for the Prusa MK4 frame.

 - Buy me a Ko-Fi
 - Support Positron3D to fund future endeavors

## 2025 - Beta 1

This printer is in active development. Please check back regularly for bug fixes and configuration updates!

## Build Volume

X: 250mm
Y: 210mm
Z: 185mm

## Technical Support

Prusawire, technically, does not count as a Voron Switchwire. We ask you kindly not to nag the Voron Design team for technical support.

Instead, please join the Positron3D Discord for support with your build, and maybe share your progress over there too.

## Serial Numbers

We are accepting serials over on the Positron 3D Discord. Please submit your request to the #prusawire-serial-request channel over there. 

## Bill of Materials

Coming out later today! Check back soon.

## Upgrading the Einsy Rambo to Klipper - Read this

Installing Klipper on the Einsy Rambo board is possible, with extra steps. Follow the guide [published by the awesome folks at MyRigs3D](https://myrigs3d.com/blogs/infos/revive-your-prusa-mk3s-with-klipper-1-5-flash-bootloader)! We recommend Method 2.

**Note:** Some users have reported problems using `avrdude` with the latest Raspberry Pi OS version (bookworm). If you experience error messages from avrdude complaining about gpio ports being busy, please try using the bullseye version of Raspberry Pi OS instead, available as "Raspberry Pi OS (Legacy)" in Raspberry Pi Imager.

## Klipper Configuration Files

The most up–to–date Klipper configuration files for setting up or updating the Prusawire are in our [config repository](https://github.com/Positron3D/prusawire-klipper-config).

## Credits 

Many thanks to all the awesome people and companies that have made this possible. Notably:

 - Prusa Research - Cheers, Josef and the team for the MK3/4 platform on which this was built upon!
 - Voron Design - Switchwire
 - Positron 3D Team - Too many to name, you know who you are <3
   - Early development team:
     - Nomad's Galaxy
     - Koosh
     - Birb
 - Jason @ LDO Motors - Part sponsorship
 - Levendigs - Part sponsorship 
 - Early access testers:-
    - Killa_Prints
    - LinksLab
    - Safe
    - Silicon
    - TheNexusAvenger
    - torsten

## Extra Credits for Existing Printed Parts

See the collection for the most up to date! To name them:

 - Printable M3 T-Nuts for 3030 Extrusion, by Kapplion
 - Stealthburner umbilical strain relief, by nagelwerkstatt
