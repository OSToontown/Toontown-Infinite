
# ⚠️ Warning! - Do not use

<img src="https://i.ibb.co/drdyL5q/icon.png" align="right" width="200"/>

# Toontown Infinite [![Discord][discordImg]][discordLink]
A Toontown Infinite Source that just works.

# ❓ What is Toontown Infinite
Toontown Infinite is a toontown server that was made to be an harder version of Toontown. We are going to continue its legacy here.

# 🔨 Setting Up

Support is currently being worked on for MacOS and Non Arch Based Linux Distros
## 💻 Windows

### Installing Panda
To get the source running you need to install the [Panda3D](https://github.com/NormalNed/Toontown-Infinite/blob/master/Panda3D-1.11.0.exe) located in this repo.

### Installing Pip Dependencies
The next part is to get our Dependencies. To get them open a Command Prompt Window inside of the Toontown Infinite folder and run
```bash
ppython -m pip install -r requirements.txt
```

### Running the Game
Now run the [Start.bat](Start.bat) file to launch the game.

## 🐧 Linux
### Gathering Basic Dependencies
##### Arch / Manjaro
```yay -S xorg-server  xterm  libgl  python  openssl  libjpeg  libpng  freetype2  gtk2  libtiff  nvidia-cg-toolkit  openal  zlib  libxxf86dga  assimp  bullet  eigen  ffmpeg  fmodex  libxcursor  libxrandr  git  opencv  libgles  libegl```

##### Debian / Ubuntu / Linux Mint
```sudo apt-get install build-essential xterm pkg-config fakeroot python-dev libpng-dev libjpeg-dev libtiff-dev zlib1g-dev libssl-dev libx11-dev libgl1-mesa-dev libxrandr-dev libxxf86dga-dev libxcursor-dev bison flex libfreetype6-dev libvorbis-dev libeigen3-dev libopenal-dev libode-dev libbullet-dev nvidia-cg-toolkit libgtk2.0-dev libassimp-dev libopenexr-dev```

### Getting Python 2

The First step to get this Source running is obtaining a version of Python 2. The Python we use is located [here](https://github.com/NormalNed/python) but feel free to use the one in your package manager (should be **python2**)

### Installing Pip

Once you get the Python installed you need to type these following commands to install Pip
```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python2 get-pip.py
```

### Installing Pip Dependencies
The next part is to get our Dependencies. Open a Terminal inside of the Infinite Project and follow these instructions below.
```bash
pip2.7 install -r requirements.txt
```

### Installing "our" Panda 3D
We use a version of Astron Panda3D that is upstream code from the main repo. To set it up follow these instructions

```bash
git clone https://github.com/NormalNed/panda3d.git
cd panda3d
python2 makepanda/makepanda.py --everything --installer --no-egl --no-gles --no-gles2 --no-opencv --threads=4
sudo python2 makepanda/installpanda.py
sudo ldconfig
```

### Running the Game
Now run the [Start.sh](Start.sh) file to launch the game.

[discordImg]: https://img.shields.io/discord/690332444364505315.svg?logo=discord&logoWidth=18&colorB=7289DA&style=for-the-badge

[discordLink]: https://discord.gg/jnaK6JD

