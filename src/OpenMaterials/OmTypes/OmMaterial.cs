using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace OpenMaterials
{
    public class OmMaterial
    {
        Dictionary<string, object> m_properties = new Dictionary<string, object>();

        public object this[string index]
        {
            get
            {
                if (m_properties.ContainsKey(index))
                    return m_properties[index];
                return null;
            }
            set
            {
                m_properties[index] = value;
            }
        }

        public OmMaterial(Dictionary<string, object> properties=null)
        {
            if (properties != null)
                m_properties = properties;
        }

        public static OmMaterial Parse(string data)
        {
            var mat = new OmMaterial();
            mat.m_properties = JsonConvert.DeserializeObject<Dictionary<string, object>>(data);
            return mat;
        }
    }
}
