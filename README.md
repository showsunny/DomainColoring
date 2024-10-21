# DomainColoring
This repository is used to draw high-quality pictures of complex variable functions. The more samples are input, the richer the image details are, and the image size also needs to be larger.
![mandelbralt](https://github.com/showsunny/DomainColoring/blob/main/images/mandelbrot_continual.png)
## 使用方法
在终端中切换至代码所在目录然后执行以下代码(可输入自定义函数，格式为python格式，自变量为大写Z，如果需要三角函数，指数对数函数等可以直接写为np.sin()的形式)
```bash
python complexfunc.py --F 'Z**2-8/Z'
```
效果如下图

![figure1](https://github.com/showsunny/DomainColoring/blob/main/images/Figure_1.png)
