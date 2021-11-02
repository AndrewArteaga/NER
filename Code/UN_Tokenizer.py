# Removes Warnings From Console 
# May need to update numpy in the future
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import json
import spacy
import re 

# Opening JSON List Files Containing Codebook Rules
def open_txt(file):
    with open(file, 'r') as data_file:
        json_data = data_file.read()

    data = json.loads(json_data)
    return data

# Converting Rules To Proper Spacy Rule Format 
def convert(rules):
    converted_rules = []
    for w,x,y,z in rules:
        # Example Rule Format for BIO tagging:
        # {"label": "DRUG", "pattern": [{"lower": "ipratropium"}]}
        # {"label": "DRUG", "pattern": [{"lower": "ipratropium"}, {"lower": "-"}, {"lower": "albuterol"}]}
        rule_dict = {}
        # setting labels
        rule_dict[w] = x
        # setting patterns
        pattern_list = []
        for i in z.split():
            lower_dict = {}
            lower_dict['lower'] = i
            pattern_list.append(lower_dict)
        rule_dict[y] = pattern_list
        converted_rules.append(rule_dict)
    return converted_rules

# Converting Rules To Proper Spacy Rule Format THEMES
def convert_themes(rules):
    converted_rules = []
    for w,x,y,z in rules:
        # Example Rule Format for BIO tagging:
        # {"label": "DRUG", "pattern": [{"lower": "ipratropium"}]}
        # {"label": "DRUG", "pattern": [{"lower": "ipratropium"}, {"lower": "-"}, {"lower": "albuterol"}]}
        for i in z.split("; "):
            rule_dict = {}
            # setting labels
            rule_dict[w] = x
            pattern_list = []
            # setting patterns
            for j in i.split():
                lower_dict = {}
                lower_dict['lower'] = j
                pattern_list.append(lower_dict)
                rule_dict[y] = pattern_list
            converted_rules.append(rule_dict)
    return converted_rules

# https://shancarter.github.io/mr-data-converter/
'''
####
Tags
####
'''
'''
Themes
'''
CodeBook_Themes_Topic_Rules = convert_themes(open_txt('./CodeBook/Themes/Topic.json'))
CodeBook_Themes_Location_Rules = convert_themes(open_txt('./CodeBook/Themes/Location.json'))
'''
Sense of Direction
'''
# Categories of Directions:	    Definition:			
# POSITIVE	                    Welcomed, optimistic, appreciated or other positively connotated development.			
# NEGATIVE	                    Concerned, pessimistic, unappreciated or other negatively connotated development.			
# NEUTRAL	                    Development which is neither positive nor negative.			
CodeBook_Grade_of_Action_Rules = convert(open_txt('./CodeBook/Grade_of_Action.json'))

'''
Scale of Urgency
'''
# Categories of Intensifiers:	Definition:			
# NEUTRAL	                    Impartial stance without expressing a definite opinion about an issue, development or action.			
# MEDIUM	                    A stance about an issue, development or action is expressed.			
# STRONG	                    A more absolute stance regarding an issue, development or action is expressed.	
CodeBook_Scale_of_Urgency_Rules = convert(open_txt('./CodeBook/Scale_of_Urgency.json'))

'''
Grade of Action
'''
# Categories of Actions:	    Definition:			
# ACTION TAKEN	                A concrete measure was considered or adopted.			
# ACTION ADVISED	            A measure is requested, recommended, suggested or desired.			
# OTHER	                        Any other stance and opinion is expressed that does not include action.			
CodeBook_Sense_of_Direction_Rules = convert(open_txt('./CodeBook/Sense_of_Direction.json'))

# BIO Tagging UN Documents
with open("sample_text.txt") as text_file:
    contents = text_file.read()
print("Original Post:\n", contents)
contents = contents.lower()
contents = re.sub("[\(\[].*?[\)\]]", "", contents)
contents = re.sub("  ", " ", contents)
print("\nModified Post:\n", contents)
# Process the text
nlp = spacy.load("en_core_web_sm")
ruler = nlp.add_pipe("entity_ruler")
for rule in CodeBook_Themes_Topic_Rules:
    ruler.add_patterns([rule])
for rule in CodeBook_Themes_Location_Rules:
    ruler.add_patterns([rule])
for rule in CodeBook_Grade_of_Action_Rules:
    ruler.add_patterns([rule])
for rule in CodeBook_Scale_of_Urgency_Rules:
    ruler.add_patterns([rule])
for rule in CodeBook_Sense_of_Direction_Rules:
    ruler.add_patterns([rule])
doc = nlp(contents)
print("\nTokenized Version of Modified Post:")
header_0 = 'Text:'
header_1 = 'Tag:'
header_2 = 'Label:'
print(f"{header_0:<20}{header_1:<20}{header_2:<20}")
for token in doc:
    if token.text == ' ':
        pass
    print(f"{token.text:<20}{token.ent_iob_:<20}{token.ent_type_:<40}") 