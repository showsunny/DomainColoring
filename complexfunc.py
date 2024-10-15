import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from mpmath import zeta



# 创建复数平面
x_min=-2
x_max=0.5
y_min=-1.5
y_max=1.5
x = np.linspace(x_min, x_max, 4096)  # 根据图像尺寸修改样本数量
y = np.linspace(y_min, y_max, 4096)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y  # 复数平面,用于绘制普通函数
Z=0   #初始化为自定义值用于绘制迭代函数
# 计算复数函数值
#F = np.sin(Z)#Z**(2/3+1j)#zeta_values = np.vectorize(lambda z: complex(zeta(z)))(Z)#np.sin(np.log(Z**2))#(Z-2-1j)**2*(Z**2-1)/(Z**2+2+1j)# 示例函数np.e**(-Z**2)
iterations = 20
for i in range(iterations):
    Z = Z**2 + X+1j*Y # 计算 z^2 + c
F= Z

def periodic_rect_pulse(x, period=0.25, width=0.125):#使用跳跃函数来加强边界
    # 使用mod函数创建周期性
    x_mod = np.mod(x, period)
    # 使用where函数创建矩形脉冲
    pulse = np.where(x_mod < width, 1.0, 0.0)
    return pulse
period=0.25
width=0.125
offset = period / 2  # 设置偏移量

# 计算幅度和相位
magnitude = np.abs(F)
phase = np.angle(F)

pulse1 = periodic_rect_pulse(magnitude * np.cos(phase), period, width) * periodic_rect_pulse(magnitude * np.sin(phase), period, width)
pulse2 = periodic_rect_pulse(magnitude * np.cos(phase)+offset, period, width) * periodic_rect_pulse(magnitude * np.sin(phase)+offset, period, width)
pulse_combined = np.logical_or(pulse1, pulse2)
# 将相位映射到颜色
Hue = ((phase + np.pi) / (2 * np.pi) + 0.5) % 1  # 将相位旋转 180 度#[-pi, pi]->[0,2pi]
# 根据需求以下两种模式任选一种
#模式一：连续渐变，即亮度随|f(z)|的增大而增大，减小而减小。例如：当f(z)=z时原点处函数值最小原点附近呈现黑色无穷远处函数值最大呈现为白色
#Brightness = np.clip(0.6 + 1/(1+np.exp(-np.log2(magnitude + 1e-8))), 0, 1)-0.2*pulse_combined
#模式二：跳跃渐变，在|f(z)|以2^n为周期时实现0~1的亮度渐变
np.clip(0.6 + np.log2(magnitude+ 1e-8) - np.floor(np.log2(magnitude+ 1e-8)), 0, 1)-0.2*pulse_combined
Saturation = 1  # 饱和度

# 创建 HSV 颜色空间
HSV = np.zeros((4096, 4096, 3))
HSV[..., 0] = Hue  # H
HSV[..., 1] = Saturation  # S
HSV[..., 2] = Brightness  # V

# 将 HSV 转换为 RGB
RGB = mcolors.hsv_to_rgb(HSV)

# 绘制域着色图像
fig, ax = plt.subplots(figsize=(20, 20))  # 创建一个新的轴
ax.imshow(RGB, extent=(x_min, x_max, y_min, y_max), origin='lower',interpolation='nearest')

# 为色调创建 colorbar
norm = plt.Normalize(vmin=0, vmax=1)
sm = plt.cm.ScalarMappable(cmap='hsv', norm=norm)
sm.set_array([])

# 添加 colorbar 并指定颜色范围为色调
cbar = plt.colorbar(sm, ax=ax, ticks=np.linspace(0, 1, 5), label='Phase', shrink=0.8)  # 调整 shrink 参数
cbar.ax.set_yticklabels(['$0$', '$\pi/2$', '$\pi$', '$3\pi/2$', '$2\pi$'])

plt.title(r'Domain Coloring of $f(z) =(20)f^2+z,f_0=0 $')#frac{(Z^2-1)*(Z-2-i)^2}{Z^2+2+2i}

plt.grid(True, color='white', linestyle='--')  # 显示网格
#plt.savefig('output.pdf', format='pdf',dpi=600)

plt.show()
