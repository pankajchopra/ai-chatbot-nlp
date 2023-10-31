import time
import speech_recognition as sr
import json
from speechtotext import SpeechToText
from extraction_utils import ExtractionUtils as eu
from nlptasks import NLPTASKS as nt
import random
from flask import Flask, render_template,request,jsonify
from keras.models import load_model
import traceback


model = load_model('model.keras')

intents = json.loads(open('data.json').read())
tickers = json.load(open('tickers.json'))
# householdsData = json.load(open('households.json'))

speechToText = SpeechToText()

from contextInfo import ContextInfo

cntxtInfo = ContextInfo();

def getResponse(ints, intents_json):
    print(ints)
    if len(ints)==0:
        tag='noanswer'
    else:
        tag=ints[0]['intent']
    if tag=='datetime':
        # print(time.strftime("%A"))
        # print (time.strftime("%d %B %Y"))
        # print (time.strftime("%H:%M:%S"))
        response = time.strftime("%A") + ", " + time.strftime("%d %B %Y") + " Time is " + time.strftime("%H:%M:%S")
        return response
    # if tag=='timer':
    #     mixer.init()
    #     x=input('Minutes to timer..')
    #     time.sleep(float(x)*60)
    #     mixer.music.load('Ring01.wav')
    #     mixer.music.play()

    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    res=""  
    if not msg:
        return;
       
    try:
        print(cntxtInfo.serialize())
        if cntxtInfo.status and cntxtInfo.tag and cntxtInfo.tag =='stockOption' and cntxtInfo.symbol:
            stockchartList = [ 'STOCK CHART', 'CHART', 'CHART PLEASE','STOP CHAT', 'STOP CHART', 'TALK CHART']
            stocknewsList=['STOCK NEWS','NEWS', 'STOCKNEWS', 'NEWS PLEASE', 'STOP NEWS', 'TALK NEWS']
            
            if option_result(msg, stocknewsList)>0 :
                print(cntxtInfo.org)
                res = eu.create_json_response('stockNews', None, cntxtInfo.symbol, cntxtInfo.org, None)
                cntxtInfo.clear()
                return res;
            elif option_result(msg, stockchartList):
                res = eu.create_json_response(tag='stockChart', name=None, symbol=cntxtInfo.symbol, org=cntxtInfo.org, error=None)
                cntxtInfo.clear()
                return res;
            else:
                res = eu.create_json_response(tag=None, name=None, symbol=None, org=None, error="Sorry, I didn't understand, Can you repeat whole question please..")
                cntxtInfo.clear()
                return res;
        if cntxtInfo.status and not cntxtInfo.tag:
            NoptionList = ['NO', 'THANKS', 'THANKYOU', "NO PLEASE", "NO THANK YOU"]
            YesOptionList = ['YES', 'PLEASE', 'SURE', "YES PLEASE"]
            if option_result(msg, NoptionList)>0:
                res = eu.create_json_response(tag=None, name=None, symbol=None, org=None, error="Ok")
                cntxtInfo.clear()
                return res;
            if option_result(msg, YesOptionList)>0:
                res = nlp_chatbot_response("morning briefing please")
                cntxtInfo.clear()
                return res;
            else:
                cntxtInfo.clear()
                res = eu.create_json_response(tag=None, name=None, symbol=None, org=None, error="Sorry, I did not get it my mistake, can you repeat it, please")
                return res;
        else:    
            res = nlp_chatbot_response(msg)
    except:
        cntxtInfo.clear()
        print("found error but continuing")
        traceback.print_exc(1000)
    return res

