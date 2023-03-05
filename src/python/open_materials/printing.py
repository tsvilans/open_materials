import ifcopenshell

def print_elements(ifc):

    element_types = ["IfcWall", "IfcBeam", "IfcSlab", "IfcColumn"]

    for etype in element_types:
        elements = ifc.by_type(etype)
        print(f"{etype} ({len(walls)})")
        for element in elements:
            print(f"    {element.Name}")

def print_materials(ifc):

    materials = ifc.by_type("IfcMaterial")
    material_db = {}

    print()
    print("Materials: ")
    for material in materials:
        tokens = material.Name.split(',')
        category = tokens[0]
        product = "<generic>"
        if len(tokens) > 1:
            product = tokens[1]

        if category not in material_db.keys():
            material_db[category] = []
        material_db[category].append(product)

    for key in material_db.keys():
        print(f"    {key}")
        for product in material_db[key]:
            print(f"        {product}")

def print_storey_elements(ifcfile, storey):
    '''
    Get all elements associated with a particular storey
    '''
    elements = [e for e in ifcopenshell.util.element.get_decomposition(storey) if e.get_info()["type"] in element_types]
    print(f"There are {len(elements)} elements located on storey {storey.Name}, they are:")
    for element in elements:
        print(element.Name)