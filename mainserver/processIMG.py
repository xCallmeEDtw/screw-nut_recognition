import cv2
import numpy as np
import getImg
def detect_object_properties(image):
    # 读取图像
    
    height, width = image.shape[:2]
    center_x, center_y = width // 2, height // 2  # 图像中心坐标

    # 将图像转换为灰度
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 反转灰度图像（黑变白，白变黑）
    gray = cv2.bitwise_not(gray)

    # 应用阈值处理
    _, thresh = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY)
    cv2.imwrite('./thresh.png', thresh)
    # 进行膨胀和腐蚀操作
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thresh = cv2.dilate(thresh, kernel, iterations=3)
    thresh = cv2.erode(thresh, kernel, iterations=3)
    thresh = cv2.dilate(thresh, kernel, iterations=5)
    thresh = cv2.erode(thresh, kernel, iterations=5)
    # thresh = cv2.erode(thresh, kernel, iterations=5)
    # thresh = cv2.dilate(thresh, kernel, iterations=3)
    
    # 保存阈值处理后的图像
    cv2.imwrite('./thresh_afterdilate.png', thresh)

    return thresh


# def extract_center_black_area(img):
#     # 将图像转换为灰度图
#     if len(img.shape) == 3:
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     else:
#         gray = img.copy()

#     # 对灰度图进行二值化，提取黑色区域
#     threshold = 50
#     _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)

#     # 寻找轮廓
#     contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # 找到离图像中心最近的黑色区域
#     h, w = gray.shape
#     center = (w // 2, h // 2)
#     min_distance = float('inf')
#     closest_contour = None

#     for contour in contours:
#         # 计算轮廓的质心
#         M = cv2.moments(contour)
#         if M["m00"] == 0:
#             continue
#         cX = int(M["m10"] / M["m00"])
#         cY = int(M["m01"] / M["m00"])
#         # 计算质心到图像中心的距离
#         distance = ((cX - center[0]) ** 2 + (cY - center[1]) ** 2) ** 0.5
#         if distance < min_distance:
#             min_distance = distance
#             closest_contour = contour

#     # 创建一个全白的输出图像
#     output = np.full_like(gray, 255)

#     # 如果找到最近的轮廓，就在输出图像上绘制
#     if closest_contour is not None:
#         cv2.drawContours(output, [closest_contour], -1, (0), thickness=cv2.FILLED)

#     return output

