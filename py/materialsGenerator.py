from material import MaterialSummary, partedMaterialSchema, materialSchema, materialPartSchema, Material, MaterialPart, PartedMaterial, PartType, ResourceSubtype, ResourceType, Rarity
import gpt4
import pyjson5 as json
import functools
from enum import StrEnum

# MaterialsLib
materialsLib: dict[str, Material | PartedMaterial] = {}

# Descriptions
resourceTypeDescriptions: dict[ResourceType,str] = {}
resourceSubtypeDescriptions: dict[ResourceSubtype,str] = {}
partTypeDescriptions: dict[PartType,str] = {}

# Coefficients
rarityValueCoefficients = {
     Rarity.COMMON: 1,
     Rarity.UNCOMMON: 1.5 ,
     Rarity.RARE: 3,
     Rarity.VERYRARE: 7.5 ,
     Rarity.LEGENDARY: 22.5 
}
partTypeValueCoefficients: dict[PartType,float] = {}

rarityRates: dict[Rarity,float] = {
    Rarity.COMMON: 30,
    Rarity.UNCOMMON: 25,
    Rarity.RARE: 20,
    Rarity.VERYRARE: 15,
    Rarity.LEGENDARY: 10
}
partTypeBaseValues: dict[PartType,(float, float)] = {}
primaryPartCoefficient: float = 1
secondaryPartCoefficient: float = 0.7

# Incomes
tradespersonIncome = 2
laypersonIncome = 0.1

def __parseJsonToMaterial__(jsonString) -> Material | PartedMaterial:
    materialClass = Material if 'parts' not in json.loads(
        jsonString) else PartedMaterial
    return materialClass(jsonData = jsonString)
    

def generateMaterial(messages: list[str]) -> Material | PartedMaterial:
    response = gpt4.getChatResponse(messages)
    
    try:
        return __parseJsonToMaterial__(response)
    except:
        try:
            return __parseJsonToMaterial__(response[response.index('{'):response.rfind('}')+1])
        except:
            with open('failed-parsing.txt', 'a') as outfile:
                outfile.write("\r\n" + response)
            return None

def __reduceEnumKVPToTableRow__(memo, key, enum):
    row = "{}: {}".format(key.name, enum[key])
    if memo is None or memo == '':
        return row
    return memo + ', ' + row


def convertEnumDictToChatTable(dict):
    return functools.reduce(lambda memo, key: __reduceEnumKVPToTableRow__(memo, key, dict), dict, '')

def convertEnumToChatTable(enum) -> str:
    dict = {i: i.value for i in enum}
    return convertEnumDictToChatTable(dict)

def convertEnumNamesToList(enum: StrEnum):
    return ', '.join([i.name for i in enum])

def __buildTypeContext__(messages: list[str], resourceType: ResourceType = None, resourceSubtype: ResourceSubtype = None) -> list[str]:
    messages.append({'role': 'user', 'content': "Here is a list of possible resource types: {}".format(
        convertEnumNamesToList(ResourceType))})
    messages.append(
        {'role': 'assistant', 'content': 'Thanks for the information!'})
    messages.append({'role': 'user', 'content': "Here is a list of possible resource subtypes: {}".format(
        convertEnumNamesToList(ResourceSubtype))})
    messages.append(
        {'role': 'assistant', 'content': 'Thanks for the information!'})
    if (resourceType is not None):
        messages.append(
            {'role': 'user', 'content': 'Our object is going to be a {}'.format(resourceType.name)})
        messages.append(
            {'role': 'assistant', 'content': 'Thanks for the information!'})
        if (resourceSubtype is not None):
            messages.append({'role': 'user', 'content': 'Our object is going to be a {} which is a subtype of {}.  It should not be of any other subtypes.'.format(
                resourceSubtype.name, resourceType.name)})
            messages.append(
                {'role': 'assistant', 'content': 'Thanks for the information!'})
            
            if resourceType in resourceTypeDescriptions:
                messages.append({'role': 'user', 'content': 'Here is some information on the {} resource type: {}'.format(
                    resourceType.name, resourceTypeDescriptions[resourceType])})
                messages.append(
                    {'role': 'assistant', 'content': 'Thanks for the information!'})
            if resourceSubtype in resourceSubtypeDescriptions:
                messages.append({'role': 'user', 'content': 'Here is some information on the {} resource subtype: {}'.format(
                    resourceType.name, resourceSubtypeDescriptions[resourceSubtype])})
                messages.append(
                    {'role': 'assistant', 'content': 'Thanks for the information! Is there anything else?'})
        else:
            if resourceType in resourceTypeDescriptions:
                messages.append({'role': 'user', 'content': 'Here is some information on the {} resource type: {}'.format(
                    resourceType.name, resourceTypeDescriptions[resourceType])})
                messages.append(
                    {'role': 'assistant', 'content': 'Thanks for the information!'})
            
    else:
        messages.append({'role': 'user', 'content': "You'll need to decide the reosource type and subtype.  Here are a list of available types:\r\n{}\r\n\r\nAnd here is a list of available subtypes:\r\n{}\r\n\r\nSelect the type first, then select a subtype that makes sense with regards to the selected type.".format(convertEnumToChatTable(ResourceType), convertEnumToChatTable(ResourceSubtype))})
            
    return messages

