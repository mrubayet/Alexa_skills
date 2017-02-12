import feedparser

def lambda_handler(event, context):
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.9a732577-7e8a-4bf0-b57d-d0e195668c9b"):
        raise ValueError("Invalid Application ID")
    
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])
		
def on_session_started(session_started_request, session):
    print "Starting new session."

def on_launch(launch_request, session):
    return get_welcome_response()

def on_intent(intent_request, session):
    intent_name = intent_request["intent"]["name"]

    if intent_name == "YesIntent":
        return get_yes_intent()
    elif intent_name == "NoIntent":
        return get_no_intent()
    
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    print "Ending session."
	
	
def get_welcome_response():
    session_attributes = {}
    card_title = "PASS REPORT"
    speech_output = 'Welcome to Snoqualmie pass. would you like to hear pass report?'
    reprompt_text = "With pass you can get pass report of Snoqualmie Pass on I-90. Say yes " + \
                    "to hear the last updated report. So, would you like to hear pass report "
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "PASS - Thanks"
    speech_output = "Thanks.  See you next time!"
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))		
		
		
def get_passreport():
       url = 'http://wsdot.wa.gov/traffic/api/MountainPassConditions/rss.aspx'
       d = feedparser.parse(url) 
       xx=d.entries[11].description.replace("<strong>","").replace("</strong>","").replace("<br>","").replace("<br />","").split("\n")
       xx = list(filter(None, xx))
       xx = [w.replace('&nbsp;','').replace('&',' ').replace(';',' ') for w in xx]
       speech_out=[]
       speech_out.append(xx[0]+" updated at "+xx[1] + "...For Eastbound. "+xx[3].replace("Eastbound",'')+
        "...For Westbound. "+xx[4].replace("Westbound",'')+ "...Road condition is. " + 
        xx[5].replace("Conditions:",'') + "...Weather. " + xx[6].replace("Weather:",'') +
        " With Temperature " + xx[2].replace("Temperature:",'').replace("deg",'degree').replace("F",'Farenheit'))
       return ' '.join(speech_out).encode('utf8') 
       
       
    
def get_yes_intent():
    session_attributes = {}
    card_title = "PASS REPORT"
    reprompt_text = ""
    should_end_session = False
    passreport = get_passreport()
    speech_output = 'The pass report for {}'.format(passreport)
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_no_intent():
    card_title = "PASS - Thanks"
    speech_output = 'hmmm! good bye'
    should_end_session = True
    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))		
 

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }
