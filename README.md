# CIMI
User Personal Recipe Search Engine 

*Abstract*

CIMI allows users to create a user-unique search engine where they may add ingredients that they have at home.
Well known websites are then crawled to find recipes containing said ingredients, which will link to their
respective websites.

CIMI incorporates python/django, requests and beautifulsoup4.

The recipe websites supported are 'www.allrecipes.com', 'www.food.com' and 'www.foodnetwork.com'.


*Method Overview*

Using django's built in user-profiles, anonymous users need to create a profile to grant them access to the functionality
of the site. After sign up, they are ushered to the homepage where helpful prompts will send them to either a contact page 
or short description about the usability of CIMI. They may then create a Kitchen which will be their respective search 
engine. This will alow the user to add Ingredients into their Kitchen via the 'Manage Kitchen' page. 

After user-unique ingredients are added to their Kitchen, website specific buttons will prompt them to find recipes 
containing their specific ingredients. The results's names will be a brief overview about the recipe and will double as a 
hyperlink to te respective recipe hosted on the searched site.


*Web-scrapper Method*

The added ingredients will be compressed into a string with the readability of Google's address search function, ending on the
name of the relevant website. This ensures the results shown will be of the website. The search results are then scraped using 
beautifulsoup4 and request, which will be given to the user with their hyperlinks.

Google is used in combination with beautifulsoup4, as the algorithm is drastically speeded up, as the Google's search engine is 
the world's fastest web-scrapper.


*Contact*

For any inquiries contact me on dutoitdevon@gmail.com

*Link*

Can be viewed on http://cimi.pythonanywhere.com
