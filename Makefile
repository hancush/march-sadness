.INTERMEDIATE : bpi.csv colors.csv joined.csv

scraped/%.json :
	ncds scrape --$*

%.csv : scraped/%.json
	in2csv $< > $@

joined.csv : bpi.csv colors.csv
	csvjoin --left -c team bpi.csv colors.csv > $@

march_sadness/static/data/teams.json : joined.csv
	csvjson $< > $@