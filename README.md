<h1>PocketNinja</h1>

<h3>This project is intended as a quick interface to simple operations, but also an affordable and easy-to-carry-around tool for different operations.</h3>

Based on a Raspberry Pi Zero W, with an <a href="https://github.com/adafruit/Adafruit-1.3in-Color-TFT-Bonnet-PCB">Adafruit TFT Bonnet 1.3" Display</a> and Kali OS (and maybe adding an UPS in the future), PocketNinja aims to help in quick operations, simply using the joystick and the buttons, even in combinations like A+Down or B+Left, and so on.

Coded with Python3, it accesses to the local scripts, getting which one to choose by the controls and using the display to show the proper icon.
For operations like Airodump or Bettercap, it starts them through Screen sessions, to let them operate, instead of die immediatly.
Also, the Pi Zero is kinda weak and using Screen increases the chances of complete the tasks.

Keep in mind that it's builted on a scripts base to simplify any change, modifying only the interested script and image, without the need to modify the Main.py

![1500x500](https://user-images.githubusercontent.com/25898674/142214044-52a48f16-404d-407e-bc59-ebaa9d2662f4.jpg)

<h2>Current setup</h2>
Placed in /home/kali/boot (but you can modify the path as you prefer) and started by a bash script, called from /etc/rc.local after the boot (again, a lot of operations to let any change in an easy way, but remember to adjust every path).

<h2>Current configuration</h2>

UP = Airdump-NG WEP<br>
LEFT = Airodump-NG ALL + WPS info<br>
RIGHT = MAC Changer<br>
DOWN = Proxmark3 "auto" scan<br>
CENTER = Airo-Kill but Screen Alive<br>

A + Joystick<br>
  UP = Bettercap 0/24<br>
  LEFT = Nmap 0/24<br>
  RIGHT = Nmap 1/24<br>
  DOWN = Bettercap 1/24<br>
  CENTER = Screen-Kill<br>

B + Joystick<br>
  UP = Upload<br>
  LEFT = Reboot<br>
  RIGHT = Reset<br>
  DOWN = Shutdown<br>
  CENTER = Help<br>



<h3>System configuration</h3>

I've created PocketNinja as a sort of "rapid multitool", but with the option to use it for more complex operations too.
So I've flashed the Kali Raspberry Pi Zero W image and proceeded as it follows:

-SSH
>sudo rm /etc/ssh/ssh_host_*<br>
>sudo dpkg-reconfigure openssh-server<br>
>sudo service ssh restart<br>

-Sudo without password
>sudo -i<br>
>nano -w /etc/sudoers<br>
>%sudo ALL=(ALL:ALL) NOPASSWD:ALL<br>

-Autologin
>sudo nano -w /etc/lightdm/lightdm.conf<br>
>autologin-user=kali<br>
>autologin-user-timeout=0<br>

-Disable Power Management

-System first update
>sudo kalipi-config (Tweak everything tyou need)<br>
>sudo apt update -y && sudo apt-get update -y && sudo apt-get upgrade -y<br>
>sudo shutdown -r now

-Shutdown
As a rapid tool, it has to be rapid in controlling it, so I've added an "off" command. Not necessary, but I found it nice.
>sudo nano -w /usr/bin/off<br>
><br>
>#!/bin/bash<br>
>sudo shutdown -h now<br>
>exit 0<br>
><br>
>sudo chown kali /usr/bin/off<br>
>sudo chmod +x /usr/bin/off

I'm adding this to the readme, because it's called from the Main.py and so you know this if you need to do some changes.

-X11VNC
>sudo apt-get install x11vnc autocutsel<br>
>x11vnc -storepasswd<br>
>Write password to /home/kali/.vnc/passwd?  [y]/n y<br>
><br>
>sudo nano -w /etc/systemd/system/x11vnc.service<br>
><br>
>[Unit]<br>
>Description=x11vnc remote desktop server<br>
>After=multi-user.target<br>
>[Service]<br>
>Type=simple<br>
>ExecStart=/usr/bin/x11vnc -auth guess -forever -loop -noxdamage -repeat -rfbauth /home/kali/.vnc/passwd -rfbport 5900 -shared<br>
>Restart=on-failure<br>
>[Install]<br>
>WantedBy=multi-user.target<br>
><br>Save and exit<br>
>sudo systemctl daemon-reload<br>
>sudo systemctl start x11vnc<br>
>sudo systemctl status x11vnc<br>
>sudo systemctl enable x11vnc.service<br>

-Bluetooth
<br>I noticed some troubles with the BT function, but this works for me
>sudo systemctl enable bluetooth<br>
>audo systemctl start bluetooth<br>
>wget https://gitlab.com/kalilinux/build-scripts/kali-arm/-/blob/master/bsp/bluetooth/rpi/pi-bluetooth+re4son_2.2_all.deb<br>
>wget https://gitlab.com/kalilinux/build-scripts/kali-arm/-/blob/master/bsp/bluetooth/rpi/50-bluetooth-hci-auto-poweron.rules<br>
>sudo cp 50-bluetooth-hci-auto-poweron.rules /usr/lib/udev/rules.d/50-bluetooth-hci-auto-poweron.rules<br>
>sudo dpkg --force-all -i pi-bluetooth+re4son_2.2_all.deb<br>
>sudo systemctl enable hciuart<br>
>sudo hciconfig<br>
After this it should appear the BT icon, right click on it, select "Devices" then trust and pair your device. Now open "Edit Connections" in the WiFi icon, select the Bluetooth connection you just created and modify it:
>General - Check auto connect<br>
>Ipv4 - I suggest "Manual" with a static IP address

The BT connection is useful, in combination with SSH and x11vnc, to take control of the system from a smartphone and use more advanced commands. As I said, the controls of the Bonnet are for a quick recon, just to peek around, but if you find something interesting, you can access to a terminal or a desktop to do other stuff.
Also, it can be useful to use the smartphone internet connection to send and receive data.

-Start
>sudo nano -w /etc/rc.local<br>
>sudo /home/kali/boot/starter.sh &<br>
>exit 0<br>

<h1>Additional Software</h1>

If you simply clone the repo or download the master, it won't work. You need to install other software. The reason because I've used Kali is that a lot of tools are apt-gettable.

<a href="https://rainbowstream.readthedocs.io/en/latest/">Rainbowstream</a> Used to tweet the interested output. At today, in the original configuration, is only implemented in the proxmark3 script. Notice that you will need a dedicated twitter account.

I could write a list of tools, but it's not useful, because I can suggest Proxmark3, HackRF or NFC tools, because I have them, but others can be uninterested.
Select your favourite tools and call them with the PocketNinja Scripts, just changing the path or tweaking the code.

<h1>Ideas</a>
-Auto connect to VPN
-Auto SSH Reverse Tunnel
-MouseJack
-Hackrf (specific frequency) Rec and Re-Play
-Nmap vuln

<h1>Truth to be told</h1>
I know that this is probably the worst and awful repository on github, but I'm not a coder. I needed a tool and did at my best something the most close to it. This is my first attempt at Python and I'm sure that there are better and more elegant ways to do this. This is the reason that pushed me to make the repo. So others (more experienced) can fork it or suggest improvements.<br> 
Read in friendly mode:<br>
Keep in mind, I'm not a coder, I've another job, so sadly I'll do what I can when I can. And most important the idea is the interface, not the tools. So sorry to disappoint you, but I do not recommend asking to add specific tools (because you can do that within the scripts) or open issues because an external software is not working.

