web_crawler:
	dependencies:
		csv //for save content as .csv
		urllib2 //for parsing url
		lxml //most useful parser and grabber, support xpath
		beautiful soup //great fonder but might parse incomplete html file
		[optional] win32com //control ie directly(or some window app), but can not parse the content by beautiful soup
		
	Modules:
		1. Parser
			parser_etree(url)(parsed etree for filter)
		2. filter
			filter_etree(etree, sitetag(str))(retrieved data)
		3. collector
			collector_txt(data, sitetag(str))(result file.txt)
			collector_sql(data, dbname(sitetage.db))(upload sql_table)
			readfile(filename)(list of contents)
		4. cal_score
			cal_score_txt(filename)(score in file.txt)
		5. analyzer
		
		

Developement notes:
2014/05/04:
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
		
		
		
		
		
	