import paramiko
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--host", type=str)
parser.add_argument("--serverUsername", type=str)
parser.add_argument("--password", type=str)
parser.add_argument("--executePath", type=str, default=None)
parser.add_argument("--cmd", type=str, default=None)

args, undefine_args = parser.parse_known_args()

execute_args = ' '.join(undefine_args)

trans = paramiko.Transport((args.host, 22))

trans.connect(username=args.serverUsername, password=args.password)

with paramiko.SSHClient() as ssh:
    ssh._transport = trans
    # 执行命令，和传统方法一样
    if args.executePath:
        cmd = args.executePath + ' ' + execute_args
        if args.executePath.endswith('.ps1'):
            cmd = 'powershell ' + cmd
    else:
        cmd = args.cmd

    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)

    while not stdout.channel.exit_status_ready():
        result = stdout.readline()
        print(result)
        # 由于在退出时，stdout还是会有一次输出，因此需要单独处理，处理完之后，就可以跳出了
        if stdout.channel.exit_status_ready():
            a = stdout.readlines()
            print(a)
            break
