import scrape

race_id_list = []
for place in range(1, 11, 1):
    for kai in range(1, 13, 1):
        for day in range(1, 13, 1):
            for r in range(1, 13, 1):
                race_id = "2019" + str(place).zfill(2) + str(kai).zfill(2) + str(day).zfill(2) + str(r).zfill(2)
                race_id_list.append(race_id)
Results = scrape.Results()
results = Results.scrape(race_id_list)