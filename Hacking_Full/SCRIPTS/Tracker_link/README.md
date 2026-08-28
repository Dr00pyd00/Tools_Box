
# Mini Tracker http

Http server to run and use ngrok for have a clickable link to get some datao.

The script run in:
- `ip` = localhost
- `port` = 8000

#### Start the script
```bash 
python3 tracker.py
```

#### use ngrok for have link on internet

```bash 
ngrok http 8000
```
- `ngrok` : software that give you tunnel in internet
- `http` : protocole use
- `8000` : port listen

It display you a new URL link to your script !

--- 
### save data 

Automatic save of data received in `tracker_data.txt`.
