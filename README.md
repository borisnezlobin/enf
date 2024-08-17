# Electrical Network Frequency Analysis

This repo is where I do all of my ENF work. I collaborate with Bellingcat's open-source team to work on various
bits of the ENF process. Right now, I'm working on getting accurate data on the European grid (you can find my progress, and data, in `/collection`).

## Data Collection Approach

I found a website that displayed ENF data of the European grid: https://mainsfrequency.com

This was good, so I tracked where it was sending its requests:
```
https://netzfrequenzmessung.de:9081/frequenz02c.xml?c={number}
```
Where {number} was randomly generated between 0 and 310,000.
Then, I started trying edge-case numbers (0, 310000, 310001, -1, -31). -31 and 310000 always seemed to work, whereas other ones were sketchy or didn't work at all. So, I started a script (running on [HackClub's Nest](https://github.com/hackclub/nest), which is amazing (and free!!)!!) that would write the data from this server every second. I write every day of data to a CSV file, but then I also
chunked my data by day, limiting each file to 86.5 thousand lines. Every month, I run a script that compiles each day into one massive month-long Parquet file (which is better than CSV at that size), which you'll soon find published here.