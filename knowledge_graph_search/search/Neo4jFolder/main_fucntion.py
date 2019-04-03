


# select graph or list and select types of information
Graph = ['fdsfdsa']
List =[]
types = 'Scholar_paper'

# Assign author name or topics title

Author1 = "Yunchen Pu"
Author2 = "Lawrence Carin"
Paper_title = []



if Graph != []:

	# if types == 'All'

	# 	import Graph_ScholarPaper_User

	# 	if Author2 != []:
	# 		print(Author1 + " and " + Author2 + " wrote: ")
	# 		Graph_ScholarPaper_User.Worked_With (Author1,Author2)

	# 	if Author1 != [] and Paper_title != [] and Author2==[]:
	# 		print (Author1 + " wrote '" + Paper_title + "' with:" )
	# 		print('')
	# 		Graph_ScholarPaper_User.Recommend_Author(Author1,Paper_title)
	


	# 	elif Author1 != [] and Paper_title == [] and Author2==[]:
	# 		print (Author1 + " wrote :" )
	# 		Graph_ScholarPaper_User.Match_name(Author1)
	# 		# print (Author1 + " also worked with the following authors:")
	# 		# Worked_With (Author1)
	# 	elif Author1 == [] and Paper_title != [] and Author2==[]:
			
	# 		print (Paper_title + " written by :" )
	# 		print ()
	# 		Graph_ScholarPaper_User.Match_Title (Paper_title)
	

	if types == 'Scholar_paper' :

		import Graph_ScholarPaper_User

		if Author2 != []:
			print(Author1 + " and " + Author2 + " wrote: ")
			Graph_ScholarPaper_User.Worked_With (Author1,Author2)

		if Author1 != [] and Paper_title != [] and Author2==[]:
			print (Author1 + " wrote '" + Paper_title + "' with:" )
			print('')
			Graph_ScholarPaper_User.Recommend_Author(Author1,Paper_title)
	


		elif Author1 != [] and Paper_title == [] and Author2==[]:
			print (Author1 + " wrote :" )
			Graph_ScholarPaper_User.Match_name(Author1)
			# print (Author1 + " also worked with the following authors:")
			# Worked_With (Author1)
		elif Author1 == [] and Paper_title != [] and Author2==[]:
			
			print (Paper_title + " written by :" )
			print ()
			Graph_ScholarPaper_User.Match_Title (Paper_title)


if List != []:


	# if types == 'All':

	# 	import userneo4j

	# 	if Author1 != [] and Paper_title != [] and Author2==[]:
	# 		print (Author1 + " Wrote '" + Paper_title + "' with:" )
	# 		print('')
	# 		userneo4j.Recommend_Author(Author1,Paper_title)

	# 	elif Author1 != [] and Paper_title == [] and Author2==[]:
	# 		print (Author1 + " Wrote :" )
	# 		userneo4j.Match_name(Author1)		

	# 	elif Author1 == [] and Paper_title != [] and Author2==[]:
	
	# 		print (Paper_title + " written by :" )
	# 		print ()
	# 		userneo4j.Match_Title (Paper_title)

	# 	elif Author2 != []:
	# 		print(Author1 + " and " + Author2 + " Wrote: ")
	# 		userneo4j.Worked_With (Author1,Author2)
			
	if types == 'Scholar_paper' :

		import userneo4j

		if Author1 != [] and Paper_title != [] and Author2==[]:
			print (Author1 + " Wrote '" + Paper_title + "' with:" )
			print('')
			userneo4j.Recommend_Author(Author1,Paper_title)

		elif Author1 != [] and Paper_title == [] and Author2==[]:
			print (Author1 + " Wrote :" )
			userneo4j.Match_name(Author1)		

		elif Author1 == [] and Paper_title != [] and Author2==[]:
	
			print (Paper_title + " written by :" )
			print ()
			userneo4j.Match_Title (Paper_title)

		elif Author2 != []:
			print(Author1 + " and " + Author2 + " Wrote: ")
			userneo4j.Worked_With (Author1,Author2)

		# userneo4j.Match_name("Jonathon Shlens")