def __buildSchemaContext__(messages: list[str], isParted: bool = False) -> list[str]:
    messages.append(
        {'role': 'user', 'content': "Now let's talk about the schema for these items.  I'd like them returned as JSON objects."})
    messages.append({'role': 'assistant',
                     'content': 'Great! What schema should I use for generating these?'})

    if (isParted):
        messages.append({'role': 'user', 'content': partedMaterialSchema})
        messages.append(
            {'role': 'assistant', "content": 'Understood.  What is the Schema for the Parts array?'})
        messages.append({'role': 'user', 'content': materialPartSchema})
    else:
        messages.append({'role': 'user', 'content': materialSchema})

    messages.append({'role': 'assistant',
                     "content": 'Understood.  I will not deviate from this schema.'})
    return messages

def __buildRarityContext__(messages: list[str], rarity: Rarity = None) -> list[str]:
    messages.append(
        {'role': 'user', 'content': "Now let's talk about the object's rarity. Rarity scales according to the following information:\r\n{}".format(convertEnumToChatTable(Rarity))})
    messages.append({'role': 'assistant',
                     'content': "That makes sense.  I will remember that mapping of integers to rarity levels."})
    if(rarity is not None):
        messages.append(
            {'role': 'user', 'content': "This item needs to be {}.".format(rarity.name)})
        messages.append({'role': 'assistant',
                         'content': "Okay! I will make this item {}.".format(rarity.name)})
    else:
        messages.append(
            {'role': 'user', 'content': "This item can be of any rarity, so you decide what rarity it should be.  Here is a quick breakdown of the rate of a rarity ocurring randomly (given as a decimal):\r\n{}".format(convertEnumDictToChatTable(rarityRates))})
        messages.append(
            {'role': 'assistant', 'content': "Okay! I'll decide the item's rarity myself."})
        
    return messages



def __buildPartValueContext__(messages: list[str], primaryPartType: PartType = None, primaryCoefficient: float = 1, secondaryCoefficient: float = 1) -> list[str]:
    if primaryPartType is not None:
        messages.append({'role': 'user', 'content': "Now, let's talk about the value of the item's parts.  The primary part of this item is the {}.  As a reminder, the pimary part value coefficient is {} and the secondary part value coefficient is {}.".format(
            primaryPartType.name, primaryCoefficient, secondaryCoefficient)})
    else:
        messages.append({'role': 'user', 'content': "Now, let's talk about the value of the item's parts.  As a reminder, the pimary part value coefficient is {} and the secondary part value coefficient is {}.  You'll need to determine which part is the primary part of the item.".format(
            primaryCoefficient, secondaryCoefficient)})
        messages.append({'role': 'assistant', 'content': "Understood.  I'll make sure to multiply the values of the item parts by the primary part value coefficient if it is the primary part.  Otherwise I will multiply it by the secondar part value coefficient."})
    
    return messages

