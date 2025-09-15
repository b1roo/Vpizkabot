start_text = ('🙋‍♂️ Привет!'
              '\n\nЭто бот *Vpizki* для удобного использования конспектов, дз и ещё чего нибудь'
              '\n\n🔹 /notes -- конспекты'
              '\n🔹 /hwfiles -- файлы дз'
              '\n🔹 /allfiles -- все загруженные в бота файлы'
              '\n\n❓ По предложениям для бота пишите [сюда](https://t.me/arust_dav)')

notes_text = ('📚 *Тут представлены все конспекты по дисциплинам, разделённые на курсы* '
              '\n\n🎓1 курс'
              '\n🔹 [Парадигмы языков программирования](https://docs.google.com/document/d/1ZXtE6CzU16tITnMxE4piOwzXqou50iLYs2nXM4TweEM/edit?usp=sharing)'
              '\n🔹 [Введение в программную инженерию](https://docs.google.com/document/d/1JhO_1VTSPNd-XFe26N43coXCH0xGaYVq5T3Qn09B3Qk/edit?usp=sharing)'
              '\n🔹 [История России](https://docs.google.com/document/d/1MaPZQZh4yLjPIAZ3g1lJYrX_pPf33nZp7V1Z_VNzVrk/edit?usp=sharing)'
              '\n🔹 [Методология профессиональной деятельности - зачёт](https://docs.google.com/document/d/1t6KLGIary6rcuvy4WUoyjzL9F89-o6g7PBAom5JStlc/edit?usp=sharing)'
              '\n🔹 [Алгоритмы и структуры данных - экз](https://docs.google.com/document/d/1a4ou-_9-BNKlkTXZWVe6kiX_aR_l0ZAR/edit?usp=sharing&ouid=102503748029941178599&rtpof=true&sd=true)'
              '\n\n🎓2 курс'
              '\n🔹 [Русский язык и культура речи](https://docs.google.com/document/d/1-BhyeqoABLtoT5QiVpoMlv-EePHYCvY09xbGV7mvlvg/edit?usp=sharing)'
              '\n🔹 [Психология](https://docs.google.com/document/d/10sJjhM0F8_Zd_NV87yKrEln5Bz0bjJO0aRFOhXLMGeE/edit?usp=sharing)'
              '\n🔹 [Социология](https://docs.google.com/document/d/117MLNEERUi_1Rr2-XLrmDPUyLZkSjen1OAM5cUn5bAM/edit?usp=sharing)'
              '\n🔹 [Концепция современного естествознания](https://docs.google.com/document/d/113sPjAJuUswHCVkkoLB0tn-XbUDo7effbQeLmMS-aDg/edit?usp=sharing)'
              '\n🔹 [ТРПО](https://docs.google.com/document/d/11lWxgRAiKahe9Rh_wumh0LaIGCaKkCbK8wETYbZSACo/edit?usp=sharing)'
              '\n🔹 [ОРГ](https://docs.google.com/document/d/14xTvaqrC6bsXVTZ5y66A3CZgEkdTZPziQWaOzg8zzwg/edit?usp=sharing)'
              '\n🔹 [ЭВМ](https://docs.google.com/document/d/11nLQzRagT8pUu-snuCcxXEW0qsXr9xwv_Lvg_tMGoqs/edit?usp=sharing)'
              '\n\n❓ По секрету - всё кликабельно)'
              '')

homework_files_text = ('📚 Домашние задания'
                 '\n\nВыберите предмет:')

all_files_text = ('Тут представлены все файлы, загруженные в бота ранее. Вы также можеет загрузить файл сами)')

search_files_text = ('Выберите предмет')

#Важно, что key совпадал с названием папки, в которой находятся файлы
#Название не должно быть слишком большим
subjects_homework = {
    'russian': 'Русский язык',
    'psychology': 'Психология',
    'osys': 'Операционные системы',
    'infotech': 'ИТ',
    'TRPO': 'ТРПО',
    'other': 'Другое'
}

file_path_homework = 'homework_files'

subjects_others = {
    'osys': 'ОС',
    'asd': 'АСД',
    'infotech': 'ИТ',
    'TRPO': 'ТРПО',
    'IBM': 'ЭВМ'
}

file_types_others = {
    'KR': 'Курсовая работа',
    'LR': 'Лабораторные работы',
    'PPT': 'Презентации',
    'OTHER': 'Другие материалы'
}

file_path_others = 'other_files'
in_others_key = ['KR', 'LR', 'PPT', 'OTHER']

add_file_text = "📤 Добавить файл"
back_text = "◀️ Назад"

FILES_PER_PAGE = 8  # Количество файлов на одной странице
HOMEWORK_FILES_PER_PAGE = 8  # Для домашних работ

admins_id = [1135316756, 1044378766]


