from cx_Freeze import setup, Executable

setup(
    name='LukiChat',
    version='1.0',
    executables=[Executable("client.py")])
