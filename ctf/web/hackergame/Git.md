Git? Git!
图片使用 AI 技术生成，与真实人物无关。


![alt text](image-14.png)
「幸亏我发现了……」马老师长吁了一口气。

「马老师，发生甚么事了？」马老师的一位英国研究生问。

「刚刚一不小心，把 flag 提交到本地仓库里了。」马老师回答，「还好我发现了，撤销了这次提交，不然就惨了……」

「这样啊，那太好了。」研究生说。

马老师没想到的是，这位年轻人不讲武德，偷偷把他的本地仓库拷贝到了自己的电脑上，然后带出了实验室，想要一探究竟……



给定文件

使用`git reflog` 查看本地仓库中的引用日志

```shell
$ git reflog
ea49f0c (HEAD -> main) HEAD@{0}: commit: Trim trailing spaces
15fd0a1 (origin/main, origin/HEAD) HEAD@{1}: reset: moving to HEAD~
505e1a3 HEAD@{2}: commit: Trim trailing spaces
15fd0a1 (origin/main, origin/HEAD) HEAD@{3}: clone: from https://github.com/dair-ai/ML-Course-Notes.git
(base)
```

`git show`查看

```shell
$ git show 505e1a3
```

可使用/flag 搜索即可获得结果
