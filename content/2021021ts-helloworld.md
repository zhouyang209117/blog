# typescript hello world
```
npm install -g typescript
npm install -g ts-node
npm install -D tslib @types/node
```
app.ts的内容为
```
let message: string = 'Hello, World!'
console.log(message)
```
这时候直接在命令行运行ts-node app.ts就能显示结果.如果要在webstorm里运行.要的安装ts-node插件.
## 参考资料
* [webstorm中直接运行ts(TypeScript)](https://www.cnblogs.com/yangfanjie/p/12036118.html) 
* [ts-node报错 return new TSError(diagnosticText, diagnosticCodes)](https://blog.csdn.net/SEKIRO_DJ/article/details/119701877) 