using System;
using System.IO;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text.RegularExpressions;
using System.Web.Script.Serialization;
using System.Windows.Forms;
class Launcher {
 [STAThread] static void Main(string[] args) {
  try {
   if(args.Length != 1) throw new Exception("Expected one project link.");
   Match m=Regex.Match(args[0], @"\Atechart-ue://(lounge|materials|debris|niagara|week9)/?\z");
   if(!m.Success) throw new Exception("Unknown project link.");
   string dir=AppDomain.CurrentDomain.BaseDirectory;
   var json=new JavaScriptSerializer();
   var config=json.Deserialize<Dictionary<string,object>>(File.ReadAllText(Path.Combine(dir,"projects.json")));
   var projects=(Dictionary<string,object>)config["projects"];
   string id=m.Groups[1].Value;
   if(!projects.ContainsKey(id)) throw new Exception("Project is not configured. Re-run setup.");
   string project=(string)projects[id], editor=(string)config["editor"];
   if(!File.Exists(project) || !project.EndsWith(".uproject",StringComparison.OrdinalIgnoreCase) || !File.Exists(editor)) throw new Exception("Configured project/editor has moved. Re-run setup.");
   var start=new ProcessStartInfo(editor,"\""+project+"\""); start.UseShellExecute=false;
   var process=Process.Start(start);
   File.AppendAllText(Path.Combine(dir,"launch-log.jsonl"),json.Serialize(new {time=DateTimeOffset.Now.ToString("o"),project_id=id,project=project,process_id=process.Id})+Environment.NewLine);
  } catch(Exception e) { MessageBox.Show(e.Message,"Technical Art launcher",MessageBoxButtons.OK,MessageBoxIcon.Error); }
 }
}
