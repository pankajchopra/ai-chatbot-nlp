import spacy
import json
import re
from yfinance import Tickers as tickers
# from spacy.pipeline import EntityRuler
# from spacy.matcher import PhraseMatcher

person_pattern = ["porter family", "potter family",
                          "Ron Dock", "ron dock", "dock ron"]
entity_rules = [
    {"label": "PERSON", "pattern": "porter family"},
    {"label": "PERSON", "pattern": "potter family"},
    {"label": "PERSON", "pattern": "dock ron"},
    {"label": "PERSON", "pattern": "ron dock"},
    {"label": "APPLICATION", "pattern": "account detail"},
    {"label": "APPLICATION", "pattern": "account detail"},
    {"label": "APPLICATION", "pattern": "household"},
    {"label": "APPLICATION", "pattern": "stock chart"},
    {"label": "APPLICATION", "pattern": "date or time or datetime"},
    {"label": "APPLICATION", "pattern": "stock news"},
    {"label": "ORG", "pattern": "amazon"},
    {"label": "ORG", "pattern": "Amazon"},
    {"label": "ORG", "pattern": "CISCO"},
    {"label": "ORG", "pattern": "cisco"}
    # {"label": "ORG", "pattern": "wellsfargo"}
]


class ExtractionUtils:
  def extract_entities(sentence):
      """Extracts entities from a sentence using NLP.
    Args:
      sentence: A string containing the sentence to extract entities from.
    Returns:
      A list of dictionaries containing the entities extracted from the sentence,
      where each dictionary contains the following keys:
        * `text`: The text of the entity.
        * `label`: The label of the entity, such as `PERSON`, `ORGANIZATION`,
          or `LOCATION`.
    """
      # Create a spaCy EntityRuler object.
      # entity_ruler = EntityRuler(nlp, overwrite_ents=True)



      # Load the spaCy English language model.
      nlp = spacy.load("en_core_web_sm")
      # matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
      # patterns = [nlp.make_doc(name) for name in person_pattern]
      # matcher.add("PERSON", patterns)
      
      entity_ruler = nlp.add_pipe("entity_ruler")
      # Add the custom entity rules to the EntityRuler object.
      for rule in entity_rules:
          entity_ruler.add_patterns([rule])

      # Process the sentence using the spaCy NLP pipeline.
      doc = nlp(sentence)

      # Extract all of the named entities from the sentence.
      entities = []
      for ent in doc.ents:
          entity = {
              "text": ent.text,
              "label": ent.label_,
          }
          entities.append(entity)

      # Return the list of entities.
      return entities

  def extract_names(self, sentence):
    names = []
    entities = self.extract_entities(sentence)
    if(entities):
      names = [entity['text'] for entity in entities if entity['label'] in ['PERSON']]
      return names
    else:
      return names

  def extract_these_entities(self, sentence, entity_label=[]):
    entity_extracted = []
    entities = self.extract_entities(sentence)
    if(entities):
      entity_extracted = [entity for entity in entities if entity['label'] in entity_label]
      return entity_extracted
    else:
      return entity_extracted
    
  def search_tickers(self, tickers, substr:str):
    result = []
    if not tickers:
      tickers = json.loads('tickers.json')
    if substr:  
      # res = [ticker for ticker in tickers if ((substr.upper() in str(ticker['Name']).upper() ) or substr.upper() in (str(ticker['Symbol']).upper()))]
      result = [ticker for ticker in tickers if (self.search_sentence_words_in_other_sentence(substr.upper(),str(ticker['Name']).upper() )) or (substr.upper() in re.findall("\w+",str(ticker['Symbol']).upper() ))]
    return result

  def search_tickers_symbol(self, tickers, substr:str):
    if not tickers:
      tickers = json.loads('tickers.json')
    res = []
    if substr:  
      # res = [ticker for ticker in tickers if ((substr.upper() in str(ticker['name']).upper() ) or substr.upper() in (str(ticker['symbol']).upper()))]
      res = [ticker for ticker in tickers if (self.search_sentence_words_in_other_sentence(substr.upper(),str(ticker['name']).upper() )) or (substr.upper() in re.findall("\w+",str(ticker['symbol']).upper() ))]
    if res and len(res)>0:
        return res
    else:
      return None
    
  def search_households(self,households, substr:str):
    res = []
    if substr:  
      res = [household for household in households if (self.search_sentence_words_in_other_sentence(substr.upper(),str(household['name']).upper() ))]
    
    if res and len(res)>0:
        return res
    else:
      return None
    
  def search_sentence_words_in_other_sentence(search_for, search_in):
    search_for_words = search_for.split()
    search_in_words_set = set(search_in.split())
    matching_words = []
    for word in search_for_words:
      if word in search_in_words_set:
        matching_words.append(word)
    # print(matching_words)
    
    if len(matching_words) >0:
      return True
    else:
      return False
    
  def create_json_response(tag, name, symbol, org, error):
      res:json = "{"
      if error:
          res = res + "error:'"+error +"'"
      else:
          if tag:
              res = res+ "tag:'"+tag+"'"              
          if name:
              if len(res)>2:
                  res = res+","
              res = res+ "name:'"+name+"'"
          if symbol:
              if len(res)>2:
                  res = res+","
              res = res + "symbol:'"+symbol+"'"          
          if org:
              if len(res)>2:
                  res = res+","
              res = res + "'org':'"+org+"'"
      res= res +"}"
      return res    
    
  
