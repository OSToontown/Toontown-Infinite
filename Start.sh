#!/bin/sh
clear
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo What do you want to do!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo 1 - Run Toontown Infinite
echo    


while true; do
    read -p "Selection: " sel
    case $sel in
        [1]* )
        clear
        echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
        echo What do you want to launch!
        echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
        echo 1 - Locally Host a Server
        echo 2 - Connect to an Existing Server
        echo    
        while true; do
            read -p "Selection: " sel2
            case $sel2 in
                [1]* )
                clear
                echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
                echo Starting Localhost!
                echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
                cd tools
                echo Launching the AI Server...
                xterm -e sh autostart-ai-server.sh &
                echo Launching Astron...
                xterm -e sh autostart-astron-cluster.sh &
                echo Launching the Uberdog Server...
                xterm -e sh autostart-uberdog-server.sh &
                cd ..
                export TTS_GAMESERVER=127.0.0.1
                clear
                echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
                echo Username [!] This does get stored in your source code so beware!
                echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
                read -p "Username: " ttsUsername
                export ttsUsername=$ttsUsername
                export TTS_PLAYCOOKIE=$ttsUsername
                clear
                echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
                echo Welcome to Toontown Infinite, $ttsUsername!
                echo The Tooniverse Awaits You!
                echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
                while [ true ]
                do
                    /usr/bin/python2 -m toontown.toonbase.ToontownStart
                    read -r -p "Press any key to continue..." key
                done
                ;;
                [2]* )
                clear
                echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
                echo What Server are you connecting to!
                echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
                read -p "Server IP: " TTS_GAMESERVER
                TTS_GAMESERVER=${TTS_GAMESERVER:-"127.0.0.1"}
                export TTS_GAMESERVER=$TTS_GAMESERVER
                clear
                echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
                echo Username [!] This does get stored in your source code so beware!
                echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
                read -p "Username: " ttsUsername
                export ttsUsername=$ttsUsername
                export TTS_PLAYCOOKIE=$ttsUsername
                clear
                echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
                echo Welcome to Toontown Infinite, $ttsUsername!
                echo The Tooniverse Awaits You!
                echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
                while [ true ]
                do
                    /usr/bin/python2 -m toontown.toonbase.ToontownStart
                    read -r -p "Press any key to continue..." key
                done
                ;;
                * ) echo "";;
            esac
        done
        ;;
        * );;
    esac
done
