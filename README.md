# Pandora-Record

Record songs from pandora to mp3

**Requirements**

pianobar and libav-tools

**Installation**

```sudo apt-get install pianobar libav-tools```

To setup pianobar after installing: 

```mkdir ~/.config/pianobar```  
```sudo nano ~/.config/pianobar/config``` - see example config file  
You will need to add your email and password for pandora   
You will also need to run pianobar once from the command line and choose a starting station, then set the long string of numbers you get for the station in the autostart_station of the pianobar config

```sudo nano  /etc/pulse/daemon.conf```  
change default-sample-rate to 480000

```pactl list sources```  
probabaly looking for source #0 or something like this:  alsa_output.pci-0000_00_14.2.analog-stereo.monitor

```sudo nano  record-pandora.conf```  
In line 1 put your source you got from the last step  
In line 2 put you minimum file size you would like to save (to prevent ads from being saved in kb - ie. 800)  
In line 3 put mp3 or ogg for the format you want saved  

Optional, create a whitelist-artists.txt file with the names of the artists you only want to hear/record. Each line must be capitalized as pianobar shows them and the last line must have a blank line under it. Example:

```
Modest Mouse
Pink Floyd

```

Optional, create a blacklist-artists.txt file with the names of the artists you dont want to hear/record. Each line must be capitalized as pianobar shows them and the last line must have a blank line under it.

**Usage**  
```python recorder.py```
