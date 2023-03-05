def get_product_materials(ifc, product):
    '''
    Get all materials associated with a product.
    '''

    #Data.load(ifc, product.id())
    #print(Data.products[product.id()])
    #return

    if product.HasAssociations:
        for i in product.HasAssociations:
            if i.is_a('IfcRelAssociatesMaterial'):
                #print(f"Material is a {i.RelatingMaterial}")
                if i.RelatingMaterial.is_a("IfcMaterialConstituentSet"):
                    return [(m.Material, m.Fraction) for m in i.RelatingMaterial.MaterialConstituents]
                elif i.RelatingMaterial.is_a('IfcMaterial'):
                    return [i.RelatingMaterial]
                elif i.RelatingMaterial.is_a('IfcMaterialList'):
                    return i.RelatingMaterial.Materials
                elif i.RelatingMaterial.is_a('IfcMaterialLayerSetUsage'):
                    return [mat for mat in i.RelatingMaterial.ForLayerSet.MaterialLayers]
                return None