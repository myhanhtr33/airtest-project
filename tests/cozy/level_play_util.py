
def is_wait_for_parent_place(objName,parentMapping,placedObjs):
    # Determine whether the parent of the given object has been placed.Object can be placed only if its parent has been placed.
    parentID=None
    for obj in parentMapping:
        for child in obj['Children']:
            if child['ID']==objName:
                parentID= obj['ID']
                break
        if parentID is not None:
            break
    if parentID is None:
        return False
    return parentID not in placedObjs
