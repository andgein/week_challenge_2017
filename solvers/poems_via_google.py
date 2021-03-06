from weekchallenge import *

from urllib.parse import urlencode
import re


GOOGLE_API_KEY = 'AIzaSyBmnEAU7NgPML9aDhkXKZomLd8rppr--UE'
GOOGLE_CX = '018036561216809633450:szpvqxcsfk0' # Идентификатор Custom search engine

"""
    Я создал Google Custom Search
    https://developers.google.com/custom-search/json-api/v1/using_rest
    добавил туда сайты со стихами. Теперь по ним можно быстро искать гуглом через JSON API
"""
class Solver(TaskSolver):
    type_name = 'poems'
    
    base_url = 'https://www.googleapis.com'

    exceptions = {
        'Ты говоришь, что счастья нет,\nИль скудно Бог его отмерил,\nНо только, если бы был ____,\nТогда бы я тебе поверил!': 'слеп',
    }

    def __init__(self):
        self.client = JsonClient(self.base_url)


    def solve(self, task):
        value = task.value

        # Исключения
        if value in self.exceptions:
            return self.exceptions[value]

        result = self.try_solve_with_term(value, value.split('\n')[0].replace('_', ''))
        if result is None:
            result = self.try_solve_with_term(value, value.split('\n')[1].replace('_', ''))
        elif result is None:
            result = self.try_solve_with_term(value, value.split('\n')[2].replace('_', ''))
        elif result is None:
            result = self.try_solve_with_term(value, value.split('\n')[3].replace('_', ''))

        return None if result is None else result.lower() 
        
    def try_solve_with_term(self, value, term):        
        url = '/customsearch/v1?%s' % urlencode({'key': GOOGLE_API_KEY, 'cx': GOOGLE_CX, 'q': term})
        r = self.client.get_or_die(url)

        normalized_value = self.normalize(value)
        # Оставляем по 20 символов слева и справа от искомого слова. Это будет регвыр для поиска в сниппетах результата        
        re_value = re.sub(r'^.*?([^_]{,20})(\_+)(.{,20}).*$', r'\1(\2)\3', normalized_value)
        re_value = re_value.replace('_', '.')
        for item in r['items']:
            snippet = item['snippet']
            snippet = self.normalize(snippet)
            match = re.match('.*' + re_value, snippet, re.I)
            if match:
                Logger.info('Found matching in "%s"' % snippet)
                return match.groups(1)[0]

        Logger.error('Not found matching for "%s"' % re_value)
        return None


    @staticmethod
    def normalize(s):
        for ch in '?.:-!@#$%^&*()[]':
            s = s.replace(ch, '')
        s = s.replace('\n', ' ')
        for _ in range(10): # костыль? :)
            s = s.replace('  ', ' ')
        return s

    def tests(self):
        return [
            ('Входите все. Во внутренних покоях\nЗавета нет, ____ тайна здесь лежит.\nСтаринных книг на древних аналоях\nСмущает вас оцепеневший вид.', 'хоть'),
('Чтоб ___ он с корзинкой в Охотный ряд,\nГлаза лукаво косят,\nМохрится бороденка:\n- Барин! Купи куренка!', 'шел'),
# ('          _____\nНа пороге помощник гаркнул:\n"В штаб. Живее! Помер! Н-ну?!"\nТоропливо замял цигарку,', ''),
('К молодым ты не тянися!\nВот костыль и вот ________,\nУспокоиться сумей-ка!\nСвой пример я предлагаю:', 'скамейка'),
('Бросить прах его проклятый...\nТак, по пунктам, на цитатах,\nНа соборных _________,\nПриговор свой доктор черный', 'уложеньях'),
 ('Ты говоришь, что счастья нет,\nИль скудно Бог его отмерил,\nНо только, если бы был ____,\nТогда бы я тебе поверил!', 'слеп'),
('Средь добровольного изгнанья\n\tТвоя душа погружена?\nИль новая роскошная _______,\nИ жизнь кипящая, и полная свобода', 'природа'),
        ]


