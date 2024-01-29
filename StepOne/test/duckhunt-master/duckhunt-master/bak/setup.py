from distutils.core import setup
import py2exe, sys, os

# 用于将脚本更改为exe的步骤：
# 修改duckhunt-configurable.py文件中的变量，然后运行此脚本
sys.argv.append('py2exe')

setup(

    name = 'duckhunt',
    description = 'duckhunt-',

    # 设置编译选项
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    
    # 指定要编译的脚本
    windows = [{'script': "duckhunt-configurable.py"}],
    
    # 不包括在zip文件中的文件
    zipfile = None,
)