# Web Shark  
![Local Image](logo.jpg){:height="125px" width="125px"} 

### Mission
We aren't swimming in Google's wake... we're following following a trail of blood!

### Features
1. Lightning fast semantic search... 5.38x faster than Google!
2. Intelligent web surfer (crawler)
3. Build a search index with just a root url!
4. Respects user privacy 1,000,000 times better than Google

### Dependencies
1. conda
2. GPU (recommended)

### Usage
1. Run setup
`./setup.sh`

2. Activate the environment
`conda activate webshark`

3. Run crawler 
`python crawl.py --root https://en.wikipedia.org/wiki/World_War_II --page_limit 100 --save_path wikipedia`

4. Start searching!
`python search.py --index_path wikipedia`