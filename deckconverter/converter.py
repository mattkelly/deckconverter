"""
Converter class to convert a parse and write different deck formats.

Supported deck formats:
    .cod
    .coll
    .csv
    .dec
    .text
    .mwdeck
"""

import re

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
            has_price_avg = True
            try:
                header = reader.next()
                qty_index = header.index('Count')
                name_index = header.index('Name')
                sideboard_index = header.index('Sideboard') # Boolean indicating whether this is for sideboard or not
                try:
                    price_avg_index = header.index('Price Avg')
                except ValueError:
                    has_price_avg = False
                
                for row in reader:
                    if len(row) == 0:
                        continue
                    if len(row) != len(header):
                        sys.stderr.write("ERROR: line %d is malformed in %s\n" % (reader.line_num, csv_in))
                        return False

                    qty = int(row[qty_index])
                    name = row[name_index] 
                    sideboard = int(row[sideboard_index])

                    card = Card(name)

                    if has_price_avg:
                        price_avg = row[price_avg_index]
                        card.set_price_avg(price_avg)

                    if not sideboard:
                        self.deck.add_to_main(card, qty)
                    else:
                        self.deck.add_to_sideboard(card, qty)

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
        # TODO error checking
        # ///mvid:265418 qty:4 name:Azor's Elocutors loc:(Deck|SB)
        re_first = re.compile(r'///mvid:(\d+)\s+qty:(\d+)\s+name:(.+)\s+loc:(Deck|SB)')
        # TODO is second line just redundant?
        # (SB:)? 4 Azor's Electors
        #re_second = re.compile(r'^\s*(\d)\s+(.+)\s*$')
        with open(cod_in, 'r') as dec_file:
            for line in dec_file:
                match = re_first.match(line)
                if match:
                    mvid = match.group(1)
                    qty = int(match.group(2))
                    name = match.group(3)
                    loc = match.group(4)

                    card = Card(name)
                    if loc == 'Deck':
                        self.deck.add_to_main(card, qty)
                    else:
                        self.deck.add_to_sideboard(card, qty)

                    #match = re_second.match(line)
                    #if match:
                        #qty = match.group(1)
                        #name = match.group(2)

        return True

    def parse_mwdeck(self, cod_in):
        raise NotImplementedError('mwdeck parsing not yet supported!')

    def write_csv(self, csv_out, sort_by, reverse):
        header = ['Count', 'Name', 'Price Avg', 'Sideboard']
        rows = []
        for card in self.deck.get_sorted_cards(sort_by, reverse):
            main_qty= self.deck[card][0]
            if main_qty > 0:
                rows.append( [main_qty, card.get_name(), card.get_price_avg(), 0] )

        # Always write sideboard second
        for card in self.deck.get_sorted_cards(sort_by, reverse):
            sideboard_qty = self.deck[card][1]
            if sideboard_qty > 0:
                rows.append( [sideboard_qty, card.get_name(), card.get_price_avg(), 1] )
            
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
        root = ET.Element('cockatrice_deck', {'version' : '1'})
        if self.deck.get_main_quantity() > 0:
            main = ET.SubElement(root, 'zone', {'name' : 'main'})
        if self.deck.get_sideboard_quantity() > 0:
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
                    'price'  : str(card.get_price_avg()),
                    'name'   : card.get_name()
                })
            if sideboard_qty > 0:
                ET.SubElement(sideboard, 'card', {
                    'number' : str(sideboard_qty),
                    'price'  : str(card.get_price_avg()),
                    'name'   : card.get_name()
                })

            with open(cod_out, 'w') as cod_file:
                cod_file.write(self.prettify_xml(root))

        return True

    def write_coll(self, coll_out):
        raise NotImplementedError('coll writing not yet supported!')

    def write_dec(self, dec_out, sort_by, reverse):
        # TODO error checking
        with open(dec_out, 'w') as dec_file:
            deck_name = self.deck.get_name()
            deck_desc = self.deck.get_description()
            if deck_name:
                dec_file.write("// Name: %s\n" % deck_name)
            if deck_desc:
                dec_file.write("// Description: %s\n" % deck_desc)
            for card in self.deck.get_sorted_cards(sort_by, reverse):
                main_qty= self.deck[card][0]
                if main_qty > 0:
                    dec_file.write("///mvid:%s qty:%d name:%s loc:Deck\n" % (card.get_mvid(), main_qty, card.get_name()))
                    dec_file.write("%d %s\n" % (main_qty, card.get_name()))
     
            # Always write sideboard second
            for card in self.deck.get_sorted_cards(sort_by, reverse):
                sideboard_qty = self.deck[card][1]
                if sideboard_qty > 0:
                    dec_file.write("///mvid:%s qty:%d name:%s loc:SB\n" % (card.get_mvid(), sideboard_qty, card.get_name()))
                    dec_file.write("SB: %d %s\n" % (sideboard_qty, card.get_name()))

        return True

    def write_mwdeck(self, mwdeck_out):
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
        
