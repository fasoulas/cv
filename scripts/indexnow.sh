#!/bin/sh
# Ping IndexNow (Bing, Yandex, etc.) after deploy. Key file lives at site root.
KEY=4033fa35f5fc2b7efdce9edf7ee74c26
curl -s -o /dev/null -w "%{http_code}\n" \
  "https://api.indexnow.org/indexnow?url=https://fasoulas.com/&key=$KEY&keyLocation=https://fasoulas.com/$KEY.txt"
