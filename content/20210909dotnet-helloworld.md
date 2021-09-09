# asp.net hello world
1. 按装vs2019
1. 打开vs2019,选创建新项目,在项目模版里选"ASP.NET Web应用程序(.NET Framework)",然后在"配置新项目"界面填好
   "项目名称","位置","解决方案名称","框架".假定"框架"选了.Net Framework 2.0. 后面再选空项目模版.最后点"创建"
1. 右键项目名,选"添加",再选"新建项",再选"Web窗体",填好名称,如hello.aspx,最后点添加.
1.把下面的内容粘贴到hello.aspx里
    ```
    <!-- directives -->
    <% @Page Language="C#" %>
    
    <!-- code section -->
    <script runat="server">
    
       private void convertoupper(object sender, EventArgs e)
       {
          string str = mytext.Value;
          changed_text.InnerHtml = str.ToUpper();
       }
    </script>
    
    <!-- Layout -->
    <html>
       <head> 
          <title> Change to Upper Case </title> 
       </head>
       
       <body>
          <h3> Conversion to Upper Case </h3>
          
          <form runat="server">
             <input runat="server" id="mytext" type="text" />
             <input runat="server" id="button1" type="submit" value="Enter..." OnServerClick="convertoupper"/>
             
             <hr />
             <h3> Results: </h3>
             <span runat="server" id="changed_text" />
          </form>
          
       </body>
       
    </html>
    ```
1. 点"IIS Express"能看到运行出来的界面,说明开发环境正常.下面讲如果发布到IIS让外部访问.
1. 新目录D:\csharp\tmp,在VS上点"生成",再点"发布",选"文件夹"(发布到服务器以后再讨论),在"文件夹位置"里填"D:\csharp\tmp",
   点"完成",再点"发布".VS后面类似如下输出,此时IIS需要的文件已经发布到文件夹D:\csharp\tmp里.
   ```
   已启动生成…
   1>------ 已启动生成: 项目: WebApplication2, 配置: Release Any CPU ------
   1>  WebApplication2 -> D:\csharp\sln_3\WebApplication2\bin\WebApplication2.dll
   2>------ 发布已启动: 项目: WebApplication2, 配置: Release Any CPU ------
   2>正在连接到 D:\csharp\tmp...
   2>已使用 D:\csharp\sln_3\WebApplication2\Web.Release.config 将 Web.config 转换为 obj\Release\TransformWebConfig\transformed\Web.config。
   2>正在将所有文件都复制到以下临时位置以进行打包/发布:
   2>obj\Release\Package\PackageTmp。
   2>正在发布文件夹 /...
   2>正在发布文件夹 bin...
   2>Web 应用已成功发布 file:///D:/csharp/tmp
   2>
   ========== 生成: 成功 1 个，失败 0 个，最新 0 个，跳过 0 个 ==========
   ========== 发布: 成功 1 个，失败 0 个，跳过 0 个 ==========
   ```         
1. 打开"IIS管理器",右键"网站",选"添加网站","网站名称"根据需要填,如hello1."物理路径"填D:\csharp\tmp.端口根据需要填,
  不要和已经有的重复即可,如81.最后点确定.
1. 因为建项目时选的.Net Framework 2.0,所以在"应用程序池"里把hello1的.Net CLR版本改成v2.0. 在"网站管理"里面重新启动.
1. 在浏览器输入localhost:81/hello.aspx能看到界面.
1. 参考资料
* [vs2019官方网站](https://visualstudio.microsoft.com/zh-hans/vs/) 
* [ASP.NET - First Example](https://www.tutorialspoint.com/asp.net/asp.net_first_example.htm) 
* [asp.net开发web工程网站项目发布IIS服务器上运行？从开发环境到生产环境
](https://www.bilibili.com/video/BV1Ke411473K) 