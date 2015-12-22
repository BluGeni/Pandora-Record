#!/usr/bin/python
import subprocess, time, os, sys

# Requires Pulse audio to be in use

# record-pandora.conf - config file. LINE 1: Audio source | LINE 2 - min output file size per track, anything smaller is deleted | LINE 3 - output format, ogg or mp3
# To get the parm for line 1 do this at the command line: pactl list sources

# EXAMPLE CONFIG FILE: 

# alsa_output.pci-0000_00_1b.0.analog-stereo.monitor
# 800
# mp3


# whitelist-artists.txt -- a list of artists to record, one per line, case sensitive, names must match Pandora name output exactly

# blackist-artists.txt -- a list of artists to NOT record, one per line, case sensitive, names must match Pandora name output exactly
dontDelete = False

def startRecord(playingInfo1, playingInfo2, playingInfo3):

    try: #try to create new artist dir if not already there
        #remove illegal character / for file/folder names
        #playingInfo1 = playingInfo1.replace("/", "-")
        #playingInfo2 = playingInfo2.replace("/", "-")
        #playingInfo3 = playingInfo3.replace("/", "-")
        #above moved
        global dontDelete
        if(not os.path.exists("Music/" + playingInfo1)):
            os.mkdir("Music/" + playingInfo1)
            print "Created new artist dir"
            
        #create new Album dir if not already there
        if(not os.path.exists("Music/" + playingInfo1 + "/" + playingInfo2)):
            os.mkdir("Music/" + playingInfo1 + "/" + playingInfo2)
            print "Created new album dir"
            
        #record new song if not already recorded
        if(not os.path.exists("Music/" + playingInfo1 + "/" + playingInfo2 + "/" + playingInfo3 + "." + outputType)):
            try: ### the next line is for specific sound card, edit it
                
                if(outputType == "" or outputType == "ogg"):
                    os.system('avconv -loglevel panic -f pulse -i ' + audioDevName + ' -acodec libvorbis -ac 2 -vn "Music/' + playingInfo1 + '/' + playingInfo2 + '/' + playingInfo3 + '.ogg" &')
                elif (outputType == "mp3"):
                    # -aq 0 >= 320kbps, -aq 2 >= 166kbps -aq 3 >= 118kbps -aq 5 >= 96kbps
                    os.system('avconv -loglevel panic -f pulse -i ' + audioDevName + ' -acodec libmp3lame -aq 3 -ac 2 -vn "Music/' + playingInfo1 + '/' + playingInfo2 + '/' + playingInfo3 + '.mp3" &')

                print "Created new song file, now recording...\n"
                dontDelete = False
            except:
                print "Error opening avconv! Is libav-tools installed?\n"
        else:
            dontDelete = True
    except:
        print "******************Couldn't create new song file!*******************\n"
        e = sys.exc_info()[0]
        print "Error: %s" % e        

### program start here ###

#variables and lists
p2 = ""

#create music dir if it doesn't exist
if(not os.path.exists("Music")):
    os.mkdir("Music")
    
#read configuration file
try:
    if(os.path.exists("record-pandora.conf")):
	print "Loading config file...\n"
	confFile = open("record-pandora.conf", "r")
        audioDevName = confFile.readline()
        audioDevName = audioDevName.rstrip("\n")
        delFileSize = confFile.readline()
        delFileSize = delFileSize.rstrip("\n")
        outputType = confFile.readline()
        outputType = outputType.rstrip("\n")
        confFile.close()
        if(outputType == ""):
		outputType = "ogg"
	elif(outputType != "ogg" and outputType != "mp3"):
		outputType = "ogg"
	print "Recording format: " + outputType + "\n"
    else:
        print "record-pandora.conf not found, please create it\nwith your audio device name and desired delete file size in bytes.\n"
        print "Example 1:\nalsa_output.pci-0000_00_14.2.analog-stereo.monitor\n800\nogg\n"
        print "Example 2:\nalsa_output.pci-0000_00_14.2.analog-stereo.monitor\n800\nmp3\n"
except:
    print "Error trying to read conf file"

