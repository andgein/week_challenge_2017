import glob

files = glob.glob('libverse.ru/*/*.html')

with open('libverse.ru.txt', 'w', encoding='utf-8') as output:
    for filename in files:
        with open(filename, encoding='windows-1251') as f:
            try:
                output.write(f.read())
            except:
                pass
                