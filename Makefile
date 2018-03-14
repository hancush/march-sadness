DATA_FILE=static/data/teams.json

refresh : clean $(DATA_FILE)

clean :
	rm $(DATA_FILE)

$(DATA_FILE) :
	python march_sadness/refresh_data.py 2018 > $@