def extract_center_black_area(img):
    # 将图像转换为灰度图
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()

    # 对灰度图进行二值化，提取黑色区域
    threshold = 50
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)

    # 寻找轮廓
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 找到离图像中心最近且面积大于1000的黑色区域
    h, w = gray.shape
    center = (w // 2, h // 2)
    min_distance = float('inf')
    closest_contour = None

    for contour in contours:
        # 计算轮廓的面积，排除面积小于1000的轮廓
        area = cv2.contourArea(contour)
        if area < 1000:
            continue  # 跳过面积小于1000的轮廓

        # 计算轮廓的质心
        M = cv2.moments(contour)
        if M["m00"] == 0:
            continue  # 避免除以零
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # 计算质心到图像中心的距离
        distance = ((cX - center[0]) ** 2 + (cY - center[1]) ** 2) ** 0.5

        if distance < min_distance:
            min_distance = distance
            closest_contour = contour

    # 创建一个全白的输出图像
    output = np.full_like(gray, 255)

    # 如果找到符合条件的轮廓，就在输出图像上绘制
    if closest_contour is not None:
        cv2.drawContours(output, [closest_contour], -1, (0), thickness=cv2.FILLED)

    return output

def draw_center_contour(center_img, real_img):
    # 确保 center_img 是灰度图
    if len(center_img.shape) == 3:
        gray_center = cv2.cvtColor(center_img, cv2.COLOR_BGR2GRAY)
    else:
        gray_center = center_img.copy()

    # 二值化处理，提取黑色区域
    threshold = 50
    _, binary = cv2.threshold(gray_center, threshold, 255, cv2.THRESH_BINARY_INV)

    # 寻找轮廓
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 找到离图像中心最近的轮廓
    h, w = gray_center.shape
    center_point = (w // 2, h // 2)
    min_distance = float('inf')
    closest_contour = None

    for contour in contours:
        # 计算轮廓的质心
        M = cv2.moments(contour)
        if M["m00"] == 0:
            continue
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # 计算质心到图像中心的距离
        distance = ((cX - center_point[0]) ** 2 + (cY - center_point[1]) ** 2) ** 0.5
        if distance < min_distance:
            min_distance = distance
            closest_contour = contour

    # 在 real_img 上绘制黑色的轮廓边框
    if closest_contour is not None:
        # 确保 real_img 是彩色图像
        if len(real_img.shape) == 2:
            real_img_color = cv2.cvtColor(real_img, cv2.COLOR_GRAY2BGR)
        else:
            real_img_color = real_img.copy()

        cv2.drawContours(real_img_color, [closest_contour], -1, (0, 0, 0), thickness=2)

        return real_img_color
    else:
        print("未找到中心的黑色区域轮廓。")
        return real_img


def classify_object(center_img):
    # 将图像转换为灰度图
    if len(center_img.shape) == 3:
        gray = cv2.cvtColor(center_img, cv2.COLOR_BGR2GRAY)
    else:
        gray = center_img.copy()

    # 二值化处理，提取黑色区域
    threshold = 50
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)

    # 寻找轮廓
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 找到离图像中心最近的轮廓
    h, w = gray.shape
    center_point = (w // 2, h // 2)
    min_distance = float('inf')
    closest_contour = None

    for contour in contours:
        # 计算轮廓的质心
        M = cv2.moments(contour)
        if M["m00"] == 0:
            continue
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # 计算质心到图像中心的距离
        distance = ((cX - center_point[0]) ** 2 + (cY - center_point[1]) ** 2) ** 0.5
        if distance < min_distance:
            min_distance = distance
            closest_contour = contour

    # 如果找到轮廓，进行分类
    if closest_contour is not None:
        # 计算外接矩形
        x, y, w, h = cv2.boundingRect(closest_contour)
        area = cv2.contourArea(closest_contour)
        perimeter = cv2.arcLength(closest_contour, True)

        # 计算长宽比
        aspect_ratio = float(w) / h

        # 计算圆形度
        if perimeter == 0:
            circularity = 0
        else:
            circularity = 4 * np.pi * area / (perimeter * perimeter)

        # 判断是否为螺帽或螺丝
        if circularity >= 0.7 :#and 0.9 <= aspect_ratio <= 1.1:
            classification = 'nut'  # 近似圆形，长宽比接近1
        else:
            classification = 'screw'  # 长条形，长宽比偏离1

        # 可选：在图像上绘制结果（如果需要可取消注释）
        result_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(result_img, [closest_contour], -1, (0, 255, 0), 2)
        # cv2.putText(result_img, f'Classification: {classification}', (x, y - 10),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.imwrite('./Result.png', result_img)

        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        return classification
    else:
        return '未找到物体'

# 示例使用
# center_img = cv2.imread('center_image.jpg')
# result = classify_object(center_img)
# print(f'分类结果: {result}')

# # 调用函数进行物体检测


def calculate_black_area(center_img):
    # 将图像转换为灰度图
    if len(center_img.shape) == 3:
        gray = cv2.cvtColor(center_img, cv2.COLOR_BGR2GRAY)
    else:
        gray = center_img.copy()

    # 二值化处理，提取黑色区域
    threshold = 50
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)

    # 寻找轮廓
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 找到离图像中心最近的轮廓
    h, w = gray.shape
    center_point = (w // 2, h // 2)
    min_distance = float('inf')
    closest_contour = None

    for contour in contours:
        # 计算轮廓的质心
        M = cv2.moments(contour)
        if M["m00"] == 0:
            continue
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # 计算质心到图像中心的距离
        distance = ((cX - center_point[0]) ** 2 + (cY - center_point[1]) ** 2) ** 0.5
        if distance < min_distance:
            min_distance = distance
            closest_contour = contour

    # 如果找到最近的轮廓，计算其面积
    if closest_contour is not None:
        area = cv2.contourArea(closest_contour)
        return area
    else:
        print("未找到中心的黑色区域。")
        return 0



def proc_img():
    image_path = './capture_image.jpg'  # 替换为你的图片路径
    image = cv2.imread(image_path)
    img_thresh = detect_object_properties(image)
    # extract_black_center(img_thresh)

    # image = cv2.imread('thresh.png')
    center_img = extract_center_black_area(img_thresh)
    cv2.imwrite('./center.png', center_img)

    CenterArea = calculate_black_area(center_img)
    print(CenterArea)
    if CenterArea > 4500:
        return "err"


    out_img = draw_center_contour(center_img,image)

    cv2.imwrite('./out.png', out_img)

    return(classify_object(center_img))
if __name__ == '__main__':
    image_url = "http://192.168.38.78/capture"
    
    # 保存的檔案路徑
    save_path = "capture_image.jpg"
    
    # 下載圖片
    getImg.download_image(image_url, save_path)
    print(proc_img())