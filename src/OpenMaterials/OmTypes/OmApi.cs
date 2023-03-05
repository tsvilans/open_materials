using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Threading.Tasks;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace OpenMaterials
{
    public static class OmApi
    {
        public static OmMaterial GetMaterial(string supplier, string product, string qstring)
        {
            var jsonStr = File.ReadAllText(Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.Desktop),
                "materials.json"));


            var parsed = JObject.Parse(jsonStr);
            var data = parsed["data"]
                .Where(x =>
                x.Value<String>("supplier").Equals(supplier, StringComparison.InvariantCultureIgnoreCase)
                && x.Value<String>("product").Equals(product, StringComparison.InvariantCultureIgnoreCase))
                .FirstOrDefault();

            var material = new OmMaterial(JObject.FromObject(data).ToObject<Dictionary<string, object>>());
            return material;
        }
    }
}
