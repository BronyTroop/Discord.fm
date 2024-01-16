<p align="center">
  <img src="https://i.imgur.com/sBPf84B.png" style="max-height: 128px">
</p>
<p align="center">
  <img src="https://i.imgur.com/EcePBfb.gif" style="max-height: 350px">
</p>

----

<p align="center">
   <img src="https://img.shields.io/badge/Windows-blue?style=for-the-badge&logo=windows&logoColor=white&labelColor=black" alt="Windows Platform Badge">
   <img src="https://img.shields.io/badge/Linux-gold?style=for-the-badge&logo=linux&logoColor=white&labelColor=black" alt="Linux Platform Badge">
</p>

<p align="center">
   <img alt="GitHub release downloads (latest by date)" src="https://img.shields.io/github/downloads/EmanuelVH/Discord.fm/latest/total?label=downloads&style=flat-square&labelColor=black">
    <img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/EmanuelVH/Discord.fm/test-build.yml?style=flat-square&labelColor=black&label=build %26 tests">
   <img src="https://img.shields.io/github/license/EmanuelVH/Discord.fm?style=flat-square&labelColor=black" alt="License: MIT">
   <img src="https://img.shields.io/badge/using-pypresence-00bb88.svg?style=flat-square&logo=discord&logoWidth=20&logoColor=white&labelColor=black" alt="Using pypresence package">
</p>

Background service that shows what you're scrobbling on Last.fm to on Discord, with automatic updates,
cover art image, support for Discord Canary and a UI for changing settings.

Forked from [Discord.fm](https://github.com/androidWG/Discord.fm) by [androidWG](https://github.com/androidWG), which was originally forked from [Last.fm-Discord-Rich-Presence](https://github.com/Gust4Oliveira/Last.fm-Discord-Rich-Presence) by [Gust4Oliveira](https://github.com/Gust4Oliveira)

## Installation
The app currently supports Windows (minimum **Windows 10**).

- Download the [latest release](https://github.com/EmanuelVH/Discord.fm/releases/latest)
- Run the installer
- Wait a bit and the app's settings will open. Type in your Last.fm username and close the window.
- Done!

## Setting up dev environment

Discord.fm provides a setup script with some useful functions for devs. A full list of parameters can be viewed by running the command `python setup.py -h` or simply running the script with no flags or commands.

### Requirements

- [Python 3.11](https://www.python.org/downloads/release/python-3110/) or above
- [Git](https://git-scm.com/download/win)
- [Visual Studio with C++](https://visualstudio.microsoft.com/vs/features/cplusplus/)
- [Inno Setup](https://jrsoftware.org/isdl.php)

### Setting up, running and building

After all requirements are met, just run the following commands to set everything up:

````commandline
git clone https://github.com/BronyTroop/Discord.fm
````
````commandline
cd Discord.fm
````
````commandline
pip install -r requirements.txt
````
````commandline
python setup.py setup
````

Then, you can run the app with:

```commandline
python setup.py run
```

To build the app, simply use this command:

````commandline
python setup.py build
````

The script will set up anything if needed, then build the app and subsequently the installer. You can pass the flag `--installer-only` or `--build-only` to skip the other step.
