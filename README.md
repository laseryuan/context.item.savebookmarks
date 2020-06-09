```
cd ~/projects/kodi/context.item.savebookmarks

docker run -it --rm --name=kodi \
  --privileged \
  -e DISPLAY=unix:0 -v /tmp/.X11-unix:/tmp/.X11-unix \
  -e PULSE_SERVER=unix:/run/user/1000/pulse/native -v /run/user/1000:/run/user/1000 \
  -v /var/run/dbus/:/var/run/dbus/ \
  -v /home/laser/Videos/:/home/kodi/Videos/ `# mount video library`\
  -v kodi-config:/home/kodi/.kodi/userdata `# persist kodi configuration`\
  -v kodi-addons:/home/kodi/.kodi/addons/ `# persist kodi addon dependencies`\
  -v $(pwd)/:/home/kodi/.kodi/addons/context.item.savebookmarks/ `# mount the addon; needs to be enabled in kodi config`\
  lasery/codebench:kodi \
  bash

  -v $(pwd)/../plugin.googledrive/:/home/kodi/.kodi/addons/plugin.googledrive/ `# mount the addon; needs to be enabled in kodi config`\
  -v $(pwd)/../plugin.googledrive/fork/script.module.clouddrive.common:/home/kodi/.kodi/addons/script.module.clouddrive.common/ `# mount the dependency addon`\

cd ~/.kodi/addons/context.item.savebookmarks/
pytest utils.py kodidb.py

pytest utils.py -s
pytest kodidb.py -s
pytest kodidb.py::test_get_posts_from_bookmark -s

cat /home/kodi/.kodi/temp/kodi.log
```

