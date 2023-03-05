import ifcopenshell
import ifcopenshell.geom
try:
    from .ifc import get_product_materials
except:
    from ifc import get_product_materials

import numpy as np
import os
import rhino3dm

settings = ifcopenshell.geom.settings()
#settings.set(settings.USE_BREP_DATA,True)
#settings.set(settings.SEW_SHELLS,True)
#settings.set(settings.USE_PYTHON_OPENCASCADE, True)
#settings.set(settings.USE_WORLD_COORDS,True)

def cross(v0, v1):
    return (
        v0[1] * v1[2] - v0[2] * v1[1], 
        v0[2] * v1[0] - v0[0] * v1[2], 
        v0[0] * v1[1] - v0[1] * v1[0])

def placement_to_plane(placement, scale):
    coords = placement.RelativePlacement.Location.Coordinates
    xx = placement.RelativePlacement.P[0].DirectionRatios
    yy = placement.RelativePlacement.P[1].DirectionRatios

    planes = []

    if placement.PlacementRelTo is not None:
        planes.extend(placement_to_plane(placement.PlacementRelTo, scale))

    #print(placement.RelativePlacement.P[0].DirectionRatios)
    #print(placement.RelativePlacement.P[1].DirectionRatios)
    #print(placement.RelativePlacement.P[2].DirectionRatios)
    #print(f"pos: {coords}")
    #print(f"    xx: {xx}")
    #print(f"    yy: {yy}")

    xx = (xx[0], -xx[1], xx[2])
    yy = (-yy[0], yy[1], yy[2])

    #xx = (1,0,0)
    #yy = (0,1,0)

    origin = rhino3dm.Point3d(*coords) * scale
    xaxis = rhino3dm.Vector3d(*xx)
    yaxis = rhino3dm.Vector3d(*yy)


    plane = rhino3dm.Plane(origin, xaxis, yaxis)

    return [plane]

def plane_to_transform(plane):
        xform = rhino3dm.Transform(1)

        xform.M00 = plane.XAxis.X
        xform.M01 = plane.XAxis.Y
        xform.M02 = plane.XAxis.Z
        xform.M03 = plane.Origin.X

        xform.M10 = plane.YAxis.X
        xform.M11 = plane.YAxis.Y
        xform.M12 = plane.YAxis.Z
        xform.M13 = plane.Origin.Y

        xform.M20 = plane.ZAxis.X
        xform.M21 = plane.ZAxis.Y
        xform.M22 = plane.ZAxis.Z
        xform.M23 = plane.Origin.Z

        return xform

def element_to_rhino(rfile, element, data, scale=1000.0, scale_position=1000.0):
    shape = ifcopenshell.geom.create_shape(settings, element)
    if shape is None:
        return None

    planes = placement_to_plane(element.ObjectPlacement, scale_position)
    #print(f"Got {len(planes)} planes.")
    #print(dir(element.ObjectPlacement))
    #print(element.ObjectPlacement.PlacementRelTo)

    xforms = [plane_to_transform(p) for p in planes]

    #print(xform.ToFloatArray(True))

    faces = shape.geometry.faces # Indices of vertices per triangle face e.g. [f1v1, f1v2, f1v3, f2v1, f2v2, f2v3, ...]
    verts = shape.geometry.verts # X Y Z of vertices in flattened list e.g. [v1x, v1y, v1z, v2x, v2y, v2z, ...]
    materials = shape.geometry.materials # Material names and colour style information that are relevant to this shape
    material_ids = shape.geometry.material_ids # Indices of material applied per triangle face e.g. [f1m, f2m, ...]

    # Since the lists are flattened, you may prefer to group them per face like so depending on your geometry kernel
    grouped_verts = [[verts[i], verts[i + 1], verts[i + 2], 1] for i in range(0, len(verts), 3)]
    grouped_faces = [[faces[i], faces[i + 1], faces[i + 2]] for i in range(0, len(faces), 3)]

    mesh = rhino3dm.Mesh()

    for v in grouped_verts:
        mesh.Vertices.Add(v[0] * scale, v[1] * scale, v[2] * scale)

    for f in grouped_faces:
        mesh.Faces.AddFace(f[0], f[1], f[2])

    for xform in xforms:
        mesh.Transform(xform)

    attr = rhino3dm.ObjectAttributes()

    if data is not None:
        attr.SetUserString("open_materials", data)


    rfile.Objects.AddMesh(mesh, attr)

def elements_to_rhino(filepath, ifcelements, json, scale=1000.0, scale_position=1000.0):
    rfile = rhino3dm.File3dm()
    for element in ifcelements:
        element_to_rhino(element, )

    rfile.Write(filepath)
    print(f"Wrote 3dm to '{filepath}'")

if __name__=="__main__":
    ifc = ifcopenshell.open(r"model.ifc")
    storeys = ifc.by_type("IfcBuildingStorey")
    elements = [e for e in ifcopenshell.util.element.get_decomposition(storeys[0])]
    filepath = os.path.abspath("../RhinoTest2.3dm")

    rfile = rhino3dm.File3dm()
    for element in elements:
        element_to_rhino(rfile, element, "null", 1000, 1)
    rfile.Write(filepath)
