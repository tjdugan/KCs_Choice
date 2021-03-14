# KC'S CHOICE

A site built using Django that provides a ranking order of Beatles songs - best to worst - that is continually updated as the user selects between two random songs. If the song selected is currently rated lower than the other song that it is being compared to, it will replace that song in the current ranking and the other song will be pushed down one spot. All the songs rated between the two songs will be pushed down as well.

The results are saved as a list of integers that are pointers to the primary keys of the songs' records in the RatedItem model. The list of pointer values is saved as a comma-seperated text file and stored in the CurrentRating model.

Each model has a foreign key field - ItemGroup - that can be used in the future to expand the program to compare other items - (books, movies, etc.)

Application was built using: 
* Python version 3.8.2
* Django version 3.1.7
* Django-Widget-Tweaks version 1.4.8
* Bootstrap 4
* JQuery version 3.5.1
