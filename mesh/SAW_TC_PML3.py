import gmsh
import sys
import numpy as np
import math


# from array import array


def GM(pitch, n_idt, Aperture, eta, Hidt, Hidt_LT, n_f, n_we, msh_max, msh_min, msh_r, msh_f):
    gmsh.initialize()

    gmsh.model.add("SAW_TC_PML3")

    n_f = int(n_f)
    n_we = int(n_we)

    w = 2 * pitch  # 波长
    d = Hidt  # 指条厚度
    h = Hidt_LT  # 压电材料高度

    hsio2 = 0.72144
    hsin = 0.04

    n_w1 = n_idt[n_f:(n_f + n_we)]
    n_w2 = n_idt[(n_f + n_we)+1:(n_f + 2*n_we)+1]

    Nidt_WL = np.sum(n_w1)  # 左半边加权电极的个数
    Nidt_WR = np.sum(n_w2)  # 右半边加权电极的个数

    nn = len(n_idt)
    idx_e = math.floor(nn/2)
    Nidt_e = n_idt[idx_e]
    p = pitch[idx_e]

    Nidt = Nidt_WL + Nidt_e + Nidt_WR

    N_zheng = math.ceil(Nidt / 2)  # 正电极根数
    N_fu = math.floor(Nidt / 2)

    N_side = 3 * p  # 两侧附加宽度
    N_IDT = np.sum(n_idt)

    # # PML厚度
    pml = 2*p  # or 2

    lc = msh_min  # or 0.3

    # 器件x方向最大值
    xmax = np.sum(n_idt * pitch) + 2 * N_side

    # 压电平面中的点
    gmsh.model.geo.addPoint(0, 0, 0, lc, 1)
    gmsh.model.geo.addPoint(xmax, 0, 0, lc, 2)
    gmsh.model.geo.addPoint(xmax, h, 0, lc, 3)
    gmsh.model.geo.addPoint(0, h, 0, lc, 4)

    # TC温补层上的点
    gmsh.model.geo.addPoint(0, h+hsio2, 0, lc, 5001)
    gmsh.model.geo.addPoint(xmax, h + hsio2, 0, lc, 5002)

    gmsh.model.geo.addPoint(0, h + hsio2+hsin, 0, lc, 5003)
    gmsh.model.geo.addPoint(xmax, h + hsio2+hsin, 0, lc, 5004)

    # PML中的点
    gmsh.model.geo.addPoint(0 - pml, 0, 0, lc, 5)
    gmsh.model.geo.addPoint(0 - pml, 0 - pml, 0, lc, 6)
    gmsh.model.geo.addPoint(0, 0 - pml, 0, lc, 7)

    gmsh.model.geo.addPoint(xmax, 0 - pml, 0, lc, 8)
    gmsh.model.geo.addPoint(xmax + pml, 0 - pml, 0, lc, 9)
    gmsh.model.geo.addPoint(xmax + pml, 0, 0, lc, 10)

    gmsh.model.geo.addPoint(xmax + pml, h, 0, lc, 11)
    gmsh.model.geo.addPoint(0 - pml, h, 0, lc, 12)

    # 悬浮电极起始点
    node = 2
    x1 = N_side
    idx_node = 0
    for idx in range(0, nn):
        if idx == 0:
            x1 = x1 + pitch[idx] / 2 * (1-eta[idx])
            x2 = h
            for t in range(1, n_idt[idx] + 1):
                gmsh.model.geo.addPoint(x1, x2, 0, lc, 4 * (t + node) + 1)
                gmsh.model.geo.addPoint(x1 + pitch[idx] * eta[idx], x2, 0, lc, 4 * (t + node) + 2)
                gmsh.model.geo.addPoint(x1 + pitch[idx] * eta[idx], x2 + d, 0, lc, 4 * (t + node) + 3)
                gmsh.model.geo.addPoint(x1, x2 + d, 0, lc, 4 * (t + node) + 4)

                x1 = x1 + pitch[idx]
        else:
            x1 = x1 - pitch[idx-1]/2 * ((1-eta[idx-1])) + pitch[idx]/2 * ((1-eta[idx]))
            x2 = h
            idx_node = idx_node + n_idt[idx-1]
            for t in range(1, n_idt[idx] + 1):
                gmsh.model.geo.addPoint(x1, x2, 0, lc, 4 * (t + node + idx_node) + 1)
                gmsh.model.geo.addPoint(x1 + pitch[idx]*eta[idx], x2, 0, lc, 4 * (t + node + idx_node) + 2)
                gmsh.model.geo.addPoint(x1 + pitch[idx]*eta[idx], x2 + d, 0, lc, 4 * (t + node + idx_node) + 3)
                gmsh.model.geo.addPoint(x1, x2 + d, 0, lc, 4 * (t + node + idx_node) + 4)

                x1 = x1 + pitch[idx]

    # 增加电极线
    for t in range(1, N_IDT + 1):
        gmsh.model.geo.addLine(4 * (t + node) + 1, 4 * (t + node) + 2, 1 + 4 * (t - 1))
        gmsh.model.geo.addLine(4 * (t + node) + 2, 4 * (t + node) + 3, 2 + 4 * (t - 1))
        gmsh.model.geo.addLine(4 * (t + node) + 3, 4 * (t + node) + 4, 3 + 4 * (t - 1))
        gmsh.model.geo.addLine(4 * (t + node) + 4, 4 * (t + node) + 1, 4 + 4 * (t - 1))

    # 增加电极之间的线
    for t in range(1, N_IDT):
        gmsh.model.geo.addLine(4 * (t + node) + 2, 4 * (t + node) + 2 + 3, t + 4 * N_IDT)

    # 增加压电外围线
    gmsh.model.geo.addLine(13, 4, 5000)
    gmsh.model.geo.addLine(4, 1, 5001)
    gmsh.model.geo.addLine(1, 2, 5002)
    gmsh.model.geo.addLine(2, 3, 5003)
    gmsh.model.geo.addLine(3, 4 * N_IDT + 2 + 8, 5004)

    # 增加PML线
    gmsh.model.geo.addLine(4, 12, 5005)
    gmsh.model.geo.addLine(12, 5, 5006)
    gmsh.model.geo.addLine(5, 1, 5007)

    gmsh.model.geo.addLine(5, 6, 5008)
    gmsh.model.geo.addLine(6, 7, 5009)
    gmsh.model.geo.addLine(7, 1, 5010)

    gmsh.model.geo.addLine(7, 8, 5011)
    gmsh.model.geo.addLine(8, 2, 5012)

    gmsh.model.geo.addLine(8, 9, 5013)
    gmsh.model.geo.addLine(9, 10, 5014)
    gmsh.model.geo.addLine(10, 2, 5015)

    gmsh.model.geo.addLine(10, 11, 5016)
    gmsh.model.geo.addLine(11, 3, 5017)

    # TC上的线
    gmsh.model.geo.addLine(3, 5002, 5018)
    gmsh.model.geo.addLine(5002, 5001, 5019)
    gmsh.model.geo.addLine(5001, 4, 5020)

    gmsh.model.geo.addLine(5002, 5004, 5021)
    gmsh.model.geo.addLine(5004, 5003, 5022)
    gmsh.model.geo.addLine(5003, 5001, 5023)

    # 增加电极 curve loop and plane
    for t in range(1, N_IDT + 1):
        gmsh.model.geo.addCurveLoop([1 + 4 * (t - 1), 2 + 4 * (t - 1), 3 + 4 * (t - 1), 4 + 4 * (t - 1)], t)
        gmsh.model.geo.addPlaneSurface([t], t)
        gmsh.model.geo.mesh.setRecombine(2, t)  # Recombine


    # 增加压电平面
    l5 = 4 * N_IDT - 3
    l6 = 4 * N_IDT + N_IDT - 1
    l7 = 4 * N_IDT - 3
    for t in range(1, N_IDT):
        l5 = np.append(l5, l6 + 1 - t)
        l5 = np.append(l5, l7 - 4 * t)
    l5 = -l5
    l8 = [5000, 5001, 5002, 5003, 5004]
    l9 = np.append(l8, l5)
    l9 = l9.tolist()
    gmsh.model.geo.addCurveLoop(l9, 1000)
    gmsh.model.geo.addPlaneSurface([1000], 1000)
    # Recombine
    gmsh.model.geo.mesh.setRecombine(2, 1000)

    # 增加TC平面
    l5 = [5004, -5018, -5019, -5020, 5000]
    l6 = 4 * N_IDT + 1
    l7 = 4

    for t in range(1, N_IDT+1):
        l5 = np.append(l5, l7 + 4*(t-1))
        l5 = np.append(l5, l7 - 1 + 4 * (t - 1))
        l5 = np.append(l5, l7 - 2 + 4 * (t - 1))

        if t != N_IDT:
            l5 = np.append(l5, -(l6 - 1 + t))

    l5 = -l5
    l5 = l5.tolist()
    gmsh.model.geo.addCurveLoop(l5, 1006)
    gmsh.model.geo.addPlaneSurface([1006], 1006)
    gmsh.model.geo.mesh.setRecombine(2, 1006)

    # trimm
    gmsh.model.geo.addCurveLoop([-5019, 5021, 5022, 5023], 1007)
    gmsh.model.geo.addPlaneSurface([1007], 1007)
    gmsh.model.geo.mesh.setRecombine(2, 1007)

    # 增加PML平面
    # left-PML
    gmsh.model.geo.addCurveLoop([5005, 5006, 5007, -5001], 1001)
    gmsh.model.geo.addPlaneSurface([1001], 1001)
    gmsh.model.geo.mesh.setRecombine(2, 1001)
    # left-PML-1
    gmsh.model.geo.addCurveLoop([-5007, 5008, 5009, 5010], 1002)
    gmsh.model.geo.addPlaneSurface([1002], 1002)
    gmsh.model.geo.mesh.setRecombine(2, 1002)
    # low-PML
    gmsh.model.geo.addCurveLoop([-5002, -5010, 5011, 5012], 1003)
    gmsh.model.geo.addPlaneSurface([1003], 1003)
    gmsh.model.geo.mesh.setRecombine(2, 1003)
    # right-PML-1
    gmsh.model.geo.addCurveLoop([-5012, 5013, 5014, 5015], 1004)
    gmsh.model.geo.addPlaneSurface([1004], 1004)
    gmsh.model.geo.mesh.setRecombine(2, 1004)
    # right-PML
    gmsh.model.geo.addCurveLoop([-5015, 5016, 5017, -5003], 1005)
    gmsh.model.geo.addPlaneSurface([1005], 1005)
    gmsh.model.geo.mesh.setRecombine(2, 1005)

    gmsh.model.geo.synchronize()

    # Al平面--1
    p1 = np.arange(1, N_IDT + 1, 1)
    p1 = p1.tolist()
    gmsh.model.addPhysicalGroup(2, p1, 1)

    # TC平面

    # 压电平面--2
    gmsh.model.addPhysicalGroup(2, [1000], 2)

    # 左反射栅--3
    if n_f == 1:
        l1 = np.arange(1, n_idt[0] * 4 + 1, 1)
        gmsh.model.addPhysicalGroup(1, l1, 3, name = "左反射栅")

        l2 = np.arange(4 * N_IDT + 1 - n_idt[nn-1] * 4, 4 * N_IDT + 1, 1)
        gmsh.model.addPhysicalGroup(1, l2, 4, name = "右反射栅")

        l3 = [n_idt[0] * 4 + 1, n_idt[0] * 4 + 2, n_idt[0] * 4 + 3,
              n_idt[0] * 4 + 4]
        for t in range(1, N_zheng):
            x1 = [n_idt[0] * 4 + 1 + 8 * t, n_idt[0] * 4 + 2 + 8 * t,
                  n_idt[0] * 4 + 3 + 8 * t, n_idt[0] * 4 + 4 + 8 * t]
            l3.extend(x1)
        gmsh.model.addPhysicalGroup(1, l3, 5, name="正电极")

        l4 = [n_idt[0] * 4 + 4 + 1, n_idt[0] * 4 + 4 + 2, n_idt[0] * 4 + 4 + 3,
              n_idt[0] * 4 + 4 + 4]
        for t in range(1, N_fu):
            x2 = [n_idt[0] * 4 + 4 + 1 + 8 * t, n_idt[0] * 4 + 4 + 2 + 8 * t,
                  n_idt[0] * 4 + 4 + 3 + 8 * t,
                  n_idt[0] * 4 + 4 + 4 + 8 * t]
            l4.extend(x2)
        gmsh.model.addPhysicalGroup(1, l4, 6, name="负电极")


    if n_f == 2:
        l1 = np.arange(1, (n_idt[0]+n_idt[1]) * 4 + 1, 1)
        gmsh.model.addPhysicalGroup(1, l1, 3, name = "左反射栅")

        l2 = np.arange(4 * N_IDT + 1 - (n_idt[nn-1]+n_idt[nn-2]) * 4, 4 * N_IDT + 1, 1)
        gmsh.model.addPhysicalGroup(1, l2, 4, name = "右反射栅")

        l3 = [(n_idt[0]+n_idt[1]) * 4 + 1, (n_idt[0]+n_idt[1]) * 4 + 2, (n_idt[0]+n_idt[1]) * 4 + 3,
              (n_idt[0]+n_idt[1]) * 4 + 4]
        for t in range(1, N_zheng):
            x1 = [(n_idt[0]+n_idt[1]) * 4 + 1 + 8 * t, (n_idt[0]+n_idt[1]) * 4 + 2 + 8 * t,
                  (n_idt[0]+n_idt[1]) * 4 + 3 + 8 * t, (n_idt[0]+n_idt[1]) * 4 + 4 + 8 * t]
            l3.extend(x1)
        gmsh.model.addPhysicalGroup(1, l3, 5, name = "正电极")

        l4 = [(n_idt[0]+n_idt[1]) * 4 + 4 + 1, (n_idt[0]+n_idt[1]) * 4 + 4 + 2, (n_idt[0]+n_idt[1]) * 4 + 4 + 3,
              (n_idt[0]+n_idt[1]) * 4 + 4 + 4]
        for t in range(1, N_fu):
            x2 = [(n_idt[0]+n_idt[1]) * 4 + 4 + 1 + 8 * t, (n_idt[0]+n_idt[1]) * 4 + 4 + 2 + 8 * t,
                  (n_idt[0]+n_idt[1]) * 4 + 4 + 3 + 8 * t,
                  (n_idt[0]+n_idt[1]) * 4 + 4 + 4 + 8 * t]
            l4.extend(x2)
        gmsh.model.addPhysicalGroup(1, l4, 6, name = "负电极")


    # 固定边界--7
    gmsh.model.addPhysicalGroup(1, [5009, 5011, 5013], 7)

    # PML-left
    gmsh.model.addPhysicalGroup(2, [1001], 8)
    # PML-left-1
    gmsh.model.addPhysicalGroup(2, [1002], 9)
    # PML-low
    gmsh.model.addPhysicalGroup(2, [1003], 10)
    # PML-right-1
    gmsh.model.addPhysicalGroup(2, [1004], 11)
    # PML-right
    gmsh.model.addPhysicalGroup(2, [1005], 12)

    # 二氧化硅层
    gmsh.model.addPhysicalGroup(2, [1006], 13)
    # trimm layer
    gmsh.model.addPhysicalGroup(2, [1007], 14)

    gmsh.option.setNumber("Mesh.Algorithm", 8)
    gmsh.option.setNumber("Mesh.RecombinationAlgorithm", 1)  # or 3
    gmsh.option.setNumber("Mesh.SubdivisionAlgorithm", 1)

    gmsh.model.mesh.generate(2)

    # Set the element order and the desired interpolation order:
    elementOrder = 2
    gmsh.model.mesh.setOrder(elementOrder)

    gmsh.write("SAW_TC_PML3.m")

    if '-nopopup' not in sys.argv:
        gmsh.fltk.run()

    # if '-nopopup' not in sys.argv:
    #     gmsh.fltk.initialize()

    # # v = gmsh.view.getTags()
    # # gmsh.graphics.draw()
    # gmsh.write("mesh.jpg")

    gmsh.finalize()


