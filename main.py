import pygame
from src.brain import *

pygame.init()  # inicializē pygame bibliotēku

SCREEN_SIZE = (1000, 500)  # glabā ekrāna izmēru pikseļos

screen = pygame.display.set_mode(SCREEN_SIZE)  # izveido loga objektu ar izmēru SCREEN_SIZE
pygame.display.set_caption('Mancala')  # iestata loga virsrakstu

# Izveido Clock objektu spēles ātruma kontrolēšanai
clock = pygame.time.Clock()


# Izveido fonta objektus teksta renderēšanai, izmantojot fonta failu
font_small = pygame.font.Font('assets/fonts/OpenSans-Regular.ttf', 18)
font = pygame.font.Font('assets/fonts/OpenSans-Regular.ttf', 32)
font_large = pygame.font.Font('assets/fonts/OpenSans-Regular.ttf', 42)


# Ekrāna koordinātes bedrēm, kuros likt dimantus
POINTS = [
    (800, 275), (680, 275), (560, 275), (440, 275), (320, 275), (200, 275), (75, 350),
    (200, 425), (320, 425), (440, 425), (560, 425), (680, 425), (800, 425), (925, 350)
]


gems = [0] * 14  # Glabā cik daudz dimantu ir katrā bedrē

first_move = True  # Nosaka kurš ies pirmais
current_move = True  # Glabā tekošo gājienu - True ir spēlētājs, False ir dators


# ----- Surface un Rectangle objekti pogu zīmēšanai -----
play_button = font.render('SPĒLĒT', True, (255, 255, 255))
play_button_rect = play_button.get_rect()
play_button_rect.x = SCREEN_SIZE[0] / 2 - play_button.get_width() / 2
play_button_rect.y = 290

quit_button = font.render('IZIET', True, (255, 255, 255))
quit_button_rect = quit_button.get_rect()
quit_button_rect.x = SCREEN_SIZE[0] / 2 - quit_button.get_width() / 2
quit_button_rect.y = 360

turn_lbl = font_small.render('PIRMAIS GĀJIENS', True, (200, 200, 200))
turn_lbl_rect = turn_lbl.get_rect()
turn_lbl_rect.x = SCREEN_SIZE[0] / 2 - turn_lbl.get_width() / 2
turn_lbl_rect.y = 190

pl_button = font.render('SPĒLĒTĀJS', True, (255, 255, 255) if current_move else (128, 128, 128))
pl_button_rect = pl_button.get_rect()
pl_button_rect.x = SCREEN_SIZE[0] / 2 - pl_button.get_width() / 2 + 85
pl_button_rect.y = 220

cpu_button = font.render('DATORS', True, (128, 128, 128) if current_move else (255, 255, 255))
cpu_button_rect = cpu_button.get_rect()
cpu_button_rect.x = SCREEN_SIZE[0] / 2 - cpu_button.get_width() / 2 - 80
cpu_button_rect.y = 220
# -------------------------------------------------------


# Dictionary objekts, glabā ielādētos attēlus spēles objektiem
ASSETS = {
    'board': pygame.transform.scale(pygame.image.load('assets/images/Mancala.png').convert_alpha(), (1000, 300)),
}

# Ielādē visus dimantu sttēlus no gems_1.png līdz gems_24.png
for i in range(16):
    ASSETS[f'gems_{i+1}'] = pygame.image.load(f'assets/images/gems/gems_{i+1}.png').convert_alpha()


# Pārbauda vai spēle ir beigusies (vai viena no spēlētāju pusēm ir tukša)
def is_game_over():
    o1 = True
    o2 = True
    for i in range(0, 6, 1):
        if gems[i] != 0:
            o1 = False
            break
    for i in range(7, 13, 1):
        if gems[i] != 0:
            o2 = False
            break
    return o1 or o2

