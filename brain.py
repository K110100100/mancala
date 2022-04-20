from src.state import State


# nosaka datora labāko gājienu
# root - pašreizējais spēles stāvoklis
# depth - ģenerētā spēles koka daļas dziļums (līmeņu skaits)
def get_best_move(root, depth):

    # --- 1. SOLIS ---
    # Ģenerēt spēles koku
    generated = {}  # Glabā ģenerēto spēles stāvokļu laukumus kā atslēgas, un norādes uz stāvokļu objektiem kā vērtības
    leaf_nodes = []  # Saraksts ar norādēm uz stāvokļiem, kas ir lapas spēles koka daļā
    queue = [root]  # Rinda ar stāvokļiem, kas jāapmeklē

    # Kamēr rinda nav tukša, apmeklēt katru stāvokli rindā
    while len(queue) > 0:
        state = queue.pop(0)

        # atkarībā no tā, vai jāiet spēlētājam vai datoram, iegūst indeksus bedrēm, no kurām var veikt gājienus
        r = (0, 0)
        if state.move:
            r = (7, 12)
        else:
            r = (0, 5)

        # iziet cauri katram iespējamajam gājienam
        for i in range(r[0], r[1] + 1):
            if state.gems[i] > 0:
                # Izveido jaunu stāvokli, kuru iegūst veicot tekošo gājienu
                temp = State(state, state.level + 1, state.get_move_result(i, state.move), not state.move, i)
                # Ja šāds stāvoklis jau eksistē tajā pašā spēles koka daļas līmenī,
                # tad uz to izveido saiti un nepievieno kokam vēlreiz
                if temp.gems_to_str() in generated:
                    if generated[temp.gems_to_str()].level == temp.level:
                        state.children.append(generated[temp.gems_to_str()])
                        continue
                # Ja šāds stāvoklis tajā pašā līmenī vēl neeksistē,
                # tad uz to izveido saiti un pievieno to spēles koka daļai
                state.children.append(temp)
                generated[temp.gems_to_str()] = temp
                # ja stāvoklis ir dziļākajā atļautajā līmenī vai tam nav bērnu,
                # sarakstam ar koka daļas lapām pievieno norādi uz to
                if temp.level == depth or len(temp.children) == 0:
                    leaf_nodes.append(temp)

        # ja stāvokļa bērni nav dziļākajā atļautajā līmenī,
        # pievieno tos apskatāmo stāvokļu rindai
        if state.level < depth - 1:
            for c in state.children:
                queue.append(c)

    # --- 2. SOLIS ---
    # Katram stāvoklim, kas koka daļā ir lapa, piešķir vērtību,
    # kas ir spēlētāja punktu un datora punktu starpība
    for leaf in leaf_nodes:
        leaf.score = leaf.gems[13] - leaf.gems[6]

    # --- 3. SOLIS ---
    # Izmantojot MiniMax algoritmu, piešķir vērtības katram stāvoklim
    assign_value(root)

    # atgriež gājienu uz stāvokli ar viszemāko vērtību (dators vienmēr ir minimizētājs)
    m = root.children[0]
    for i in range(1, len(root.children), 1):
        if root.children[i].score < m.score:
            m = root.children[i]
    return m.path


# Minimaxa algoritms, piešķir vērtības koka stāvokļiem
# rekursīva funkcija
def assign_value(root: State):
    if root.score is None:

        # Izsauc funkciju uz visiem stāvokļa bērniem, nosakot tiem vērtību
        for c2 in root.children:
            assign_value(c2)

        # nosaka vērtību tekošajam stāvoklim
        # ja move = True, tad maksimizētājs, savādāk minimizētājs
        if len(root.children) > 0:
            # Iestata tekošā stāvokļa vērtību uz tā pirmā pēcteča vērtību
            root.score = root.children[0].score
            # Ja stāvoklim ir vairāk par vienu pēcteci,
            # iziet cauri tiem
            if len(root.children) > 1:
                for i in range(1, len(root.children), 1):
                    # Ja stāvoklis ir maksimizētājs UN bērna vērtība ir lielāka par stāvokļa vērtību,
                    # piešķirt stāvoklim bērna vērtību
                    if root.move and root.children[i].score > root.score:
                        root.score = root.children[i].score
                    # Ja stāvoklis ir minimizētājs UN bērna vērtība ir mazāka par stāvokļa vērtību,
                    # piešķirt stāvoklim bērna vērtību
                    elif not root.move and root.children[i].score < root.score:
                        root.score = root.children[i].score