def nlp_chatbot_response(msg):
    print("in nlp_chatbot_response")
    print(msg)
    ints = nt.predict_class(nt, msg, model)
    res = ""
    if len(ints)>0:
        tag = ints[0]['intent']
        entities = eu.extract_entities(sentence=msg)
        print(entities)
        print(tag)
            
        if(tag=='account360'):
            names = []
            names_temp = [next((entity["text"] for entity in entities if entity["label"]=="PERSON"), None)]
            names = [ x for x in names_temp if x is not None]
            if(names and len(names)>1):
                res = eu.create_json_response(tag=None, name=None, symbol=None, org=None, error="More than one name found in the query [{}]".format(','.join(names)))
            elif (not names or len(names)==0):
                res = eu.create_json_response(tag=None, name=None, symbol=None, org=None, error="No name found in the query.")
            elif(names and len(names)==1):
                households = eu.search_households(eu, householdsData,names[0])
                print(households)
                hhid=households[0].get('hhid')
                name=households[0].get('name')
                res = eu.create_json_response(tag=tag, name=name, symbol=hhid, org=None, error=None)

            else:
                res = eu.create_json_response(tag=tag, name=names[0], symbol=None, org=None, error=None) 
        elif(tag in ['stockNews','stockChart','stockOption']):
            org_temp = [next((entity["text"] for entity in entities if entity["label"]=="ORG"), None)]
            org = [ x for x in org_temp if x is not None]
            
            
            # -----------------------------------------
            print("org:"+','.join(org))
            print("tag:"+tag)
            if org and len(org)>1:
                return eu.create_json_response(tag=None, name=None, symbol=None, org=None, error="More than one org names found in the query [{}]".format(','.join(org)));
            elif not org or len(org)==0:
                return eu.create_json_response(tag=None, name=None, symbol=None, org=None, error="Please repeat, No org found in the query.")
            # -----------------------------------------
            elif not org or len(org)==1:        
                tckrs = eu.search_tickers_symbol(eu, tickers, org[0])
                print(tckrs)
                if(not tckrs):
                    res = eu.create_json_response(tag=tag, name=None, symbol=None, org=org[0], error="Possible Ticker DB not updated.. No ticker found for {}".format(org[0])) 
                else:
                    if(len(tckrs)==1):
                        symbol_temp = [next((ticker['symbol'] for ticker in tckrs if org[0].upper() in ticker["name"].upper()), None)]
                        symbol = [ x for x in symbol_temp if x is not None]
                        orgname = next((ticker['name'] for ticker in tckrs if ticker["symbol"]==symbol[0]), None)
                        
                        if(symbol and len(symbol)==1):
                            if(tag=='stockOption'):
                                # res = getResponse(ints, intents)
                                # res=res.format(orgname+"(NYSE:"+symbol[0]+")")
                                # res = eu.create_json_response(tag=None, name=None, symbol=None, org=None, error=res)
                                print(orgname)
                                cntxtInfo.set(tag='stockOption',symbol=symbol[0], org=orgname, status=True, error=None)
                                print(cntxtInfo.org)
                                return eu.create_json_response(tag=None, name=None, symbol=symbol[0], org=orgname, error=getResponse(ints, intents)) 
                            else:
                                cntxtInfo.clear()
                                return eu.create_json_response(tag, None, symbol[0], orgname, error=None)
                        else:
                            cntxtInfo.clear()
                            return eu.create_json_response(tag=tag, name=None, symbol=None, org=orgname, error="No tickers found for {}".format(orgname))
        else:
            return eu.create_json_response(tag=None, name=None, symbol=None, org=None, error=getResponse(ints, intents))   
    else:
        return eu.create_json_response(tag=None, name=None, symbol=None, org=None, error="Didn't get it! my mistake, can you repeat please")
        
    return res


    print("org:"+','.join(org))
    print("tag:"+tag)
    if org and len(org)>1:
        res = eu.create_json_response(tag=None, name=None, symbol=None, org=None, error="More than one org names found in the query [{}]".format(','.join(org)));
    elif not org or len(org)==0:
        res = eu.create_json_response(tag=None, name=None, symbol=None, org=None, error="Please repeat, No org found in the query.")
    return res;

def option_result(msg:str, lst):
    if not msg:
        return 0;
    if(msg.upper() in lst):
        return 1;
    else:
        msg_words = msg.split()
        for m in msg_words:
            result = len([k for k in lst if m.upper()==k])
        return result
    




app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    if userText and userText == 'Sorry, I could not understand what you were saying':
        return 'Sorry, I could not understand what you were saying, can you repeat please'
    return chatbot_response(userText)

@app.route('/process_input',methods=['POST'])
def process_input():
    text = speechToText.speechToTextRun()
    if text and len(text)>0:
        print("text after speechToTextRun:"+text)
        text = json.loads(text.replace('\n', ''))
        response ={
         'textResponse':text["text"],
        }
    # response ={
    #     'textResponse':'"What you can do?',
    # }
        return jsonify(response)
    else:
        print("speechtotext return an empty String")
        return ""

@app.route("/refresh")
def refresh():
    cntxtInfo.clear()
    cntxtInfo.status=True
    

if __name__ == "__main__":
    # chatbot_response("Can you show me account details for James Scott")
    # chatbot_response("Can you show me household info for porter family")
    # chatbot_response("Get me stock news for Wells Fargo")
    # chatbot_response("Can you show me stock chart for Amazon")
    # chatbot_response("Fetch me stock news for international")
    # chatbot_response("Get me stock chart for Ford")
    cntxtInfo.status=True
    app.run()

    
def org_check_fail(org, tag):
    res = None
