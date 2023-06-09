from enum import Enum, StrEnum

class Rarity(StrEnum):
    COMMON = 'common'
    UNCOMMON = 'uncommon'
    RARE = 'rare'
    VERYRARE = 'very-rare'
    LEGENDARY = 'legendary'

class ResourceType(StrEnum):
    ANIMAL = 'animal'
    MINERAL = 'vegetable'
    VEGETABLE = 'mineral'

class ResourceSubtype(StrEnum):
    #Animal Subtypes
    ABERRATION = 'aberation'
    BEAST = 'beast'
    OUTSIDER = 'outsider'
    CELESTIAL = 'celestial'
    CONSTRUCT = 'construct'
    DRAGON = 'dragon'
    ELEMENTAL = 'elemental'
    FEY = 'fey'
    FIEND = 'fiend'
    GIANT = 'giant'
    HUMANOID = 'humanoid'
    MONSTROSITY = 'monstrosity'
    OOZE = 'ooze'
    PLANT = 'plant'
    UNDEAD = 'undead'

    #Mineral Subtypes
    METAL = 'metal'
    STONE = 'stone'
    CRYSTAL = 'crystal'

    #Plant Subtypes
    FUNGUS = 'fungus'
    HERB = 'herb'
    SHRUB = 'shrub'
    TREE = 'tree'
    VINE = 'vine'
    

class PartType(StrEnum):
    ANTLER = 'antler'
    ARM = 'arm'
    ASHES = 'ashes'
    BARK = 'bark'
    BEAK = 'beak'
    BERRY = 'berry'
    BLOOD = 'blood'
    BONE = 'bone'
    BRAIN = 'brain'
    BULB = 'bulb'
    CAP = 'cap'
    CHITIN = 'chitin'
    CLAW = 'claw'
    CORE = 'core'
    DUST = 'dust'
    EAR = 'ear'
    ECTOPLASM = 'ectoplasm'
    EYE = 'eye'
    FANG = 'fang'
    FAT = 'fat'
    FEATHER = 'feather'
    FIN = 'fin'
    FINGER = 'finger'
    FLOWER = 'flower'
    FOOT = 'foot'
    FRUIT = 'fruit'
    FUR = 'fur'
    HAIR = 'hair'
    HEART = 'heart'
    HIDE = 'hide'
    HOOF = 'hoof'
    HORN = 'horn'
    ICHOR = 'ichor'
    JAW = 'jaw'
    LEAF = 'leaf'
    LEG = 'leg'
    LIVER = 'liver'
    LOG = 'log'
    MANDIBLE = 'mandible'
    MEAT = 'meat'
    MUCUS = 'mucus'
    NUT = 'nut'
    PELT = 'pelt'
    PETAL = 'petal'
    PINCER = 'pincer'
    PLATE = 'plate'
    POLLEN = 'pollen'
    QUILL = 'quill'
    ROOT = 'root'
    SALIVA = 'saliva'
    SAP = 'sap'
    SCALE = 'scale'
    SEED = 'seed'
    SHELL = 'shell'
    SINEW = 'sinew'
    SKIN = 'skin'
    SKULL = 'skull'
    SPLITLOG = 'splitlog'
    SPORES = 'spores'
    STALK = 'stalk'
    STEM = 'stem'
    STINGER = 'stinger'
    TAIL = 'tail'
    TALON = 'talon'
    TENTACLE = 'tentacle'
    TOE = 'toe'
    TONGUE = 'tongue'
    TOOTH = 'tooth'
    TUBER = 'tuber'
    TUSK = 'tusk'
    VENOM = 'venom'
    VINE = 'vine'
    WING = 'wing'