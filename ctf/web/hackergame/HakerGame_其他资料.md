## git

### 1.查看记录

要查看Git项目从创建开始到现在的所有push记录，可以使用以下命令：

```
git log --all --grep="push"
```

该命令将显示包含关键词"push"的所有提交记录。其中，`--all`选项表示显示所有分支的提交记录，而`--grep="push"`则指定了只显示包含"push"关键词的提交。

如果你只想查看某个特定分支的push记录，可以使用以下命令：

```
git log <branch> --grep="push"
```

其中，`<branch>`是要查看的分支名称。

这些命令会以时间顺序列出所有符合条件的提交记录，包括作者、提交时间、提交信息等。如果有很多记录，可以通过按下空格键逐页滚动查看。

请注意，以上命令仅查看本地Git仓库中的提交记录。如果你想查看远程仓库的push记录，需要先进行`git fetch`命令从远程仓库获取最新的提交记录，然后再执行上述命令查看本地仓库中的记录。



要查看特定文件的版本历史并回退到以前的版本，可以使用以下Git命令：

### 2. 查看指定文件的版本历史

```
git log --follow <file_path>
```

该命令将列出指定文件的所有提交历史。 `--follow` 参数用于跟踪文件的重命名和移动。

### 3. 回退到特定版本

```
git checkout <commit_hash> <file_path>
```

其中 `<commit_hash>` 是要回退到的提交哈希值， `<file_path>` 是要修改的文件路径。 这个命令会将文件恢复到指定提交的版本。

如果你想回到最新的版本，你可以运行以下命令：

```
git checkout HEAD <file_path>
```

这将把文件恢复到当前分支的最新提交。

如果你想彻底删除文件的某个版本，可以使用以下两个命令：

### 4. 删除指定版本的文件

```
git rm <file_path>
```

### 5.提交更改

```
git commit -m "Removed file from specific version"
```

这将从版本历史中永久删除指定版本的文件。

但需要注意的是，如果在公共代码库中使用此方法，删除历史版本可能会导致其他人的代码出现问题。因此，在对公共代码库进行更改之前，请确保理解您的操作会影响到哪些人，并与同事讨论。



### 6. 查看某个提交的具体变动

```
git show <commit_hash>
```

其中 `<commit_hash>` 是要查看的提交的哈希值。该命令将显示指定提交的详细信息，包括修改的文件和具体的变动内容。

对于你提供的提交历史，你可以运行以下命令来查看每个提交的实际修改内容：

```
git show ea49f0cd3d36edb2965f89581b11151959d20991
```

这将显示提交 `ea49f0cd3d36edb2965f89581b11151959d20991` 的详细信息，包括修改的文件和具体的变动内容。

你可以按照类似的方式查看其他提交的具体变动。只需将 `<commit_hash>` 替换为相应提交的哈希值即可。

这样，你就可以逐个查看每个提交所做的实际修改，并了解文件的变化。







### 7. 查看撤销前的提交历史记录：

```
git reflog
```

这个命令将显示仓库的操作历史，包括提交、重置等。找到之前撤销的提交的哈希值。

#### 7.1 恢复撤销的提交：

```
git cherry-pick <commit_hash>
```

其中 `<commit_hash>` 是之前撤销的提交的哈希值。这个命令将会将之前撤销的提交应用到当前分支，并创建一个新的提交。

请注意，如果你已经进行了其他的提交或分支切换操作，那么恢复撤销的提交可能会导致冲突。在执行 `git cherry-pick` 命令之前，请确保工作区是干净的（没有未提交的修改）。

另外，如果你想要恢复整个被撤销的提交序列，而不仅仅是单个提交，可以使用 `git reflog` 查看更多历史记录，并使用 `git reset <commit_hash>` 将当前分支回退到相应的提交。

建议在执行重要操作前，先备份代码，以防止意外情况发生。



一种可能的方法是，逐个检查每个历史记录，直到找到包含 `flag` 的提交。你可以从较旧的历史记录开始，使用以下命令：

```
git show <commit_hash>
```

其中 `<commit_hash>` 为某个历史记录中的提交哈希值。执行该命令后，将显示该提交的详细信息，包括文件变更。如果该提交包含 `flag`，则你需要记录下该提交的哈希值。

重复执行上述命令，直到找到包含 `flag` 的提交。

找到包含 `flag` 的提交后，你可以使用 `git cherry-pick` 命令来将该提交应用到当前分支。

```
git cherry-pick <commit_hash>
```

其中 `<commit_hash>` 为包含 `flag` 的提交的哈希值。

如果你想一次性恢复多个提交，你可以使用 `git rebase -i` 命令来交互式地重写提交历史。这个命令将打开一个文本编辑器，让你更改提交历史记录。通过编辑提交历史记录，你可以选择删除提交、重新排序提交或合并提交。请注意，这种方法可能会改变提交历史记录，并影响其他团队成员的代码库，因此建议在进行操作之前与团队成员进行沟通。

### 8.实际获得flag过程

#### 8.1 查看reflog

```shell
Roy@LAPTOP-VGJP8LVS MINGW64 ~/Desktop/ctf/ustc/.git (GIT_DIR!)
$ git reflog
ea49f0c (HEAD -> main) HEAD@{0}: commit: Trim trailing spaces
15fd0a1 (origin/main, origin/HEAD) HEAD@{1}: reset: moving to HEAD~
505e1a3 HEAD@{2}: commit: Trim trailing spaces
15fd0a1 (origin/main, origin/HEAD) HEAD@{3}: clone: from https://github.com/dair-ai/ML-Course-Notes.git
(base)

```



#### 8.2 查看回退版本

1.执行

```shell
$ git show 505e1a3
```

2.利用vi编辑器的/+关键词查找flag

```shell
/flag
```







## http集邮



### 2. 无状态码

```http
POST /HTTP/1.1\r\nHost: examasple.co\n\r\n\r
```

