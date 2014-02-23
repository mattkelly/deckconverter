"""
TODO
"""

# Use ElementTree C implementation if available
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import xml.parsers.expat as expat
import sys
import csv
from deckconverter.deck import Deck
from deckconverter.card import Card

class Converter:

    def __init__(self):
        self.deck = Deck()

    def prettify_xml(self, element):
        rough_string = ET.tostring(element, 'UTF-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent = '    ', encoding = 'UTF-8')

    def get_file_extension(self, filename):
        return filename.split(".")[-1]

    def parse_csv(self, csv_in):
        with open(csv_in, 'rb') as csv_file:
            reader = csv.reader(csv_file)
            try:
                header = reader.next()
                main_qty_index = header.index('Count')
                name_index = header.index('Name')
                sideboard_qty_index = header.index('Sideboard')
                
                for row in reader:
                    if len(row) == 0:
                        continue
                    if len(row) != len(header):
                        sys.stderr.write("ERROR: line %d is malformed in %s\n" % (reader.line_num, csv_in))
                        return False

                    main_qty = int(row[main_qty_index])
                    name = row[name_index] 
                    sideboard_qty = int(row[sideboard_qty_index])

                    card = Card(name)

                    if main_qty > 0:
                        self.deck.add_to_main(card, main_qty)
                    if sideboard_qty > 0:
                        self.deck.add_to_sideboard(card, sideboard_qty)

            except csv.Error as e:
                sys.stderr.write("ERROR: %s line %d: %s\n" % (csv_in, reader.line_num, e))
                return False
                     
        return True

    def parse_cod(self, cod_in):
        try:
            tree = ET.parse(cod_in)
            root = tree.getroot()
            
            name = root[0].text
            description = root[1].text

            for zone in root.findall('zone'):
                if zone.attrib['name'].lower() == 'main': 
                    for card_element in zone:
                        main_qty = int(card_element.attrib['number'])
                        name = card_element.attrib['name']
                        card = Card(name)
                        self.deck.add_to_main(card, main_qty)

                elif zone.attrib['name'].lower() == 'sideboard':
                    for card_element in zone:
                        sideboard_qty = int(card_element.attrib['number'])
                        name = card_element.attrib['name']
                        card = Card(name)
                        self.deck.add_to_sideboard(card, sideboard_qty)

        except ParseError as e:
            (line, col) = e.position
            sys.stderr.write("ERROR: %s line %d, column %d: %s\n" % (cod_in, line, col, expat.ErrorString(e.code)))
            return False
                    
        return True

    def parse_coll(self, cod_in):
        raise NotImplementedError('coll parsing not yet supported!')

    def parse_dec(self, cod_in):
        raise NotImplementedError('dec parsing not yet supported!')

    def parse_mwdeck(self, cod_in):
        raise NotImplementedError('mwdeck parsing not yet supported!')

    def write_csv(self, csv_out, sort_by, reverse):
        header = ['Count', 'Name', 'Sideboard']
        rows = []
        for card in self.deck.get_sorted_cards(sort_by, reverse):
            (main_qty, sideboard_qty) = self.deck[card]
            rows.append( [main_qty, card.get_name(), sideboard_qty] )
            
        with open(csv_out, 'wb') as csv_file:
            writer = csv.writer(csv_file)
            try:
                writer.writerow(header)
                writer.writerows(rows)

            except csv.Error as e:
                sys.stderr.write("ERROR: %s: %s\n" % (csv_out, e))
                return False

        return True

    def write_cod(self, cod_out, sort_by, reverse):
        # TODO error checking
        root = ET.Element('cockatrice_deck', {'version' : '1'})
        main = ET.SubElement(root, 'zone', {'name' : 'main'})
        sideboard = ET.SubElement(root, 'zone', {'name' : 'sideboard'})

        if self.deck.get_name():
            ET.SubElement(root, 'deckname').text = self.deck.get_name()
        if self.deck.get_description():
            ET.SubElement(root, 'comments').text = self.deck.get_description()

        for card in self.deck.get_sorted_cards(sort_by, reverse):
            (main_qty, sideboard_qty) = self.deck[card]
            if main_qty > 0:
                ET.SubElement(main, 'card', {
                    'number' : str(main_qty),
                    'price'  : str(card.get_price()),
                    'name'   : card.get_name()
                })
            if sideboard_qty > 0:
                ET.SubElement(sideboard, 'card', {
                    'number' : str(sideboard_qty),
                    'price'  : str(card.get_price()),
                    'name'   : card.get_name()
                })

            with open(cod_out, 'w') as cod_file:
                cod_file.write(self.prettify_xml(root))

        return True

    def write_coll(self, cod_out):
        raise NotImplementedError('coll writing not yet supported!')

    def write_dec(self, cod_out):
        raise NotImplementedError('dec writing not yet supported!')

    def write_mwdeck(self, cod_out):
        raise NotImplementedError('mwdeck writing not yet supported!')

    def convert(self, source_file, destination_file, sort_by = 'name', reverse = False):
        parse_method = getattr(self, 'parse_' + self.get_file_extension(source_file))
        write_method = getattr(self, 'write_' + self.get_file_extension(destination_file))
        # TODO error checking
        if not parse_method(source_file):
            return False
        print self.deck
        if not write_method(destination_file, sort_by, reverse):
            return False
        return True
        
