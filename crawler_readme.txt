web_crawler:
	dependencies:
		lxml //most useful parser and grabber, support xpath
		beautiful soup //great fonder but might parse incomplete html file
		[optional] win32com //control ie directly(or some window app), but can not parse the content by beautiful soup
		
	Modules:
		1. Parser
			parser_etree
		2. filter
			filter_etree
		3. collector
			collector
		4. cal_score
		5. analyzer