#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import string

class PersianEditor():
    """
    """
    
    def __init__(self, text):
        """
        """
        self.text = text
        self.fix_dashes = False
        self.fix_three_dots = True
        self.fix_english_quotes = True
        self.fix_hamzeh = True
        self.cleanup_zwnj = False
        self.fix_spacing_for_braces_and_quotes = False
        self.fix_arabic_numbers = False
        self.fix_english_numbers = False
        self.fix_misc_non_persian_chars = False
        self.fix_perfix_spacing = True
        self.fix_suffix_spacing = True
        self.aggresive = False
        self.cleanup_kashidas = False
        self.cleanup_extra_marks = False
        self.cleanup_spacing = False
        self.cleanup_begin_and_end = False
        self.cleanup()
    def cleanup(self):
        """
        
        Arguments:
        - `self`:
        """
        text = self.text

        # replace double dash to ndash and triple dash to mdash
        if self.fix_dashes:
            text = re.sub(r'-{3}', '—', text)
            text = re.sub(r'-{2}', '–', text)
        # replace three dots with ellipsis
        if self.fix_three_dots:
            text = re.sub(r'\s*\.{3,}', '…', text)

        # replace English quotes with their Persian equivalent
        if self.fix_english_quotes:
            text = re.sub("([\"'`]+)(.+?)(\1)", '«\2»', text)

        # should convert ه ی to ه
        # The original regex to find was: (\S)(ه[\s]+[ی])(\s)
        # and in python it removes one more letter at first.
        # I mean = 'همه ی' after this function changed to 'ههٔ'
        if self.fix_hamzeh:
            #find = re.compile(ur'(ه[\s]+[ی])(\s)', flags = re.U)
            text = re.sub(ur'(ه[\s]+[ی])(\s)',ur'هٔ ', text)

        # remove unnecessary zwnj char that are succeeded/preceded by a space
        if self.cleanup_zwnj:
            text = re.sub(r'\s+|\s+', ' ', text)

        # character replacement
        # Resource: http://langref.org/ruby+python/search?q=tr&s=go
        persian_numbers = u"۱۲۳۴۵۶۷۸۹۰"
        bad_chars = ",;كي%"
        good_chars = "،؛کی٪"
        #arabic_numbers = string.maketrans(u"١٢٣٤٥٦٧٨٩٠", persian_numbers)
        #english_numbers = string.maketrans(u"1234567890", persian_numbers)
        #fix_chars = string.maketrans(bad_chars, good_chars)
        
        if self.fix_english_numbers:
            text.translate(english_numbers)
        if self.fix_arabic_numbers:
            text.translate(arabic_numbers)
        if self.fix_misc_non_persian_chars:
            text.translate(fix_chars)

        # should not replace english chars in english phrases
        #
        # I have to look here later

        # put zwnj between word and prefix (mi* nemi*)
        # there's a possible bug here: می and نمی could separate nouns and not prefix
        if self.fix_perfix_spacing:
            #find = re.compile(ur"\s+(ن?می)\s+", flags = re.U)
            text = re.sub(ur"\s+(ن?می)\s+",ur' \1‌', text)

        # put zwnj between word and suffix (*tar *tarin *ha *haye)
        # there's a possible bug here: های and تر could be separate nouns and not suffix
        #if self.fix_suffix_spacing:
        #    text.sub(r'\s+(تر(ی(ن)?)?|ها(ی)?)\s+', '\1 ') # in case you can not read it: \s+(tar(i(n)?)?|ha(ye)?)\s+

        # -- Aggressive Editing -------------------------------------------------
        if self.aggresive:
            # replace more than one ! or ? mark with just one
            if self.cleanup_extra_marks:
                text.sub(r'(!){2,}', '\1')
                text.sub(r'(؟){2,}', '\1')

            # should remove all kashida
            if self.cleanup_kashidas:
                text.sub(r'_+', "")
            
        # -----------------------------------------------------------------------
        # should fix outside and inside spacing for () [] {} "" «»

        if self.fix_spacing_for_braces_and_quotes:
            text.sub(r'[   ‌]*(\()\s*([^)]+?)\s*?(\))[   ‌]*', ' 1\2\3 ')
            text.sub(r'[   ‌]*(\[)\s*([^)]+?)\s*?(\])[   ‌]*', ' 1\2\3 ')
            text.sub(r'[   ‌]*(\{)\s*([^)]+?)\s*?(\})[   ‌]*', ' 1\2\3 ')
            text.sub(r'[   ‌]*(“)\s*([^)]+?)\s*?(”)[   ‌]*', ' 1\2\3 ')
            text.sub(r'[   ‌]*(«)\s*([^)]+?)\s*?(»)[   ‌]*', ' 1\2\3 ')

        # : ; , ! ? and their persian equivalents should have one space after and no space before
        if self.fix_spacing_for_braces_and_quotes:
            text.sub(r'[ ‌  ]*([:;,؛،.؟!]{1})[ ‌  ]*', '\1')
            text.sub(r'([۰-۹]+):\s+([۰-۹]+)', '\1:\2')

        # should fix inside spacing for () [] {} "" «»
        if self.fix_spacing_for_braces_and_quotes:
            text.sub(r'(\()\s*([^)]+?)\s*?(\))', '\1\2\3')
            text.sub(r'(\[)\s*([^)]+?)\s*?(\])', '\1\2\3')
            text.sub(r'(\{)\s*([^)]+?)\s*?(\})', '\1\2\3')
            text.sub(r'(“)\s*([^)]+?)\s*?(”)', '\1\2\3')
            text.sub(r'(«)\s*([^)]+?)\s*?(»)', '\1\2\3')

        # should replace more than one space with just a single one
        if self.cleanup_spacing:
            text.sub(r'[ ]+', ' ')
            text.sub(r'([\n]+)[   ‌]', '\1')

        # remove spaces, tabs, and new lines from the beginning and end of file
        if self.cleanup_begin_and_end:
            text.strip()

        print text.encode('utf-8')

if __name__ == "__main__":
    sstring = unicode( 'همه ی شما ها می توانید باشید ها عمه ات', encoding='utf-8')
    run = PersianEditor(sstring)
    print run 
    
