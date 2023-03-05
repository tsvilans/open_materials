import ifcopenshell
import ifcopenshell.geom
from ifcopenshell.util.selector import Selector

import open_materials
from open_materials.printing import print_elements, print_materials
from open_materials.rhino import element_to_rhino
from open_materials.ifc import get_product_materials
from open_materials.api import make_index, get_material_data
from open_materials.api import index as material_map

import json
import re

settings = ifcopenshell.geom.settings()
settings.set(settings.USE_BREP_DATA,True)
settings.set(settings.SEW_SHELLS,True)
settings.set(settings.USE_PYTHON_OPENCASCADE, True)
#settings.set(settings.USE_WORLD_COORDS,True)

selector = Selector()

def query_database(supplier, product):
    
    res = None
    with open(r"C:\Users\tsvi\Desktop\materials.json", "r") as file:
        data = json.load(file)["data"]
        products = [p for p in data if ("supplier" in p.keys()) and (p["supplier"] == supplier) and ("product" in p.keys()) and (p["product"] == product)]
        if len(products) > 0:
            res = products[0]
    return res


def apply_material_properties_deprec(ifcfile, element, material):
    '''
    Apply material properties from database as a property set
    '''
    element_material = (ifcopenshell.util.element.get_material(element))
    if element_material is None:
        return None
        existing = selector.parse(ifcfile, f".IfcMaterial[Name *= \"{material['supplier']}::{material['product']}\"]")
        if len(existing) < 1:
            element_material = ifcfile.createIfcMaterial(f"{material['supplier']}::{material['product']}")
        else:
            element_material = existing[0]

    existing = [mat for mat in selector.parse(ifcfile, f".IfcMaterialProperties[Material *= \"{element_material.Name}\"]") if mat.Name == "OpenMaterials"]
    if len(existing) > 0:
        return None

    #print(element_material)

    property_values_material  = []
    for key in material.keys():
        property_values_material.append(ifcfile.createIfcPropertySingleValue(key, key, ifcfile.create_entity("IfcLabel", str(material[key])), None))
    
    #property_set = ifcfile.createIfcPropertySet(create_guid(), owner_history, "Pset_WallCommon", None, property_values_material )


    matprops = ifcfile.createIfcMaterialProperties("OpenMaterials", 'OpenMaterials property set', property_values_material, element_material)
    #print(matprops.get_info())
    ifcfile.add(matprops)

    return matprops

def apply_material_properties(ifcfile, ifc_material, om_material):
    property_values_material  = []
    for key in om_material.keys():
        property_values_material.append(ifcfile.createIfcPropertySingleValue(key, key, ifcfile.create_entity("IfcLabel", str(om_material[key])), None))

    matprops = ifcfile.createIfcMaterialProperties("OpenMaterials", 'OpenMaterials property set', property_values_material, ifc_material)
    ifcfile.add(matprops)

def XXXget_product_materials(product):
    '''
    Get all materials associated with a product.
    '''
    if product.HasAssociations:
        for i in product.HasAssociations:
            if i.is_a('IfcRelAssociatesMaterial'):
                if i.RelatingMaterial.is_a("IfcMaterialConstituentSet"):
                    return [(m.Material, m.Fraction) for m in i.RelatingMaterial.MaterialConstituents]
                return i.RelatingMaterial

def get_element_volume(element):

    shape = ifcopenshell.geom.create_shape(settings, element)
    print(shape.geometry)
    print(dir(shape.geometry))
    pass

def main():

    make_index()

    element_types = ["IfcWall", "IfcBeam", "IfcSlab", "IfcColumn"]
    material_dict = {}

    # Open IFC file
    ifc = ifcopenshell.open(r"2104_220426_12_55__IFC Export TIMBER_OS Komplett.ifc")
    #ifc = ifcopenshell.open(r"C:\Users\tsvi\OneDrive - Det Kongelige Akademi\Documents\test3.ifc")

    mat_properties = []
    # Get all materials
    materials = ifc.by_type("IfcMaterial")

    for material in materials:
        # Wrangle first material name for demo
        category = material.Name.split(',')[0]
        if category not in material_map:
            continue

        supplier = "Tom"
        product = material_map[category]
        om_data = query_database(supplier, product)

        matprops = apply_material_properties(ifc, material, om_data)
        if matprops is not None:
            material_dict[material.Name] = om_data
            mat_properties.append(matprops)

    '''
    Create new IFC and write material properties
    '''
    new_ifc = ifcopenshell.file()

    #for matprops in mat_properties:
    #    new_ifc.add(matprops)

    for material in materials:
        components = ifc.get_inverse(material)
        for c in components:
            #print(c)
            new_ifc.add(c)
        new_ifc.add(material)
        

    new_ifc.write("OmTest01.ifc")

    '''
    wall = ifc.by_type("IfcWall")[0]

    #get_element_volume(wall)
    pset = ifcopenshell.util.element.get_psets(wall)

    wall_material = get_product_materials(wall)
    if wall_material:
        print(f"The wall has a material {wall_material}")
    '''

    storeys = ifc.by_type("IfcBuildingStorey")
    elements = [e for e in ifcopenshell.util.element.get_decomposition(storeys[3]) if e.get_info()["type"] in element_types]

    import rhino3dm

    filepath = "OmTest06.3dm"
    rfile = rhino3dm.File3dm()

    counter = 0
    for element in elements:
        
        jdata = {}
        materials = get_product_materials(ifc, element)
        mat_name = "null"
        if len(materials) > 0:
            try:
                print(materials)
                if isinstance(materials[0], tuple):
                    mat_name = materials[0][0].Name
                else:
                    mat_name = materials[0].Name

                jdata = get_material_data(re.split(r',|\s+', mat_name)[0])

                #if mat_name in material_dict.keys():
                #    jdata = material_dict[mat_name]
            except:
                print(f"ERROR: {materials[0]}")
                if len(materials[0]) > 1:
                    print(materials[0][0])
                    mat_name = materials[0][0].Name

                    jdata = get_material_data(re.split(r',|\s+', mat_name)[0])

                    #if mat_name in material_dict.keys():
                    #    jdata = material_dict[mat_name]
        jdata["material_name"] = mat_name
        element_to_rhino(rfile, element, str(jdata), 1000, 1000)

        if counter > 2000: 
            break
        counter += 1

    rfile.Write(filepath)


if __name__=="__main__":
    #print(query_database("Tom", "Glass"))
    main()