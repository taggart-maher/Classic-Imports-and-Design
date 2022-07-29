import csv

convert = {
    'Etagere':'Decoration > Home Accents > Etagere',
    'Lighting > Tables Lamps' : 'Lighting > Table Lamps',
    'Tables > Center Tables' : 'Furniture > Living > Center Tables'
}
new_cats = []
cat_col = 3
filename = 'Baker.csv'

with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    linepos = 0
    for row in csv_reader:
        old_cat = row[cat_col].strip()
        if old_cat in convert:
            new_cat = [convert[old_cat], row[0]]
            new_cats.append(new_cat)
        else: 
            new_cats.append('INVALID_CAT#' + old_cat)

#write new catagories
with open('output.csv','w') as output_file:
    csv_writer = csv.writer(output_file)
    csv_writer.writerows(new_cats)