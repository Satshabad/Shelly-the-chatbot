import cPickle

class Chatbot:
    """This class holds the chat-bot methods"""
    RESPONSE_MAP_FILE_NAME = "responseMappings"


    def __init__(self):
        """
        This constructor attempts to open the response mapping file, 
        if it can't be found then it creates a new responseMap dictionary
        
        """
        try:
            fileHandle = open(self.RESPONSE_MAP_FILE_NAME, 'r')
            self.responseMap = cPickle.load(fileHandle)
        except:
            self.responseMap = {}
   
   
    def __get_some_info(self):
        # This will try and gain responses for previous interactions which have no response yet.
        # Later this can ask a certain number of questions depending on how many answers we have for each
        for statement in self.responseMap.keys():
            if self.responseMap[statement] == []:
                print "Shelly: ",
                print statement
                print "You: ",
                userInput = raw_input()
                self.responseMap[statement].append(userInput)
        return None
     

    def start_chatting(self):
        # first try to fill in missing info
        self.__get_some_info()

        # then change to accepting user input
        print "Shelly: Ask me something, say 'stop' to end"
        
        
        # Do back and forth until user says 'stop'
        while True:
            print "You: ",
            
            # get the users input
            userInput = raw_input()
            
            if userInput == 'stop':
                self.close()
                
            print "Shelly: ",
            
            # find a response
            print self.__get_response(userInput)
            
            #for debugging let's see where we are getting our info
            print self.responseMap
        
        #save our new info
        self.close()
        return None
    
    
    def __get_response(self, userInput):
        
        # go though all the statements we have 
        for response in self.responseMap.keys():

            # try to find a match, .5 is the strictness of the match
            if self.__compare_input(response, userInput, .5):
                
                # if we have a match then we add all the given responses 
                # for that match to the key of the usersInput so we 
                # can expand our recognition power
                self.responseMap[userInput] = self.responseMap[response]
                 
                # We have a range of responses, later we can pick best
                return self.responseMap[response][0]

        # No good match was found for the user's input
        self.responseMap[userInput] = []
        return self.__no_response(userInput)

    
    def __no_response(self, userInput):
        # called if we can find no sutible response, currently this is a stub
        return "..."


    def __compare_input(self, strOne, strTwo, ratioCondition=.75):
        # This method determines whether to strings are semanticlly equivelent,
        # right now it just matches characters and gets the ratio of correct to the length,
        # but eventually it can match similar words         
        strOne = strOne.lower()
        strTwo = strTwo.lower()
        arrayOfMatchingChars = [0]
        longerStr = ""
        shorterStr = ""
        if len(strOne) > len(strTwo):
            arrayOfMatchingChars *= len(strOne)
            longerStr = strOne
            shorterStr = strTwo
        else:
            arrayOfMatchingChars *= len(strTwo)
            longerStr = strTwo
            shorterStr = strOne
        for index, character in enumerate(shorterStr):
            if character == longerStr[index]:
                arrayOfMatchingChars[index] = 1
        charMatchSum = sum(arrayOfMatchingChars)
        matchRatio = float(charMatchSum) / float(len(longerStr))
        if (matchRatio >= ratioCondition):
            return True
        return False


    def close(self):
        # call this everytime the session is over to save learned data
        fileHandle = open(self.RESPONSE_MAP_FILE_NAME, 'w')
        cPickle.dump(self.responseMap, fileHandle)


if __name__ == "__main__":
    c = Chatbot()
    c.start_chatting()
