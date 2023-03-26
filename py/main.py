from gpt4 import getChatResponse
from material import getEnumName, MaterialSummary, Material, MaterialPart, PartedMaterial, PartType
from materialsGenerator import convertEnumNamesToList, ResourceSubtype, ResourceType, Rarity, materialsLib, partedMaterialSchema, materialSchema, materialPartSchema, resourceTypeDescriptions, partTypeValueCoefficients, partTypeBaseValues, primaryPartCoefficient,  secondaryPartCoefficient, tradespersonIncome, laypersonIncome, generateMaterial, buildContext
import time
import pyjson5 as json

waitTimeInSeconds = 180
resourceTypeToGenerate = ResourceType.MINERAL
resourceSubtypeToGenerate = ResourceSubtype.METAL



history: list[MaterialSummary] = []
def loadHistory(resourceType: ResourceType = None, resourceSubtype: ResourceSubtype = None):
    types: list[str] = convertEnumNamesToList(ResourceType) if resourceType is None else [resourceType.name]
    sectionNames: list[str] = convertEnumNamesToList(ResourceSubtype) if resourceSubtype is None else [resourceSubtype.name]

    for type in types:
        with open(type + 's.json', 'r+') as file:
            stringData = file.read()
            parsedData = None if stringData is None or stringData == '' else json.loads(stringData)
            for sectionName in sectionNames:
                if sectionName in parsedData:
                    for item in parsedData[sectionName]:
                        history.append(MaterialSummary(jsonObject = item))


def updateHistory(material: Material | PartedMaterial):
    history.append(MaterialSummary(material = material))
    print(material.toJSON())
    
    fileName: str = getEnumName(material.resourceType, ResourceType) + 's.json'
    category: str = getEnumName(material.resourceSubtype, ResourceSubtype)
    parsedData = {}

    with open(fileName, 'r+') as file:
        stringData = file.read()
        if stringData is not None and stringData != '':
            parsedData = json.loads(stringData)
                
        if category not in parsedData:
            parsedData[category] = []
        
        parsedData[category].append(material)
        file.seek(0)
        dump = json.dumps(parsedData, indent=4)
        file.write(dump)
        file.truncate()

loadHistory(resourceType=resourceTypeToGenerate, resourceSubtype=resourceSubtypeToGenerate)
print('Initial History: ', len(history))
while len(history) < 1000:
    context = ''
    material = None
    try:
        context = buildContext(resourceType=resourceTypeToGenerate, resourceSubtype=resourceSubtypeToGenerate, history=history)
    except Exception as ex:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
              ' -- Context Error: ', type(ex).__name__, ': ', ex)
        continue
        
    try:
        material = generateMaterial(context)
    except Exception as ex:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
              ' -- Generation Error: ', type(ex).__name__, ': ', ex)
        time.sleep(waitTimeInSeconds)
        continue
            
    if material is not None:
        try:
            updateHistory(material)
        except Exception as ex:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                  ' -- Update Error -- ', type(ex).__name__,': ' ,ex)
            time.sleep(waitTimeInSeconds)
            continue
    
    time.sleep(waitTimeInSeconds)
