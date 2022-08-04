import csv
from pprint import pprint as pp

convert = {
    'Lighting > Table Lamps': 'Lighting > Table Lamps',
    'Lighting > Chandeliers' : 'Lighting > Chandeliers',
    'Lighting > Floor Lamps' : 'Lighting > Floor Lamps',
    'Lighting > Flush Mount' : 'Lighting > Flush Mounts',
    'Lighting > Pendants' : 'Lighting > Pendants',
    'Lighting > Semi-Flush' : 'Lighting > Semi-Flush',
    'Lighting > Tables Lamps' : 'Lighting > Table Lamps',
    'Lighting > Wall Sconces' : 'Lighting > Wall Sconces',
    'Etagere':'Decoration > Home Accents > Etagere',
    'Tables > Center Tables' : 'Furniture > Living > Tables > Center Tables',
    'Tables > Cocktail Tables' : 'Furniture > Living > Tables > Cocktail Tables',
    'Tables > Console Tables' : 'Furniture > Living > Tables > Console Tables',
    'Tables > Dining Tables' : 'Furniture > Dining > Dining Tables',
    'Tables > End Tables' : 'Furniture > Living > Tables > End Tables',
    'Tables > Game Tables' : 'Decoration > Home Accents > Game Tables',
    'Tables > Occasional Tables' : 'Furniture > Living > Tables > Occasional Tables',
    'Credenzas & Sideboards' : 'Furniture > Dining > Credenzas, Sideboards, & Buffets',
    'Furniture > Dining > Credenzas, Sideboards, & Buffets' : 'Credenzas Sideboards & Buffets',
    'Seating > Bar Stools' : 'Furniture > Dining > Barstools & Counterstools',
    'Seating > Benches & Ottomans' : 'Furniture > Living > Benches & Ottomans',
    'Seating > Chaises & Settees' : 'Furniture > Living > Chaises & Settees',
    'Seating > Counter Stools' : 'Furniture > Dining > Barstools & Counterstools',
    'Seating > Dining Chairs' : "Furniture > Dining > Dining Chairs",
    'Seating > Game Chairs' : 'Decoration > Home Accents > Game Chairs',
    'Seating > Occasional Chairs' : 'Furniture > Living > Occasional Chairs',
    'Seating > Sofas' : "Furniture > Living > Sofas",
    'Beds' : 'Furniture > Bedroom > Beds',
    'Dressers' : 'Furniture > Bedroom > Dressers',
    'Nightstands' : 'Furniture > Bedroom > Nightstands',
    'Chests' : 'Furniture > Bedroom > Chests',
    'Accessories > Dcor' : 'Decoration > Artistic Ornaments > Miscellaneous',
    'Accessories > Bookends' : 'Decoration > Home Accents > Bookends',
    'Accessories > Candelabras' : 'Decoration > Home Accents > Candelabras',
    'Centerpieces' : 'Decoration > Artistic Ornaments > Centerpieces',
    'Accessories > Centerpieces' : 'Decoration > Artistic Ornaments > Centerpieces',
    'Décor' : 'Decoration > Artistic Ornaments > Miscellaneous',
    'Accessories > Mirrors' : 'Decoration > Home Accents > Mirrors',
    'Accessories > Pedestals' : 'Decoration > Artistic Ornaments > Pedestals',
    'Accessories > Trays' : 'Decoration > Home Accents > Trays',
    'Accessories > Vases' : 'Decoration > Artistic Ornaments > Vases',
    'Antiques' : 'Showroom Inventory',
    'Armoires & Wardrobes' : 'Furniture > Bedroom > Armoires & Wardrobes',
    'Art > Lithographs & Serigraphs' : 'Decoration > Artistic Ornaments > Wall Art',
    'Art > Paintings' : 'Decoration > Artistic Ornaments > Wall Art',
    'Art > Prints' : 'Decoration > Artistic Ornaments > Wall Art',
    'Art > Wall Art' : 'Decoration > Artistic Ornaments > Wall Art',
    'Art > Sculptures > Acrylic' : 'Decoration > Artistic Ornaments > Sculptures',
    'Art > Sculptures > Bronze' : 'Decoration > Artistic Ornaments > Sculptures',
    'Art > Sculptures > Marble' : 'Decoration > Artistic Ornaments > Sculptures',
    'Art > Sculptures > Porcelain' : 'Decoration > Artistic Ornaments > Sculptures',
    'Art > Sculptures > Stainless Steel' : 'Decoration > Artistic Ornaments > Sculptures',
    'Étagère' : 'Decoration > Home Accents > Etagere',
    'Clocks' : 'Decoration > Artistic Ornaments > Miscellaneous',
    'Crystal' : 'Decoration > Artistic Ornaments > Sculptures',
    'Decor' : 'Showroom Inventory',
    'Display Cabinets' : 'Furniture > Living > Cabinets',
    'Fireplace Mantels' : 'Decoration > Home Accents > Fireplace Mantels',
    'Fountains' : 'Decoration > Home Accents > Fountains',
    'Pedestals' : 'Decoration > Artistic Ornaments > Pedestals',
    'Urns' : 'Decoration > Artistic Ornaments > Urns',
    'Vases' : 'Decoration > Artistic Ornaments > Vases',
    'Bars' : 'Furniture > Dining > Bars',
    'Bookcases' : 'Furniture > Living > Bookcases',
    'Cabinets' : 'Furniture > Living > Cabinets',
    'Desks' : 'Furniture > Living > Desks',
    'Entertainment' : 'Furniture > Living > Entertainment Cabinet',
    'Mirrors' : 'Decoration > Home Accents > Mirrors',
    'Sink Chests' : 'Furniture > Living > Sink Chests'
}
new_cats = []
cat_col = 3
filename = 'Classic-Imports-and-Design\Catagory Software\OLD-CSVS\input.csv'

with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        sku = row[0].strip()
        old_cat = row[cat_col].strip()
        if old_cat in convert:
            new_cat = [convert[old_cat], sku]
            new_cats.append(new_cat)
        else: 
            new_cats.append(['INVALID_CAT#' + old_cat, sku])
pp(new_cats)

#write new catagories
with open('Classic-Imports-and-Design\Catagory Software\output.csv','w') as output_file:
    output_file.truncate()
    csv_writer = csv.writer(output_file)
    csv_writer.writerows(new_cats)
    output_file.close()