### whitelist section ###
def whiteListArtists():
    try:
        if(os.path.exists("whitelist-artists.txt")):
            whitelistArtists = open("whitelist-artists.txt", "r")
            whitelistArtistsList = whitelistArtists.readlines()
            whitelistArtists.close()
        else:
            whitelistArtistsList = ""
            print "No whitelist-artists.txt found.\n"
    except:
        print "Error tying to read whitelist-artists.txt"
    
    return(whitelistArtistsList)
### end whitelist section ###
    
### blacklist section ###
def blackListArtists():
    try:
        if(os.path.exists("blacklist-artists.txt")):
            blacklistArtists = open("blacklist-artists.txt", "r")
            blacklistArtistsList = blacklistArtists.readlines()
            blacklistArtists.close()
        else:
            blacklistArtistsList = ""
            print "No blacklist-artists.txt found.\n"
    except:
        print "Error tying to read blacklist-artists.txt"
    
    return(blacklistArtistsList)
### end whitelist section ###
    
    
#try to run pianobar
try:
    print "Running pianobar...\n"
    cmd = "pianobar"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    output = p.stdout.readline()
except:
    print "Error opening pianobar! Is it installed?\n"

while(True):
    if('|>  "' in output): #beginning of songs playing
        try:
            #kill recording of last song
            os.system("killall avconv")
            if(os.path.getsize("Music/" + playingInfo1 + "/" + playingInfo2 + "/" + playingInfo3 + "." + outputType) <= int(delFileSize)):
                os.remove("Music/" + playingInfo1 + "/" + playingInfo2 + "/" + playingInfo3 + "." + outputType)
                print "Removed file - too small: Music/" + playingInfo1 + "/" + playingInfo2 + "/" + playingInfo3 + "." + outputType
        except:
            print "Exception, avconv is not running - this is usually ok\n"
        try:
            #try to clean up and format pianobar's output
            cleanPianobarChars = output.split('|>  "', 1)
            songName = cleanPianobarChars[1].split('" by "', 1)
            artistName = songName[1].split('" on "', 1)
            albumName = artistName[1].split('"', 1)
            #put Artist name, Album name and Song name into a list
            playingInfo1 = artistName[0]
            playingInfo2 = albumName[0]
            playingInfo3 = songName[0]
            #skip all artists not in whitelist
            whiteList = whiteListArtists()
            blackList = blackListArtists()
            if(blackList and playingInfo1 + "\n" in blackList):
                print "Skipping blacklisted artist: " + playingInfo1 + "\n"
            elif(playingInfo1 + "\n" in whiteList or whiteList == ""):
                    #remove illegal character / for file/folder names and remove extra spaces
                    playingInfo1 = playingInfo1.replace("/", "-").replae("&", "and").strip()
                    playingInfo2 = playingInfo2.replace("/", "-").replae("&", "and").strip()
                    playingInfo3 = playingInfo3.replace("/", "-").replae("&", "and").strip()
                    print "\nArtist: " + playingInfo1 + "\nAlbum: " + playingInfo2 + "\nSong: " + playingInfo3 + "\n"
                    #start dir check or creation and record to file
                    startRecord(playingInfo1, playingInfo2, playingInfo3)
            else:
                print "Not recording\nArtist: " + playingInfo1 + "\nAlbum: " + playingInfo2 + "\nSong: " + playingInfo3 + "\n(Not in whitelist)\n"
        except:
            print "Something went wrong with cleaning up pianobar output...\n"
    try:
        output = p.stdout.readline()
    except (KeyboardInterrupt, SystemExit):
        print('\nProgram shutting down...')
        
        if dontDelete == False:
            print('Removing current recording song')
            os.remove("Music/" + playingInfo1 + "/" + playingInfo2 + "/" + playingInfo3 + "." + outputType)
            #check if album folder is empty now and delete if so
            if not os.listdir(os.getcwd() + "/" + "Music/" + playingInfo1 + "/" + playingInfo2):
                os.rmdir(os.getcwd() + "/" + "Music/" + playingInfo1 + "/" + playingInfo2)
                print "Removed empty album folder"
            if not os.listdir(os.getcwd() + "/" + "Music/" + playingInfo1):
                os.rmdir(os.getcwd() + "/" + "Music/" + playingInfo1)
                print "Removed empty artist folder"
        print('Exiting...')
        sys.exit(-1)
        raise
