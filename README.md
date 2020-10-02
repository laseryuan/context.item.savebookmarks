[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/laseryuan/context.item.savebookmarks)
## Gitpod dev
```
pytest utils.py bookmark_test.py -s
```

## UI dev
```
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

cat /home/kodi/.kodi/temp/kodi.log
```

## Deploy
```
git archive --prefix context.item.savebookmarks/ --format=zip -o savebookmark.zip HEAD
```

