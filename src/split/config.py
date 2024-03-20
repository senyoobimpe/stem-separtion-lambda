import pathlib
from pathlib import Path
import os

from pydantic_settings import BaseSettings
from pydantic import  DirectoryPath
from tomlkit import parse


root_dir = pathlib.Path(__file__).parent.resolve()


# model_dir = root_dir / "./models/"
# data_dir =  root_dir / "./data/"
# static_dir = root_dir / "./"
# tmp_dir = root_dir / "./tmp"
model_dir = "/tmp/models/"
data_dir =  "/tmp/data/"
static_dir = "/tmp/"
tmp_dir = "/tmp/"
print(f'ROOT:::{root_dir}')

class Settings(BaseSettings):
    try:
        os.mkdir(model_dir)
        os.mkdir(data_dir)
        os.mkdir(tmp_dir)

        os.mkdir(static_dir)
    except Exception as e :
        print(e)
    model: DirectoryPath = model_dir
    data: DirectoryPath = data_dir
    static: DirectoryPath = static_dir
    docker: bool = False

    class Config:
        env_prefix = "demucs_"




settings = Settings()

settings_file = root_dir / Path("settings.toml")
if settings_file.exists():
    file_settings = parse(settings_file.read_text())
    settings = Settings.parse_obj(file_settings)