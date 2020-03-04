from api import get_qrcode
from qr_code import qr_code_reader


def main():
    code = get_qrcode()
    qr_code_reader(code)


if __name__ == '__main__':
    main()
