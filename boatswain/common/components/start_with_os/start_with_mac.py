import os
import sys

from boatswain.common.components.start_with_os.start_with_os import StartWithOS


class StartWithMac(StartWithOS):
    startup_dir = '~/Library/LaunchAgents'
    startup_file = '%s/boatswain_launcher.plist' % startup_dir

    def isEnabled(self):
        return os.path.isfile(self.startup_file)

    def enableStartWithOS(self):
        content = '''
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        <dict>
            <key>Label</key>
            <string>com.theboatswain.boatswain</string>
            <key>ProgramArguments</key>
            <array>                
                <string>%s</string>
            </array>
            <key>StandardErrorPath</key>
            <string>/var/log/boatswain.error</string>
            <key>KeepAlive</key>
            <true/>
        </dict>
        </plist>
        '''
        with open(self.startup_file) as bat_file:
            bat_file.write(content % sys.executable)

    def disableStartWithOS(self):
        os.remove(self.startup_file)
