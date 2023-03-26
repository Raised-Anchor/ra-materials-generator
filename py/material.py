from materialsEnums import Rarity, ResourceType, ResourceSubtype, PartType
import pyjson5 as json
from varname import nameof
import enum

def getEnumName(value: int | str, e: enum.IntEnum):
    if isinstance(value, int):
        return e(value).name
    elif isinstance(value, str):
        value = value.lower()
        for item in (e):
            if item.name.lower() == value: return item.name
    
    return None


def __getValue__(property, propertyName, json, e = None):
    v = property if json is None or propertyName not in json else json[propertyName]
    if e is not None and issubclass(e, enum.IntEnum) and isinstance(v, int):
        return e(v)
        
    return v


class Material:
    def __init__(self, jsonData: str = None, jsonObject = None, name: str = None, rarity: Rarity = None, value: float = None, description: str = None, resourceType: ResourceType = None, resourceSubtype: ResourceSubtype = None, visualDescription: str = None, specialProperties: list[str] = None, physicalProperties: list[str] = None, density: float = None, weight: float = None, uses: list[str] = None):
        j = jsonObject
        if jsonData is not None:        
            j = json.loads(jsonData)
        self.name = __getValue__(name, nameof(name), j)
        self.rarity = __getValue__(rarity, nameof(rarity), j, Rarity)
        self.value = __getValue__(value, nameof(value), j)
        self.description = __getValue__(
            description, nameof(description), j)
        self.resourceType = __getValue__(
            resourceType, nameof(resourceType), j, ResourceType)
        self.resourceSubtype = __getValue__(
            resourceSubtype, nameof(resourceSubtype), j, ResourceSubtype)
        self.visualDescription = __getValue__(
            visualDescription, nameof(visualDescription), j)
        self.specialProperties = __getValue__(
            specialProperties, nameof(specialProperties), j)
        self.physicalProperties = __getValue__(
            physicalProperties, nameof(physicalProperties), j)
        self.uses = __getValue__(uses, nameof(uses), j)
        self.density = __getValue__(density, nameof(density), j)
        self.weight = __getValue__(weight, nameof(weight), j)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

materialSchema = '''{ 
    "name": string // The name of the material
    "rarity": number // The integer value from the rarity enum
    "value": number // The gold piece value of the material. Minimum value is 0.01
    "description": string // A general description of the material
    "resourceType": string // The type of resource
    "resourceSubtype": string // The subtype of resource
    "visualDescription": string // A detailed visual description of the material that can be fed to an image generation AI to create an icon for the material.
    "specialProperties": string[] // An array of special properties the material possesses.  Special properties are magical or supernatural, such as silver's ability to damage lycanthropes.
    "physicalProperties": string[] // An array of physical properties the material possesses.  Physical properties are mundane in nature, such as an object's smell, texture, hardness, or taste.
    "uses": string[] // An array of typical uses for the item.
    "density": number // The density of the material in grams per cubic centimeter.
    "weight": number // The weight of one unit of material.  One unit is the smallest amount needed to fulfill one of the uses.  Weight is measured in pounds.  Any weight less than 0.01 is 0.
}'''


class MaterialPart:
    def __init__(self, jsonData: str = None, jsonObject=None, value: float = None, description: str = None, resourceSubtype: ResourceSubtype = None, partType: PartType = None, visualDescription: str = None, specialProperties: list[str] = None, physicalProperties: list[str] = None, density: float = None, weight: float = None, uses: list[str] = None):
        j = jsonObject
        if jsonData is not None:
            j = json.loads(jsonData)
        self.value = __getValue__(value, nameof(value), j)
        self.description = __getValue__(
            description, nameof(description), j)
        self.resourceSubtype = __getValue__(
            resourceSubtype, nameof(resourceSubtype), j, ResourceSubtype)
        self.visualDescription = __getValue__(
            visualDescription, nameof(visualDescription), j)
        self.specialProperties = __getValue__(
            specialProperties, nameof(specialProperties), j)
        self.physicalProperties = __getValue__(
            physicalProperties, nameof(physicalProperties), j)
        self.partType = __getValue__(partType, nameof(partType), j, PartType)
        self.uses = __getValue__(uses, nameof(uses), j)
        self.density = __getValue__(density, nameof(density), j)
        self.weight = __getValue__(weight, nameof(weight), j)
        self.isParted = False


materialPartSchema = '''{ 
    "value": number // The gold piece value of the material. Minimum value is 0.01
    "description": string // A general description of the material
    "resourceSubtype": string // The subtype of resource
    "visualDescription": string // A detailed visual description of the material that can be fed to an image generation AI to create an icon for the material.
    "specialProperties": string[] // An array of special properties the material possesses.  Special properties are magical or supernatural, such as silver's ability to damage lycanthropes.
    "physicalProperties": string[] // An array of physical properties the material possesses.  Physical properties are mundane in nature, such as an object's smell, texture, hardness, or taste.
    "uses": string[] // An array of typical uses for the item.
    "density": number // The density of the material in grams per cubic centimeter.
    "weight": number // The weight of one unit of material.  One unit is the smallest amount needed to fulfill one of the uses.  Weight is measured in pounds.  Any weight less than 0.01 is 0.
    "partType": number // The integer value of the PartType enum.
}'''


def __getParts__(jsonKey: str, jsonData=None, parts: list[MaterialPart] = None) -> list[MaterialPart]:
    if parts is not None: return parts

    parts = []
    if jsonData is not None and jsonKey in jsonData:
        data = jsonData[jsonKey]
        if isinstance(data, list):
            for part in data:
                parts.append(MaterialPart(jsonData = str(part)))
        else:
            parts.append(MaterialPart(jsonData = str(data)))
    
    return parts

class PartedMaterial:
    def __init__(self, jsonData: str = None, jsonObject=None, name: str = None, rarity: Rarity = None, description: str = None, resourceType: ResourceType = None, resourceSubtype: ResourceSubtype = None, parts: list[MaterialPart] = None):
        j = jsonObject
        if jsonData is not None:
            j = json.loads(jsonData)
        self.name = __getValue__(name, nameof(name), j)
        self.rarity = __getValue__(rarity, nameof(rarity), j, Rarity)
        self.description = __getValue__(
            description, nameof(description), j)
        self.resourceType = __getValue__(
            resourceType, nameof(resourceType), j, ResourceType)
        self.resourceSubtype = __getValue__(
            resourceSubtype, nameof(resourceSubtype), j, ResourceSubtype)
        self.parts = __getParts__('parts', j)
        self.isParted = True

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


partedMaterialSchema = '''{ 
    "name": string // The name of the material, animal, or plant
    "rarity": number // The integer value from the rarity enum
    "description": string // A general description of the material, animal, or plant
    "resourceType": string // The type of resource
    "resourceSubtype": string // The subtype of resource
    "parts": MaterialPart[] // The parts of the material, animal, or plant.
}'''


class MaterialSummary:
    def __init__(self, material: Material | PartedMaterial = None, jsonData: str = None, jsonObject=None):
        j = jsonObject
        if jsonData is not None:
            j = json.loads(jsonData)
        
        self.name = None
        if j is not None and 'name' in j:
            self.name = j['name']
        elif material is not None:
            self.name = material.name
            
        self.description = None
        if j is not None and 'description' in j:
            self.description = j['description']
        elif material is not None:
            self.description = material.description
