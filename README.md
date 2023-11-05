# appium_jyys



# 安装问题
1. lap包在linux中安装遇到问题。
```
error: subprocess-exited-with-error
  
  × python setup.py bdist_wheel did not run successfully.
  │ exit code: 1
  ╰─> [59 lines of output]
      Partial import of lap during the build process.
      Generating cython files
      running bdist_wheel
      running build
      running config_cc
      running config_fc
      running build_src
      /home/max/anaconda3/lib/python3.8/site-packages/setuptools/command/install.py:34: SetuptoolsDeprecationWarning: setup.py install is deprecated. Use build and pip and other standards-based tools.  
```
解决办法：
```
pip install git+git://github.com/gatagat/lap.git
或者
conda install -c conda-forge lap
```