# Izpilda gājienu, balstoties uz uzklikšķināto bedri un pašreizējo kārtu
def move(pit):
    temp_gems = gems[pit]
    gems[pit] = 0
    while temp_gems > 0:
        pit += 1
        if pit == len(gems):
            pit = 0
        # Ja dimanti ir uz pretinieka mankalas, nenovietot dimantu un turpināt uz nākamo bedri
        if (current_move and pit == 6) or (not current_move and pit == 13):
            continue
        temp_gems -= 1
        gems[pit] += 1
    # Ja pēdējais dimants nonāk tukšā bedrē
    if gems[pit] == 1:
        # Un ja bedre ir ejošā spēlētāja pusē
        if (current_move and 7 <= pit <= 12) or (not current_move and 0 <= pit <= 5):
            # Un ja bedre pretējā laukuma pusē nav tukša
            if gems[pit + 2 * (6 - pit)] > 0:
                # Tad abu bedru saturi nonāk ejošā spēlētāja mankalā
                if current_move:
                    gems[13] += gems[pit] + gems[pit + 2 * (6 - pit)]
                else:
                    gems[6] += gems[pit] + gems[pit + 2 * (6 - pit)]
                gems[pit] = 0
                gems[pit + 2 * (6 - pit)] = 0

# atgriež indeksu bedrei ar koordinātām pos
# atgriež -1 ja koordinātās pos nav bedres
def get_clicked_pit(pos):
    for i in range(len(POINTS)):
        if abs(POINTS[i][0] - pos[0]) < 50 and abs(POINTS[i][1] - pos[1]) < 50:
            return i
    return -1

# Atgriež spēles uzvarētāju, vai 'NEIZŠĶIRTS' ja ir neizšķirts
def get_winner():
    if gems[13] > gems[6]:
        return 'SPĒLĒTĀJS'
    elif gems[13] < gems[6]:
        return 'DATORS'
    else:
        return 'NEIZŠĶIRTS'

# Uzzīmē dimantus bedrē ar indeksu i
def draw_pit(i):
    if gems[i] == 0:
        return
    screen.blit(ASSETS[f'gems_{gems[i]}'], (POINTS[i][0] - 50, POINTS[i][1] - 50))

# Uzzīmē dimantus katrā bedrē, atbilstoši dimantu skaitiem
def draw_all_pits():
    for i in range(len(gems)):
        draw_pit(i)

# Uzzīmē tekstu, kas parāda pašreizējo gājienu
def draw_move_text():
    move_label = font_small.render('GĀJIENS', True, (200, 200, 200))
    if current_move:
        move_text = font.render('SPĒLĒTĀJS', True, (255, 255, 255))
    else:
        move_text = font.render('DATORS', True, (255, 255, 255))
    screen.blit(move_label, (SCREEN_SIZE[0] / 2 - move_label.get_width() / 2, 10))
    screen.blit(move_text, (SCREEN_SIZE[0] / 2 - move_text.get_width() / 2, 35))

# Uzzīmē tekstu, kas parāda spēlētāju rezultātus
def draw_score_text():
    player_label = font_small.render('SPĒLĒTĀJS', True, (200, 200, 200))
    cpu_label = font_small.render('DATORS', True, (200, 200, 200))
    player_text = font.render(str(gems[13]), True, (255, 255, 255))
    cpu_text = font.render(str(gems[6]), True, (255, 255, 255))
    screen.blit(cpu_label, (10, 10))
    screen.blit(cpu_text, (10, 35))
    screen.blit(player_label, (SCREEN_SIZE[0] - player_label.get_width() - 10, 10))
    screen.blit(player_text, (SCREEN_SIZE[0] - player_text.get_width() - 10, 35))

# Uzzīmē tekstu, kas parāda spēles uzvarētāju
def draw_game_over_text():
    winner_label = font.render('UZVARĒTĀJS', True, (200, 200, 200))
    winner_text = font_large.render(get_winner(), True, (255, 255, 255))
    screen.blit(winner_label, (SCREEN_SIZE[0] / 2 - winner_label.get_width() / 2, 10))
    screen.blit(winner_text, (SCREEN_SIZE[0] / 2 - winner_text.get_width() / 2, 45))

# Uzzīmē spēles izvēlni - paneli un pogas
def draw_menu():
    s = pygame.Surface((500, 300), pygame.SRCALPHA)  # per-pixel alpha
    s.fill((0, 0, 0, 210))  # notice the alpha value in the color
    screen.blit(s, (SCREEN_SIZE[0] / 2 - s.get_width() / 2, 150))
    screen.blit(play_button, play_button_rect)
    screen.blit(quit_button, quit_button_rect)
    screen.blit(turn_lbl, turn_lbl_rect)
    screen.blit(pl_button, pl_button_rect)
    screen.blit(cpu_button, cpu_button_rect)


game_over = True  # Glabā vai spēle ir beigusies