def __buildValueContext__(messages: list[str], isParted: bool = False, resourceType: ResourceType = None, primaryPartType: PartType = None, rarity: Rarity = None) -> list[str]:
    primaryCoefficient = primaryPartCoefficient
    secondaryCoefficient = secondaryPartCoefficient

    messages.append({'role': 'user', 'content': "When you determine something's value, keep in mind the average tradesperson only earns about {} value per day and the average layperson only earns about {} per day.".format(
        tradespersonIncome, laypersonIncome)})
    messages.append({'role': 'assistant', 'content': "Okay.  I'll make sure to consider the average tradesperson's and layperson's income when setting the price of things and ensure that a family of four can live well on a tradesperson's income."})
    
    messages.append({'role': 'user', 'content': "Also consider the laws of supply and demand and the behaviors of complementary and supplementary goods when setting values.  The sap of a legendary tree may be difficult to collect and rare, but if it is functionally identical to maple sap, it's value will be no higher than that of maple sap."})
    messages.append({'role': 'assistant', 'content': "I'll try and consider the economic behaviours around an item or item part when determining the value."})

    if rarity is not None:
        if isParted:
            primaryCoefficient *= (rarityValueCoefficients[rarity] or 1)
            secondaryCoefficient *= (rarityValueCoefficients[rarity] or 1)
            messages = __buildPartValueContext__(
                messages, primaryPartType, primaryCoefficient, secondaryCoefficient)
        else:
            messages.append({'role': 'user', 'content': "The rarity value coefficient for this item is {}.  The value for the item should be multiplied by this value to represent the increase in price for the rarity of the item.".format(
                rarityValueCoefficients[rarity])})
            messages.append({'role': 'assistant', 'content': "That sounds good.  Since rarity is both a measure of scarcity and effectiveness, rarer items should be worth more than their more commonplace counterparts."})
    else:
        messages.append({'role': 'user', 'content': "Since you haven't determined the item's rarity yet, here are a list of value coefficients by rarity:\r\n{}".format(convertEnumDictToChatTable(rarityValueCoefficients))})
        if isParted:
            messages.append({'role': 'assistant', 'content': "Great!  Once I determine the rarity, I will multiply the base value of each part by the rarity value coefficient."})
            messages = __buildPartValueContext__(
                messages, primaryPartType, primaryCoefficient, secondaryCoefficient)
        else:
            messages.append({'role': 'assistant', 'content': "Great! Once I determine the rarity, I will multiply the item's value by the rarity value coefficient."})
        
    return messages

def __buildPartPropertyContext__(messages: list[str], specialPropertyHint: dict[PartType, str] = None, physicalPropertyHint: dict[PartType, str] = None) -> list[str]:
    if specialPropertyHint is not None:
        messages.append({'role': 'user', 'content': "Here are some hints or themes for special properties based on part time for this item:\r\n{}".format(convertEnumDictToChatTable(specialPropertyHint))})
        messages.append({'role': 'assistant', 'content': "Great! I'll make sure to consider these themes and hints when determining special properties for a given part."})

    if physicalPropertyHint is not None:
        messages.append({'role': 'user', 'content': "Here are some hints or themes for physical properties based on part time for this item:\r\n{}".format(
            convertEnumDictToChatTable(physicalPropertyHint))})
        messages.append(
            {'role': 'assistant', 'content': "Great! I'll make sure to consider these themes and hints when determining physical properties for a given part."})
    
    return messages

def __buildPropertyContext__(messages: list[str], isParted: bool = False, specialPropertyHint: str | dict[PartType, str] = None, physicalPropertyHint: str | dict[PartType,str] = None) -> list[str]:
    if(isParted):
        messages = __buildPartPropertyContext__(messages, specialPropertyHint, physicalPropertyHint)
    else:
        messages.append({'role': 'user', 'content': "When building the physical propertes and special properties of this material, please try and make sure the material is reasonably distinct from any other materials you have generated."})
        messages.append({'role': 'assistant', 'content': "If you give me a history of items I have generated, I will compare the item I generate to them to make sure it is sufficientyly distinct, and change it if necessary."})
        if specialPropertyHint is not None:
            messages.append({'role': 'user', 'content': "When you build the special properties for the item, at least one of the special properties should be related to this: \"{}\".".format(specialPropertyHint)})
            messages.append({ 'role': 'assistant', 'content': "I will make sure that at least one of the special properties I generate for this item relates to \"{}\".".format(specialPropertyHint)})
        
        if physicalPropertyHint is not None:
            messages.append({'role': 'user', 'content': "When you build the physical properties for the item, at least one of the physical properties should be related to this: \"{}\".".format(physicalPropertyHint)})
            messages.append({'role': 'assistant', 'content': "I will make sure that at least one of the physical properties I generate for this item relates to \"{}\".".format(
            physicalPropertyHint)})

    return messages

