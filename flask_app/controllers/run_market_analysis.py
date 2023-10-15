from flask_app.models.market_analysis import MarketAnalysis


def initMarketAnalysis(text, say):
    
    # Extract niche, state, and population range from the user input
    try:
        state, niche, min_pop, max_pop = [x.strip() for x in text.split(",")]
    except ValueError:
        say("Please provide the input in the format 'state, niche, minimum population, maximum population'")
        return
    
    say(f"Running analysis for cities in {state}, offering {niche}, with populations between {min_pop} and {max_pop}...")
    
    # Use MarketAnalysis to get a list of cities in the state with populations between min_pop and max_pop
    cities = MarketAnalysis.get_cities(state, min_pop, max_pop)
    
    say(f"Found {len(cities)} cities in {state} with populations between {min_pop} and {max_pop}...")
    
    for city in cities:
        # Use MarketAnalysis to get the google front page results
        location = f"{city}, {state}"
        search_results = MarketAnalysis.get_search_results(niche, location)
        
        # If no results are found, skip to the next city
        if not search_results:
            say(f"No results found for {location}")
            continue
        
        # If map pack results are not found, skip to the next city
        if not search_results.get('map_pack'):
            say(f"No map pack results found for {location}")
            continue
        
        # Use MarketAnalysis to process the map pack and organic results
        processed_map_pack = MarketAnalysis.process_map_pack(search_results.get('map_pack'))
        processed_organic_results = MarketAnalysis.process_organic_results(search_results.get('organic_results'))

        # Use MarketAnalysis to count instances of prameters: city name in title, more than 10 reviews, and connected websites
        map_pack_analysis = MarketAnalysis.analyze_map_pack(processed_map_pack, city)
        
        # Use MarketAnalysis to count instances of parameters: city name in title, city name in link
        organic_analysis = MarketAnalysis.analyze_organic_results(processed_organic_results, city)
        
        # Use MarketAnalysis to compare niche to types of map pack results and descriptions of organic results
        type_analysis = MarketAnalysis.analyze_types(processed_map_pack, niche)
        description_analysis = MarketAnalysis.analyze_descriptions(processed_organic_results, niche)
        
        # Use MarketAnalysis to prepare the response in table format
        # table_response = MarketAnalysis.prepare_response(map_pack_analysis, organic_analysis, type_analysis, description_analysis)
        # say(blocks=table_response)

        # Use MarketAnalysis to decide weather or not to proceed with the analysis
        final_decision = MarketAnalysis.decide_to_proceed(map_pack_analysis, organic_analysis, int(type_analysis), int(description_analysis))
        
        say(f"{final_decision} {location}")
    
    return "First glance analysis complete, bot terminating..."