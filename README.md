# WoT Python Dumping Tool
## World of Tanks (PC) Modification
## Latest Release
v1.0.0 for World of Tanks 1.11.0.0 and Python 2.7.x

## Description
This tool is intended for mod making and reverse engineering for World of Tanks. The game has no publically available documentation or client API so this tool hopefully serves as a way to help use/manipulate the game's code. It can dump information about any World of Tanks Python module, including any module level or class level attributes. This includes Python builtin modules (written in C) that are built into in WorldOfTanks.exe (such as BigWorld).

## Usage
The tool is installed just like any other WOT mod. Just put the .wotmod file in World_of_Tanks/mods/[version] and run the game normally.

The dumps are created in World_of_Tanks/dumps when the game loads.

To configure which modules are dumped, open World_of_Tanks/mods/config/builtins_dump/builtins_dump.json (created the first time the mod is loaded) in a text editor and add the module names to the "module_list" array. These are written exactly how they would be used in an import statement (eg "import items.vehicles" would be entered as "items.vehicles" in the config file).

To also dump Python magic methods (\_\_getattr\_\_, \_\_class\_\_, etc...) set the field "show_magic_methods" in the config file to True (default False).
