# News_Prediction
This project has been accomplished in 4 phases and are as follows:
1) Scraping - We extracted 5 columns namely Title, Published_Date, Author_Name, Genre and Number_of_Comments. Scraping was accomplished with help of urllib and Beautiful Soup utility. 

2) Cleaning - With the help of Regular expression and Beautiful soup utility we further cleaned the column values in proper formats.

3) Feature Engineering - We derived various new columns that can be a deciding factor to predict the Number of comments. 
We used Pandas library to paly with various function like sum,count,unique and various others.
4) Prediction - We predicted the Number_of_Comments(Label),using 11 independent variables that we derived after feature engineering.
For Instance: If Author X writes an article on Genre, then how many comments he can receive?



