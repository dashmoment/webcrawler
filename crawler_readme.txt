web_crawler:
	dependencies:
		csv #for save content as .csv
		urllib2 #for parsing url
		lxml #most useful parser and grabber, support xpath
		beautiful soup #great fonder but might parse incomplete html file
		[optional] win32com #control ie directly(or some window app), but can not parse the content by beautiful soup
		
	Modules:
		1. Parser
			parser_etree(url)(parsed etree for filter)
		2. filter
			filter_etree(etree, sitetag(str))(retrieved data)
		3. collector
			collector_txt(data, sitetag(str))(result file.txt)
			collector_sql(data, dbname(sitetage.db))(upload sql_table)
			readfile(filename)(list of contents)
		4. sorting:
			sort(filename_for_sortedresults, filename_for_rank, content, tag)(sorted file)
			matcher(data, list)(matched index in list)
			matcher_part(data, list)(matched index in list) #only need partly matched. For matching title
		4. cal_score
			cal_score_txt(filename)(score in file.txt)
		5. analyzer
		
		

Developement notes:
2015/05/04:
	reviews:
	1. collector_txt()
		Finished parsing html by lxml package and filt functions for store, tilte and price are done by etree.xpath
		The parsed content sucess to saved into txt file, but content in the txt file is hard to retrieved.
		txt file seperated all data by char. It's means a string become a squence which length equal the number of char.
		In fact, contents in each rows should be contain of four column [score store price title].
		To doing this, I tried to use 
			1. file.write(','.join(content))
			2. file.write('%s\n'%content)
			3. file.writeline(content)
		
		none of then reach my expectation.
	
		Alternatively, import csv package, the content can be saved as .csv(or txt). 
		By using csv, contents can save in to a list [score store price title] and save as 4 cols by:
			writer.writer(list)
		All details are implented in function "collector_txt()"
	
	2. readfile():
		To read .csv file, I implemented a function "readfile()", this function can read .csv and return a 4 cols list:
		list [score store price title]
		
	3. sort():
		Next step, I would like to a sorting function which can sort contents by score, price or store
		Sorted by store will be finished firstly, and derive a corresponding rank.
		The rank of store will be one of factors for calculating scoe, so do sorted by price
		
		
2015/05/05:
	1. Psudo code for sorting by store:
		def sortbystore(data):
			sorted = []
			index = []
			idx = 0
			for idx in range(length(data)):
			
				in_sorted = find_data_in_sorted(data[i],sorted) #if found return last position; else return -1
				in_idx = find_idx_in_index(idx, index) ##if found return 0; else return -1
				
				if in_sorted == -1:
					sorted.append(content)
					index.append(idx):
				else if in_sorted != -1 and in_idx == -1:
					index.append(idx)
					insert(in_sorted + 1, data[i])
			return sorted
			
	2. To implement sortbystore or sortbytitle, matchers for comparing string and string in list are needed.
		for sortbystore, matcher is simply implmented by compare string and string in file contents. 
		After finding matched store name, the stores will be saved in a dict('storename':value), 
		the value means how many products of key store shows in top searching results.

		for sortbytitle, function matcher_part() are utlized for matching. Since it hard find exactly the same title in top searching results, 
		I use:
			matched_words/total_words
		as matchiing rule. By doing so, the most similar title will be sorted together. Although there are still some problem, the results look okay.
		
	3. Next step:
		1. fix problems of matcher_part()
		2. implment cal_score for ML



2014/05/07
	1. Finish sortbytitle which is merged in function sort():
		At first I ran into a trouble that csv writer can not write row correctly by:
			 writer_s.writerow(row_content)
			 
		The solution is that I need to add:
			rank_t = sorted(rank_t.items(), key = operator.itemgetter(1))
			
		where rank_t is the dict which store result data.
		I do not know why I need this before write row, but it did work well.
		So, just do it.
		
		Note: This only need for dict object. For list object, just use write row, it will do it own jod.











		
		
	