
# MCLA database

该仓库保存了结构化后的Minecraft错误及其解决方案

### Schema

#### `version.json`
- 保存当前数据库的版本
- 例子:
    ```js
    {
    	"major": 0,  // 代表当前结构规范版本, 0 总是代表 dev. 当版本不相符时客户端需报错并要求更新
    	"minor": 0,  // 当 errors/solutions 修改后自增. 客户端需要尝试重新获取全部数据文件以确保使用的是最新版本
    	"patch": 37, // 与 errorIncId/solutionIncId 同时自增. 客户端仅需要比较新旧 IncId 以确认需要获取的文件列表
    	"errorIncId": 22,
    	"solutionIncId": 15
    }
    ```

#### `errors/{id}.json`
- 保存错误匹配信息
- 例子:
    ```js
    {
    	// 异常类, 可用 *. 前缀匹配任意包名
    	"error": "net.minecraft.util.ResourceLocationException",
    	// 异常信息
    	"message": "Non [a-z0-9_.-] character in namespace of location: .DS_Store",
    	// 解决方案ID列表
    	"solutions": [
    		1
    	],
        // [可选] 附属脚本ID
        // 用于分析复杂错误(如: fabric mod缺失错误), 以及提供更多附加信息(如: 提供mod下载链接)
        // "scripts": 1
    }
    ```

#### `solutions/{id}.json`
- 保存解决方案
- 例子:
    ```js
    {
    	// 解决方案标签
    	"tags": [
    		"macos"
    	],
    	// 导致此问题的原因的简短描述
    	"description": "macOS 下存在 .DS_Store 文件导致报错",
    	// 链接
    	"link_to": "/client/system.html#macos-下存在-ds-store-文件导致报错"
    }
    ````
<!-- TODO:
#### `scripts/{id}.mjs`
- 提供对应solution的附加信息
- 支持的事件:
    - `afterAnalyze`: 解析附加信息
- 例子:
    ```js
    export function afterAnalyze(error){
        return info
    }
    ```
 -->
