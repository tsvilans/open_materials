/*
 * Open Materials
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * 
 */

using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using System.Timers;
using GH_IO.Serialization;
using Grasshopper.GUI;
using Grasshopper.GUI.Canvas;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Attributes;
using Grasshopper.Kernel.Data;
using Grasshopper.Kernel.Types;
using Grasshopper.Kernel.Parameters;

using Rhino.Geometry;

namespace OpenMaterials.GH.Components
{

    public class GetThermalProperties : GH_Component
    {
        public GetThermalProperties()
          : base("ThermProperties", "TProp",
              "Get the thermal properties of a material.",
              OpenMaterials.GH.GH_Api.ComponentCategory, "Basic")
        {
        }

        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddTextParameter("Supplier", "S", "Name of supplier.", GH_ParamAccess.item);
            pManager.AddTextParameter("Product", "P", "Name of product.", GH_ParamAccess.item);
            pManager.AddTextParameter("Filters", "F", "Filters for query.", GH_ParamAccess.item);

            pManager[2].Optional = true;
        }

        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.AddNumberParameter("Thermal conductivity", "TC", "Thermal conductivity of material.", GH_ParamAccess.item);
            pManager.AddNumberParameter("Specific heat", "SH", "Specific heat capacity of material.", GH_ParamAccess.item);
        }

        protected Param_GenericObject CreateParameter(string name)
        {
            var param = new Param_GenericObject();
            param.Name = name;
            param.NickName = name;
            param.Description = $"Material property {name}";
            param.Optional = true;

            return param;
        }

        protected override void SolveInstance(IGH_DataAccess DA)
        {
            string supplier = "", product = "", qstring = "";
            DA.GetData("Supplier", ref supplier);
            DA.GetData("Product", ref product);
            DA.GetData("Filters", ref qstring);

            var material = OmApi.GetMaterial(supplier, product, qstring);

            /*
            if (Params.Output.Count > 0)
                for (int i = Params.Output.Count - 1; i >= 0; i--)
                    Params.UnregisterOutputParameter(Params.Output[i]);

            var param = CreateParameter("Density");
            Params.RegisterOutputParam(param);

            DA.SetData(param.Name, material["density"]);
            */

            DA.SetData("Thermal conductivity", material["thermal_conductivity"]);
            DA.SetData("Specific heat", material["specific_heat"]);

        }

        protected override System.Drawing.Bitmap Icon
        {
            get
            {
                //return Properties.Resources.GridDisplay_01;
                return null;
            }
        }

        public override Guid ComponentGuid
        {
            get { return new Guid("7ccf8128-8d94-44e0-8da3-107d6958eac3"); }
        }
    }


}
