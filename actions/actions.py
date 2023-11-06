# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from serpapi import GoogleSearch
from serpapi import YoutubeSearch
from database_connectivity import DataUpdate

class ActionGetTestResults(Action):
    def name(self):
        return 'action_get_test_results'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("q1_slot_value: " + tracker.get_slot('q1_level'))
        print("q2_slot_value: " + tracker.get_slot('q2_level'))
        print("q4_slot_value: " + tracker.get_slot('q4_level'))
        q1_slot_value = int(tracker.get_slot('q1_level'))
        q2_slot_value = int(tracker.get_slot('q2_level'))
        q4_slot_value = int(tracker.get_slot('q4_level'))

        total =  q1_slot_value + q2_slot_value + q4_slot_value
        if (total < 6):
            dispatcher.utter_message(' Your test result shows no signs of ADHD https://media.makeameme.org/created/sit-back-and-a57daf87da.jpg' )
        elif (total < 10):
            search = YoutubeSearch({"search_query": "ADD & Loving It?!","api_key": "ed648658bba17cb474ec55c93b02818c09f3906afcf045efe82014d75b07e97a"})
            r = search.get_object()
            dispatcher.utter_message('Here is a documentary on ADHD, hope it helps :) \n ' + r.video_results[0].link )
        else:
            search = GoogleSearch({"q": "ADHD professionals near me", "location": "Austin,Texas","api_key": "ed648658bba17cb474ec55c93b02818c09f3906afcf045efe82014d75b07e97a"})
            r = search.get_object()
            dispatcher.utter_message('I have found ADHD professionals near you \n ' + r.search_metadata.google_url )

        return []

class ActionSubmitFeedback(Action):
    def name(self):
        return 'action_submit_user_feedback'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            conversation=tracker.events
            logFileName = 'chats.txt'
            import os
            if not os.path.isfile('chats.txt'):
                with open(logFileName,'w') as file:
                    file.write("intent,user_input,entity_name,entity_value,action,bot_reply\n")
            chat_data=''
            for i in conversation:
                if i['event'] == 'user':
                    # chat_data+=i['parse_data']['intent']['name']+','+i['text']+','
                    print('user: {}'.format(i['text']))
                    if len(i['parse_data']['entities']) > 0:
                        # chat_data+=i['parse_data']['entities'][0]['entity']+','+i['parse_data']['entities'][0]['value']+','
                        print('extra data:', i['parse_data']['entities'][0]['entity'], '=',
                              i['parse_data']['entities'][0]['value'])
                    else:
                        chat_data+=" | "
                elif i['event'] == 'bot':
                    print('Bot: {}'.format(i['text']))
                    try:
                        chat_data+=i['metadata']['utter_action']+' | '+i['text']+'\n'
                    except KeyError:
                        pass
            else:
                with open('chats.txt','a') as file:
                    file.write(chat_data)

            dispatcher.utter_message(text="Your feedback is recorded. Thanks!")

            DataUpdate("Pranai","Feedback from Pranai",logFileName)