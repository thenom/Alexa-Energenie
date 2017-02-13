"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG

"""

from __future__ import print_function
import requests

GET_URL = 'https://<external host>/powersocket/'
URL_User = "username"
URL_Pass = "password"

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "Energenie - " + title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Skills Kit sample. " \
                    "Please tell me your favorite color by saying, " \
                    "my favorite color is red"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me your favorite color by saying, " \
                    "my favorite color is red."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
        
        
def turn_on_all(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = True
    error_speech_output = "There was an error turning on all the lights"

    if 'plural_socket_type' in intent["slots"]:
        speech_output = "Turning on all the %s" % (intent["slots"]["plural_socket_type"]["value"])
    else:
        speech_output = "Illuminate!"
    reprompt_text = ""
    
    if send_request('update_socket/allon/'):
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
    else:
        return build_response(session_attributes, build_speechlet_response(card_title, error_speech_output, reprompt_text, should_end_session))
    
def turn_off_all(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = True
    error_speech_output = "There was an error turning off all the lights"

    if 'plural_socket_type' in intent["slots"]:
        speech_output = "Turning off all the %s" % (intent["slots"]["plural_socket_type"]["value"])
    else:
        speech_output = "Enter darkness!"
    reprompt_text = ""
    
    if send_request('update_socket/alloff/'):
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
    else:
        return build_response(session_attributes, build_speechlet_response(card_title, error_speech_output, reprompt_text, should_end_session))
    
def turn_on(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = True
    change = "0"

    try:
        if 'value' in intent["slots"]["socket_name"]:
            if 'value' in intent["slots"]["socket_type"]:
                speech_output = "Turning on the %s %s" % (intent["slots"]["socket_name"]["value"],intent["slots"]["socket_type"]["value"])
                error_speech_output = "There was an error turning on the " + intent["slots"]["socket_name"]["value"]
                change = intent["slots"]["socket_name"]["value"] + " " + intent["slots"]["socket_type"]["value"]
            else:
                speech_output = "Turning on the %s" % (intent["slots"]["socket_name"]["value"])
                error_speech_output = "There was an error turning on the " + intent["slots"]["socket_name"]["value"]
                change = intent["slots"]["socket_name"]["value"]
        elif 'value' in intent["slots"]["socket_number"]:
            speech_output = "Turning on socket number %s" % (intent["slots"]["socket_number"]["value"])
            error_speech_output = "There was an error turning on the socket " + intent["slots"]["socket_number"]["value"]
            change = intent["slots"]["socket_number"]["value"]
        else:
            speech_output = "Please provide a socket to turn on"
    except KeyError as err:
        raise_error = 'Key error with the response:\n{0}\n\n{1}'.format(intent,err)
        raise KeyError(raise_error)
        
    reprompt_text = ""
    
    if send_request('update_socket/' + change + '/',"on"):
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
    else:
        return build_response(session_attributes, build_speechlet_response(card_title, error_speech_output, reprompt_text, should_end_session))

def turn_off(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = True
    change = "0"

    try:
        if 'value' in intent["slots"]["socket_name"]:
            if 'value' in intent["slots"]["socket_type"]:
                speech_output = "Turning off the %s %s" % (intent["slots"]["socket_name"]["value"],intent["slots"]["socket_type"]["value"])
                error_speech_output = "There was an error turning off the " + intent["slots"]["socket_name"]["value"]
                change = intent["slots"]["socket_name"]["value"] + " " + intent["slots"]["socket_type"]["value"]
            else:
                speech_output = "Turning off the %s" % (intent["slots"]["socket_name"]["value"])
                error_speech_output = "There was an error turning off the " + intent["slots"]["socket_name"]["value"]
                change = intent["slots"]["socket_name"]["value"]
        elif 'value' in intent["slots"]["socket_number"]:
            speech_output = "Turning off socket number %s" % (intent["slots"]["socket_number"]["value"])
            error_speech_output = "There was an error turning off the socket " + intent["slots"]["socket_number"]["value"]
            change = intent["slots"]["socket_number"]["value"]
        else:
            speech_output = "Please provide a socket to turn off"
    except KeyError as err:
        raise_error = 'Key error with the response:\n{0}\n\n{1}'.format(intent,err)
        raise KeyError(raise_error)
        
    reprompt_text = ""
    
    if send_request('update_socket/' + change + '/',"off"):
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
    else:
        return build_response(session_attributes, build_speechlet_response(card_title, error_speech_output, reprompt_text, should_end_session))

def send_request(request,state = ""):
    POST_URL = GET_URL+request

    client = requests.session()

    # Retrieve the CSRF token first
    client.get(GET_URL, auth=(URL_User, URL_Pass))  # sets cookie
    csrftoken = client.cookies['csrftoken']

    print("Got CSRF token: " + csrftoken)

    if state <> "":
        login_data = dict(csrfmiddlewaretoken=csrftoken, next='/', change_to=state)
    else:
        login_data = dict(csrfmiddlewaretoken=csrftoken, next='/')

    r = client.post(POST_URL, data=login_data, headers=dict(Referer=GET_URL), auth=(URL_User, URL_Pass))

    if r.status_code == 200:
        return True
    else:
        raise_error = 'Error calling URL, got response code {0}.  URL: {1}'.format(r.status_code,POST_URL)
        raise ValueError(raise_error)
        return False

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "TurnOnAll":
        return turn_on_all(intent, session)
    elif intent_name == "TurnOffAll":
        return turn_off_all(intent, session)
    elif intent_name == "TurnOn":
        return turn_on(intent, session)
    elif intent_name == "TurnOff":
        return turn_off(intent, session)
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] != "amzn1.ask.skill.f9c07957-73d9-43d7-bc92-967570945716"):
        raise_error = "Invalid Application ID (%s)" % (event['session']['application']['applicationId'])
        raise ValueError(raise_error)

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
