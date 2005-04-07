## 1 DESCRIPTION

QBRutracker is fast and open source Python 3 search plug-in for QBittorrent that provides convenient way of search through offline http://rutracker.org torrents database.

**Features:**

* Fast and reliable search without any dependency on site availability;

* Compact (latest database bzip size is only 90MB);

* Cross platform;

* Open Source under GPLv3;

* Configurable trackers list;

* Convenient search, integrated into bittorrent client (search by category, order by size, include and exclude words, limit results);

**Requirements:**
	
* QBittorrent http://qbittorrent.org

* Python 3 https://python.org


## 2 USAGE


*To install...*

1. download ```qbrutracker.py``` and follow this tutorial http://www.techsupportalert.com/qbittorrent-help-torrent-search-engine

2. download magnet:?xt=urn:btih:628F28C998A79D780455DC1B60892DD721EE44D1 or http://rutracker.org/forum/viewtopic.php?t=4824458 into ```%localappdata%\qbittorrent``` (or ```~/.local/share/data/qBittorrent```)

3. optionally put your public ```"tracker.txt"``` list into ```%localappdata%\qbittorrent\rutracker-torrents``` (or ```~/.local/share/data/qBittorrent/rutracker-torrents```)


*Search...*

will output all torrents with description that contains all search bar keywords. Excluding words that begin with "-" symbol. Search result is limited by defining word that begins with "=" immediately followed by digits. Example: "photo moscow -meet =10".


*To compact database...*

enter QB_PACK keyword into search bar. This will launch the process of packing (rutracker-torrents will be packed into bzip, then deleted), which leads to decrease of disk space occupied by database and search slowdown.


## 3 SUPPORT

If you find this software useful, please consider donating to this Bitcoin address: ```15Fagn4E2EzTEEZygJj5SpKVqg4tXEcGUU```
	
	
## 4 AUTHORS	

alvin, <alvin1979@mail.ru> idea and implementation.
	
	
## 5 NEWS AND UPDATES

https://github.com/alvin1979/qbrutracker