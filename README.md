Requirements:
pip3 install matplotlib

Setup steps :
1. Place foreground_working.py at $HOME/wellnessapp/ and ensure same path is present in all your plist files.
2. Place all plist files in Library/LaunchAgents/
3. Load all plist files and ensure they have been loaded successfully:
                launchctl load ~/Library/LaunchAgents/idletimer-onlogin.plist
                launchctl load ~/Library/LaunchAgents/meetingtime-onlogin.plist
                launchctl load ~/Library/LaunchAgents/internettime-onlogin.plist 
                launchctl load ~/Library/LaunchAgents/apptimer-onlogin.plist
4. Place Akatracker.py, plot_graph.py, index2.html and main in $HOME/wellnessapp/
5. To create Automator:
                a. chmod 755 main
                b. Launch Automator(takes some time) -> click Application -> Choose
                c. On the left panel select Files and Folders -> Get specified Finder Items(drag and drop into right gray area)
                d. Once Get Finder Items is in the gray area, Select Add -> and choose the main executable file
                e. Now drag and drop Open finder items(left panel) to gray area. Leave with Default application.
                f. Command + S(Save with *.app)
 
Voila! You should now have a robot looking app on your Desktop which will launch a Tkinter window. Click on “Show me stats” to run the scripts to plot graphs and display them.

