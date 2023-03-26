from material import Material, MaterialPart, PartedMaterial, PartType, ResourceSubtype, ResourceType, Rarity

def buildConstraint( 
                resourceType: ResourceType = None, 
                resourceSubtype: ResourceSubtype = None, 
                rarity: Rarity = None, 
                valueMin: float = None, 
                valueMax: float = None,
                specialPropertyHint: str = None,
                physicalPropertyHint: str = None):
    constraintClauses = []
    if resourceType is not None:
        constraintClauses.append('has a ResourceType of {}'.format(resourceType.name))

    if resourceSubtype is not None:
        constraintClauses.append('has a Resource Subtype of {}'.format(resourceSubtype.name))

    if rarity is not None:
        constraintClauses.append('has a rarity of {}'.format(rarity.name))

    if valueMin is not None:
        if valueMax is not None:
            constraintClauses.append('has a value between {} and {} (or equal to either)'.format(valueMin, valueMax))
        else:
            constraintClauses.append('has a value greater than or equal to {}'.format(valueMin))
    elif valueMax is not None:
        constraintClauses.append('has a value less than {}'.format(valueMax))

    if specialPropertyHint is not None:
        constraintClauses.append('has a special property related to "{}"'.format(specialPropertyHint))
        
    if physicalPropertyHint is not None:
        constraintClauses.append('has physicalProperties related to "{}"'.format(physicalPropertyHint))

    if(len(constraintClauses) > 0):
        return "Please make sure this material meets the following criteria: " + ', '.join(constraintClauses) + '.'
    
    return None
