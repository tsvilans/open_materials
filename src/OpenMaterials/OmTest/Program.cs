using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using System.Net.Http;

namespace OmTest
{
    internal class Program
    {
        private static readonly HttpClient client = new HttpClient();

        static void Main(string[] args)
        {
            GetSomething("https://opensource-construction.github.io/KBOB/data/Abfalltrennsystem.json");

            System.Console.ReadLine();
        }

        static async void GetSomething(string url)
        {
            var responseString = await client.GetStringAsync(url);

            System.Console.WriteLine(responseString.ToString());
        }
    }
}
