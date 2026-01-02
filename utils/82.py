import os
import glob
from PIL import Image

def resize_images(directory):
    # 获取所有 JPG 图片的路径
    image_paths = glob.glob(os.path.join(directory, "*.jpg"))

    if not image_paths:
        print(f"目录 {directory} 中没有找到 JPG 图片。")
        return

    total_height = 0
    total_width = 0
    valid_image_count = 0  # 记录有效图片数量

    # 计算所有图片的总高度和总宽度
    for path in image_paths:
        try:
            with Image.open(path) as img:
                total_height += img.height
                total_width += img.width
                valid_image_count += 1
        except Exception as e:
            print(f"无法打开图片 {path}: {e}")

    # 计算平均高度和平均宽度
    average_height = total_height // valid_image_count if valid_image_count else 0
    average_width = total_width // valid_image_count if valid_image_count else 0

    if average_height == 0 or average_width == 0:
        print("没有找到有效的图片，或图片宽度/高度为零。")
        return

    # 调整所有图片的大小，使它们的宽度为平均宽度，高度保持不变
    for path in image_paths:
        try:
            with Image.open(path) as img:
                new_width = average_width
                new_height = average_height
                resized_img = img.resize((new_width, new_height), Image.LANCZOS)
                resized_img.save(path)
        except Exception as e:
            print(f"调整图片 {path} 大小时出错: {e}")

    prefix_map = {}

    # 拼接最大和最小图片
    for path in image_paths:
        prefix = os.path.splitext(os.path.basename(path))[0].rsplit("_", 1)[0]
        if prefix not in prefix_map:
            prefix_map[prefix] = {}

        if path.endswith("_largest.jpg"):
            prefix_map[prefix]["largest"] = path
        elif path.endswith("_smallest.jpg"):
            prefix_map[prefix]["smallest"] = path

    for prefix, files in prefix_map.items():
        if "largest" in files and "smallest" in files:
            try:
                with Image.open(files["largest"]) as largest_img, Image.open(files["smallest"]) as smallest_img:
                    spacing = largest_img.width // 10
                    new_width = largest_img.width + spacing + smallest_img.width
                    new_img = Image.new("RGB", (new_width, average_height))
                    new_img.paste(largest_img, (0, 0))
                    new_img.paste(smallest_img, (largest_img.width + spacing, 0))
                    new_img.save(os.path.join(directory, f"{prefix}.jpg"))
                    os.remove(files["largest"])
                    os.remove(files["smallest"])
            except Exception as e:
                print(f"拼接图片 {prefix} 时出错: {e}")

    # 纵向拼接的部分
    single_item_images = {}

    for path in glob.glob(os.path.join(directory, "*.jpg")):
        filename = os.path.basename(path)
        parts = filename.split("_")
        if len(parts) > 1 and parts[-1].endswith("分增减.jpg"):
            try:
                item_number = int(parts[-1].replace("分增减.jpg", ""))
                if 1 <= item_number <= 10:
                    prefix = parts[0]
                    if prefix not in single_item_images:
                        single_item_images[prefix] = {}
                    single_item_images[prefix][item_number] = path
            except ValueError:
                pass

    for prefix, items in single_item_images.items():
        sorted_items = sorted(items.items())
        if len(sorted_items) > 0:
            try:
                total_height = 0
                image_list = []
                for _, path in sorted_items:
                    try:
                        img = Image.open(path)
                        if img is None:
                            print(f"警告：无法打开图片 {path}，跳过。")
                            continue
                        total_height += img.height
                        image_list.append(img)
                    except Exception as inner_e:
                        print(f"打开图片 {path} 时发生错误：{inner_e}")
                        continue

                if not image_list:
                    print(f"警告：前缀 {prefix} 没有有效的图片，跳过。")
                    continue

                new_img = Image.new("RGB", (image_list[0].width, total_height))
                y_offset = 0
                for img in image_list:
                    new_img.paste(img, (0, y_offset))
                    y_offset += img.height

                new_img.save(os.path.join(directory, f"{prefix}_单项.jpg"))
                for _, path in sorted_items:
                    os.remove(path)

            except Exception as e:
                print(f"拼接单项图片 {prefix} 时出错：{e}")

if __name__ == "__main__":
    directory = "year_end_report"
    resize_images(directory)
    print("处理完成。")
