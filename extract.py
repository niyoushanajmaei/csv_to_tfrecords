def color(st):
    st = st.lower()
    all_colors = ["multicolor","khaki","beige","black","blue","brown","camouflage","crimson","cyan","green","gold","gray","grey","lime","lilac","lavender","magenta"
                    ,"mustard","maroon","white","navy","olive","orange","pink","purple","red","rose","scarlet","yellow","silver","violet"]
    colors =  []
    for c in all_colors:
        if c in st:
            colors.append(c)
    return colors

def category(st):
    st = st.lower()
    category = None
    all_categories = ["t-shirt","shirt","trousers","track pants","vest","jacket","raincoat","coat","underwear","brief","cargos","blazer","sweatshirt","polo","pants"
                        ,"cargo shorts","chino shorts","bermuda shorts","cycling shorts","gym shorts","shorts","track suit","suspenders","pajamas"
                        ,"pullover","sweater","football shoes","cricket shoes","basketball shoes","running shoes","badminton shoes",
                        "walking shoes","shoes","loafers","sneakers","slip on","sandals","boots","suit","top","skirt","wallet"]
    for c in all_categories:
        if c in st:
            category = c
            break
    return category

def gender(st):
    st = st.lower()
    all_genders = ["men","women","unisex"]
    genders =  []
    for g in all_genders:
        if g in st:
            genders.append(g)
    return genders

def pattern(st):
    st = st.lower()
    all_patterns = ["solid","printed","camouflage","washed","graphic","geometric","striped","checkered","animal print","typography"]
    patterns =  []
    for p in all_patterns:
        if p in st:
            patterns.append(p)
    return patterns

def neckline(st):
    st = st.lower()
    all_necklines = ["round","button down","crew","collared","v-neck","spread collar","mandarin collar","polo","turtle neck","hood"]
    necklines =  []
    for n in all_necklines:
        if n in st:
            necklines.append(n)
    return necklines

def sleeves(st):
    st = st.lower()
    all_sleeves = ["full sleeve"]
    sleeves =  []
    for s in all_sleeves:
        if s in st:
            sleeves.append(s)
    return sleeves

def material(st):
    st = st.lower()
    all_materials = ["canvas","cashmere","chenille","chiffon","cotton","crêpe","crepe","damask","georgette","gingham","jersey",
                    "lace","leather","linen","wool","modal","muslin","organza","polyester","satin","silk","spandex","suede","taffeta",
                    "toile","tweed","twill","velvet","viscose","synthetic matrials"]
    materials =  []
    for m in all_materials:
        if m in st:
            materials.append(m)
    return materials