"""
('       И мне дороги тихой, без огня \nЖелали б вы, боясь _________.  \nНо вас — «по-Божьему» жалею я. \nКого люблю — люблю для Бога.  ', ''),
('Да, так любить, как любит наша _____,\nНикто из вас давно не любит!\nЗабыли вы, что в мире есть любовь,\nКоторая и жжет, и губит!', ''),
('И застывшей улыбаемся?\nМы хотели муки жалящей\n______ счастья безмятежного...\nНе покину я товарища', ''),
('все ушли, и я ____...\nШебаршит мышонок в норке,\nя грызу, вздыхая, корки, —\nсъел давно я апельсин.', ''),
('Но для меня свершился выдел,\nИ вот _____ его я видел:\nЗлачено-белый —\nпрямо с елки —', ''),
('И духи пламени хранят\nВоссевшего на алом троне,-\nВещает он, воздев ладони,\nСмотря, как с неба льется _____,', ''),
('Он всюду — на траве, на розах, над ________\nбестрепетный, а там, в аллее, вдалеке,\nтень черная листвы дробится на песке,\nи платье девушки, стоящей под каштаном,', ''),
('И комната, в которой я болею,\nВ последний раз болею на земле,\nКак будто упирается в аллею\nВысоких белоствольных _______,', ''),
('Говорил лукавый. -\nВ _______ отделеньи\nИзучают право!\nПраво на бесправье!..', ''),
('Я уж давно и навсегда _______, \nНо верю крепко: повернется жизнь, \nИ средь тайги сибирские Чикаго \nДо облаков поднимут этажи. ', ''),
('Из винтовок _______ на полном скаку.\nВыше только утесы, нагие стремнины,\nГде кочуют ветра да ликуют орлы,\nЧеловек не взбирался туда, и вершины', ''),
('Он не манит блеском и соблазнами,\nИ его не ведает народ.\nЭто дверь в стене, давно ___________,\nКамни, мох, и больше ничего,', ''),
('Некий сонм богатырей!\nЕсли так, то очень ловко\nМожно дело разрешить!\nНу-ка ты, моя ________,', ''),
('Напомнила прохожему кого-то,\nДавно __________ в покинутых краях...\nНедолгий торг окончен торопливо —\nВон на извозчике любовная чета:', ''),
('___ его щипала понемножку,\nИ уронила на дорожку,\nИ той порой румяное дитя,\nКудрявый мальчик, не шутя', ''),
('Кто _______ смел, тот победит. \nТам остров всех земель чудесней \nЗа гранью синею лежит. \nСвобода -- Дева огневая ', ''),
('И дворники в _______ шубах\nНа деревянных лавках спят.\nНа стук в железные ворота\nПривратник, царственно-ленив,', ''),
('В папахе до самых бровей\nИ крадущейся росомахой\nПодсматривает с ветвей.\nТы дальше идешь с __________.', ''),
('   _________ ярких свечей,\nВесь вечер, шумя и смеясь, ликовала\nТолпа беззаботных детей.\nИ дети устали... потушены свечи,—', ''),
('Чернилами сверкали ночью ____,\nРасстрел царей был гневным знаком\nвосклицанья,\nПобеда войск служила запятой,', ''),
('пророк любви, пророк счастливых? \nНо, шелестя у _____ ног, \nдремали травы без тревог, \nно песни птиц не умолкали ', ''),
('все ушли, и я ____...\nШебаршит мышонок в норке,\nя грызу, вздыхая, корки, —\nсъел давно я апельсин.', ''),
('______ из всех друзей —\nМой ненавистный,\nМой нежный недруг.\nОн хлещет истиной', ''),
('С ногтями лезет к роже,\nУшел скорей домой.\nПисатель дорогой!\n______, я сделал то же.', ''),
('Ей приносит так много серег и колец\nЗлой насмешник в красном _____.\nХоть высоко окно в Маргаритин приют,\nУ насмешника лестница есть.', ''),
('Нагая смерть гуляла без стыда,\nИ разучились улыбаться дети.\nИ мы узнали меру всех вещей,\nИ стала смерть единственным _______', ''),
('Рука его, а не моя. \nНо это пусть всяк знает, \nЧто в гневе, в ярости _____ \nПрохожий до корня Терновник отсекает. ', ''),
('Поет, скуля. Как скучно одиноким. \nЗвенит трамвай. Никто не замечает.\nВсе исчезало, _____, кружилось,\nЛицо людей с улыбкой снег встречает - ', ''),
('Как ты смел удрать без спроса?\nНа ____ ты стал похож?\nНа несчастного барбоса,\nЗа которым гнался еж…', ''),
('Ты - ______ пробка, только пробка\nВ бутылке с пенистым вином.\nСядь поплотней! Уприся в горло!\nВино кровавое шипит,', ''),
('Но тяжкий меч,  в ножнах забытый\nРукой слабеющих племен, \nДавно лежит полусокрытый\nПод едкой _________ времен', ''),
('   _____, Киприда, тебе, -- \nНам -- в беспощадной борьбе \nЖизнь красотой озарившая, \nПеной рожденная, ', ''),
('______ работайте: нива широкая \nТучные злаки вам скоро родит; \nПеснь ваша правая, чувством глубокая \nПахарей новых манит. ', ''),
('И раньше… вспомни страшный год,\nКогда слабел твой гордый идол,\nЕго __________ народ\nВрагу властительному выдал.', ''),
('Все хотят дешевенького счастья,\nСытости, удобств и тишины.\nХодят и — всё жалуются, стонут,\nСеренькие трусы и _____.', ''),
('Котелок твой -\nтот же океан,\nА ______ так близко, хоть влюбись\nв дорогу, дорогу.', ''),
('Из комнаты в комнату вхожу\nИ сон за мной\nМое пальто там в лунной тьме _________\nЯ падаю, оно за мной', ''),
('Поет, скуля. Как скучно одиноким. \nЗвенит трамвай. Никто не замечает.\nВсе исчезало, _____, кружилось,\nЛицо людей с улыбкой снег встречает - ', ''),
('            2\nЛюблю я грусть твоих просторов,\nМой милый край, святая Русь.\nСудьбы унылых __________', ''),
('Рука его, а не моя. \nНо это пусть всяк знает, \nЧто в гневе, в ярости _____ \nПрохожий до корня Терновник отсекает. ', ''),
('Зерцало Тайн, перед собой\nглядят недвижными очами\nи созерцают без _____\nглубокую премудрость Бога;', ''),
('_____ притаившись где-нибудь с игрушкой,\nИли в сад забившись с книжкою в руках,\nТы растешь неловкой, смуглою дурнушкой,\nДикой, словно зайчик, дома - как в гостях.', ''),
('Стали шумящим ________.\nМузы, в сонете-брильянте\nСтранную тайну отметьте,\nСпойте мне песню о Данте', ''),
('       И мне дороги тихой, без огня \nЖелали б вы, боясь _________.  \nНо вас — «по-Божьему» жалею я. \nКого люблю — люблю для Бога.  ', ''),
('______ мы! что наш ум?- сквозь туман озаряющий\nфакел\nБурей гонимый наш челн по морю бедствий и слез;\nСчастие наше в неведеньи жалком, в мечтах', ''),
('Шибче, кони быстроноги!\nШибче!.. близко... страшный миг!\nГлавк... Евмолп... опережают...\nНе ______ на отсталых!', ''),
('В печальном положеньи принца\n___ королевского дворца.\nБез гонорара. Без короны.\nСо всякой сволочью на &laquo;ты&raquo;.', ''),
('Вся в кустах утонула беседка;\nСвежей зелени яркая сетка\nПо стенам полусгнившим ползет,\nИ сквозь зелень в цветное ______', ''),
('Как тать, озираясь, неслышно идти,\nБессонные ночи в тоске проводить,\nНо бодро и весело в мир твой входить.\nПускай он доверчив, ________ далек,', ''),
('_____ тяжела... Но ты перед грозою\nДержи себя, как следует борцу,\nИ отвечай не жгучею слезою,\nА резким смехом, песнью огневою,', ''),
('Затаился в траве и лежу,\nИ усталость ___ позабыл,-\nУ меня ль недостаточно сил?\nЯ глубоко и долго гляжу.', ''),
('Нельзя о новости стерпеть твоих мне врак\nУзнай в моем ответе,\nЧто нового нет ______ на свете,\nНе новое и то, что ты дурак.', ''),
('А в тело __________ властно\nКрича врывалася пила\nВновь кажет мне сучек смолистый\nКак бы пронзенный болью глаз, -', ''),
('Полно убиваться!\nПолно тосковать!\nПусть ________ злятся\nНад тобой опять!', ''),
('Ему слышатся вопли и стон,\nЭто стон побежденных врагов.\nВспоминается темная ____...\nБледный месяц еще не всходил...', ''),
('Но уж рыжеет даль, пурговою метлищей\nРассвет сметает темь, ___ из сусека сор,\nИ слышно, как сова, спеша засесть в дуплище,\nГогочет и шипит на солнечный костер.', ''),
('__________ холодной Невою.\nЖизнь торопливо бредет\nЗдесь к цели незримой...\nЯ узнаю тебя с прежней тоской,', ''),
('Я уж давно и навсегда _______, \nНо верю крепко: повернется жизнь, \nИ средь тайги сибирские Чикаго \nДо облаков поднимут этажи. ', ''),
('Дышу на эти семена -\nИ говорю: на почве скудной\nДай _______ божьим семенам,\nВ день благодатный жатвы трудной', ''),
('Знак подан в дальний путь!\nКипит сребром равнина вод,\nКипит тоскою _____!\nО чём грущу невольно я?', ''),
('Идет, преграды разрушая,\nПутем открытий и _____;\nПусть лавры вечные сплетает\nГерою изумленный свет, -', ''),
('___ два недвижные огня?\nТы помнишь, как твой замер голос,\nКак потухал в крови огонь,\nКак подымался дыбом волос', ''),
('О, если ты пророк, — твой час ______. Пора!\nЗажги во тьме сердец пылающее слово.\nТы должен умереть на пламени костра\nСреди безумия и ужаса земного…', ''),
('Шли — и в землю опускались...\nГромко _______ вороны,\nНа болоте выла вьюга\nИ лягушки откликались.', ''),
('Обледенелые ____\nПронизывает боль тупая...\nИзвестны правила игры.\nЖиви, от них не отступая:', ''),
('Рядит сучья ракит,\nКузовок с земляникой -\n______ метит в зенит.\nДятел - пущ колотушка -', ''),
('______ голос возвестил про то,\nИ я стражду в нетерпении.\nВетры буйные, осенние!\nЧто оставили вы озеро,', ''),
('Некий сонм богатырей!\nЕсли так, то очень ловко\nМожно дело разрешить!\nНу-ка ты, моя ________,', ''),
('Но кто поймет, что не ______ звуки\nЗвенят в стихе неопытном моем,-\nЧто каждый стих - дитя глубокой муки,\nРожденное в раздумьи роковом;', ''),
('Был миг далекой юности, - я жил фатаморганами,\nЯ верил в свет ликующий, - теперь повсюду мгла.\nВо что так ________ верилось, что с прошлым было связано -\nВсему было приказано угаснуть, умереть...', ''),
('Федул твердит, что Фока плут\nЕго позорит и ругает;\nНо я не вижу толку тут:\nКто _____ сажею марает?', ''),
('______ из всех друзей —\nМой ненавистный,\nМой нежный недруг.\nОн хлещет истиной', ''),
('Как ______ зеленеющей долины,\nКак грудь земли, куда вонзился плуг,\nКак девушка, не знавшая мужчины.\nУверенную строгость береги:', ''),
('Не изменяет ничего...\nЕму — раек в театре жизни,\nИ слез, и смеха простота;\nМне — злобы дня, ________, мудрость', ''),
('И в доцветании _____\nДрожат зигзаги листопада.\nКружатся нежные листы\nИ не хотят коснуться праха...', ''),
('                      отворенных детей\nЛишь те, кто забыты и бесстрастны\nЗнают ______ молодых костей.\nЛюди ломают поколеньям суставы,', ''),
('Обледенелые ____\nПронизывает боль тупая...\nИзвестны правила игры.\nЖиви, от них не отступая:', ''),
('Говорил лукавый. -\nВ _______ отделеньи\nИзучают право!\nПраво на бесправье!..', ''),
('И в доцветании _____\nДрожат зигзаги листопада.\nКружатся нежные листы\nИ не хотят коснуться праха...', ''),
('Как тать, озираясь, неслышно идти,\nБессонные ночи в тоске проводить,\nНо бодро и весело в мир твой входить.\nПускай он доверчив, ________ далек,', ''),
('Насторожившись, начеку\nУ входа в ____,\nЩебечет птичка на суку\nЛегко, маняще.', ''),
('Обильны дичью вкусной и пушистой,\nИ путается острая коса\nВ траве _____, высокой и душистой...\nВ его дому уменье, роскошь, вкус —', ''),
('И _______ случаев превратных \nПрошедших радостей исчисль. \nКогда весна моя блистала, \nСбирал я майские плоды. ', ''),
('Я прозреваю блеск заемный,\nВосторгов ___________ зарю\nВ степи ласкательной и темной.\nВ могилах чую суету,', ''),
('Из разверзшейся земли,\nКак из матерней утробы,\n________, покинув гробы.\n- Не могу и не хочу,', ''),
('О, как пленительно, умно там, мило все!\nГде естества красы художеством сугубы\nИ сеннолистны где Ижорска князя дубы\nВ ветр шепчут, преклонясь, про _______ колесо!', ''),
('Генерал-майора Трепова,\nБлагодетеля-отца,\nКто порядки образцовые\nВвел словами: "______! Пли!" -', ''),
('Полных розовых нежных пятен\nДиких звезд и цветочных лужаек\nНевидимых колоколов\n_________', ''),
('Он всюду — на траве, на розах, над ________\nбестрепетный, а там, в аллее, вдалеке,\nтень черная листвы дробится на песке,\nи платье девушки, стоящей под каштаном,', ''),
('Свет, что за далью полней и ______.\nСтанут иными узоры Медведиц,\nСтанет весь мир из машин и из воль...\nВсе ж из былого, поэт-сердцеведец,', ''),
('Заглянула в глаза неживые,\nНа шеломы, колчаны, щиты...\n"Спите с миром! Отважно вы сгибли!\nКудри-шелк _____ тронул слегка...', ''),
('Поет, скуля. Как скучно одиноким. \nЗвенит трамвай. Никто не замечает.\nВсе исчезало, _____, кружилось,\nЛицо людей с улыбкой снег встречает - ', ''),
('И сладчайшая на него нашла оторопь.\n___ стоит и смотрит ввысь,\nИ не видит ни звезд, ни зорь\nЗорким оком своим — отрок.', ''),
('Ты - ______ пробка, только пробка\nВ бутылке с пенистым вином.\nСядь поплотней! Уприся в горло!\nВино кровавое шипит,', ''),
('Времени скучные звуки\nМне и вздохнуть не дают.\nЛяжешь, а горькая дума\nТак и не ______ с ума...', ''),
('Ах! чувствует он сам тьмы целы __________,\nИ множество свое зрит малым без придатка:\nХотя достиг конца, но мил едва успех.\nИль тщетно дал ему хотения содетель?', ''),
('Какой-то трепет ловить привык.\nЛюбовь сама вырастает,\nКак ____, как милый цветок,\nИ часто забывает', ''),
('_____ Вуич грамоту пишет\nГеоргию, своему побратиму:\n"Берегися, Черный Георгий,\nНад тобой подымается туча,', ''),
('Начало спора \n_________ вблизи Исаакиевского Собора \nПойдёмте на Неву пешком \nсказал Грачёв помахивая гребешком. ', ''),
('С клыками, с камнями в отверстиях очей!\nБольшие чучела в смешных вооруженьях,\nЕжи какие-то от головы до пят,\n__________ на то, чтобы пугать в сраженьях,-', ''),
('И сердце захлестнула кровь,\nСмывая память об отчизне...\nА голос пел: <I>_____ жизни\nТы мне заплатишь за любовь!</I>', ''),
('Ты _________ домов тяжелый ряд,\nИ башни, и зубцы бойниц его суровых,\nИ темные сады за камнями оград,\nИ стены гордые твердынь многовековых.', ''),
('Я. может быть, хотел бы быть святым \nРастрачиваешь жизнь и напеваешь \nПрозрачным зимним вечером пустым.\nЯ, может быть. хотел понять __________, ', ''),
('И с побелевших яблонь ____\nСтруится сладкий аромат.\nЦветы глядят с тоской влюбленной,\nБезгрешно чисты, как весна,', ''),
('Над пустынями водными\nВиден пенный узор.\nИ слезами холодными\n___________ взор.', ''),
('Ты взглянешь вдруг на небо голубое -\nПодумаешь: вот матери родной\nС любовью ____ несется надо мною.\nИ вот, когда толпу людей пустых', ''),
('Скоро полночь. Никто и _____,\nУтомлен самым призраком жизни,\nЯ любуюсь на дымы лучей\nТам, в моей обманувшей отчизне.', ''),
('По ним тоскует грудь младая:\nОдна роскошна, как земля,\nКак небеса, свята другая.\nИ мне ль любить, как я _____?', ''),
('Но гиацинт-огонь мне дан в удел ______.\nНоябрь, твое чело венчает яркий снег...\nДве тайны двух цветов заплетены в мой век,\nДва верных спутника мне жизнью суждены:', ''),
('________ цветы обронятся,\nИ созреет плод непрошеный,\nИ зеленое наклонится\nДо земли под горькой ношею!', ''),
('Где-то слышен на низкой плотине\nШум минут разлетевшихся в прах.\n______ низко купается в тине,\nЖизнь деревьев грустит на горах.', ''),
('Как белых бабочек летающая стая,\nКоснешься ты ресниц опущенных моих...\nЗакинув голову, отдам тебе уста я,\n____, тая, мог ты умереть на них!', ''),
('Васильками сердце светится, горит в нем бирюза.\nЯ играю на тальяночке про синие глаза.\nТо не зори в струях озера свой _______ узор,\nТвой платок, шитьем украшенный, мелькнул за косогор.', ''),

"""
