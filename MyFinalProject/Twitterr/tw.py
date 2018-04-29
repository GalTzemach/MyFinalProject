import twitter

class Twtr:
    """description of class"""

    api = twitter.Api(consumer_key='', 
                      consumer_secret=	'', 
                      access_token_key=	'', 
                      access_token_secret=	'')


    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def Search(rawQuery=None):
        if rawQuery:
            results = api.GetSearch(raw_query)
            print(results)
        elif rawQuery == None:
            print("The function Search() received an empty parameter")
            
            
            
#raw_query = "q=twitter%20&result_type=recent&since=2014-07-19&count=100"