# pitch = array('d', [3,2,1,2,3])
# n_idt = array('d', [2,2,2,2,2])
# eta = array('d', [0.5,0.5,0.5,0.5,0.5])

# pitch = np.array([1, 2, 1, 2, 1, 2, 1, 2, 1])
# n_idt = np.array([4, 4, 3, 4, 5, 4, 3, 2, 1])
# eta = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
# n_f = 2
# n_we = 2

# n_f = 1
# n_we = 3

# pitch = np.array([1, 1, 1])  # 左悬浮电势 中间IDT 右悬浮电势
# n_idt = np.array([4, 4, 4])  # 对应根数
# eta = np.array([0.5, 0.5, 0.5])   # 对应金属化率
# n_f = 1    # 对称结构 单侧悬浮电势的种类数
# n_we = 0   # 对称结构 单侧电极的种类数

pitch = np.array([1.9936/2, 1.9936/2, 1.9936/2])  # 左悬浮电势 中间IDT 右悬浮电势
n_idt = np.array([6, 24, 6])  # 对应根数
# n_idt = np.array([1, 2, 1])  # 对应根数
eta = np.array([0.45945945945945943, 0.45945945945945943, 0.45945945945945943])   # 对应金属化率
n_f = 1    # 对称结构 单侧悬浮电势的种类数
n_we = 0   # 对称结构 单侧电极的种类数

msh = GM(pitch, n_idt, 2, eta, 0.166332, 3*1.9936, n_f, n_we, 0, 0.5, 0, 0)

