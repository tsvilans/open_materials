using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Http;
using System.Net.Http.Headers;

namespace OpenMaterials
{
    public static class WebClient
    {
        private static readonly HttpClient client = new HttpClient();
        internal static string Token = "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";

        public static async Task<string> GetSomething(string url)
        {
            var responseString = await client.GetStringAsync(url);

            return responseString;
        }

        public static string Wrapper(string url)
        {
            return GetSomething(url).ToString();
        }

        public static string Get(string url)
        {
            using (var client = new HttpClient())
            {
                client.BaseAddress = new Uri("https://opensource-construction.github.io/data/");
                client.DefaultRequestHeaders.Add("X-Version", "1");
                client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", Token);
                client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/vnd.github+json"));

                var response = client.GetAsync(url).GetAwaiter().GetResult();
            if (response.IsSuccessStatusCode)
            {
                var responseContent = response.Content;
                return responseContent.ReadAsStringAsync().GetAwaiter().GetResult();
            }
            else return response.Content.ReadAsStringAsync().GetAwaiter().GetResult();
            }
        }
    }
}
