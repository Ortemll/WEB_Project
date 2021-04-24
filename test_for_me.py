import vk_api
from vk_api import *
import requests


def auth_handler():
    key = input()
    remember_device = True
    return key, remember_device


def main():
    vk_session = vk_api.VkApi(
        token='8ba6aa5d8ada2d6926e5244114983100e4cad74591e72fbaa6716d2556521ea310a976eba6b1d11b85d78'
    )
    vk = vk_session.get_api()
    response = vk.users.get(vk_id=452858725)
    print(response)


if __name__ == '__main__':
    a = requests.get('https://vk.com/3423406709951')
    if not a:
        print("ADIOS")
    elif a:
        print('No_ADIOS')
    print([a])
    main()
