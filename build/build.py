import sys
import os
import subprocess
import codecs

#- Парсинг аргументов командной строки
args = sys.argv[1:]
filepath = args[0]
discipline = filepath.split('/')[-2]
filename = filepath.split('/')[-1]
clearname = filename.strip(".md")

#- Задание аггрегирующего tex-файла для сборки
template = """
\\documentclass[12pt,a4paper,oneside,final]{{report}} 
\\input{{thesis-template-macro}}
\\pagenumbering{{arabic}}
\\usepackage{{graphicx}}
\\usepackage{{setspace}}
\\usepackage{{{}/title}}
\\title{{{}}}
\\begin{{document}}
    \\maketitle
    \\tableofcontents
    \\newpage
    \\input{{{}}}
\\end{{document}}
"""

#- Заголовок документа в зависимости от названия документа 
title_map = {
    "CMP":"План управления конфигурацией",
    "DP":"План разработки",
    "VP":"План верификации",
    "Paper":"Разработка лабораторного комплекса по курсу «Дискретная математика (логические исчисления)»",
    "SSRD":"System and Software Requirements Document"
}

#- Создание необходимых для билда tex-файлов
template = template.format(discipline, title_map[clearname], discipline + '/' + clearname)
with codecs.open('./.latex/' + clearname + '.tex', 'w', 'utf-8') as tex_template:
    tex_template.write(template)
subprocess.run(["node", "build.js", filepath])

os.chdir(".latex")

#- Дополнительная обработка документа
document = []
with codecs.open('./' + discipline + '/' + clearname + '.tex', 'r', 'utf-8') as tex_content:
    document = tex_content.readlines()
    #-- Поднятие заголовков на уровень вверх
    document = [ 
        line.replace("\\section{","\\chapter{").replace("\\subsection{", "\\section{").replace("\\subsubsection{", "\\subsection{").replace("\\paragraph{", "\\subsubsection{")
        for line in document
    ]
    #-- Задание размера картинок
    imagemapper = {}
    with codecs.open('imagemapper.txt', 'r', 'utf-8') as imgmapfile:
        imgmapfilelines = imgmapfile.readlines()
        imagemapperlist = [[item.strip(' \r\n') for item in line.split('=')] for line in imgmapfilelines]
        for pair in imagemapperlist:
            imagemapper[pair[0]] = pair[1]
    for i in range(len(document)):
        #--- Установка ширины изображений
        def set_width():
            line = document[i]
            includegraphics_word = '\\includegraphics'
            pos = line.find(includegraphics_word)
            if pos == -1:
                return
            rbrace_index = line.find(r'}', pos) # ошибка не обрабатывается
            image_name = line[pos + len(includegraphics_word) + 1 : rbrace_index]
            image_name = image_name.split('/')[-1]
            image_width = imagemapper[image_name]
            parts = line.split(includegraphics_word) # предполагается только 2 элемента
            document[i] = parts[0] + includegraphics_word + '[width=' + image_width + ']' + parts[1]
        #--- Установка места отрисовки картинки
        def set_figure_place():
            line = document[i]
            figure_word = r'\begin{figure}'
            pos = line.find(figure_word)
            if pos == -1:
                return
            parts = line.split(figure_word)
            document[i] = parts[0] + figure_word + '[h]' + parts[1]
        set_width()
        set_figure_place()

#-- Фиксирование результатов обработки
with codecs.open('./' + discipline + '/' + clearname + '.tex', 'w', 'utf-8') as tex_content:
    for line in document:
        tex_content.write(line)

#- Окончательный билд документов
subprocess.run(["latexmk", "-time", "-xelatex", "-silent", "-outdir=../{}/pdf".format(discipline), "-gg", clearname + ".tex"])

#- Чистка временных файлов
subprocess.run(["latexmk", "-c", "-silent", "-outdir=../{}/pdf".format(discipline)])
os.chdir("../")
os.remove(".latex/"+clearname+".tex")
