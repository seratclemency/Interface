[app]
title = Interface
package.name = com.serat.onelove
source.include_exts = py,png,jpg,kv,atlas
package.domain =
source.dir = .
version = 1.0
requirements = python3, kivy==master, https://github.com/kivymd/KivyMD/archive/master.zip, beautifulsoup4, requests, google, soupsieve
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE
android.manifest = /content/AndroidManifest.xml
orientation = portrait
fullscreen = 0