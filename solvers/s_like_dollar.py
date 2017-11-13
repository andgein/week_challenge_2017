from weekchallenge import *


class Solver(TaskSolver):
    type_name = 's-like-$'

    def __init__(self):
        self.descriptions = []
        with open('files/s_like_$.txt', encoding='utf-8') as f:
            for line in f:
                splitted = line.strip().split()
                if len(splitted) < 2:
                    continue

                char, description = splitted[0], ' '.join(splitted[1:])
                self.descriptions.append((char, description))

    def solve(self, task):
        splitted = task.value.split(';')
        answer = ''
        for part in splitted:
            part = part.strip()
            if part == 'пробел':
                answer += ' '
                continue

            upper_case = False
            if part.endswith(' большенькая'):
                upper_case = True
                part = part.replace(' большенькая', '')

            Logger.info('Looking for "%s" in descriptions list' % part)
            for char, description in self.descriptions:
                if description == part:
                    if upper_case:
                        answer += char.upper()
                    else:
                        answer += char
                    break
            else:
                Logger.error('Not found "%s" in descriptions list' % part)
        return answer

    
    def tests(self):
        return [
            ('пэ, как русская эр; дефис; как «к» с палочками; двоеточие; знак вопроса', 'p-k:?'),
            ('кавычка… ну… такая, как два меньше; эс как Супермен; о — как зеркальце; эм — как расчёска; как русская «e»; пробел; как Макдональдс; о — как зеркальце; русская «и» наоборот; как русская «e»; как русская у,; кавычка… ну… такая, как два больше', '«some money»'),
            ('больше; меньше; машинописная кавычка; карет; больше; dollar sign', '><"^>$'),
            ('тэ как могильный крестик; хэк; крестик плюс; перевёрнутая «г» когда заглавная; кавычка универсальная; тюрьма; как русская эр наоборот; ку, как флажок налево; б «как палочка такая, и животик как бы вправо смотрит»', r't\+l"#qqb'),
('левая скобочка; тире; икс; «и украинская»; средний дефис; тэ как могильный крестик', '(—xi-t'),
('двоеточие; жесткий_пробел; как «н» русская когда заглавная; эс как Супермен; хэ русская; как значок «Опеля»; a как русская', ':_hsxza'),
('первёрнутая «М», как значок «Volkswagen»; точка с запятой; обратный слеш; первёрнутая «М», как значок «Volkswagen»; перевёрнутый восклицательный знак; тэ как могильный крестик; тэ как могильный крестик; как «у» подковкой; как тросточка; тэ как зонтик сломанный; тюрьма; саблайн; «бэ как пудреница, влево открытая»', r'w;\witturt#_b'),
('ухо; как русская сэ; процент; как русская «e»; б «как палочка такая, и животик как бы вправо смотрит»; запятая; эф как флажок; кружочком; кавычка универсальная; перевёрнутый восклицательный знак', '@c%eb,fo"i'),
('плюсик; такая запятая над буквами; ка русская; тюрьма; правая скобочка; знак вопроса; крестик плюс; как букетик; пробел; знак вопроса; двоеточие; эль — «большая палочка»; дубльвэ как две галочки; обратный слеш', '+\'k#)?+v ?:lw\\'),
('падающая вправо; о — как зеркальце; точка с запятой; как «у» подковкой; крышка от домика; запятая; эс как доллар; жесткий_пробел; б «как палочка такая, и животик как бы вправо смотрит»; обратный слеш; русская «и» наоборот; эль — «большая палочка»; хэ русская; эм — как расчёска; как «у» подковкой; «а» в кружочке; зэт как Зорро; правая скобочка; пробел; тюрьма', '/o;u^,s_b\\nlxmu@z) #'),
('машинописная кавычка; жесткий_пробел; b в другую сторону; закрывающая круглая скобка; средний дефис; эс как Супермен; падающая вправо; правая скобочка', '"_d)-s/)'),
('латинская и с точкой большенькая; пробел; как номер; как русская «e»; как букетик; как русская «e»; как тросточка', 'I never'),
('эс как ЕВРО без палочки; a как русская; тэ как зонтик сломанный; как русская сэ; как «н» русская когда заглавная; пробел; a как русская; русская «и» наоборот; рогатка.; тэ как могильный крестик; аш как постоянная Планка; «и украинская»; эн — как русская пэ; хэк; пробел; русская «и» наоборот; о — как зеркальце; первёрнутая «М», как значок «Volkswagen»; обратный слеш', 'catch anythin\\ now\\'),
('как русская сэ; зэт как Зорро; процент; тэ как зонтик сломанный; запятая; палочка с точечкой; вэ как галочка; эль — «большая палочка»; вэ-победа; линия такая волнистая (она на букве ё); улитка; о — как зеркальце; dollar sign; «к как наша»; как значок «Опеля»; русская «и» наоборот; как флажочек направо; «бэ как пудреница, влево открытая»; как «к» с палочками', 'cz%t,ivlv~@o$kznpbk'),
('тэ как могильный крестик большенькая; аш как постоянная Планка; как русская «e»; пробел; как русская сэ; как гэ; игрек; эс как интеграл; тэ как зонтик сломанный; a как русская; перевёрнутая «г» когда заглавная', 'The crystal'),
('как русская у,; как тросточка; процент; русская «и» наоборот; кавычка… ну… такая, как два меньше; тире', 'yr%n«—'),
('у как русская и; тире; о — как зеркальце; палочка; закрывающая круглая скобка; хэ русская; как значок «Опеля»; джи как гугл; закрывающая угловая скобка', 'u—o/)xzg>'),
('аш как постоянная Планка большенькая; a как русская; как гэ; как тросточка; рогатка.; пробел; как флажочек направо большенькая; о — как зеркальце; тэ как могильный крестик; тэ как могильный крестик; как русская «e»; как тросточка', 'Harry Potter'),
('кавычка… ну… такая, как два меньше; как флажочек направо большенькая; перевёрнутая «г» когда заглавная; как русская «e»; a как русская; эс как Супермен; как русская «e»; пробел; первёрнутая «М», как значок «Volkswagen»; a как русская; перевёрнутый восклицательный знак; тэ как могильный крестик; пробел; ку, как флажок налево; как пэ верх ногами; «и украинская»; как русская «e»; тэ как могильный крестик; эль — «большая палочка»; как русская у,; кавычка… ну… такая, как два больше', '«Please wait quietly»'),
('запятая; карет; ку, как флажок налево; точка; йот как поварёшка; эн — как русская пэ; палочка с точечкой; обезьяна; кружочком; виктори; ка русская', ',^q.jni@ovk'),
('кавычка… ну… такая, как два меньше; a как русская большенькая; эн — как русская пэ; как русская у,; о — как зеркальце; русская «и» наоборот; как русская «e»; пробел; эс как доллар; латинская и с точкой; тэ как зонтик сломанный; тэ как зонтик сломанный; латинская и с точкой; эн — как русская пэ; джи как гугл; пробел; тэ как зонтик сломанный; Н как водород; как русская «e»; как тросточка; как русская «e»; знак вопроса; кавычка… ну… такая, как два больше', '«Anyone sitting there?»'),
('запятая; «бэ как русская р вверх тормашками»; там, где русская «п» на клавиатуре; рогатка.; левая скобочка; a как русская; пробел; плюсик; как русская эр наоборот; как флажочек направо', ',bgy(a +qp'),
('как русская у,; процент; двоеточие; запятая; как русская сэ; карет; слеш; кружочком; меньше; кавычка… ну… такая, как два больше; аш как постоянная Планка; запятая', 'y%:,c^/o<»h,'),
        ]

        """
('Н как водород большенькая; a как русская; как тросточка; как гэ; рогатка.; пробел; тэ как могильный крестик; о — как зеркальце; эль — «большая палочка»; b в другую сторону', ''),
('карет; пэ, как русская эр; эф английская (гэ с палочкой); рогатка.; первёрнутая «М», как значок «Volkswagen»; консоль; ку, как флажок налево; крючочек с точечкой; кавычка… ну… такая, как два меньше; средний дефис; знак вопроса; перевёрнутая «г» когда заглавная; фембэкслеш; как «у» подковкой; циркумфлекс; кавычка… ну… такая, как два больше; b в другую сторону; эс как доллар; «бэ как русская р вверх тормашками»', ''),
('двоеточие; точка с запятой; игрек; как русская сэ; пробел; тире; «Джей Севен» (сок в коробке); процент; клюшка; как гэ; палочка с точечкой; запятая', ''),
('больше; точка; астериск; андерстрайк; эс как ЕВРО без палочки; тэ как зонтик сломанный; «к как наша»; как тросточка; «к как наша»; знак вопроса; джи как гугл; эф как флажок; кавычка… ну… такая, как два больше', ''),
('«а» в кружочке; a как русская; аш — как стульчик такой; кавычка… ну… такая, как два больше; хэ русская; коммерческое at.; икс; звездочка; как «у» подковкой; упавший минус; как значок «Опеля»; игрек; двоеточие; коммерческое «и»', ''),
('точка с запятой; падающая вправо; как номер; открывающая угловая скобка; восьмерка с закорючкой; коммерческое «и»; как букетик; жесткий_пробел; как пэ верх ногами; знак вопроса; пробел; как русская «e»; тэ как зонтик сломанный; тильда', ''),
('дефисоминус; звездочка; аш как постоянная Планка; как Макдональдс; кавычка… ну… такая, как два больше; как пэ верх ногами; «бэ как русская р вверх тормашками»; фембэкслеш; закрывающая угловая скобка; открывающая круглая скобка; эс как доллар; игрек', ''),
('двоеточие; a как русская; перевёрнутая «г» когда заглавная; пробел; как номер; дэ как пудреница, вправо открытая; нижнее подчеркивание; машинописная кавычка; эф английская (гэ с палочкой); эн — как русская пэ; «бэ как русская р вверх тормашками»; эс как интеграл', ''),
('Н как водород большенькая; a как русская; как тросточка; как гэ; рогатка.; пробел; тэ как могильный крестик; о — как зеркальце; эль — «большая палочка»; b в другую сторону', ''),
('машинописная кавычка; запятая; вэ-победа; кавычка… ну… такая, как два меньше; слеш; конъюнкция; как значок «Опеля»; коммерческое «и»; аш как постоянная Планка; закрывающая круглая скобка', ''),
('Н как водород; как русская «e»; обратная косая черта; дэ как пудреница, вправо открытая; пробел; «как русская вэ»; как «я» наоборот; кружочком; у как русская и; джи как гугл; аш как постоянная Планка; тэ как зонтик сломанный', ''),
('плюсик; такая запятая над буквами; ка русская; тюрьма; правая скобочка; знак вопроса; крестик плюс; как букетик; пробел; знак вопроса; двоеточие; эль — «большая палочка»; дубльвэ как две галочки; обратный слеш', ''),
('тэ как могильный крестик большенькая; как «н» русская когда заглавная; как русская «e»; как тросточка; как русская «e»; пробел; первёрнутая «М», как значок «Volkswagen»; a как русская; эс как интеграл', ''),
('аш как постоянная Планка большенькая; a как русская; как «я» наоборот; как тросточка; игрек; пробел; эс как интеграл; первёрнутая «М», как значок «Volkswagen»; a как русская; эль — «большая палочка»; перевёрнутая «г» когда заглавная; кружочком; первёрнутая «М», как значок «Volkswagen»; как русская «e»; b в другую сторону', ''),
('эс как Супермен большенькая; аш — как стульчик такой; как русская «e»; пробел; тэ как могильный крестик; как «у» подковкой; как «я» наоборот; русская «и» наоборот; как русская «e»; b в другую сторону', ''),
('процент; Н как водород; a как русская; линия такая волнистая (она на букве ё); открывающая угловая скобка; кавычка универсальная; доллар как доллар; «Джей Севен» (сок в коробке); точка с запятой', ''),
('консоль; правая скобочка; зэт как Зорро; двоеточие; вэ-победа; пэ, как русская эр; процент; точка с запятой; икс; виктори; b в другую сторону; пробел', ''),
('кружочком большенькая; как флажочек направо; как русская «e»; русская «и» наоборот; прямая косая черта; как русская сэ; перевёрнутая «г» когда заглавная; о — как зеркальце; эс как интеграл; как русская «e»; b в другую сторону', ''),
('астериск; закрывающая круглая скобка; меньше; плюсик; перевёрнутый восклицательный знак; палочка; решеточка; ка русская; a как русская; андерстрайк; машинописная кавычка; ка русская; как «к» с палочками; кавычка… ну… такая, как два меньше; кавычка… ну… такая, как два меньше; процент; эс как интеграл', ''),
('правая скобочка; русская «и» наоборот; дефис; как пэ верх ногами; больше', ''),
('как русская у,; как тросточка; процент; русская «и» наоборот; кавычка… ну… такая, как два меньше; тире', ''),
('запятая; «бэ как русская р вверх тормашками»; там, где русская «п» на клавиатуре; рогатка.; левая скобочка; a как русская; пробел; плюсик; как русская эр наоборот; как флажочек направо', ''),
('эф английская (гэ с палочкой); точка; амперсанд; треугольные скобки; вэ как галочка; знак вопроса; первёрнутая «М», как значок «Volkswagen»; точка; прямая косая черта; dollar sign', ''),
('карет; как Макдональдс; коммерческое at.; пэ, как русская эр; у как русская и; треугольные скобки; a как русская; ручка у зонтика; икс; процент; амперсанд; кружочком; андерскор; запятая; эф английская (гэ с палочкой); звездочка; кавычка… ну… такая, как два больше; крестик плюс; запятая', ''),
('карет; пэ, как русская эр; эф английская (гэ с палочкой); рогатка.; первёрнутая «М», как значок «Volkswagen»; консоль; ку, как флажок налево; крючочек с точечкой; кавычка… ну… такая, как два меньше; средний дефис; знак вопроса; перевёрнутая «г» когда заглавная; фембэкслеш; как «у» подковкой; циркумфлекс; кавычка… ну… такая, как два больше; b в другую сторону; эс как доллар; «бэ как русская р вверх тормашками»', ''),
('падающая вправо; о — как зеркальце; точка с запятой; как «у» подковкой; крышка от домика; запятая; эс как доллар; жесткий_пробел; б «как палочка такая, и животик как бы вправо смотрит»; обратный слеш; русская «и» наоборот; эль — «большая палочка»; хэ русская; эм — как расчёска; как «у» подковкой; «а» в кружочке; зэт как Зорро; правая скобочка; пробел; тюрьма', ''),
('двоеточие; точка с запятой; игрек; как русская сэ; пробел; тире; «Джей Севен» (сок в коробке); процент; клюшка; как гэ; палочка с точечкой; запятая', ''),
('эн — как русская пэ; обратный слеш; обратный слеш; снежинка звёздочка; кружочком; перевёрнутая «г» когда заглавная; консоль; плюсик; двоеточие; машинописная кавычка; как русская тэ; точка с запятой', ''),
('знак вопроса; перевёрнутая «г» когда заглавная; собачка; тюрьма; пробел; a как русская; больше; дефисоминус; джи как гугл; консоль; процент; джи как гугл; точка; как русская эр наоборот; фембэкслеш', ''),
('процент; как номер; «б как мягкий знак»; как флажочек направо; как гэ; тэ как зонтик сломанный; точка с запятой; тэ как зонтик сломанный; линия такая волнистая (она на букве ё); как русская «e»; точка; средний дефис; эф как флажок', ''),
('двоеточие; a как русская; перевёрнутая «г» когда заглавная; пробел; как номер; дэ как пудреница, вправо открытая; нижнее подчеркивание; машинописная кавычка; эф английская (гэ с палочкой); эн — как русская пэ; «бэ как русская р вверх тормашками»; эс как интеграл', ''),
('тэ как могильный крестик большенькая; как «н» русская когда заглавная; как русская «e»; как тросточка; как русская «e»; пробел; первёрнутая «М», как значок «Volkswagen»; a как русская; эс как интеграл', ''),
('эф как флажок; машинописная кавычка; зэт как Зорро; эс как ЕВРО без палочки; конъюнкция; a как русская; дефисоминус; открывающая угловая скобка; пробел; тильда; эль — «большая палочка»; циркумфлекс; как русская эр наоборот; «а» в кружочке', ''),
('кружочком; «б как мягкий знак»; йот как поварёшка; как русская «e»; как русская сэ; тэ как могильный крестик; дефисоминус; кружочком; как «я» наоборот; палочка с точечкой; как русская «e»; русская «и» наоборот; тэ как могильный крестик; как русская «e»; дэ как пудреница, вправо открытая; пробел; дэ как пудреница, вправо открытая; как русская «e»; эс как интеграл; палочка с точечкой; там, где русская «п» на клавиатуре; как номер', ''),
('как русская у,; процент; двоеточие; запятая; как русская сэ; карет; слеш; кружочком; меньше; кавычка… ну… такая, как два больше; аш как постоянная Планка; запятая', ''),
('кружочком; аш как постоянная Планка; sharp; дефис; меньше; как тросточка; дефис; тэ как зонтик сломанный; двоеточие; знак вопроса; эс как доллар; закрывающая угловая скобка', ''),
('у как русская и; тире; о — как зеркальце; палочка; закрывающая круглая скобка; хэ русская; как значок «Опеля»; джи как гугл; закрывающая угловая скобка', ''),
('йот как поварёшка; подчёркивание; b в другую сторону; слеш; тэ как зонтик сломанный; dollar sign; коммерческое at.; кавычка… ну… такая, как два больше; dollar sign; решеточка; кавычка универсальная; дубльвэ как две галочки; кавычка… ну… такая, как два меньше; закрывающая угловая скобка; ка русская; кружочком; тэ как зонтик сломанный', ''),
('кавычка… ну… такая, как два больше; улитка; о — как зеркальце; кавычка… ну… такая, как два меньше; как русская «e»; эс как интеграл; зэт как Зорро; пробел; кавычка… ну… такая, как два больше; тильда; точка с запятой; a как русская; первёрнутая «М», как значок «Volkswagen»; жесткий_пробел; саблайн', ''),
('двоеточие; a как русская; перевёрнутая «г» когда заглавная; пробел; как номер; дэ как пудреница, вправо открытая; нижнее подчеркивание; машинописная кавычка; эф английская (гэ с палочкой); эн — как русская пэ; «бэ как русская р вверх тормашками»; эс как интеграл', ''),
('дефис; двоеточие; обратная косая черта; тире; икс; тире; средний дефис; тюрьма; плюсик; как пэ верх ногами; первёрнутая «М», как значок «Volkswagen»; средний дефис', ''),
('как «н» русская когда заглавная; как русская у,; коммерческое at.; эс как доллар; кружочком; эс как Супермен; прямая косая черта; dollar sign; виктори; эф как флажок; крестик плюс', ''),
('как русская сэ; зэт как Зорро; процент; тэ как зонтик сломанный; запятая; палочка с точечкой; вэ как галочка; эль — «большая палочка»; вэ-победа; линия такая волнистая (она на букве ё); улитка; о — как зеркальце; dollar sign; «к как наша»; как значок «Опеля»; русская «и» наоборот; как флажочек направо; «бэ как пудреница, влево открытая»; как «к» с палочками', ''),
('кавычка… ну… такая, как два меньше; как флажочек направо большенькая; перевёрнутая «г» когда заглавная; как русская «e»; a как русская; эс как Супермен; как русская «e»; пробел; первёрнутая «М», как значок «Volkswagen»; a как русская; перевёрнутый восклицательный знак; тэ как могильный крестик; пробел; ку, как флажок налево; как пэ верх ногами; «и украинская»; как русская «e»; тэ как могильный крестик; эль — «большая палочка»; как русская у,; кавычка… ну… такая, как два больше', ''),
('тэ как зонтик сломанный; как букетик; точка; андерлайн; меньше; птички; треугольные скобки; русская «и» наоборот; дефис; как «н» русская когда заглавная; собачка; dollar sign; амперсанд; b в другую сторону; коммерческое «и»; двоеточие; a как русская; машинописная кавычка; как Макдональдс', ''),
('как «я» наоборот; кавычка… ну… такая, как два больше; dollar sign; правая скобочка; амперсанд; джи как гугл; тэ как зонтик сломанный; прямой слеш; о — как зеркальце; о — как зеркальце; как гэ; пробел; падающая вправо; зэт как Зорро; плюсик; эм — как расчёска; открывающая круглая скобка; дубльвэ как две галочки; открывающая круглая скобка', ''),
('эс как Супермен; дэ как пудреница, вправо открытая; андерскор; правая скобочка; кавычка… ну… такая, как два больше', ''),
('кавычка… ну… такая, как два больше; улитка; о — как зеркальце; кавычка… ну… такая, как два меньше; как русская «e»; эс как интеграл; зэт как Зорро; пробел; кавычка… ну… такая, как два больше; тильда; точка с запятой; a как русская; первёрнутая «М», как значок «Volkswagen»; жесткий_пробел; саблайн', ''),
('кавычка… ну… такая, как два меньше; дубльвэ как две галочки большенькая; как русская «e»; пробел; первёрнутая «М», как значок «Volkswagen»; как русская «e»; как гэ; как русская «e»', ''),
('как русская у,; процент; двоеточие; запятая; как русская сэ; карет; слеш; кружочком; меньше; кавычка… ну… такая, как два больше; аш как постоянная Планка; запятая', ''),
('закрывающая круглая скобка; запятая; конъюнкция; как букетик; палочка; дэ как пудреница, вправо открытая; там, где русская «п» на клавиатуре; тэ как зонтик сломанный; как Макдональдс; первёрнутая «М», как значок «Volkswagen»; как русская сэ; эм — как расчёска; тэ как могильный крестик', ''),
('о — как зеркальце; средний дефис; амперсанд; кочерга; коммерческое «и»', ''),
('эн — как русская пэ; кружочком; пробел; дубльвэ как две галочки; Н как водород; перевёрнутый восклицательный знак; тэ как зонтик сломанный; как русская «e»; эс как интеграл; пэ, как русская эр; a как русская; эс как ЕВРО без палочки; как русская «e»; эс как Супермен', ''),
('как русская тэ; андерскор; дубльвэ как две галочки; первёрнутая «М», как значок «Volkswagen»; фембэкслеш; точка; ручка у зонтика; точка с запятой; эф как флажок; закрывающая круглая скобка; открывающая угловая скобка; тэ как могильный крестик; кавычка… ну… такая, как два больше', ''),
('дефисоминус; звездочка; аш как постоянная Планка; как Макдональдс; кавычка… ну… такая, как два больше; как пэ верх ногами; «бэ как русская р вверх тормашками»; фембэкслеш; закрывающая угловая скобка; открывающая круглая скобка; эс как доллар; игрек', ''),
('как «я» наоборот; тюрьма; падающая вправо; эм — как расчёска; тильда', ''),
('Н как водород большенькая; a как русская; как тросточка; как гэ; рогатка.; пробел; тэ как могильный крестик; о — как зеркальце; эль — «большая палочка»; b в другую сторону', ''),
('кавычка универсальная; «к как наша»; открывающая круглая скобка; дефисоминус; эс как Супермен; правая скобочка; a как русская; решеточка', ''),
('кавычка… ну… такая, как два меньше; эс как Супермен; о — как зеркальце; эм — как расчёска; как русская «e»; пробел; как Макдональдс; о — как зеркальце; русская «и» наоборот; как русская «e»; как русская у,; кавычка… ну… такая, как два больше', ''),
('«и украинская»; доллар как доллар; дэ как пудреница, вправо открытая; знак вопроса; крышка от домика; клюшка; средний дефис; как русская «e»; правая скобочка; sharp', ''),
('аш как постоянная Планка большенькая; a как русская; как гэ; как тросточка; рогатка.; пробел; как флажочек направо большенькая; о — как зеркальце; тэ как могильный крестик; тэ как могильный крестик; как русская «e»; как тросточка', ''),
('двоеточие; дубльвэ как две галочки; консоль; знак вопроса; земля', ''),
('линия такая волнистая (она на букве ё); правая скобочка; тэ как могильный крестик; плюсик; кавычка… ну… такая, как два меньше; процент; «б как мягкий знак»; йот как поварёшка; тире', ''),
('как значок «Опеля»; точка с запятой; кавычка… ну… такая, как два меньше; двоеточие; dollar sign; ка русская; птички; как пэ верх ногами', ''),
('правая скобочка; открывающая круглая скобка; кружочком; как русская у,; знак вопроса; амперсанд; процент; крестик плюс; двоеточие; как русская «e»; вэ-победа; кавычка универсальная; меньше; левая скобочка', ''),
('точка с запятой; крестик плюс; больше; о — как зеркальце; кавычка… ну… такая, как два больше; крестик плюс; зэт как Зорро; пробел; запятая; как значок «Опеля»; доллар как доллар; плюсик; процент; октоторп; «и украинская»', ''),
('эс как интеграл большенькая; «к как наша» большенькая; «бэ как пудреница, влево открытая» большенькая; пробел; «к как наша» большенькая; кружочком; эн — как русская пэ; тэ как зонтик сломанный; как пэ верх ногами; как «я» наоборот', ''),
('«а» в кружочке; a как русская; аш — как стульчик такой; кавычка… ну… такая, как два больше; хэ русская; коммерческое at.; икс; звездочка; как «у» подковкой; упавший минус; как значок «Опеля»; игрек; двоеточие; коммерческое «и»', ''),
('Н как водород большенькая; a как русская; как тросточка; как гэ; рогатка.; пробел; тэ как могильный крестик; о — как зеркальце; эль — «большая палочка»; b в другую сторону', ''),
('двоеточие; дубльвэ как две галочки; консоль; знак вопроса; земля', ''),
('крышка от домика; a как русская; процент; линия такая волнистая (она на букве ё); эс как ЕВРО без палочки; дэ как пудреница, вправо открытая; как тросточка; точка; тэ как зонтик сломанный; процент; как значок «Опеля»; двоеточие; кочерга; дэ как пудреница, вправо открытая', ''),
('кочерга; там, где русская «п» на клавиатуре; Н как водород; тире; русская «и» наоборот; машинописная кавычка; как букетик; как значок «Опеля»; карет; звездочка; саблайн; конъюнкция; запятая; открывающая круглая скобка', ''),
('астериск; закрывающая круглая скобка; меньше; плюсик; перевёрнутый восклицательный знак; палочка; решеточка; ка русская; a как русская; андерстрайк; машинописная кавычка; ка русская; как «к» с палочками; кавычка… ну… такая, как два меньше; кавычка… ну… такая, как два меньше; процент; эс как интеграл', ''),
('крышка от домика; a как русская; процент; линия такая волнистая (она на букве ё); эс как ЕВРО без палочки; дэ как пудреница, вправо открытая; как тросточка; точка; тэ как зонтик сломанный; процент; как значок «Опеля»; двоеточие; кочерга; дэ как пудреница, вправо открытая', ''),
('b в другую сторону; машинописная кавычка; машинописная кавычка; открывающая угловая скобка; ку, как флажок налево; закрывающая круглая скобка; точка; точка; закрывающая угловая скобка; о — как зеркальце; конъюнкция; пробел; как флажочек направо; эль — «большая палочка»; закрывающая круглая скобка; птички; эль — «большая палочка»; запятая', ''),
('ручка у зонтика большенькая; как пэ верх ногами; эс как доллар; тэ как зонтик сломанный; пробел; тэ как могильный крестик; аш — как стульчик такой; как русская «e»; русская «и» наоборот', ''),
('как русская у,; как тросточка; процент; русская «и» наоборот; кавычка… ну… такая, как два меньше; тире', ''),
('эс как интеграл; двоеточие; знак вопроса; как флажочек направо; дефис; эф английская (гэ с палочкой); ка русская; точка; как русская тэ; как русская эр наоборот; йот как поварёшка; прямой слеш; кавычка… ну… такая, как два меньше; как номер; хэ русская; ручка у зонтика; андерлайн; b в другую сторону; октоторп; эф английская (гэ с палочкой)', ''),
('русская «и» наоборот; открывающая угловая скобка; машинописная кавычка; виктори; прямая косая черта; аш — как стульчик такой; восьмерка с закорючкой; кавычка… ну… такая, как два меньше; открывающая круглая скобка; ку, как флажок налево; меньше; закрывающая круглая скобка; точка', ''),
('закрывающая круглая скобка; запятая; конъюнкция; как букетик; палочка; дэ как пудреница, вправо открытая; там, где русская «п» на клавиатуре; тэ как зонтик сломанный; как Макдональдс; первёрнутая «М», как значок «Volkswagen»; как русская сэ; эм — как расчёска; тэ как могильный крестик', ''),
('«и украинская» большенькая; эн — как русская пэ; пробел; аш как постоянная Планка; палочка с точечкой; эс как доллар', ''),
('прямой слеш; упавший минус; икс; крышка от домика; тире; подчёркивание; знак вопроса; нижнее подчеркивание; эф как флажок; кружочком; вэ-победа; снежинка звёздочка; меньше; эф жирафиком; обезьяна', ''),
('крышка от домика; пробел; ка русская; перевёрнутая «г» когда заглавная; ку, как флажок налево', ''),
('крестик плюс; как тросточка; меньше; крестик плюс; коммерческое «и»; виктори; «Джей Севен» (сок в коробке); коммерческое at.; астериск; меньше; знак вопроса; эс как ЕВРО без палочки; эф жирафиком; «к как наша»; тире; кавычка… ну… такая, как два меньше; пробел', ''),
('a как русская; собачка; тюрьма; процент; аш — как стульчик такой; точка; sharp; тире', ''),
('меньше; тэ как могильный крестик; процент; звездочка; средний дефис; как «у» подковкой; ку, как флажок налево; знак вопроса', ''),
('как русская «e»; двоеточие; как пэ верх ногами; рогатка.; звездочка; дефис; как номер; палочка', ''),
('крышка от домика; пробел; ка русская; перевёрнутая «г» когда заглавная; ку, как флажок налево', ''),
('эм — как расчёска большенькая; a как русская; b в другую сторону; a как русская; как Макдональдс; пробел; Н как водород большенькая; о — как зеркальце; о — как зеркальце; как русская сэ; аш — как стульчик такой', ''),
('карет; пэ, как русская эр; эф английская (гэ с палочкой); рогатка.; первёрнутая «М», как значок «Volkswagen»; консоль; ку, как флажок налево; крючочек с точечкой; кавычка… ну… такая, как два меньше; средний дефис; знак вопроса; перевёрнутая «г» когда заглавная; фембэкслеш; как «у» подковкой; циркумфлекс; кавычка… ну… такая, как два больше; b в другую сторону; эс как доллар; «бэ как русская р вверх тормашками»', ''),
('крышка от домика; пробел; ка русская; перевёрнутая «г» когда заглавная; ку, как флажок налево', ''),
('пробел; конъюнкция; крышка от домика; ку, как флажок налево; машинописная кавычка; аш как постоянная Планка; кавычка… ну… такая, как два больше; первёрнутая «М», как значок «Volkswagen»; sharp; эс как ЕВРО без палочки; тэ как могильный крестик; эс как доллар; открывающая круглая скобка; кавычка… ну… такая, как два больше; запятая; доллар как доллар; точка; «к как наша»; зэт как Зорро; как номер', ''),
('тильда; знак вопроса; эль — «большая палочка»; кавычка универсальная; консоль; как флажочек направо; линия такая волнистая (она на букве ё); нижнее подчеркивание; эф как флажок; доллар как доллар', ''),
"""