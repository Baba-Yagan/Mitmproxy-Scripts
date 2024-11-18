# Mitmproxy-Scripts
mitmproxy scripts that are designed to archive and download

## dumper.py
1) download mitmproxy
2) set up as per instructions
3) download the dumper.py file
4) change the directory to your own in the file
```
addons = [
    FileDumpAddon(output_dir="DIRECTORY_HERE")
]
```
5) `./mitmweb -s dumper.py`
