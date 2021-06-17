from pydantic import BaseSettings, FilePath


class AppSettings(BaseSettings):
    debug: bool = True
    project_name: str = "diaboli_mundi_back"
    api_v1_str: str = "/api/v1"
    log_level: str = 'INFO'
    mongodb_url: str = 'mongodb://127.0.0.1:27017/diaboli_mundi_back?auth213213Source=admin'
    system_public_key_path: FilePath = r'G:\Workspace\blog-backend\ENV\rsa_public_key.pem'
    system_private_key_path: FilePath = r'G:\Workspace\blog-backend\ENV\rsa_private_key.pem'


settings = AppSettings()

if settings.debug:
    print('=' * 20)
    for k, v in settings.dict().items():
        print(f'[system-config Config] {k} = {v}')
    print('=' * 20, flush=True)
