
using System;
using System.Threading;

using Newtonsoft.Json;
using System.Text.RegularExpressions;
using System.IO;


namespace Awesome
{
    public class MemberInfo
    {
        public String eth_address { get; set; }
        public int user_id { get; set; }
        public String first_name { get; set; }
        public String last_name { get; set; }
        public String usr_name { get; set; }
    }

    class Program
    {
        static void Main()
        {

            System.IO.DirectoryInfo di = new System.IO.DirectoryInfo(@"D:\airdrop\TelegramDataMemberInfo");
            System.IO.FileInfo[] files = di.GetFiles("*.json", System.IO.SearchOption.AllDirectories);

            using (StreamWriter sw = new StreamWriter(@"c.txt", false, System.Text.Encoding.UTF8))
            {

                //ListBox1に結果を表示する
                foreach (System.IO.FileInfo f in files)
                {
                    using (StreamReader sr = new StreamReader(f.FullName, System.Text.Encoding.UTF8))
                    {
                        String text = sr.ReadToEnd();
                        var mi = JsonConvert.DeserializeObject<MemberInfo>(text);
                        sw.WriteLine(mi.user_id + "\t" + mi.eth_address + "\t" + mi.first_name + "\t" + mi.last_name + "\t" + mi.usr_name);

                    }
                }

            }

        }



    }
}