# Sāk jaunu spēli - iestata dimantu skaitu bedrēs uz sākuma skaitu, tekošo gājienu uz pirmo gājienu
# un spēles statusu uz nav beigusies
def start_game():
    global gems
    gems = [2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 0]
    global current_move
    current_move = first_move
    global game_over
    game_over = False


# ----- Spēles galvenais cikls -----

running = True  # glabā vai spēles ciklam jāturpina darboties
while running:  # spēles cikls apstāsies, ja running tiks iestatīts uz False

    game_over = is_game_over()  # pārbauda vai spēle nav beigusies

    # Ja tekošais gājiens ir datoram
    if (not game_over) and (not current_move):
        pygame.time.wait(1000)  # pagaidīt 1000 milisekundes (1 sekundi)
        bm = get_best_move(State(None, 0, gems, current_move, None), 5)  # atrast datora labāko gājienu
        move(bm)  # veikt atrasto gājienu
        current_move = not current_move  # samainīt tekošo gājienu uz spēlētāja

    # Iziet cauri katram 'notikumam' un veic atbilstošās darbības
    for event in pygame.event.get():
        # ja notikuma tips ir 'QUIT' (spēlētājs ir uzklikšķinājis uz krustiņa), pārtraukt spēles darbību
        if event.type == pygame.QUIT:
            running = False
        # ja spēlētājs ir veicis peles kreiso klikšķi spēles logā
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()  # iegūst peles kursora koordinātas
            # ja spēle nav beigusies
            if not game_over:
                # un pašreizējais gājiens ir spēlētājam
                if current_move:
                    pit = get_clicked_pit(event.pos)  # iegūt uzklikšķinātās bedres indeksu
                    if pit != -1:  # ja atgrieztais bedres indekss ir -1, tad bedre netika uzklikšķināta
                        if 7 <= pit <= 12:  # ja uzklikšķinātā bedre ir spēlētāja pusē
                            if gems[pit] > 0:  # ja bedre nav tukša
                                move(pit)  # vaikt gājienu
                                current_move = not current_move  # samainīt gājienu uz spēlētāja

            # ja spēlētājs uzklikšķināja uz pogas, kas samaina pirmo gājienu uz spēlētāja
            # samainīt pirmo gājienu uz spēlētāja un samainīt pogu krāsas
            elif pl_button_rect.collidepoint(pos[0], pos[1]):
                first_move = True
                pl_button = font.render('SPĒLĒTĀJS', True, (255, 255, 255) if first_move else (128, 128, 128))
                cpu_button = font.render('DATORS', True, (128, 128, 128) if first_move else (255, 255, 255))
            # ja spēlētājs uzklikšķināja uz pogas, kas samaina pirmo gājienu uz datora
            # samainīt pirmo gājienu uz datora un samainīt pogu krāsas
            elif cpu_button_rect.collidepoint(pos[0], pos[1]):
                first_move = False
                pl_button = font.render('SPĒLĒTĀJS', True, (255, 255, 255) if first_move else (128, 128, 128))
                cpu_button = font.render('DATORS', True, (128, 128, 128) if first_move else (255, 255, 255))
            # ja spēlētājs uzklikšķināja uz 'SPĒLĒT' pogas, sākt spēli
            elif play_button_rect.collidepoint(pos[0], pos[1]):
                start_game()
            # ja spēlētājs uzklikšķina uz 'IZIET' pogas, apstādināt spēles ciklu
            elif quit_button_rect.collidepoint(pos[0], pos[1]):
                running = False

    # Piepilda ekrānu ar zaļu krāsu
    screen.fill((54, 84, 66))

    # Uzzīmē spēles laukumu
    screen.blit(ASSETS['board'], (0, 200))

    # Uzzīmē dimantus bedrēs
    draw_all_pits()

    # Uzzīmē spēlētāju rezultātus
    draw_score_text()
    # Ja spēle nav beigusies, uzzīmē pašreizējā gājiena tekstu
    if not game_over:
        draw_move_text()
    # Ja spēle ir beigusies, uzzīmē uzvarētāja tekstu un izvēlni
    else:
        draw_game_over_text()
        draw_menu()

    pygame.display.flip()  # parāda visu uzzīmēto uz ekrāna
    clock.tick(60)  # kontrolē spēles ātrumu uz 60 rāmjiem sekundē

pygame.quit()  # iztīra ielādētos attēlus un fontus no atmiņas un iziet no spēles
