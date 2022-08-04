from fuzzywuzzy import fuzz
from fuzzywuzzy import process

print(fuzz.partial_ratio('RAYLEIGH FABRIC CANOPY BED KING'.lower(), 'Beds'.lower()))

title = ''
cats = {
    'beds':'Furniture > Living > Beds'
}

for text in cats.keys():
    if fuzz.partial_ration(title.lower(), text.lower() > 65):
        catagory = cats[text]
    
