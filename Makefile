DATA_FILE=march_sadness/static/data/teams.json

refresh : clean $(DATA_FILE)

clean :
	rm $(DATA_FILE)

$(DATA_FILE) :
	python refresh_data.py > $@
