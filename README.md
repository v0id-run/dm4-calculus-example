# DM4-LogicalCalculus.Docs

## Требования
1. Установить VSCode.
2. Установить расширение *Markdown Preview Enhanced* от *Yiyi Wang*.
3. Залезть в *Settings* (*Ctrl+,*) -> *Extensions* -> *Markdown Preview Enhanced* и установить:
    - Math Rendering Option: `katex`
    - Math Inline Delimiters: добавить в файл следующую строку: 
    ```code
    "markdown-preview-enhanced.mathInlineDelimiters": [["$","$"]]
    ```
4. Перезагрузить VSCode.
5. Установить расширение *Code Spell Checker*. А также дополнение к нему - *Russian - Code Spell Checker*.
6. Активировать проверку русской орфографии теперь можно так: *Ctrl+Shift+P* $`\to`$ *Enable Russian Spell Cheker Dictionary*.

## Руководства
* Справка по [markdown](https://paulradzkov.com/2014/markdown_cheatsheet/).
* Руководство по используемому [markdown-расширению](https://shd101wyy.github.io/markdown-preview-enhanced/#/).

# Как вносить изменения в репозиторий

**В первый раз:**
1. Открыть консоль и перейти в какую-нибудь папку, где будет храниться код проекта.
1. Склонировать репозиторий:
    ```bash
    git clone https://gitlab.com/mephi-b16-504/dm4-logicalcalculus.docs.git
    ```
1. Открыть папку `dm4-logicalcalculus.docs` в vscode через *File->Open Folder*.
1. Открыть терминал, встроенный в vscode через *Terminal->New Terminal*.
1. Проверить состояние репозитория через
    ```bash
    git status
    ```
1. Если нет ошибок, то всё хорошо.
1. Для нормального использования git с русскими названиями папок и файлов ввести:
    ```bash
    git config core.quotepath false
    ```

**При выполнении очередной таски:**
1. Проверить, что вы находитесь в ветке мастер, исходя из вывода команды
    ```bash
    git status
    ```
    Должно быть написано что-то вроде "on branch master" в самом верху.
1. Зайти внутрь таски, нажать на кнопку *Create merge request*. В этот момент для таски создастся собственная ветка. Обычно она будет иметь название `<номер таски>-`.
1. После сделать 
    ```bash
    git pull
    ```
1. В локальном репозитории переключиться на созданную ветку:
    ```bash
    git checkout <название ветки>
    ```
    Пока висит мерж-реквест, можно звать народ на обсуждение таски, в целом вносить изменения.
1. Далее пишется текст в заданный в таске файл. Затем нужно добавить изменения через:
    ```bash
    git status
    git add <путь до файла>
    ```
    Если в git status видно, что изменён только один файл (или только те файлы, которые нужно изменить), то можно написать:
    ```bash
    git add --all
    ```
1. После этого нужно закоммитить:
    ```bash
    git commit -m "<текст сообщения>"
    ```
1. Соглашение о тексте сообщения в коммитах: "Issue #<номер таски>: <что сделано кратко по-английски>". Пример: `Issue #666: requirement rule updated`.
1. После нужно запушить коммит в гитлаб и убрать из названия merge request префикс `WIP:`, после чего таска считается выполненной:
    ```bash
    git push
    ```
1. Далее @iMashtak или кто-либо другой будет проводить ревью, оставлять замечания.
1. В конце нужно не забыть переключиться обратно на ветку мастер:
    ```bash
    git checkout master
    ```