def __buildPartDescriptionContext__(messages: list[str], visualDescriptionHint: dict[PartType, str] = None, descriptionHint: dict[PartType, str] = None):
    if visualDescriptionHint is not None:
        messages.append({'role': 'user', 'content': "Here are some hints or themes for visual descriptions based on part time for this item:\r\n{}".format(
            convertEnumDictToChatTable(visualDescriptionHint))})
        messages.append(
            {'role': 'assistant', 'content': "Great! I'll make sure to consider these themes and hints when determining visual descriptions for a given part."})

    if descriptionHint is not None:
        messages.append({'role': 'user', 'content': "Here are some hints or themes for descriptions based on part time for this item:\r\n{}".format(
            convertEnumDictToChatTable(descriptionHint))})
        messages.append(
            {'role': 'assistant', 'content': "Great! I'll make sure to consider these themes and hints when determining descriptions for a given part."})
    
    return messages


def __buildDescriptionContext__(messages: list[str], isParted: bool = False, visualDescriptionHint: str | dict[PartType,str] = None, descriptionHint: str | dict[PartType,str] = None) -> list[str]:
    if isParted:
        messages = __buildPartDescriptionContext__(messages, visualDescriptionHint, descriptionHint)
    else:
        messages.append({'role': 'user', 'content': "When you build the visual description for the item, the text you generate should be highly descriptive so that it can be fed to an image generation AI to build an icon for the item."})
        messages.append(
            {'role': 'assistant', 'content': "I will make sure the visual description is extremely detailed."})
        if visualDescriptionHint is not None:
            messages.append({ 'role': 'user', 'content': "When you build the visual description for the item, it should be related to this: \"{}\".".format(visualDescriptionHint)})
            messages.append({ 'role': 'assistant', 'content': "I will make sure the visual description I generate for this item relates to \"{}\".".format(visualDescriptionHint)})
        
        if visualDescriptionHint is not None:
            messages.append({'role': 'user', 'content': "When you build the description for the item, it should be related to this: \"{}\".".format(
                descriptionHint)})
            messages.append({'role': 'assistant', 'content': "I will make sure the description I generate for this item relates to \"{}\".".format(
                descriptionHint)})

    return messages


def __buildInformationContext__(messages: list[str], information: str = None) -> list[str]:
    if information is not None:
        messages.append({'role': 'user', 'content': "Here is some extra information I think you might need to know about this item: {}".format(information)})
        messages.append(
            {'role': 'assistant', 'content': "Thank you.  I make sure to consider this information when designing the item."})
    
    return messages

def __buildHistoryContext__(messages: list[str], history: list[MaterialSummary] = None) -> list[str]:
    if history is not None:
        messages.append({'role': 'user', 'content':'Here is a list of item summaries you have already provided: {}'.format(', '.join(map(lambda item: item.name + ': ' + item.description,history)))})
        messages.append({'role': 'assistant', 'content': "Okay.  I'll refrain from providing any duplicate items and I'll try and make sure each item is sufficiently destinct from any other items in the history.."})

    return messages

def buildContext(
        resourceType: ResourceType = None, 
        resourceSubtype: ResourceSubtype = None, 
        rarity: Rarity = None,
        isParted: bool = False,
        primaryPart: PartType = None,
        specialPropertyHint: str = None,
        physicalPropertyHint: str = None,
        visualDescriptionHint: str = None,
        descriptionHint: str = None,
        information: str = None,
        history: list = None) -> list[str]:
    messages = [
        {'role': 'system', 'content': 'Hello.  I need you to help me create some special materials and monsters for my Dungeons & Dragons game.' },
        ]
    
    messages = __buildTypeContext__(messages, resourceType, resourceSubtype)
    messages = __buildSchemaContext__(messages, isParted)
    messages = __buildRarityContext__(messages, rarity)
    messages = __buildValueContext__(messages, isParted, primaryPart, rarity)
    messages = __buildPropertyContext__(messages, isParted, specialPropertyHint, physicalPropertyHint)
    messages = __buildDescriptionContext__(messages, isParted, visualDescriptionHint, descriptionHint)
    messages = __buildInformationContext__(messages, information)
    messages = __buildHistoryContext__(messages, history)

    messages.append({'role': 'user', 'content': "Fill in any values for the schema which I haven't already provided using the constraints and tables I've given you.  If I haven't specified any tables or constraints, you have the freedom to decide for yourself.  The schemas provided must be followed strictly, with no omissions."})

    return messages
