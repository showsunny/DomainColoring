import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import argparse

def periodic_rect_pulse(x, period=0.25, width=0.125):
    x_mod = np.mod(x, period)
    pulse = np.where(x_mod < width, 1.0, 0.0)
    return pulse

def plot_domain_coloring(F_expression, phase_contour_increase, phase_contour_decrease, 
                          modulus_contour_increase, modulus_contour_decrease, 
                          checkboard, continual_gradient, axes, coordinates, figsize):
    # 创建复数平面
    faces = (4096, 4096)
    x_min, x_max, y_min, y_max = coordinates
    x = np.linspace(x_min, x_max, faces[0])
    y = np.linspace(y_min, y_max, faces[1])
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y  # 复数平面

    # 计算复数函数值
    F = eval(F_expression)

    # 计算幅度和相位
    magnitude = np.abs(F)
    phase = np.angle(F)

    # 矩形脉冲函数
    period = 0.25
    width = 0.125
    offset = period / 2
    pulse1 = periodic_rect_pulse(magnitude * np.cos(phase), period, width) * periodic_rect_pulse(magnitude * np.sin(phase), period, width)
    pulse2 = periodic_rect_pulse(magnitude * np.cos(phase) + offset, period, width) * periodic_rect_pulse(magnitude * np.sin(phase) + offset, period, width)
    pulse_combined = np.logical_or(pulse1, pulse2)

    # 将相位映射到颜色
    Hue = ((phase + np.pi) / (2 * np.pi) + 0.5) % 1

    # 计算亮度
    Brightness_contimual = np.exp(np.log(0.9) * (3 / magnitude) ** 2)
    Brightness_modulus_contour = np.log2(magnitude+ 1e-8) - np.floor(np.log2(magnitude+ 1e-8))
    Brightness_phase_contour = np.log2(1 + phase * 6 / np.pi - np.floor(phase * 6 / np.pi))




    # 处理相位和幅度的轮廓
    if continual_gradient:
        Brightness = np.clip(0.6+Brightness_contimual, 0, 1)
        Saturation = np.clip(1.2 - Brightness_contimual, 0, 1)
    else:
        Saturation = 1
        if (phase_contour_increase==True and phase_contour_decrease==True) or (modulus_contour_increase==True and modulus_contour_decrease==True):
            raise ValueError("Both increase and decrease cannot be True for the same contour type.")

        ### 亮度方案
        if phase_contour_increase==True:
            if modulus_contour_increase == True:
                Brightness = np.clip(np.clip(Brightness_phase_contour + 0.6, 0, 1) + np.clip(Brightness_modulus_contour + 0.6, 0, 1) - 1, 0, 1)
            else:
                if modulus_contour_decrease == True:
                    Brightness = Brightness = np.clip(np.clip(Brightness_phase_contour + 0.6, 0, 1) + np.clip(1 - Brightness_modulus_contour + 0.6, 0, 1) - 1, 0, 1)
                else:
                    Brightness = np.clip(0.6+Brightness_phase_contour, 0, 1)
        else:
            if phase_contour_decrease==True:
                if modulus_contour_increase == True:
                    Brightness = Brightness = np.clip(np.clip(1 - Brightness_phase_contour + 0.6, 0, 1) + np.clip(Brightness_modulus_contour + 0.6, 0, 1) - 1, 0, 1)
                else:
                    if modulus_contour_decrease == True:
                        Brightness = Brightness = np.clip(np.clip(1 - Brightness_phase_contour + 0.6, 0, 1) + np.clip(1- Brightness_modulus_contour + 0.6, 0, 1) - 1, 0, 1)
                    else:
                        Brightness = np.clip(0.6+(1-Brightness_phase_contour), 0, 1)
            else:
                if modulus_contour_increase == True:
                    Brightness = np.clip(0.6+Brightness_modulus_contour, 0, 1)
                else:
                    if modulus_contour_decrease == True:
                        Brightness = np.clip(0.6+(1-Brightness_modulus_contour), 0, 1)
                    else:
                        Brightness = 1

    if checkboard:
        Brightness = Brightness - 0.2*pulse_combined

    # 处理渐变
    # 创建 HSV 颜色空间
    HSV = np.zeros((faces[0], faces[1], 3))
    HSV[..., 0] = Hue
    HSV[..., 1] = Saturation
    HSV[..., 2] = Brightness

    # 将 HSV 转换为 RGB
    RGB = mcolors.hsv_to_rgb(HSV)

    # 绘制域着色图像
    fig, ax = plt.subplots(figsize=(figsize[0], figsize[1]))  # 创建一个新的轴
    ax.imshow(RGB, extent=(x_min, x_max, y_min, y_max), origin='lower')

    # 为色调创建 colorbar
    norm = plt.Normalize(vmin=0, vmax=1)
    sm = plt.cm.ScalarMappable(cmap='hsv', norm=norm)
    sm.set_array([])

    # 添加 colorbar 并指定颜色范围为色调
    cbar = plt.colorbar(sm, ax=ax, ticks=np.linspace(0, 1, 5), shrink=0.9)  # 调整 shrink 参数
    cbar.ax.set_yticklabels(['$0$', '$\pi/2$', '$\pi$', '$3\pi/2$', '$2\pi$'])

    #plt.title(r'Domain Coloring of $f(z) =\frac{(\frac{1}{z})^{18}-\frac{1}{z}}{\frac{1}{z}-1} $', fontsize=20)#frac{(Z^2-1)*(Z-2-i)^2}{Z^2+2+2i}

    if axes:
        plt.grid(True, color='white', linestyle='--')  # 显示网格
    #plt.savefig("output.svg")

    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Domain Coloring with optional contours and checkerboard")
    parser.add_argument("--F", type=str, required=True, help="Function expression for F (e.g., 'Z**2')")
    parser.add_argument("--phase_contour_increase", action="store_true", default=False, help="Enable phase contour increasing")
    parser.add_argument("--phase_contour_decrease", action="store_true", default=False, help="Enable phase contour decreasing")
    parser.add_argument("--modulus_contour_increase", action="store_true", default=True, help="Enable modulus contour increasing")
    parser.add_argument("--modulus_contour_decrease", action="store_true", default=False, help="Enable modulus contour decreasing")
    parser.add_argument("--checkboard", action="store_true", default=True, help="Add checkerboard pattern")
    parser.add_argument("--continual_gradient", action="store_true", default=False, help="Enable continual gradient mode")
    parser.add_argument("--axes", action="store_true", default=False, help="Enable grid on the plot")
    parser.add_argument("--coordinates", type=float, nargs=4, default=(-3, 3, -3, 3), help="Coordinates as x_min, x_max, y_min, y_max")
    parser.add_argument("--figsize", type=float, nargs=2, default=(8, 8), help="Figure size as width height")
    args = parser.parse_args()

    plot_domain_coloring(args.F, args.phase_contour_increase, args.phase_contour_decrease, 
                          args.modulus_contour_increase, args.modulus_contour_decrease, 
                          args.checkboard, args.continual_gradient, args.axes,
                          tuple(args.coordinates), 
                          tuple(args.figsize))
