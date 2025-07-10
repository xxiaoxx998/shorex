import hashlib
import datetime
import os
import subprocess


def get_six_digits():
    """获取用户输入的6位数字"""
    while True:
        user_input = input("请输入6位签到码数字 (直接回车使用随机生成): ").strip()
        if not user_input:
            import random
            return str(random.randint(100000, 999999))
        if user_input.isdigit() and len(user_input) == 6:
            return user_input
        print("输入错误！请输入6位纯数字。")


def generate_checkin_code(six_digits):
    """生成完整的签到码"""
    base_number = "id"
    suffix = "roomnumber"
    raw_code = base_number + six_digits + suffix
    md5_hash = hashlib.md5(raw_code.encode("utf-8"))
    return md5_hash.hexdigest()


def save_to_file(checkin_code, six_digits):
    """将签到码保存到固定目录"""
    today = datetime.date.today().strftime("%Y-%m-%d")
    save_path = r"git-command-path"  # 固定保存路径

    # 确保目录存在
    os.makedirs(save_path, exist_ok=True)

    # 构建文件名
    file_name = f"{today}"
    file_path = os.path.join(save_path, file_name)

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"{checkin_code}")
        print(f"\n签到码已保存到: {file_path}")
        return file_path
    except Exception as e:
        print(f"保存文件失败: {e}")
        return None


def execute_git_commands(file_path, branch_name="yourbranch"):
    """执行Git命令提交签到码"""
    if not file_path:
        print("没有文件可提交")
        return False

    # 获取文件名和目录
    directory = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    today = datetime.date.today().strftime("%Y-%m-%d")

    try:
        # 定义Git命令
        commands = [
            ["git", "add", file_name],
            ["git", "commit", "-m", f"Sign-in for {today}"],
            ["git", "push", "origin", branch_name]
        ]

        # 在文件所在目录执行Git命令
        for cmd in commands:
            result = subprocess.run(
                cmd,
                cwd=directory,
                capture_output=True,
                text=True,
                check=True
            )
            print(f"执行命令: {' '.join(cmd)}")
            if result.stdout:
                print(f"  输出: {result.stdout.strip()}")

        print("\n✅ Git提交成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Git命令执行失败: {e.stderr.strip()}")
        return False
    except Exception as e:
        print(f"\n❌ 发生未知错误: {e}")
        return False


if __name__ == "__main__":
    six_digits = get_six_digits()
    checkin_code = generate_checkin_code(six_digits)

    print(f"\n原始字符串: id + {six_digits} + roomnumber")
    print(f"MD5 签到码: {checkin_code}")

    # 保存到文件
    file_path = save_to_file(checkin_code, six_digits)

    # 询问是否执行Git提交
    if file_path:
        confirm = input("\n是否执行Git提交? (y/n): ").strip().lower()
        if confirm == 'y':
            execute_git_commands(file_path)
