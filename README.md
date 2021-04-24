
<h3 align="center">Сайт для просмотра ониме</h3>

<div>

![Liness of code](https://img.shields.io/tokei/lines/github/lk2322/Super_Secret_Anime_Project)

</div>

---
## 🧐 О проекте <a name = "about"></a>

Сайт на flask, с помощью которого можно просматривать аниме
Функции:
- Регистрация и логин
- Система ролей для управления сайтом (админы)
- Полное управление сайтом через админку
- Удобный плеер для просмотра

## 🏁 Установка <a name = "getting_started"></a>
```
git clone https://github.com/lk2322/Super_Secret_Anime_Project
cd Super_Secret_Anime_Project
pip install -r requirements.txt
```
В config.ini необходимо заменить secret_key и ids(список пользователей, которым нужно выдать админку)
### Установка ffmpeg и ffprobe
#### Windows
[Скачайте](https://www.gyan.dev/ffmpeg/builds) билд ffmpeg для Windows и расположите ffmpeg.exe и ffprobe.exe в корне проекта
#### Linux
Установите привычным способом ffmpeg(необходимо, чтобы он был в PATH)



## 🎈 Использование <a name="usage"></a>
Для запуска со стандартным сервером Flask
```
python app.py
```


## ✍️ Автор <a name = "authors"></a>

- [@lk2322](https://github.com/lk2322)
