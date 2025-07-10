import sys
import re


def analyze_file(file_path):
    """读取文本文件并分析行、单词和字符数量"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

            # 统计行数
            line_count = len(lines)

            # 连接所有行以进行单词和字符统计
            content = ''.join(lines)

            # 使用正则表达式匹配所有单词
            words = re.findall(r'\b\w+\b', content)
            word_count = len(words)

            # 统计字符数（包括空格和换行符）
            char_count = len(content)

            return {
                'lines': line_count,
                'words': word_count,
                'characters': char_count
            }
    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 不存在")
        return None
    except Exception as e:
        print(f"错误: 无法读取文件 - {str(e)}")
        return None


def main():
    """主函数，程序入口点"""
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("用法: python text_analyzer.py <文件路径>")
        sys.exit(1)

    file_path = sys.argv[1]
    stats = analyze_file(file_path)

    if stats:
        print(f"文件统计信息: {file_path}")
        print(f"  行数: {stats['lines']}")
        print(f"  单词数: {stats['words']}")
        print(f"  字符数: {stats['characters']}")


if __name__ == "__main__":
    main()