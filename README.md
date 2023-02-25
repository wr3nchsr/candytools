# candytools
A tool to automate the process of preparing an Android OTA image for analysis.

## Main Functionalities
* **Unpack** kernel images *(boot.img, recovery.img)*.
* **Convert** system image from sparse/sdat to ext4.
* **Extract** the ext4 system image.
* **Calculate** checksums for all the unpacked/extracted files.
* **Differentiate** checksum files between OTA versions.
* **Decompile** applications. *(android < 8)*

# Installation
## Requirements
* Linux host.
* Python >= 3.7


```bash
./install.sh
```

# Usage
You can either use the `prep` command to use the entire pipeline or use each functionality separately when needed.

```
usage: candy [-h] {prep,unpack,extract,decompile,checksum} ...

Candy CLI Tools

positional arguments:
  {prep,unpack,extract,decompile,checksum}
    prep                Prepare an OTA update for analysis
    unpack              Unpack kernel image
    extract             Convert and extract system images
    decompile           Decompile applications recursively
    checksum            Compute and differentiate checksum files

optional arguments:
  -h, --help            show this help message and exit
```

## Example
```bash
python3 candy.py prep -i unzipped_ota_directory -o output_directory
```
In this case the input directory should look like this 
```
unzipped_ota_directory/
├── boot.img
├── recovery.img
├── system.img (if sparse)
├── system.new.dat (if sdat)
└── system.transfer.list (if sdat)
```
And the output directory should look like this.
```
output_directory/
├── apps/ (decompi)
├── boot/
├── recovery/
├── system/
├── checksums.txt
└── system.img
```

# Docker Support
## Build

```bash
docker build -t "candytools" .
```
## Sample Usage

```bash
cd unzipped_ota_directory/
docker run -it -v ${PWD}:/ota --rm "candytools" prep -i /ota -o /ota/output -d
```

# Todo
- [ ] Add comments to the code.
- [ ] Add tests.
- [ ] Automate the identification of files inside the OTA directory.
- [ ] Support split sparse images conversion.
- [ ] Support VDEX for decompilation (android >= 8).
<!-- https://github.com/lief-project/LIEF/issues/549 -->
<!-- https://github.com/anestisb/vdexExtractor -->

# Dependencies
* Deodexing by [LIEF](https://github.com/lief-project/LIEF).
* Kernel image unpacking by [AIK](https://github.com/ndrancs/AIK-Linux-x32-x64).
* Algorithm for converting sdat to ext4 from [sdat2img](https://github.com/xpirt/sdat2img).
* Converting sparse to ext4 by [simg2img](https://github.com/anestisb/android-simg2img).
* Decompiling by [JADX](https://github.com/skylot/jadx).

# License
This project is under the [GNU GPLv3](./LICENCE) licence.

# Authors
Saif Aziz ([@wr3nchsr](https://www.twitter.com/wr3nchsr))